from concurrent.futures import ThreadPoolExecutor
from timeit import timeit
from enum import Enum
from dataclasses import dataclass, InitVar, field
import requests
import json
from nbt.nbt import NBTFile
import io
import base64


def main():
    items_dict = get_data()
    # Pets crafting (in Progress) # Pet(Rarity.EPIC, 10, 1e+4, 'None', 0, '').pets_profit_calc(items_dict)
    Pet('Armadillo', Rarity.COMMON, 1, 1e+4, 'None', 0, ).pets_profit_calc(items_dict)
    Pet('Armadillo', Rarity.UNCOMMON, 1, 3e+4, 'None', 0).pets_profit_calc(items_dict)
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
    Pet('Wither Skeleton', Rarity.EPIC, 5, 25e+4, 'ENCHANTED_COAL_BLOCK', 8).pets_profit_calc(items_dict)
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


def get_data():  #
    """
    create a dict with all items, their value and rarity
    """
    # gets all data needed from the api
    pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
    urls = [f"https://api.hypixel.net/skyblock/auctions?page={i}" for i in range(pages)]
    bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
    resource_data = requests.get("https://api.hypixel.net/resources/skyblock/items").json()

    # auction items # ONLY 1 PET RARITY SAVED

    with ThreadPoolExecutor() as executor:
        items = {
            receive_item_id(auction["item_bytes"]):
                {"tier": auction["tier"],
                 "value": auction["starting_bid"],
                 "name": auction["item_name"]}
            for page in executor.map(requests.get, urls)
            for auction in page.json().get("auctions", ())
            if "bin" in auction
        }

    # this is needed because the bazaar api does not include rarity
    tiers = {}
    for item in resource_data['items']:
        if 'tier' in item:
            tiers.update({item['id']: item['tier']})
        else:
            tiers.update({item['id']: "COMMON"})

    # bazaar items
    for product_data in bz_data['products'].values():
        if product_data['quick_status']['productId'] != 'BAZAAR_COOKIE':
            items.update({
                product_data['quick_status']['productId']:
                    {"tier": tiers[product_data['quick_status']['productId']],
                     "value": product_data['quick_status']['buyPrice'] + 0.1}
            })

    # adds npc_sell_price
    for item in resource_data["items"]:
        if item["id"] in items:
            if "npc_sell_price" in item:
                items[item["id"]].update({"npc_sell_price": item["npc_sell_price"]})
            elif "tier" in items[item['id']]:
                items[item["id"]].update({"npc_sell_price": 0})
            else:
                print(item)
                print(item["id"])
                raise KeyError("ouch")

    # filler item
    items.update({"filler": {"tier": "COMMON", "value": 0}})

    # currently just for debug
    with open('items.txt', 'w', encoding="utf-8") as f:
        json.dump(items, f, indent=4, sort_keys=True)
    return items


@dataclass
class Pet:
    name_raw: InitVar[str]
    rarity: Rarity
    kat_flowers_needed: int
    cost: int | float
    item_needed: str
    item_amount: int
    next_rarity: Rarity = field(init=False)
    name: str = field(init=False)

    def __post_init__(self, name_raw):
        self.next_rarity = self.rarity.next_tier()
        self.name = f"[Lvl {{}}] {name_raw}"

    def pets_profit_calc(self, items_dict):
        rarity2_higher_cost = Pet.pets_lowest_bin(self, items_dict, self.next_rarity)
        rarity_lower_cost = Pet.pets_lowest_bin(self, items_dict, self.rarity)
        kat_flower_cost = items_dict['Kat Flower']['value'] * self.kat_flowers_needed
        coins_needed = self.cost
        item_price_n_quantity = items_dict[self.item_needed]['value'] * self.item_amount

        pet_rarity1_to_rarity2 = rarity2_higher_cost - (
                rarity_lower_cost
                + kat_flower_cost
                + coins_needed
                + item_price_n_quantity
        )
        print(f"{self.name.format(1)}, {self.rarity} to {self.next_rarity}: {pet_rarity1_to_rarity2}")

    def pets_lowest_bin(self, items_dict, rarity):
        """
        :returns the lowest bin of a pet of a specific rarity
        not done!!!
        """
        return min(
            items_dict[self.name.format(level)]["value"]
            for level in range(100)
            if self.name.format(level) in items_dict and items_dict[self.name.format(level)] == rarity
        )


def receive_item_id(raw):
    return str(NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))["i"][0]["tag"]["ExtraAttributes"]["id"])


if __name__ == '__main__':
    print(f"\n[Finished in {timeit(main, number=1):.1f}]")
