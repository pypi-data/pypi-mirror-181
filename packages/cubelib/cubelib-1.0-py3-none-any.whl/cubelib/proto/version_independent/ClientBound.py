from cubelib.types import String, Long
from cubelib.p import Night

class Status:
    class Response(Night):
        JsonRsp: String
        
    class Pong(Night):
        uniq: Long

    map = {0: Response, 1: Pong}
    inv_map = {Response: 0, Pong: 1}