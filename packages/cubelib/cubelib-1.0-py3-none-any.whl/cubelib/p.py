from dataclasses import dataclass
from types import ModuleType
from typing import Union
import zlib

from cubelib.types import VarInt, SafeBuff
from cubelib.enums import state, bound
from cubelib.errors import BadPacketException, BufferExhaustedException, DecoderException


@dataclass
class Packet:

    id: int
    payload: bytes
    bound: Union[bound, None] = None
    compressed: Union[bool, None] = None

    def __build_plain(self) -> bytes:

        r = VarInt.build(self.id)
        r += self.payload
        r = VarInt.build(len(r)) + r
        return r
    
    def __build_compressed(self, threshold: int) -> bytes:

        if len(self.payload) <= threshold:

            r = VarInt.build(0)  # set data length 0
            r += VarInt.build(self.id)
            r += self.payload

        else:

            c = VarInt.build(self.id) + self.payload
            r = VarInt.build(len(c))  # set data length
            r += zlib.compress(c)
        
        r = VarInt.build(len(r)) + r
        return r
    
    def build(self, threshold: int = -1) -> bytes:

        if threshold == -1:
            return self.__build_plain()
        return self.__build_compressed(threshold)
    
    @staticmethod    
    def read_plain(buff: bytes, bound: bound):

        buff = SafeBuff(buff)
        try:
            length = VarInt.destroy(buff)        
        except RuntimeError as e:
            raise BadPacketException("Invalid packet length field!") from e

        if not 2097151 >= length > 0:
            raise BadPacketException(f'Packet length field {length} invalid! (2097151 >= length > 0)')
        
        try:
            id, fl = VarInt.cntd_destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid packet id field!") from e

        payload = buff.read(length - fl)
        tail = buff.read()
        return (Packet(id, payload, bound, False), tail)
    
    @staticmethod
    def read_compressed(buff: bytes, bound: bound, threshold):

        buff = SafeBuff(buff)
        try:
            p_length = VarInt.destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid packet length field!") from e

        if not 2097151 >= p_length > 0:
            raise BadPacketException(f'Packet length field {length} invalid! (2097151 >= length > 0)')

        try:
            d_length, fl = VarInt.cntd_destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid data length field!") from e

        if not 2097151 >= d_length >= 0:
            raise BadPacketException(f'Data length field {length} invalid! (2097151 >= length > 0)')

        data = SafeBuff(buff.read(p_length - fl))
        tail = buff.read()

        if d_length == 0:
            pass
        elif d_length > threshold:
            data = SafeBuff(zlib.decompress(data.read()))                    
        else:
            raise BadPacketException((f'compressed data length ({d_length}) is '
                                f'less than the threshold ({threshold})'))

        id = VarInt.destroy(data)
        payload = data.read()

        return (Packet(id, payload, bound, True), tail)    
    
    def resolve(self, s: state, v: Union[ModuleType, None]):
    
        if self.bound is bound.Server:
            if s == state.Handshaking:
                return ServerBound.Handshaking.map[self.id].destroy(self.payload)

            elif s == state.Status:
                return ServerBound.Status.map[self.id].destroy(self.payload)

            elif s == state.Login:
                return v.ServerBound.Login.map[self.id].destroy(self.payload)

            elif s == state.Play:
                try:
                    p = v.ServerBound.Play.map[self.id].destroy(self.payload)
                except KeyError:
                    return NotImplementedPacket(hex(self.id), self.bound, v.name)
                return p

        else:
            if s is state.Status:
                return ClientBound.Status.map[self.id].destroy(self.payload)

            elif s == state.Login:
                return v.ClientBound.Login.map[self.id].destroy(self.payload)

            elif s == state.Play:
                try:
                    p = v.ClientBound.Play.map[self.id].destroy(self.payload)
                except KeyError:
                    return NotImplementedPacket(hex(self.id), self.bound, v.name)
                return p

def readPacketsStream(buff: bytes, threshold: int, bound: bound, packets: list):

    while 7:
        if buff:       
            try:     
                if threshold >= 0:
                    packet, tail = Packet.read_compressed(buff, bound, threshold)
                else:
                    packet, tail = Packet.read_plain(buff, bound)
                packets.append(packet)
                buff = tail
            except BufferExhaustedException:
                return buff
        return buff                   



# class for packet who has been tried to resolve but it not implemented
# returns when packet with undefined id goes via resolve
@dataclass
class NotImplementedPacket:
    hex_id: str
    bound: bound
    ver_name: str


# basic class for packet building/parsing showing(repr)/initing
# parent of all protocol packets
class Night:

    @classmethod
    def destroy(cls, buff: bytes):
        
        self = cls()
        if not hasattr(self, '__annotations__'):
            return self  # zero-body
        
        buff = SafeBuff(buff)        
        an = self.__annotations__
        
        for name in an:
            TYPE = an[name]

            try:
                val = TYPE.destroy(buff)
            except Exception as e: # NOQA
                raise DecoderException from e
            
            if isinstance(val, str):
                size = len(val)
                
            elif isinstance(val, int):
                size = val
            
            if hasattr(TYPE, 'max'):
                if size > TYPE.max:
                    raise DecoderException(f'Packet field [{name}] larger than maximum! {size} > {TYPE.max}')

            if hasattr(TYPE, 'min'):
                if size < TYPE.min:
                    raise DecoderException(f'Packet field [{name}] thinker than minimum! {size} < {TYPE.max}')
                        
            setattr(self, name, val)
        return self

    def build(self, cmp_threshold: int = -1) -> bytes:
        raw = b""
        an = None
        try:
            an = self.__annotations__
        except: # NOQA
            pass  # no-body packets
        if an:
            for name in an:
                try:
                    raw += an[name].build(getattr(self, name))
                except AttributeError:
                    raise Exception(f'Failed to get {name}. Empty?')

        pack = Packet(self.id(), raw, None, False)

        return pack.build(cmp_threshold)        

    # return packet class type and body info like string  
    def __repr__(self) -> str:
        
        full_name = str(self.__class__).split("'")[1].split(".")
        
        def typo(x): return f"'{x}'" if type(x) is str else x        

        out = f'{full_name[-2]}.{full_name[-1]}('
        
        try:
            an = self.__annotations__
        except AttributeError:            
            return out + ')'

        out += ', '.join([f'{a}={typo(getattr(self, a))}' for a in an])

        return out + ')'

    # if args are empty class init without attrs and represents only structure,
    # if args presented attrs sets like it
    def __init__(self, *args):

        if not args:
            return

        if not hasattr(self, '__annotations__'):
            return
        
        an = self.__annotations__

        if len(an) != len(args):
            v = f'{self.__class__.__name__}(' + ', '.join([f'{a}: {an[a].our.__name__}' for a in an]) + ')'
            raise ValueError(f'{v} requres {len(an)} arguments but you provided only {len(args)}')
        
        for i, a in enumerate(an):
            setattr(self, a, args[i])                    
        
    # resolve packet id by packet in-library class
    # (need for building packet from class)
    def id(self):
        from cubelib import proto
        w = str(type(self)).split("'")[1].split('.')[:-1][2:]
        map = getattr(getattr(getattr(proto, w[0]), w[1]), w[2]).inv_map
        return map[type(self)]
