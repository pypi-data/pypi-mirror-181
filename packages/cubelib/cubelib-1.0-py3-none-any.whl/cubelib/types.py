from io import BytesIO
from enum import Enum
from struct import pack, unpack

from cubelib.errors import BufferExhaustedException
from typing import Union

class SafeBuff(BytesIO):

    def read(self, *a) -> bytes:
        
        if not a:
            return super().read()

        r = super().read(a[0])
        if len(r) != a[0]:
            raise BufferExhaustedException(f'Buffer returned {len(r)} instead of required {a[0]}')
        return r

class WimpleType:
        
    def __class_getitem__(class_, val):
        obj = class_()

        # Type[int] set max length\max value
        if isinstance(val, int):
            obj.max = val            

        # Type[[int]] set excepted length\value
        elif isinstance(val, list) and len(val) == 1:
            obj.min = val[0]
            obj.max = val[0]

        # Type[int, int] set range of excepted values\len
        elif isinstance(val, tuple) and len(val) == 2:
            obj.min = val[0]
            obj.max = val[1]

        else:
            raise Exception('какой далбаеб писал анатацию?!?!')
        
        return obj

class VarInt:

    max = 2_147_483_647
    min = -2_147_483_648
    our = int

    @staticmethod
    def cntd_destroy(buff: SafeBuff) -> (int, int):
        total = 0
        shift = 0
        val = 0x80
        while val&0x80:			
            val = unpack('B', buff.read(1))[0]
            total |= ((val&0x7F)<<shift)
            shift += 7
            if shift//7 > 5:
                raise RuntimeError('VarInt is too big!')
        if total&(1<<31):
            total = total - (1<<32)
        return total, shift//7

    @staticmethod
    def destroy(buff: SafeBuff) -> int:        
        return VarInt.cntd_destroy(buff)[0]

    @staticmethod
    def build(val: int) -> bytes:
        if not VarInt.max >= val >= VarInt.min:
            raise ValueError(f'VarInt must be in range ({VarInt.max} >= value >= {VarInt.min})')

        total = b''
        if val < 0:
            val = (1<<32)+val
        while val>=0x80:
            bits = val&0x7F
            val >>= 7
            total += pack('B', (0x80|bits))
        bits = val&0x7F
        total += pack('B', bits)
        return total

class UnsignedShort:

    our = int

    def destroy(buff: SafeBuff) -> int:
        return unpack('!H', buff.read(2))[0]

    def build(val: int) -> bytes:
        return pack('!H', val)

class String(WimpleType):

    our = str
    min = 1

    @staticmethod
    def build(val: str) -> bytes:
        o = b""
        o += VarInt.build(len(val))
        o += val.encode()
        return o

    @staticmethod
    def destroy(buff: SafeBuff) -> str:
        l = VarInt.destroy(buff)
        return buff.read(l).decode()

class Long:
	def destroy(buff: SafeBuff) -> int:
		return unpack('!q', buff.read(8))[0]

	def build(val: int) -> bytes:
		return pack('!q', val)
	
class NextState(Enum):
    Status = 1
    Login = 2

    def destroy(buff: SafeBuff):
        return NextState(list(buff.read(1))[0])

    def build(obj):        
        return bytes([obj.value])

class UnsignedByte:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    def build(val: int) -> bytes:
        return pack('!B', val)

class Byte:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!b', buff.read(1))[0]

    def build(val: int) -> bytes:
        return pack('!b', val)

class Bool:

    def destroy(buff: SafeBuff) -> bool:
        return unpack('!?', buff.read(1))[0]

    def build(val: bool) -> bytes:
        return pack('!?', val)

class Int:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!i', buff.read(4))[0]

    def build(val: int) -> bytes:
        return pack('!i', val)

class ByteArray:

    def destroy(buff: SafeBuff) -> bytes:
        return buff.read()
    
    def build(val: bytes):
        return val

class Position:

    def destroy(buff: SafeBuff) -> (int, int, int):
        return (-1,-1,-1)

class Float:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!f', buff.read(4))[0]

    def build(val: int) -> bytes:
        return pack('!f', val)

class Double:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!d', buff.read(8))[0]

    def build(val: int) -> bytes:
        return pack('!d', val)

class Short:

	def destroy(buff: SafeBuff) -> int:
		return unpack('!h', buff.read(2))[0]

	def build(val: int) -> bytes:
		return pack('!h', val)

class Angle:

    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    def build(val: int) -> bytes:
        return pack('!B', val)

class Slot(ByteArray):
    pass