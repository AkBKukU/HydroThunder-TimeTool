/*
 * Hydro Thunder raw data decoding
 */

// Known Data Sections and formats

struct SettingsNetwork {
    u8 UnitID; // +1 to match menu, 0-3 range
    padding[3];
    bool Enable; // Inverted to match menu
};


struct SettingsTrackDiff {
    u8 TrackDifficulty; 
    padding[3];
};

struct SettingsTrackAi {
    u8 AiDifficulty; // 0-100 range
    padding[3];
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


struct RawData {
    u8 Unknown_static_1; // Always 01
    padding[3];
    u32 Unkown_static_2; // Always 98 BA DC FE, Version?
    u8 Unknown_static_3; // Always 01
    padding[3];
    
    // Checksum is at least partially calculated by adding bytes together
    // Has not behaved as expected for track times, may not be single value
    u16 Checksum_1;
    u16 Checksum_2;
    
    u8 Unknown_static_4; // Always 01
    padding[3];
    
    SettingsNetwork settings_net;
    
    padding[75]; // Many unknown settings
    
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
