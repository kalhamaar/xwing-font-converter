import logging


def get_logger():
    return MyLogger()


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class MyLogger(logging.Logger, Singleton):
    
    def __init__(self, name='Font Converter'):
        super(MyLogger, self).__init__(name)

        # create logger
        self.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.addHandler(ch)

