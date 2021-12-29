import os

class IconsProvider:
    def __init__(self):
        pass


def load_icons(icons_directory) -> list:
    icons = []
    for filename in os.listdir(icons_directory):
        if filename.endswith(".png"):
            icons.append(f"{icons_directory}/{filename}")

    return icons
