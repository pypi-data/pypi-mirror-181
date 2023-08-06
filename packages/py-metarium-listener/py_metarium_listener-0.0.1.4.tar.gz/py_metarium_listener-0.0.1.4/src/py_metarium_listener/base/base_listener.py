from py_metarium_decoder import Decoder


class BaseListener:

    def __init__(self, url=None) -> None:
        self.__decoder = Decoder(url)
    
    def info(self):
        return self.__decoder.info()

    def listen(self, direction, block_hash=None, block_count=None):
        for block, is_metarium in self.__decoder.decode(direction, block_hash=block_hash, block_count=block_count):
            yield block, is_metarium
