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

