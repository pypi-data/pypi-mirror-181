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
    
    class JoinGame(Night):
        Entity_ID: Int
        Gamemode: UnsignedByte
        Dimension: Byte
        Difficulty: UnsignedByte
        Max_Players: UnsignedByte
        Level_Type: String
        Reduced_dbg_info: Bool
        
    class PluginMessage(Night):
        Channel: String
        Data: ByteArray
    
    class ServerDifficulty(Night):
        Difficulty: UnsignedByte
    
    class SpawnPosition(Night):
        Location: Position
     
    class PlayerAbilities(Night):
        Flags: Byte
        Flying_Speed: Float
        FOV_Modifier: Float

    class ChatMessage(Night):
        Json_Data: String
        Position: Byte

    class KeepAlive(Night):
        Keep_Alive_ID: VarInt
    
    class PlayerPositionAndLook(Night):
        X: Double
        Feet_Y: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        Flags: Byte
    
    class TimeUpdate(Night):
        World_Age: Long
        Time_Of_Day: Long        

    
    class WindowItems(Night):
        Window_ID: UnsignedByte
        Count: Short
        Slot_Data: ByteArray
    
    class EntityRelativeMove(Night):
        Entity_ID: VarInt
        Delta_X: Byte
        Delta_Y: Byte
        Delta_Z: Byte
        On_Ground: Bool

    class EntityLook(Night):
        Entity_ID: VarInt
        Yaw: Angle
        Pitch: Angle
        On_Ground: Bool
     
    class EntityLookAndRelativeMove(Night):
        Entity_ID: VarInt
        Delta_X: Byte
        Delta_Y: Byte
        Delta_Z: Byte
        Yaw: Angle
        Pitch: Angle
        On_Ground: Bool

    class EntityHeadLook(Night):
        Entity_ID: VarInt
        Head_Yaw: Angle
    
    class EntityVelocity(Night):
        Entity_ID: VarInt
        Velocity_X: Short
        Velocity_Y: Short
        Velocity_Z: Short

    class EntityStatus(Night):
        Entity_ID: Int
        Entity_Status: Byte    
    
    class Disconnect(Night):
        reason: String        
    
    class EntityEquipment(Night):
        Entity_ID: VarInt
        Slot: Short
        Item: ByteArray#?slot

    map = {
            0x00: KeepAlive,
            0x01: JoinGame,
            0x02: ChatMessage,
            0x03: TimeUpdate,
            0x04: EntityEquipment,
            0x05: SpawnPosition,            
            #0x06: UpdateHealth,
            #0x07: Respawn,
            0x08: PlayerPositionAndLook,
            #0x09: HeldItemChange,
            #0x0A: UseBed,
            #0x0B: Animation,
            #0x0C: SpawnPlayer,
            #0x0D: CollectItem,
            #0x0E: SpawnObject,
            #0x0F: SpawnMob,
            #0x10: SpawnPainting,
            #0x11: SpawnExperienceOrb,
            0x12: EntityVelocity,
            #0x13: DestroyEntities,
            #0x14: Entity,
            0x15: EntityRelativeMove,
            0x16: EntityLook,
            0x17: EntityLookAndRelativeMove,
            #0x18: EntityTeleport,
            0x19: EntityHeadLook,
            0x1A: EntityStatus,
            #0x1B: AttachEntity,
            #0x1C: EntityMetadata,
            #0x1D: EntityEffect,
            #0x1E: RemoveEntityEffect,
            #0x1F: SetExperience,
            #0x20: EntityProperties,
            #0x21: ChunkData,
            #0x22: MultiBlockChange,
            #0x23: BlockChange,
            #0x24: BlockAction,
            #0x25: BlockBreakAnimation,
            #0x26: MapChunkBulk,
            #0x27: Explosion,
            #0x28: Effect,
            #0x29: SoundEffect,
            #0x2A: Particle,
            #0x2B: ChangeGameState,
            #0x2C: SpawnGlobalEntity,
            #0x2D: OpenWindow,
            #0x2E: CloseWindow,
            #0x2F: SetSlot,
            0x30: WindowItems,
            #0x31: WindowProperty,
            #0x32: ConfirmTransaction,
            #0x33: UpdateSign,
            #0x34: Map,
            #0x35: UpdateBlockEntity,
            #0x36: OpenSignEditor,
            #0x37: Statistics,
            #0x38: PlayerListItem,
            0x39: PlayerAbilities,
            #0x3A: TabComplete,
            #0x3B: ScoreboardObjective,
            #0x3C: UpdateScore,
            #0x3D: DisplayScoreboard,
            #0x3E: Teams,
            0x3f: PluginMessage,
            0x40: Disconnect
            #0x41: ServerDifficulty,
            #0x42: CombatEvent,
            #0x43: Camera,
            #0x44: WorldBorder,
            #0x45: Title,
            #0x46: SetCompression,
            #0x47: PlayerListHeaderAndFooter,
            #0x48: ResourcePackSend,
            #0x49: UpdateEntityNBT
        }
    inv_map = {v: k for k, v in map.items()}