from ...types import VarInt, UnsignedShort, Long, String, NextState, UnsignedByte, Byte, Bool, Int, ByteArray, Position, Float, Double, Short, Angle
from ...p import Night

class Login:
    
    class Disconnect(Night):
        reason: String
    
    class SetCompression(Night):     
        Threshold: VarInt
    
    class LoginSuccess(Night):
        uuid: String
        username: String

    map = {0: Disconnect, 2: LoginSuccess, 3: SetCompression}
    inv_map = {v: k for k, v in map.items()}

class Play:

    map = {}
    inv_map = {}