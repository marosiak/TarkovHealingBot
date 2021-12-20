import os


# In future, it will load data from json file
class InventoryBotConfig:
    def __init__(self, icons_directory: str, multi_monitors_support: bool, resolution: tuple,
                 lag_secs: float = 0.126, move_duration_secs: float = 0.2):
        self.icons_directory = icons_directory

        self.multi_monitors_support = multi_monitors_support

        # Will be needed only in case multi_monitors_support==True, in future there will be auto detection
        self.resolution = resolution

        self.icons = []
        self.load_icons(icons_directory)

        self.lag_secs = lag_secs

        self.move_duration_secs = move_duration_secs

    def load_icons(self, icons_directory):
        for filename in os.listdir(icons_directory):
            if filename.endswith(".png"):
                self.icons.append(filename)
