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
    u32 volume_AttractEn;
    u32 volume_master; // 0-255 mapped to 0-100 percentage

    float unknown_1; // Set to 1
    padding[12];

    u32 FreeFirst;
    u32 AllTracks;
    u32 BonusTrackOne; // Options 1-8
    u32 BonusTrackTwo; // Options 1-8


    SettingsTrack settings_track;

    u32 FreeLimit_En;
    u32 AllBoats;
    u32 volume_AttractVol; // 0-255 mapped to 0-100 percentage

    padding[4];

    float throttle_min;
    float throttle_max ;
    float throttle_mid;

    float wheel_min ;
    float wheel_max;
    float wheel_mid;

    // Force Feedback
    u32 Force_On; // Inverted
    u32 Force_Adjustment; // 0-255 mapped to 0-100 percentage

    float unknown_2; // Set to 0.5

    float volume_rumble;

    padding[4];

    // Pricing options with number inputs can be 0-60
    u32 Pricing_CustomOn;

    u32 Pricing_LeftUnits ;
    u32 Pricing_RightUnits ;
    u32 Pricing_CenterUnits;
    u32 Pricing_ExtraUnits;
    u32 Pricing_DVBUnits ;
    ;
    u32 Pricing_UnitsCredit;
    u32 Pricing_UnitsBonus ;

    u32 Pricing_MineUnits;

    u32 Pricing_CreditsStart ;
    u32 Pricing_CreditsContinue;

    u32 unknown_3; // Set to 32

    u32 Pricing_CoinsBill ;

    u32 Pricing_ShowFractions ;

    u32 Pricing_LeftCount ;
    u32 Pricing_RightCount ;
    u32 Pricing_CenterCount;
    u32 Pricing_ExtraCount;
    u32 Pricing_DVBCount;
    u32 Pricing_Currency; // Can be set to DOLLAR, POUND, GUILDER, SHILLING, F, KR, MARKKA, DM, LIRE, FORINT, HFI, PESETA, Y

    padding[12];
    u32 setting_FreeMulti;// Options: Off(0), 2,3,4

    padding[4];

    u32 setting_Net_WaitOp; // inverted
    u32 setting_FreeLimit_Per_copy; // Not sure, changed when value changed

    padding[8];


    HighScore score[130]; // missing 4 bytes in 1.00d, likely Wait for opperator in net settings

    u32 Unkown_static_5; // Always 41 00 00 00

    BestSplit splits[13];
};



RawData rawdata_at_0x75BE663 @ 0x75BE663;

RawData rawdata_at_0x75EE660 @ 0x75EE663;
