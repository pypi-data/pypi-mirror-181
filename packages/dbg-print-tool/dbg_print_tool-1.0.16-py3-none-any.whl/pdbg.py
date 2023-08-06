class pdbg:
    __tmp = ''
    dbg_type = 'dbg'
    log = ''

    def __new__(cls, text: str, module: str, type: str = None):
        super(pdbg, cls).__new__(cls)
        tmp_type = cls.dbg_type
        cls.dbg_type = type if type is not None else cls.dbg_type
        if cls.dbg_type == 'dbg':
            cls.f_dbg(text, module)

        elif cls.dbg_type == 'log':
            cls.f_log(text, module)
        cls.dbg_type = tmp_type

    def __init__(self):
        super(pdbg, self).__init__()

    def __repr__(self):
        super(pdbg, self).__repr__()

    def __str__(self):
        super(pdbg, self).__str__()

    @classmethod
    def f_dbg(cls, text: str, module: str):
        ret = f'\t[dbg] {module} => {text}' if dbg.get_module(module) else None

        return ret if cls.dbg_type == 'log' else print(ret)

    @classmethod
    def f_log(cls, text, module):
        if cls.f_dbg(text, module) is not None:
            cls.__tmp += f'{cls.f_dbg(text, module)} \n'
        if cls.__tmp != '':
            cls.log = f'[===== START DBG LOG =====]\n {cls.__tmp}[====== END DBG LOG ======]'
