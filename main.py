import time

from tarkov.inventory import Inventory, NotFoundException
from tarkov.inventory_bot_config import InventoryBotConfig

if __name__ == '__main__':
    cfg = InventoryBotConfig(
        icons_directory="icons/meds",
        multi_monitors_support=True,
        resolution=(1920, 1080)
    )

    inventory = Inventory(cfg)
    time.sleep(3)

    while True:
        try:
            healing_item_pos = inventory.find_any_by_icons_list(cfg.icons)
        except NotFoundException:
            continue

        inventory.open_context_menu(healing_item_pos)
        inventory.click_context_option(1)
        time.sleep(7.5)
