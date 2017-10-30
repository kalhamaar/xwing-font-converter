import logging

LOGGER = None


def get_logger(loglevel='INFO'):

    global LOGGER
    if not LOGGER:
        LOGGER = MyLogger(loglevel=loglevel)
    return LOGGER


class MyLogger(logging.Logger):
    
    def __init__(self, name='Font Converter', loglevel='INFO'):
        super(MyLogger, self).__init__(name)

        # create logger
        self.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()

        lvl = getattr(logging, loglevel, 'INFO')
        ch.setLevel(lvl)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.addHandler(ch)
