
struct SettingsNetwork {
    u8 UnitID; // +1 to match menu
    u8 na_1[3];
    bool Enable; // Inverted
};


// Example
struct SettingsTrackDiff {
    u8 TrackDifficulty;
    char na_1[0x03];
};

// Example
struct SettingsTrackAi {
    u8 AiDifficulty;
    char na_1[0x03];
};

struct SettingsTrack {
    SettingsTrackDiff trackDiff[13];
    SettingsTrackAi aiDiff[13];
};

// Example
struct HighScore {
    u8 Boat_Type;
    char Initials[0x03];
    float TimeSeconds;
};

HighScore score[130] @ 0x075BE7DF;

struct BestSplit {
    float TimeSeconds[5];
};

BestSplit splits[13] @ 0x075BEBF3;


u32 CheckSum @ 0x75BE66F;


SettingsNetwork settings_net @ 0x75BE677;
SettingsTrack settings_track @ 0x75BE6C7;

bool setting_FreePlay @ 0x75BE6B3;

