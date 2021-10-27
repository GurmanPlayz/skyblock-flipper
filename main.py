from concurrent.futures import ThreadPoolExecutor
from timeit import timeit
from enum import Enum
from dataclasses import dataclass
import requests
import json
from collections import defaultdict
import nbt
import io
import base64


def decode_nbt(raw):  # may be used in the future
    return nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))


def main():
    items_dict = get_data()
    # Pets crafting (in Progress) # Pet('', Rarity.EPIC, 10, 1e+1, 'None', 0).pets_profit_calc(items_dict)
    # Pet('Armadillo', Rarity.COMMON, 1, 1e+4, 'None', 0).pets_profit_calc(items_dict)
    '''Pet('Armadillo', Rarity.UNCOMMON, 1, 3e+4, 'None', 0).pets_profit_calc(items_dict)
    Pet('Armadillo', Rarity.RARE, 2, 25e+4, 'None', 0).pets_profit_calc(items_dict)
    Pet('Armadillo', Rarity.EPIC, 5, 1e+6, 'None', 0).pets_profit_calc(items_dict)
    Pet('Baby Yeti', Rarity.EPIC, 12, 2e+7, 'ENCHANTED_RAW_SALMON', 16).pets_profit_calc(items_dict)
    # Pet('Bat', Rarity.COMMON, 1, 2e+3, 'None', 0).pets_profit_calc(items_dict)
    Pet('Bat', Rarity.UNCOMMON, 1, 5e+3, 'None', 0).pets_profit_calc(items_dict)
    Pet('Bat', Rarity.RARE, 1, 19e+4, 'None', 0).pets_profit_calc(items_dict)
    Pet('Bat', Rarity.EPIC, 3, 25e+4, 'ENCHANTED_RED_MUSHROOM', 64).pets_profit_calc(items_dict)
    Pet('Bal', Rarity.COMMON, 1, 2e+6, 'YOGGIE', 100).pets_profit_calc(items_dict)
    Pet('Bee', Rarity.COMMON, 1, 5e+3, 'COAL', 128 * 9).pets_profit_calc(items_dict)
    Pet('Bee', Rarity.UNCOMMON, 1, 4e+4, 'GOLD_INGOT', 128 * 9).pets_profit_calc(items_dict)
    Pet('Bee', Rarity.RARE, 1, 15e+4, 'ENCHANTED_COAL_BLOCK', 9).pets_profit_calc(items_dict)
    Pet('Bee', Rarity.EPIC, 3, 45e+4, 'ENCHANTED_GOLD_BLOCK', 9).pets_profit_calc(items_dict)
    Pet('Blaze', Rarity.EPIC, 12, 1e+1, 'ENCHANTED_BLAZE_ROD', 64).pets_profit_calc(items_dict)
    Pet('Blue Whale', Rarity.COMMON, 1, 15e+3, 'None', 0).pets_profit_calc(items_dict)
    Pet('Blue Whale', Rarity.UNCOMMON, 2, 75e+3, 'None', 0).pets_profit_calc(items_dict)
    Pet('Blue Whale', Rarity.RARE, 7, 9e+5, 'None', 0).pets_profit_calc(items_dict)
    Pet('Blue Whale', Rarity.EPIC, 12, 9e+6, 'ENCHANTED_COOKED_FISH', 8).pets_profit_calc(items_dict)
    Pet('Chicken', Rarity.EPIC, 10, 1e+1, 'None', 0).pets_profit_calc(items_dict)

    Pet('Elephant', Rarity.EPIC, 10, 14e+6, 'None', 0).pets_profit_calc(items_dict)
    Pet('Wither Skeleton', Rarity.EPIC, 5, 25e+4, 'ENCHANTED_COAL_BLOCK', 8).pets_profit_calc(items_dict)'''
    # BZ to NPC (in Progress)


class Rarity(str, Enum):
    VERY_SPECIAL = "VERY_SPECIAL"
    SPECIAL = "SPECIAL"
    DIVINE = "DIVINE"
    MYTHIC = "MYTHIC"
    LEGENDARY = "LEGENDARY"
    EPIC = "EPIC"
    RARE = "RARE"
    UNCOMMON = "UNCOMMON"
    COMMON = "COMMON"

    def next_tier(self):
        next_tiers = {
            Rarity.COMMON: Rarity.UNCOMMON,
            Rarity.UNCOMMON: Rarity.RARE,
            Rarity.RARE: Rarity.EPIC,
            Rarity.EPIC: Rarity.LEGENDARY,
            Rarity.LEGENDARY: Rarity.DIVINE,
            Rarity.DIVINE: Rarity.SPECIAL,
            Rarity.SPECIAL: Rarity.VERY_SPECIAL
        }
        return next_tiers[self]


def get_data():  # create a dict with all items, their value and rarity
    # CLEAN UP THIS MESS
    # gets all data needed from the api
    pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
    urls = [f"https://api.hypixel.net/skyblock/auctions?page={i}" for i in range(pages)]
    bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
    ressource_data = requests.get("https://api.hypixel.net/resources/skyblock/items").json()

    # auction items
    with ThreadPoolExecutor() as executor:
        items = {
            recieve_item_id(auction["item_bytes"]): {"tier": auction["tier"], "value": [auction["starting_bid"]]}
            for page in executor.map(requests.get, urls)
            for auction in page.json().get("auctions", ())
            if "bin" in auction
        }

    #
    tiers = {}
    for item in ressource_data['items']:
        if 'tier' in item:
            tiers.update({item['id']: item['tier']})
        else:
            tiers.update({item['id']: "COMMON"})

    # bazaar items
    for product_data in bz_data['products'].values():
        if 1 == 1:
            items.update({
                product_data['quick_status']['productId']:
                    {"tier": tiers[product_data['quick_status']['productId']], "value": [product_data['quick_status']['buyPrice'] + 0.1]}
            })
    with open('items.txt', 'w', encoding="utf-8") as f:
        json.dump(items, f, indent=4, sort_keys=True)

    # adds npc_sell_price
    for item in ressource_data["items"]:
        if item["id"] in items:

            if "npc_sell_price" in item:
                items[item["id"]][tiers[item["id"]]].append(item["npc_sell_price"])
            else:
                if 'VANILLA' in items[item['id']]:
                    items[item["id"]]['COMMON'].append(0)
                else:
                    items[item["id"]][item['tier']].append(0)

    # filler item
    items.update({"None": {'COMMON': 0}})

    # currently just for debug
    with open('items.txt', 'w', encoding="utf-8") as f:
        json.dump(items, f, indent=4, sort_keys=True)
    return items


@dataclass
class Pet:
    name_raw: str
    rarity: Rarity
    kat_flowers_needed: int
    cost: int | float
    item_needed: str
    item_amount: int

    def pets_profit_calc(self, items_dict):
        name_formatted = f"[Lvl {{}}] {self.name_raw}"
        rarity2_higher_cost = Pet.pets_lowest_bin(self, items_dict, self.rarity.next_tier(), name_formatted)
        rarity_lower_cost = Pet.pets_lowest_bin(self, items_dict, self.rarity, name_formatted)
        kat_flower_cost = items_dict['Kat Flower']['SPECIAL'] * self.kat_flowers_needed
        coins_needed = self.cost
        item_price_n_quantity = items_dict[self.item_needed]['COMMON'] * self.item_amount

        pet_rarity1_to_rarity2 = rarity2_higher_cost - (
                rarity_lower_cost
                + kat_flower_cost
                + coins_needed
                + item_price_n_quantity
        )
        print(f"{name_formatted.format(1)}, {self.rarity} to {self.rarity.next_tier()}: {pet_rarity1_to_rarity2}")

    def pets_lowest_bin(self, items_dict, rarity, name_formatted):
        return min(
            items_dict[name_formatted.format(level)][rarity]
            for level in range(100)
            if
            name_formatted.format(level) in items_dict and items_dict[name_formatted.format(level)] == rarity
        )


def recieve_item_id(raw):
    item_nbt = decode_nbt(raw)
    print(item_nbt)
    return item_nbt[0][0][2][3][2]


def decode_nbt(raw):  # may be used in the future
    return nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))


if __name__ == '__main__':
    print(f"\n[Finished in {timeit(main, number=1):.1f}]")
