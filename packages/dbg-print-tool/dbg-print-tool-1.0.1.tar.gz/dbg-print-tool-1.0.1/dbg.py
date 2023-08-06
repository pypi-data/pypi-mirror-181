class dbg():
    def __init__(self):
        self.dbg = {}
        self.set_debug()

    def set_debug(self, debug: bool = False):
        # method for setting the debug mode
        self.debug = debug

    def get_debug(self):
        # method for getting the debug mode
        return self.debug

    def check_module(self, key: str):
        if key in self.dbg:
            return True
        else:
            return False

    def set_modules(self, debugs: dict):
        # add the debugs from dictionary
        self.dbg.update(debugs)

    def del_modules(self, debugs: dict):
        for key in debugs:
            if self.check_module(key):
                del self.dbg[key]

    def list_modules(self):
        # method for getting the debugs

        # print(sorted(self.dbg.keys()))
        return sorted(self.dbg.keys())

    def set_module(self, key: str, value: bool):
        # method for setting a module to the database
        self.dbg[key] = value

    def get_module(self, key: str):
        # method for getting a module from the database
        if self.check_module(key):
            self.dbg = {k: False for k in self.dbg.keys(
            )} if self.dbg[key] and not self.debug else self.dbg

            # print(self.dbg[key])
            return self.dbg[key]
        else:
            return None

    def del_module(self, key: str):
        if self.check_module(key):
            del self.dbg[key]