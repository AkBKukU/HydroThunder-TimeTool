/*
 * Hydro Thunder raw data decoding
 */

// Known Data Sections and formats

struct SettingsNetwork {
    u32 Net_UnitID; // +1 to match menu, 0-3 range
    u32 Net_Enable; // Inverted to match menu
};


struct SettingsTrackDiff {
    u32 TrackDifficulty;
};

struct SettingsTrackAi {
    u32 AiDifficulty; // 0-100 range
};

struct SettingsTrack {
    SettingsTrackDiff trackDiff[13];
    SettingsTrackAi aiDiff[13];
};

// Boats decoded by byte value
enum Boat : u8 {
  Banshee = 0x00,
  Tidal_Blade = 0x01,
  Rad_Hazzard = 0x02,
  Miss_Behave = 0x03,
  Damn_the_Torpedoes = 0x04,
  Cutthroat = 0x05,
  Razorback = 0x06,
  Thresher = 0x07,
  Midway = 0x08,
  Chumdinger = 0x09,
  Armed_Response = 0x0a,
  Blowfish = 0x0b,
  Tinytanic = 0x0c,
};

struct HighScore {
    Boat Boat_Type;
    char Initials[0x03];
    float TimeSeconds;
};

struct BestSplit {
    float TimeSeconds[5];
};

struct Timers {
// Selection Times
    float time_track;
    float time_boat;
    float time_high;
    float time_continue;

};


struct RawData {
    padding[12];

    // Checksum is at least partially calculated by adding bytes together
    // Has not behaved as expected for track times, may not be single value
    u16 Checksum_1;
    u16 Checksum_2;

    padding[4];

    SettingsNetwork settings_net;
    padding[12];

    Timers timers;

    u32 FreeLimit_Per;
    u32 volume_AttrackEn;
    u32 volume_master; // 0-255 mapped to 0-100 percentage

    float unknown_1;
    padding[12];

    u32 FreeFirst;
    u32 AllTracks;
    u32 BonusTrackOne; // Options 1-8
    u32 BonusTrackTwo; // Options 1-8


    SettingsTrack settings_track;

    padding[176]; // Many unknown settings

    HighScore score[130]; // missing 4 bytes in 1.00d, likely Wait for opperator in net settings

    u32 Unkown_static_5; // Always 41 00 00 00

    BestSplit splits[13];
};

//HighScore score[130] @ 0x075BE7DF;


//BestSplit splits[13] @ 0x075BEBF3;


//u32 CheckSum @ 0x75BE66F;


//SettingsNetwork settings_net @ 0x75BE677;
//SettingsTrack settings_track @ 0x75BE6C7;

//bool setting_FreePlay @ 0x75BE6B3;


RawData rawdata_at_0x75BE663 @ 0x75BE663;

bool setting_FreeFirst @ 0x75BE6B7;
u8 setting_FreeMulti @ 0x75BE7C7; // Options: Off(0), 2,3,4
bool setting_AllBoats @ 0x75BE733;
bool setting_AllTracks @ 0x75BE6BB;
u8 setting_BonusTrackOne @ 0x75BE6BF; // Options 1-8
u8 setting_BonusTrackTwo @ 0x75BE6C3; // Options 1-8
//Note: Skipping CABINET TYPE setting since impact is unknown

// Pricing options with number inputs can be 0-60
bool setting_Pricing_CustomOn @ 0x75BE76B;

u8 setting_Pricing_LeftUnits @ 0x75BE76F;
u8 setting_Pricing_RightUnits @ 0x75BE773;
u8 setting_Pricing_CenterUnits @ 0x75BE777;
u8 setting_Pricing_ExtraUnits @ 0x75BE77B;
u8 setting_Pricing_DVBUnits @ 0x75BE77F;
;
u8 setting_Pricing_UnitsCredit @ 0x75BE783;
u8 setting_Pricing_UnitsBonus @ 0x75BE787;

u8 setting_Pricing_MineUnits @ 0x75BE78B;

u8 setting_Pricing_CreditsStart @ 0x75BE78F;
u8 setting_Pricing_CreditsContinue @ 0x75BE793;



u8 setting_Pricing_CoinsBill @ 0x75BE79B;

u8 setting_Pricing_ShowFractions @ 0x75BE79F;

u8 setting_Pricing_LeftCount @ 0x75BE7A3;
u8 setting_Pricing_RightCount @ 0x75BE7A7;
u8 setting_Pricing_CenterCount @ 0x75BE7AB;
u8 setting_Pricing_ExtraCount @ 0x75BE7AF;
u8 setting_Pricing_DVBCount @ 0x75BE7B3;
u8 setting_Pricing_Currency @ 0x75BE7B7; // Can be set to DOLLAR, POUND, GUILDER, SHILLING, F, KR, MARKKA, DM, LIRE, FORINT, HFI, PESETA, Y

// Force Feedback
u8 setting_Force_On @ 0x75BE757; // Inverted
u8 setting_Force_Adjustment @ 0x75BE75B; // 0-255 mapped to 0-100 percentage



u8 setting_FreeLimit_En @ 0x75BE72F;
u8 setting_FreeLimit_Per @ 0x75BE69B;
u32 setting_FreeLimit_Per_copy @ 0x75BE7D3; // Not sure, changed when value changed

u8 setting_Net_WaitOp @ 0x75BE7CF; // inverted

u8 setting_volume_master @ 0x75BE6A3; // 0-255 mapped to 0-100 percentage
float setting_volume_rumble @ 0x75BE763;
bool setting_volume_AttrackEn @ 0x75BE69F;
u8 setting_volume_AttrackVol @ 0x75BE737; // 0-255 mapped to 0-100 percentage

float setting_throttle_min @ 0x75BE73F;
float setting_throttle_max @ 0x75BE743;
float setting_throttle_mid @ 0x75BE747;

float setting_wheel_min @ 0x75BE74B;
float setting_wheel_max @ 0x75BE74F;
float setting_wheel_mid @ 0x75BE753;










