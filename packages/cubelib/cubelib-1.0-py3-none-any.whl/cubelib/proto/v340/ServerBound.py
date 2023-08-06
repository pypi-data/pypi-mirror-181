from ...types import VarInt, UnsignedShort, Long, String, NextState, UnsignedByte, Byte, Bool, Int, ByteArray, Position, Float, Double, Short, Angle, Slot
from ...p import Night

class Login:
           
    class LoginStart(Night):
        username: String    

    map = {0: LoginStart}
    inv_map = {LoginStart: 0}

class Play:

    class ChatMessage(Night):
        Message: String

    map = {0x02: ChatMessage}
    inv_map = {v: k for k, v in map.items()}