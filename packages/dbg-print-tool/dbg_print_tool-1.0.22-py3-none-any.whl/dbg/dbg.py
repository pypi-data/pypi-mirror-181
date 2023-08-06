class dbg():

    dbg: dict = {}
    debug: bool = True

    def __new__(cls, *args, **kwargs):
        super(dbg, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super(dbg, self).__init__()

    def __repr__(self):
        super(dbg, self).__repr__()

    def __str__(self):
        super(dbg, self).__str__()

    @classmethod
    def set_debug(cls, debug: bool = True):
        # method for setting the debug mode
        cls.debug = debug

    @classmethod
    def get_debug(cls):
        # method for getting the debug mode
        return cls.debug

    @classmethod
    def check_module(cls, key: str):
        # check if module exists
        return True if key in cls.dbg else False

    @classmethod
    def set_modules(cls, debugs: dict):
        # add the debugs from dictionary
        cls.dbg.update(debugs)

    @classmethod
    def get_modules(cls, debugs: dict):
        # return the list of modules and values
        modules = {k: cls.get_module(k)
                   for k in debugs if cls.check_module(k)}

        return modules

    @classmethod
    def del_modules(cls, debugs: dict):
        for key in debugs:
            if cls.check_module(key):
                del cls.dbg[key]

    @classmethod
    def list_modules(cls):
        # method for getting the debugs
        return sorted(cls.dbg.keys())

    @classmethod
    def set_module(cls, key: str, value: bool):
        # method for setting a module to the database
        cls.dbg[key] = value

    @classmethod
    def get_module(cls, key: str):
        # method for getting a module from the database
        if cls.check_module(key):
            cls.dbg = {k: False for k in cls.dbg.keys(
            )} if cls.dbg[key] and not cls.debug else cls.dbg

            return cls.dbg[key]
        else:
            return None

    @classmethod
    def del_module(cls, key: str):
        if cls.check_module(key):
            del cls.dbg[key]
