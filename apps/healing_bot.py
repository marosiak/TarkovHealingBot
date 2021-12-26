import time

import mouse

from tarkov_lib.icons import load_icons
from tarkov_lib.inventory import Inventory, NotFoundException

if __name__ == '__main__':

    inventory = Inventory(multi_monitors_support=True)
    time.sleep(3)

    while True:
        try:
            healing_item = inventory.find_any_by_icons_list(load_icons("../icons/meds"))
        except NotFoundException:
            continue

        inventory.open_context_menu(healing_item.position)
        inventory.click_context_option(1)
        mouse.move(x=15, y=15, duration=0.1)
        time.sleep(7.5)
