import time

import mouse

from tarkov_lib.inventory import Inventory, NotFoundException
from tarkov_lib.inventory_bot_config import InventoryBotConfig

if __name__ == '__main__':
    cfg = InventoryBotConfig(
        icons_directory="../icons/meds",
        multi_monitors_support=True,
        resolution=(1920, 1080)
    )

    inventory = Inventory(cfg)
    time.sleep(3)

    while True:
        try:
            healing_item = inventory.find_any_by_icons_list(cfg.icons)
        except NotFoundException:
            continue

        inventory.open_context_menu(healing_item.position)
        inventory.click_context_option(1)
        mouse.move(x=15, y=15, duration=0.1)
        time.sleep(7.5)
