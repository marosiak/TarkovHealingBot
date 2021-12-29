import time
import keyboard
import mouse

from tarkov_lib.icons import load_icons
from tarkov_lib.inventory import Inventory, NotFoundException

if __name__ == '__main__':
    inventory = Inventory(
        multi_monitors_support=True,
        search_precision=0.8
    )

    while True:
        if keyboard.read_key() == "f6":
            start_time = time.time()
            try:
                scav_box = inventory.find_item("../icons/containers/scav_box.png")
                mouse.move(x=scav_box.position[0], y=scav_box.position[1], duration=0)

                items_to_sort = inventory.find_items(load_icons("../icons/barter_items"))
                for item in items_to_sort:
                    mouse.move(x=item.position[0], y=item.position[1], duration=0.1)

            except NotFoundException:
                print("Not found")
            print(f"Done in {(time.time() - start_time)}")




