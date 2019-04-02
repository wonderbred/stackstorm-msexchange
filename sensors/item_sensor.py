from datetime import datetime

from exchangelib import Account, Configuration, DELEGATE, EWSDateTime, \
    EWSTimeZone, ServiceAccount
from st2reactor.sensor.base import PollingSensor


class ItemSensor(PollingSensor):
    def __init__(self, sensor_service, config):
        super(ItemSensor, self).__init__(sensor_service=sensor_service,
                                         config=config)
        self._logger = self.sensor_service.get_logger(
            name=self.__class__.__name__)
        self._stop = False
        self._store_key = 'exchange.item_sensor_date_str'
        self._timezone = EWSTimeZone.timezone(config['timezone'])
        self._credentials = ServiceAccount(username=config['username'],
                                           password=config['password'])
        self.primary_smtp_address = config['primary_smtp_address']
        self.sensor_folder = config.get('sensor_folder')
        try:
            self.server = config['server']
            self.autodiscover = False if self.server is not None else True
        except KeyError:
            self.autodiscover = True

    def setup(self):
        if self.autodiscover:
            self.account = Account(
                primary_smtp_address=self.primary_smtp_address,
                credentials=self._credentials,
                autodiscover=True,
                access_type=DELEGATE)
        else:
            ms_config = Configuration(
                server=self.server,
                credentials=self._credentials)
            self.account = Account(
                primary_smtp_address=self.primary_smtp_address,
                config=ms_config,
                autodiscover=False,
                access_type=DELEGATE)
        self.stored_date = self._get_last_date()
        if not self.stored_date:
            self.stored_date = self._timezone.localize(
                EWSDateTime.from_datetime(datetime.now()))

    def poll(self):
        start_date = self._get_last_date()
        if not start_date:
            start_date = self.stored_date
        if self.sensor_folder:
            target = self.account.inbox.parent / self.sensor_folder
        else:
            target = self.account.inbox
        items = target.filter(is_read=False).filter(
            datetime_received__gt=start_date)

        self._logger.info("Found {0} items".format(items.count()))
        for item in items:
            payload = dict(
                item_id=item.item_id,
                subject=item.subject,
                body=item.body,
                text_body=item.text_body,
                datetime_received=item.datetime_received.ewsformat(),
            )
            self._logger.info(
                "Sending trigger for item '{0}'.".format(payload['subject']))
            self._sensor_service.dispatch(trigger='exchange_new_item',
                                          payload=payload)
            self._set_last_date(payload['datetime_received'])

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform
        # cleanup operations like
        # closing the connections to external system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass

    def _get_last_date(self):
        self._last_date = self._sensor_service.get_value(name=self._store_key)
        if self._last_date is None:
            return None
        return EWSDateTime.from_string(self._last_date)

    def _set_last_date(self, last_date):
        self._last_date = last_date
        self._sensor_service.set_value(name=self._store_key,
                                       value=self._last_date)
