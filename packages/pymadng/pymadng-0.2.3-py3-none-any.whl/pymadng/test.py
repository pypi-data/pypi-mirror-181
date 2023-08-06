import logging

class MyClass(object):
    def __init__(self, A=None, B=None):
        self.A = A
        self.B = B

class Test(object):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    def __init__(self):
        logging.info("init")
        self._dir = {"class1": {"A":1, "B":2}, "class2": {"A":2, "B":4}}
        self._keys = list(self._dir.keys())
    def __getattr__(self, name):
        logging.info(f"__getattr__ called: {name}")
        try: 
            return MyClass(**self._dir[name])
        except KeyError:
            raise AttributeError(name)
    def __dir__(self):
        logging.info("__dir__ called")
        return self._keys