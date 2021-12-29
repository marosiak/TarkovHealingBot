import random
import time
from dataclasses import dataclass

import mouse
from python_imagesearch.imagesearch import imagesearcharea, imagesearch, region_grabber, imagesearch_from_folder
from win32api import GetSystemMetrics

from tarkov_lib.item import Item


class NotFoundException(Exception):
    pass


@dataclass
class Region:
    x: int
    y: int
    size_x: int
    size_y: int

    @staticmethod
    def valid_region(region, resolution):
        if region is None:
            return Region(x=0, y=0, size_x=resolution[0], size_y=resolution[1])
        else:
            return region

    def __str__(self):
        return f" (Region x: {self.x} y:{self.y} size_x: {self.size_x} size_y: {self.size_y})"


class Inventory:
    def __init__(self, multi_monitors_support: bool, search_precision=0.8):
        self.lag_secs = 0.126
        self.move_duration_min = 0.1012
        self.move_duration_max = 0.431
        self.search_precision = search_precision

        self.multi_monitors_support = multi_monitors_support
        self.resolution = (GetSystemMetrics(0), GetSystemMetrics(1))

    def __search(self, item_icon_path, region: Region = None, im=None):
        region = Region.valid_region(region=region, resolution=self.resolution)

        return imagesearcharea(item_icon_path, region.x, region.y, region.size_x, region.size_y,
                               precision=self.search_precision, im=im)

    def __search_many(self, item_icons_paths: list, region: Region = None):
        region = Region.valid_region(region=region, resolution=self.resolution)

        im = region_grabber((region.x, region.y, region.size_x, region.size_y))

        output = []
        for icon in item_icons_paths:
            pos = imagesearcharea(image=icon, x1=region.x, y1=region.y, x2=region.size_x, y2=region.size_y,
                                  precision=self.search_precision, im=im)
            if pos[0] == -1:
                continue

            output.append(pos)

        return output

    def find_item(self, item_icon_path: str, region: Region = None) -> Item:
        pos = self.__search(item_icon_path, region)

        if pos[0] == -1:
            time.sleep(self.lag_secs)
            raise NotFoundException

        return Item(position=(
            pos[0] + 5, pos[1] + 5))  # +5px - so the game will detect the item, not the edge which is not clickable

    def find_items(self, item_icons_paths) -> list[Item]:
        im = region_grabber((0, 0, self.resolution[0], self.resolution[1]))

        for path in item_icons_paths:
            pos = self.__search(path, im=im)

            if pos[0] == -1:
                continue

            yield Item(position=pos)

    def find_any_by_icons_list(self, icons_list: list) -> Item:
        for icon in icons_list:

            try:
                item = self.find_item(item_icon_path=icon)
                return item
            except NotFoundException:
                continue

        raise NotFoundException

    def __get_random_move_duration(self):
        return random.uniform(self.move_duration_min, self.move_duration_max)

    def open_context_menu(self, pos, move_duration_secs: int = -1):
        if move_duration_secs == -1:
            move_duration_secs = self.__get_random_move_duration

        mouse.move(x=pos[0], y=pos[1], duration=move_duration_secs)
        mouse.click(mouse.LEFT)  # Just to set up focus, in case user is doing something on other display
        time.sleep(0.1)
        mouse.click(mouse.RIGHT)
        time.sleep(0.126)

    def click_context_option(self, button_index: int, move_duration_secs: int = -1):
        if move_duration_secs == -1:
            move_duration_secs = self.__get_random_move_duration

        mouse.move(x=17, y=7 + (25 * button_index), absolute=False, duration=move_duration_secs)
        mouse.click(mouse.LEFT)
