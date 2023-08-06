from ...types import VarInt, UnsignedShort, Long, String, NextState, UnsignedByte, Byte, Bool, Int, ByteArray, Position, Float, Double, Short, Angle, Slot
from ...p import Night

class Login:
           
    class LoginStart(Night):
        username: String    

    map = {0: LoginStart}
    inv_map = {LoginStart: 0}

class Play:    
    
    class KeepAlive(Night):
        Keep_Alive_ID: VarInt    
        
    class ChatMessage(Night):
        Message: String
        
    class UseEntity(Night): 
        Target: VarInt
        Type: VarInt
        Target_XYZ: ByteArray
        
    class Player(Night):
        On_Ground: Bool
            
    class PlayerPosition(Night):
        X: Double
        Feet_Y: Double
        Z: Double
        On_Ground: Bool
        
    class PlayerLook(Night):
        Yaw: Float
        Pitch: Float
        On_Ground: Bool
        
    class PlayerPositionAndLook(Night):
        X: Double
        Feet_Y: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        On_Ground: Bool
    
    class PlayerDigging(Night):
        Status: Byte
        Location: Position
        Face: Byte
    
    class PlayerBlockPlacement(Night):
        Location: Position
        Face: Byte
        Held_Item: Slot
    
    class HeldItemChange(Night):
        Slot: Short
    
    class Animation(Night): 
        pass
    
    class EntityAction(Night):
        Entity_ID: VarInt
        Action_ID: VarInt
        Action_Param: VarInt
    
    class SteerVehicle(Night):
        Sideways: Float
        Forward: Float
        Flags: UnsignedByte
    
    class CloseWindow(Night):
        Window_ID: UnsignedByte
    
    class ClickWindow(Night):    
        Window_ID: UnsignedByte
        Slot: Short
        Button: Byte
        Action_Number: Short
        Mode: Byte
        Clicked_Item: Slot

    class ConfirmTransaction(Night):  
        Window_ID: Byte
        Action_Number: Short
        Accepted: Bool
    
    class CreativeInventoryAction(Night):
        Slot: Short
        Clicked_Item: Slot
    
    class EnchantItem(Night):
        Window_ID: Byte
        Enchantment: Byte

    class UpdateSign(Night):
        Location: Position
        Line_1: String
        Line_2: String
        Line_3: String
        Line_4: String

    class PlayerAbilities(Night): 
        Flags: Byte
        Flying_Speed: Float
        Walking_Speed: Float
    
    class TabComplete(Night): 
        Text: String
        Has_Position: Bool
        Looked_At_Block: ByteArray

    class ClientSettings(Night):
        Locale: String
        Viev_Distance: Byte
        Chat_Mode: Byte
        Chat_Colors: Bool
        Displayed_Skin_Parts: UnsignedByte
    
    class ClientStatus(Night):
        Action_ID: VarInt

    class PluginMessage(Night):
        Channel: String
        Data: ByteArray
     
    class Spectate(Night):
        Target_Player: String
    
    class ResourcePackStatus(Night):
        Hash: String
        Result: VarInt

    map = {
            0x00: KeepAlive,
            0x01: ChatMessage,
            0x02: UseEntity,
            0x03: Player,
            0x04: PlayerPosition,
            0x05: PlayerLook,
            0x06: PlayerPositionAndLook,
            0x07: PlayerDigging,
            0x08: PlayerBlockPlacement,
            0x09: HeldItemChange,
            0x0a: Animation,     
            0x0b: EntityAction,  
            0x0c: SteerVehicle,         
            0x0d: CloseWindow,  
            0x0e: ClickWindow,         
            0x0f: ConfirmTransaction,
            0x10: CreativeInventoryAction,
            0x11: EnchantItem,
            0x12: UpdateSign,
            0x13: PlayerAbilities,
            0x14: TabComplete,          
            0x15: ClientSettings,
            0x16: ClientStatus,
            0x17: PluginMessage,
            0x18: Spectate,
            0x19: ResourcePackStatus
        }
    inv_map = {v: k for k, v in map.items()}