from config.settings_manager import (
    load_settings,
    save_settings
)


settings = load_settings()

print(settings)

settings["profile"] = "PVGC2"

save_settings(settings)

print(
    load_settings()
)