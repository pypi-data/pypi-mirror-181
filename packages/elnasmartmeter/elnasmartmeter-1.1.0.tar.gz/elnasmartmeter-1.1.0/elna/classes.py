class Information(object):
    """ Class definition of the device information. """

    def __init__(self, id, manufacturer, model, firmware, hardware, batch):
        """ Set the private variable values on instantiation. """
        self.__id = id
        self.__manufacturer = manufacturer
        self.__model = model
        self.__firmware = firmware
        self.__hardware = hardware
        self.__batch = batch

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """
        class_name   = type(self).__name__
        id           = f"id = '{self.id}'"
        manufacturer = f"manufacturer = '{self.manufacturer}'"
        model        = f"model = '{self.model}'"
        firmware     = f"firmware = '{self.firmware}'"
        hardware     = f"hardware = {self.hardware}"
        batch        = f"batch = '{self.batch}'"

        return f"{class_name}({id}, {manufacturer}, {model}, {firmware}, {hardware}, {batch})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'firmware': self.firmware,
            'hardware': self.hardware,
            'batch': self.batch,
        }

    # Information properties
    @property
    def id(self):
        return self.__id

    @property
    def manufacturer(self):
        return self.__manufacturer

    @property
    def model(self):
        return self.__model

    @property
    def firmware(self):
        return self.__firmware

    @property
    def hardware(self):
        return self.__hardware

    @property
    def batch(self):
        return self.__batch


class Electricity(object):
    """ Class definition of a set of power measurements. """

    def __init__(self, now, minimum, maximum, imported, exported):
        """ Set the private variable values on instantiation. """
        self.__now = now
        self.__minimum = minimum
        self.__maximum = maximum
        self.__imported = imported
        self.__exported = exported

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """
        class_name = type(self).__name__
        now      = f"now = '{self.now}'"
        minimum       = f"minimum = '{self.minimum}'"
        maximum  = f"maximum = '{self.maximum}'"
        imported  = f"imported = '{self.imported}'"
        exported  = f"exported = '{self.exported}'"

        return f"{class_name}({now}, {minimum}, {maximum}, {imported}, {exported})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'now': self.now,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'imported': self.imported,
            'exported': self.exported,
        }

    # Electricity properties
    @property
    def now(self):
        return self.__now

    @property
    def minimum(self):
        return self.__minimum

    @property
    def maximum(self):
        return self.__maximum

    @property
    def imported(self):
        return self.__imported

    @property
    def exported(self):
        return self.__exported



class Power(object):
    """ Class definition of a power measurement (value, unit and timestamp). """

    def __init__(self, key, value, unit, timestamp):
        """ Set the private variable values on instantiation. """
        self.__key = key
        self.__value = value
        self.__unit = unit
        self.__timestamp = timestamp

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """
        class_name = type(self).__name__
        key        = f"key = '{self.key}'"
        value      = f"value = {self.value}"
        unit       = f"unit = '{self.unit}'"
        timestamp  = f"timestamp = '{self.timestamp}'"

        return f"{class_name}({key}, {value}, {unit}, {timestamp})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'key': self.key,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp,
        }

    # Power properties
    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

    @property
    def unit(self):
        return self.__unit

    @property
    def timestamp(self):
        return self.__timestamp


class WLANInformation(object):
    """ Class definition of the device WLAN information. """

    def __init__(self, ap_key, ap_mac, ap_ssid, client_ssid, dns, dnsalt,
                 eth_mac, gateway, ip, join_status, mac, mode, n2g_id, sta_mac, subnet):
        """ Set the private variable values on instantiation. """
        self.__ap_key = ap_key
        self.__ap_mac = ap_mac
        self.__ap_ssid = ap_ssid
        self.__client_ssid = client_ssid
        self.__dns = dns
        self.__dnsalt = dnsalt
        self.__eth_mac = eth_mac
        self.__gateway = gateway
        self.__ip = ip
        self.__join_status = join_status
        self.__mac = mac
        self.__mode = mode
        self.__n2g_id = n2g_id
        self.__sta_mac = sta_mac
        self.__subnet = subnet

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """
        class_name  = type(self).__name__
        ap_key      = f"ap_key = '{self.ap_key}'"
        ap_mac      = f"ap_mac = '{self.ap_mac}'"
        ap_ssid     = f"ap_ssid = '{self.ap_ssid}'"
        client_ssid = f"client_ssid = '{self.client_ssid}'"
        dns         = f"dns = '{self.dns}'"
        dnsalt      = f"dnsalt = '{self.dnsalt}'"
        eth_mac     = f"eth_mac = '{self.eth_mac}'"
        gateway     = f"gateway = '{self.gateway}'"
        ip          = f"ip = '{self.ip}'"
        join_status = f"join_status = {self.join_status}"
        mac         = f"mac = '{self.mac}'"
        mode        = f"mode = '{self.mode}'"
        n2g_id      = f"n2g_id = '{self.n2g_id}'"
        sta_mac     = f"sta_mac = '{self.sta_mac}'"
        subnet      = f"subnet = '{self.subnet}'"

        return f"{class_name}({ap_key}, {ap_mac}, {ap_ssid}, {client_ssid}, {dns}, {dnsalt}, {eth_mac}, {gateway}, {ip}, {join_status}, {mac}, {mode}, {n2g_id}, {sta_mac}, {subnet})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'ap_key': self.ap_key,
            'ap_mac': self.ap_mac,
            'ap_ssid': self.ap_ssid,
            'client_ssid': self.client_ssid,
            'dns': self.dns,
            'dnsalt': self.dnsalt,
            'eth_mac': self.eth_mac,
            'gateway': self.gateway,
            'ip': self.ip,
            'join_status': self.join_status,
            'mac': self.mac,
            'mode': self.mode,
            'n2g_id': self.n2g_id,
            'sta_mac': self.sta_mac,
            'subnet': self.subnet,
        }

    # Power properties
    @property
    def ap_key(self):
        return self.__ap_key

    @property
    def ap_mac(self):
        return self.__ap_mac

    @property
    def ap_ssid(self):
        return self.__ap_ssid

    @property
    def client_ssid(self):
        return self.__client_ssid

    @property
    def dns(self):
        return self.__dns

    @property
    def dnsalt(self):
        return self.__dnsalt

    @property
    def eth_mac(self):
        return self.__eth_mac

    @property
    def gateway(self):
        return self.__gateway

    @property
    def ip(self):
        return self.__ip

    @property
    def join_status(self):
        return self.__join_status

    @property
    def mac(self):
        return self.__mac

    @property
    def mode(self):
        return self.__mode

    @property
    def n2g_id(self):
        return self.__n2g_id

    @property
    def sta_mac(self):
        return self.__sta_mac

    @property
    def key(self):
        return self.__key

    @property
    def subnet(self):
        return self.__subnet


