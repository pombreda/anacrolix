Attribute VB_Name = "modVals"
'character array
Public Const ADR_CHAR_NAME = &H4A12AC

Public Const LEN_CHAR = 147
Public Const SIZE_CHAR = 156

Public Const ADR_CHAR_ID = ADR_CHAR_NAME - 4
Public Const ADR_CHAR_X = ADR_CHAR_NAME + 32
Public Const ADR_CHAR_Y = ADR_CHAR_NAME + 36
Public Const ADR_CHAR_Z = ADR_CHAR_NAME + 40
Public Const ADR_CHAR_GFX_DX = ADR_CHAR_NAME + 44
Public Const ADR_CHAR_GFX_DY = ADR_CHAR_NAME + 48
Public Const ADR_CHAR_FACING = ADR_CHAR_NAME + 80
Public Const ADR_CHAR_OUTFIT = ADR_CHAR_NAME + 92
Public Const ADR_CHAR_LIGHT = ADR_CHAR_NAME + 112
Public Const ADR_CHAR_COLOR = ADR_CHAR_NAME + 116
Public Const ADR_CHAR_HP = ADR_CHAR_NAME + 128
Public Const ADR_CHAR_ONSCREEN = ADR_CHAR_NAME + 136

'character details
Public Const ADR_BATTLE_SIGN = ADR_CHAR_NAME - &HDC
Public Const ADR_TARGET_ID = ADR_CHAR_NAME - &H98
Public Const ADR_CUR_SOUL = ADR_CHAR_NAME - &H90
Public Const ADR_MAX_MANA = ADR_CHAR_NAME - &H8C
Public Const ADR_CUR_MANA = ADR_CHAR_NAME - &H88
Public Const ADR_LEVEL = ADR_CHAR_NAME - &H78
Public Const ADR_EXP = ADR_CHAR_NAME - &H74
Public Const ADR_CUR_HP = ADR_CHAR_NAME - &H6C
Public Const ADR_MAX_HP = ADR_CHAR_NAME - &H70
Public Const ADR_PLAYER_ID = ADR_CHAR_NAME - &H68

'player position
Public Const ADR_PLAYER_X = &H127078
Public Const ADR_PLAYER_Y = ADR_PLAYER_X + 4
Public Const ADR_PLAYER_Z = ADR_PLAYER_X + 8

'hotkeys
Public Const ADR_HOTKEY = &H5F4720

Public Const SIZE_HOTKEY = 256
Public Const LEN_HOTKEY = 35

Public Const ADR_HOTKEY_SENDAUTO = ADR_HOTKEY - (LEN_HOTKEY + 1)

'containers
Public Const ADR_BP_NAME = &H4A9640

Public Const SIZE_BP = 492
Public Const LEN_BP = 15
Public Const SIZE_ITEM = 12

Public Const ADR_BP_OPEN = ADR_BP_NAME - &H10
Public Const ADR_BP_NUM_ITEMS = ADR_BP_NAME + &H28
Public Const ADR_BP_MAX_ITEMS = ADR_BP_NAME + &H20
Public Const ADR_BP_ITEM = ADR_BP_NAME + &H2C
Public Const ADR_BP_ITEM_QUANTITY = ADR_BP_ITEM + 4

'inventory
Public Const SLOT_LEFT_HAND = &H6
Public Const SLOT_RIGHT_HAND = &H5
Public Const SLOT_AMMO = &HA
Public Const SLOT_RING = &H9
Public Const SLOT_BAG = &H3

Public Const ADR_AMMO = &H4A9624
Public Const ADR_RIGHT_HAND = ADR_AMMO + (SLOT_RIGHT_HAND - SLOT_AMMO) * SIZE_ITEM
Public Const ADR_LEFT_HAND = ADR_AMMO + (SLOT_LEFT_HAND - SLOT_AMMO) * SIZE_ITEM
Public Const ADR_RING = ADR_AMMO + (SLOT_RING - SLOT_AMMO) * SIZE_ITEM

'vip list
Public Const ADR_VIP_NAME = &H49EF6C

Public Const SIZE_VIP = &H2C '44
Public Const LEN_VIP = 99 '100 vips

Public Const ADR_VIP_ID = ADR_VIP_NAME - &H4
Public Const ADR_VIP_ONLINE = ADR_VIP_NAME + &H1E
Public Const ADR_VIP_SYMBOL = ADR_VIP_NAME + &H24

'other addresses
Public Const ADR_WHITE_TEXT = &H5F7058
Public Const ADR_GFX_VIEW_X = &H4ABF48
Public Const ADR_GFX_VIEW_Z = ADR_GFX_VIEW_X - 8
'Public Const ADR_GFX_UNIDENT_Z = &HD025DC
Public Const ADR_GFX_VIEW_Y = ADR_GFX_VIEW_X - 4

Public Const ADR_ACCOUNT_NUMBER = &H5F6CDC
Public Const ADR_PASSWORD = &H5F6CBC
Public Const ADR_SERVER_IP = &H5EFB50
Public Const ADR_SERVER_PORT = &H5EFBB4

'item values
Public Const ITEM_RUNE_UH = &HC58
Public Const ITEM_RUNE_SD = &HC53
Public Const ITEM_RUNE_BLANK = &HC4B
Public Const ITEM_RUNE_HMM = &HC7E
Public Const ITEM_RUNE_EXPLO = &HC80
Public Const ITEM_RUNE_GFB = &HC77
Public Const ITEM_RUNE_FBB = &HC3A

Public Const ITEM_VIAL = &HB3A
Public Const ITEM_MANA_FLUID_COLOR = 7
Public Const ITEM_LIFE_RING = &HBEC
Public Const ITEM_WORM = &HDA4
Public Const ITEM_FISHING_ROD = &HD9B
Public Const ITEM_GOLD = &HBD7
Public Const ITEM_BOLT = &HD76
Public Const ITEM_ROPE = &HBBB
Public Const ITEM_BAG = 2853
'distance items
Public Const ITEM_SPEAR = &HCCD
Public Const ITEM_SMALL_STONE = &H6F5
Public Const ITEM_THROWING_KNIFE = &HCE2
Public Const ITEM_THROWING_STAR = &HC99
'weapons
Public Const ITEM_GIANT_SWORD = &HCD1
Public Const ITEM_BRIGHT_SWORD = &HCDF
Public Const ITEM_CROSS_BOW = &HD15
Public Const ITEM_BOW = &HD16
Public Const ITEM_FIRE_AXE = &HCF8
Public Const ITEM_SKULL_STAFF = &HCFC
Public Const ITEM_DRAGON_HAMMER = &HCFA
Public Const ITEM_DRAGON_LANCE = &HCE6
Public Const ITEM_ICE_RAPIER = 3284

Public Const ITEM_FOOD_FISH = &HDFA

'OLD UNUSED CONSTANTS
'Public Const adrXGo = &H5F2AF0
'Public Const adrYGo = &H5F2AEC
'Public Const adrGo = &H49D0DC
'Public Const adrCharPos = &H12AE28
'Public Const adrWText = &H5F2DA8
'Public Const adrWhiteTT = &H5F2DA4
