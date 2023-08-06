from datetime import datetime

from elna.core import API
from elna.exceptions import *
from elna.classes import *


class Connect(object):
    """ Class definition of the Elna SmartMeter. """

    # API Connection
    __api = None

    def __init__(self, hostname):
        """ Initiate the connection to the API. """
        self.__api = API(hostname)

    # System properties
    @property
    def api(self):
        """ Return the API for direct access. """
        return self.__api

    def get_info(self):
        """ Fetch general information from the device. """
        info = self.__api.get_info()

        new_info = Information(
            id=info['id'],
            manufacturer=info['mf'],
            model=info['model'],
            firmware=info['fw'],
            hardware=info['hw'],
            batch=info['batch']
        )

        return new_info

    def get_electricity(self):
        """ Fetch power readings from SmartMeter and populate class objects. """
        power = self.__api.get_meter_now()

        # Power Readings
        power_now = Power(
            key='now',
            value=power['elec']['power']['now']['value'],
            unit=power['elec']['power']['now']['unit'],
            timestamp=datetime.fromtimestamp(power['elec']['power']['now']['time'])
        )

        power_min = Power(
            key='minimum',
            value=power['elec']['power']['min']['value'],
            unit=power['elec']['power']['min']['unit'],
            timestamp=datetime.fromtimestamp(power['elec']['power']['min']['time'])
        )

        power_max = Power(
            key='maximum',
            value=power['elec']['power']['max']['value'],
            unit=power['elec']['power']['max']['unit'],
            timestamp=datetime.fromtimestamp(power['elec']['power']['max']['time'])
        )

        power_import = Power(
            key='imported',
            value=power['elec']['import']['now']['value'],
            unit=power['elec']['import']['now']['unit'],
            timestamp=datetime.fromtimestamp(power['elec']['import']['now']['time'])
        )

        power_export = Power(
            key='exported',
            value=power['elec']['export']['now']['value'],
            unit=power['elec']['export']['now']['unit'],
            timestamp=datetime.fromtimestamp(power['elec']['export']['now']['time'])
        )

        electricity = Electricity(power_now, power_min, power_max, power_import, power_export)

        return electricity

    def get_wlan_info(self):
        """ Fetch WLAN information from the device. """
        info = self.__api.get_wlan_info()

        new_info = WLANInformation(
            ap_key=info['ap_key'],
            ap_mac=info['ap_mac'],
            ap_ssid=info['ap_ssid'],
            client_ssid=info['client_ssid'],
            dns=info['dns'],
            dnsalt=info['dnsalt'],
            eth_mac=info['eth_mac'],
            gateway=info['gateway'],
            ip=info['ip'],
            join_status=info['join_status'],
            mac=info['mac'],
            mode=info['mode'],
            n2g_id=info['n2g_id'],
            sta_mac=info['sta_mac'],
            subnet=info['subnet']
        )

        return new_info


