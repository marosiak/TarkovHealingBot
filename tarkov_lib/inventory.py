import time

import mouse
from python_imagesearch.imagesearch import imagesearcharea, imagesearch

from tarkov_lib.inventory_bot_config import InventoryBotConfig
from tarkov_lib.item import Item


class NotFoundException(Exception):
    pass


class Inventory:
    def __init__(self, config: InventoryBotConfig):
        self.cfg = config

    def find_item_position(self, item_icon) -> Item:
        icon_path = f"./{self.cfg.icons_directory}/{item_icon}"

        if self.cfg.multi_monitors_support:
            pos = imagesearcharea(icon_path, 0, 0, self.cfg.resolution[0], self.cfg.resolution[1])
        else:
            pos = imagesearch(icon_path)

        if pos[0] == -1:
            time.sleep(self.cfg.lag_secs)
            raise NotFoundException

        return Item(position=(pos[0] + 5, pos[1] + 5))  # +5px - so the game will detect the item, not the edge which is not clickable

    def find_any_by_icons_list(self, icons_list: list) -> Item:
        for icon in icons_list:
            try:
                # TODO: Podwójna weryfikacja tu
                item = self.find_item_position(item_icon=icon)
                return item
            except NotFoundException:
                continue

        raise NotFoundException

    def open_context_menu(self, pos):
        mouse.move(x=pos[0], y=pos[1], duration=self.cfg.move_duration_secs)
        mouse.click(mouse.LEFT)  # Just to set up focus, in case user is doing something on other display
        time.sleep(0.1)
        mouse.click(mouse.RIGHT)
        time.sleep(0.126)

    def click_context_option(self, button_index: int):
        mouse.move(x=17, y=7 + (25 * button_index), absolute=False, duration=self.cfg.move_duration_secs)
        mouse.click(mouse.LEFT)
