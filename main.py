from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from timeit import timeit
from enum import Enum
from dataclasses import dataclass, InitVar, field
import requests
import json
from nbt.nbt import NBTFile
import io
import base64
import os
import time


def main():
    update = "n"
    if os.path.getsize('items.json') == 0 or time.time() - os.path.getmtime('items.json') > 300 or update == "f":
        print("updating...")
        items, tiers = get_dict()
    else:
        with open('items.json', 'r', encoding="utf-8") as f:
            items = json.load(f)
        with open('tiers.json', 'r', encoding="utf-8") as f:
            tiers = json.load(f)

    print("Pet crafting:")
    Pet('Armadillo', Rarity.COMMON, 1, 1e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Armadillo', Rarity.UNCOMMON, 1, 3e+4, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Armadillo', Rarity.RARE, 2, 25e+4, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Armadillo', Rarity.EPIC, 5, 1e+6, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Baby Yeti', Rarity.EPIC, 12, 2e+7, 'ENCHANTED_RAW_SALMON', 16).pets_profit_calc(items, tiers)
    Pet('Bat', Rarity.EPIC, 3, 25e+4, 'ENCHANTED_RED_MUSHROOM', 64).pets_profit_calc(items, tiers)
    Pet('Bal', Rarity.EPIC, 10, 2e+6, 'YOGGIE', 100).pets_profit_calc(items, tiers)
    Pet('Bee', Rarity.COMMON, 1, 5e+3, 'COAL', 128 * 9).pets_profit_calc(items, tiers)
    Pet('Bee', Rarity.UNCOMMON, 1, 4e+4, 'GOLD_INGOT', 128 * 9).pets_profit_calc(items, tiers)
    Pet('Bee', Rarity.RARE, 1, 15e+4, 'ENCHANTED_COAL_BLOCK', 9).pets_profit_calc(items, tiers)
    Pet('Bee', Rarity.EPIC, 3, 45e+4, 'ENCHANTED_GOLD_BLOCK', 9).pets_profit_calc(items, tiers)
    Pet('Blaze', Rarity.EPIC, 12, 1e+1, 'ENCHANTED_BLAZE_ROD', 64).pets_profit_calc(items, tiers)
    Pet('Blue Whale', Rarity.COMMON, 1, 15e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Blue Whale', Rarity.UNCOMMON, 2, 75e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Blue Whale', Rarity.RARE, 7, 9e+5, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Blue Whale', Rarity.EPIC, 12, 9e+6, 'ENCHANTED_COOKED_FISH', 8).pets_profit_calc(items, tiers)
    Pet('Chicken', Rarity.COMMON, 1, 2e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Chicken', Rarity.UNCOMMON, 1, 5e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Chicken', Rarity.RARE, 1, 19e+4, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Chicken', Rarity.EPIC, 1, 25e+4, 'ENCHANTED_RAW_CHICKEN', 8).pets_profit_calc(items, tiers)
    Pet('Dolphin', Rarity.COMMON, 1, 1e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Dolphin', Rarity.UNCOMMON, 2, 1e+6, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Dolphin', Rarity.RARE, 7, 1e+7, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Dolphin', Rarity.EPIC, 14, 5e+7, 'ENCHANTED_RAW_FISH', 16, ).pets_profit_calc(items, tiers)
    Pet('Elephant', Rarity.COMMON, 1, 15e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Elephant', Rarity.UNCOMMON, 1, 75e+3, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Elephant', Rarity.RARE, 5, 9e+6, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Elephant', Rarity.EPIC, 10, 14e+6, 'None', 0).pets_profit_calc(items, tiers)
    Pet('Ender Dragon', Rarity.EPIC, 20, 4e+8, 'SUMMONING_EYE', 8, ).pets_profit_calc(items, tiers)
    Pet('Enderman', Rarity.COMMON, 1, 1e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Enderman', Rarity.UNCOMMON, 2, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Enderman', Rarity.RARE, 6, 1e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Enderman', Rarity.EPIC, 12, 4e+7, 'ENCHANTED_EYE_OF_ENDER', 8, ).pets_profit_calc(items, tiers)
    Pet('Endermite', Rarity.RARE, 3, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Endermite', Rarity.EPIC, 7, 25e+4, 'ENCHANTED_ENDSTONE', 512, ).pets_profit_calc(items, tiers)
    Pet('Flying Fish', Rarity.RARE, 5, 2e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Flying Fish', Rarity.EPIC, 10, 1e+6, 'ENCHANTED_RAW_FISH', 64, ).pets_profit_calc(items, tiers)
    Pet('Ghoul', Rarity.EPIC, 10, 5e+6, 'REVENANT_FLESH', 512, ).pets_profit_calc(items, tiers)
    Pet('Giraffe', Rarity.COMMON, 1, 15e+3, 'ENCHANTED_ACACIA_LOG', 1, ).pets_profit_calc(items, tiers)
    Pet('Giraffe', Rarity.UNCOMMON, 2, 75e+3, 'ENCHANTED_ACACIA_LOG', 16, ).pets_profit_calc(items, tiers)
    Pet('Giraffe', Rarity.RARE, 7, 9e+5, 'ENCHANTED_ACACIA_LOG', 128, ).pets_profit_calc(items, tiers)
    Pet('Giraffe', Rarity.EPIC, 12, 9e+6, 'ENCHANTED_ACACIA_LOG', 512, ).pets_profit_calc(items, tiers)
    Pet('Golem', Rarity.EPIC, 20, 1e+7, 'ENCHANTED_IRON_BLOCK', 8, ).pets_profit_calc(items, tiers)
    Pet('Guardian', Rarity.COMMON, 1, 2e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Guardian', Rarity.UNCOMMON, 1, 1e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Guardian', Rarity.RARE, 2, 5e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Guardian', Rarity.EPIC, 5, 3e+6, 'ENCHANTED_PRISMARINE_SHARD', 64, ).pets_profit_calc(items, tiers)
    Pet('Horse', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Horse', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Horse', Rarity.RARE, 1, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Horse', Rarity.EPIC, 1, 25e+4, 'ENCHANTED_LEATHER', 8, ).pets_profit_calc(items, tiers)
    Pet('Hound', Rarity.EPIC, 10, 5e+6, 'WOLF_TOOTH', 512, ).pets_profit_calc(items, tiers)
    Pet('Jellyfish', Rarity.EPIC, 10, 16e+4, 'ENCHANTED_SLIME_BALL', 16, ).pets_profit_calc(items, tiers)
    Pet('Jerry', Rarity.EPIC, 3, 1e+5, 'None', 0, ).pets_profit_calc(items,
                                                                     tiers)  # has all rarities but they are often sold out
    Pet('Lion', Rarity.COMMON, 1, 15e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Lion', Rarity.UNCOMMON, 2, 75e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Lion', Rarity.RARE, 7, 9e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Lion', Rarity.EPIC, 14, 14e+6, 'ENCHANTED_RAW_BEEF', 1024, ).pets_profit_calc(items, tiers)
    Pet('Magma Cube', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Magma Cube', Rarity.RARE, 5, 1e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Magma Cube', Rarity.EPIC, 10, 5e+5, 'ENCHANTED_MAGMA_CREAM', 16, ).pets_profit_calc(items, tiers)
    Pet('Megalodon', Rarity.EPIC, 20, 1e+7, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Mithril Golem', Rarity.EPIC, 20, 5e+4, 'None', 0, ).pets_profit_calc(items,
                                                                              tiers)  # has all rarities but they are often sold out
    Pet('Monkey', Rarity.COMMON, 1, 15e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Monkey', Rarity.UNCOMMON, 2, 75e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Monkey', Rarity.RARE, 7, 9e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Monkey', Rarity.EPIC, 12, 17e+6, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Ocelot', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Ocelot', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Ocelot', Rarity.RARE, 2, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Ocelot', Rarity.EPIC, 5, 25e+4, 'ENCHANTED_JUNGLE_LOG', 512, ).pets_profit_calc(items, tiers)
    Pet('Parrot', Rarity.EPIC, 14, 15e+6, 'ENCHANTED_FEATHER', 16, ).pets_profit_calc(items, tiers)
    Pet('Phoenix', Rarity.EPIC, 20, 1e+8, 'ENCHANTED_BLAZE_POWDER', 1024, ).pets_profit_calc(items, tiers)
    Pet('Pig', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Pig', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Pig', Rarity.RARE, 1, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Pig', Rarity.EPIC, 1, 25e+4, 'PORK', 512, ).pets_profit_calc(items, tiers)
    Pet('Pigman', Rarity.EPIC, 10, 25e+4, 'ENCHANTED_GRILLED_PORK', 8, ).pets_profit_calc(items, tiers)
    Pet('Rabbit', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rabbit', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rabbit', Rarity.RARE, 1, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rabbit', Rarity.EPIC, 1, 25e+4, 'RABBIT', 64, ).pets_profit_calc(items, tiers)
    Pet('Rock', Rarity.COMMON, 1, 1e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rock', Rarity.UNCOMMON, 2, 1e+6, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rock', Rarity.RARE, 7, 1e+7, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Rock', Rarity.EPIC, 14, 5e+7, 'ENCHANTED_COBBLESTONE', 64, ).pets_profit_calc(items, tiers)
    Pet('Sheep', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Sheep', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Sheep', Rarity.RARE, 3, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Sheep', Rarity.EPIC, 7, 25e+4, 'ENCHANTED_MUTTON', 512, ).pets_profit_calc(items, tiers)
    Pet('Silverfish', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Silverfish', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Silverfish', Rarity.RARE, 1, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Silverfish', Rarity.EPIC, 3, 25e+4, 'ENCHANTED_COBBLESTONE', 64).pets_profit_calc(items, tiers)
    Pet('Skeleton', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Skeleton', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Skeleton', Rarity.RARE, 1, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Skeleton', Rarity.EPIC, 3, 25e+4, 'ENCHANTED_BONE', 64).pets_profit_calc(items, tiers)
    Pet('Spider', Rarity.EPIC, 7, 25e+4, 'ENCHANTED_STRING', 512).pets_profit_calc(items, tiers)
    Pet('Spirit', Rarity.EPIC, 10, 5e+6, 'ENCHANTED_GHAST_TEAR', 64, ).pets_profit_calc(items, tiers)
    Pet('Squid', Rarity.COMMON, 1, 2e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Squid', Rarity.UNCOMMON, 1, 1e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Squid', Rarity.RARE, 2, 5e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Squid', Rarity.EPIC, 5, 3e+6, 'ENCHANTED_INK_SACK', 64, ).pets_profit_calc(items, tiers)
    Pet('Tarantula', Rarity.EPIC, 10, 5e+6, 'TARANTULA_WEB', 512, ).pets_profit_calc(items, tiers)
    Pet('Tiger', Rarity.COMMON, 1, 15e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Tiger', Rarity.UNCOMMON, 12, 75e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Tiger', Rarity.RARE, 7, 9e+5, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Tiger', Rarity.EPIC, 14, 14e+6, 'ENCHANTED_RAW_CHICKEN', 1024, ).pets_profit_calc(items, tiers)
    Pet('Turtle', Rarity.EPIC, 10, 15e+6, 'ENCHANTED_RAW_FISH', 16, ).pets_profit_calc(items, tiers)
    Pet('Wither Skeleton', Rarity.EPIC, 5, 25e+4, 'ENCHANTED_COAL_BLOCK', 8).pets_profit_calc(items, tiers)
    Pet('Wolf', Rarity.COMMON, 1, 2e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Wolf', Rarity.UNCOMMON, 1, 5e+3, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Wolf', Rarity.RARE, 2, 19e+4, 'None', 0, ).pets_profit_calc(items, tiers)
    Pet('Wolf', Rarity.EPIC, 5, 25e+4, 'ENCHANTED_SPRUCE_LOG', 512).pets_profit_calc(items, tiers)
    Pet('Zombie', Rarity.EPIC, 10, 25e+4, 'ZOMBIE_HEART', 8).pets_profit_calc(items, tiers)

    print("Bazaar to npc:")  # not sure if it not works or if it is useless
    bz_to_npc = []
    for rarity in items:
        for item in rarity:
            if "value" and "npc_sell_price" in item:
                bz_to_npc.append(item)
                bz_to_npc.append(item["npc_sell_price"] - item["value"])
    for item, potential in bz_to_npc:
        if potential > 0:
            print(f"for selling {item} to npc you earn {potential} per")

    # ForgeResult("", [["", 2]], (0, 0, 0)).calculate(items, tiers)
    ForgeResult("REFINED_DIAMOND", [["ENCHANTED_DIAMOND_BLOCK", 2]], (6, 43, 12)).calculate(items, tiers)
    
    # Hyper Catalyst


class Rarity(str, Enum):
    VERY_SPECIAL = "VERY_SPECIAL"
    SPECIAL = "SPECIAL"
    SUPREME = "SUPREME"
    MYTHIC = "MYTHIC"
    LEGENDARY = "LEGENDARY"
    EPIC = "EPIC"
    RARE = "RARE"
    UNCOMMON = "UNCOMMON"
    COMMON = "COMMON"

    # SUPREME Display name was changed to DIVINE
    def next_tier(self):
        next_tiers = {
            Rarity.COMMON: Rarity.UNCOMMON,
            Rarity.UNCOMMON: Rarity.RARE,
            Rarity.RARE: Rarity.EPIC,
            Rarity.EPIC: Rarity.LEGENDARY,
            Rarity.LEGENDARY: Rarity.SUPREME,
            Rarity.SUPREME: Rarity.SPECIAL,
            Rarity.SPECIAL: Rarity.VERY_SPECIAL
        }
        return next_tiers[self]


def get_dict():
    """
    create a dict with all items, their value and rarity
    """
    # gets all data needed from the api
    pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
    urls = [f"https://api.hypixel.net/skyblock/auctions?page={i}" for i in range(pages)]
    bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
    resource_data = requests.get("https://api.hypixel.net/resources/skyblock/items").json()

    tiers = {
        item['id']: item.get('tier', 'COMMON')
        for item in resource_data['items']
    }

    items = get_items(get_auction(urls))

    with open('items.json', 'w', encoding="utf-8") as f:
        json.dump(items, f, indent=4, sort_keys=True)

    # adds bazaar items to items
    for product_data in bz_data['products'].values():
        if product_data['quick_status']['productId'] != "BAZAAR_COOKIE":
            items[tiers[product_data['quick_status']['productId']]][product_data['quick_status']['productId']] = {
                'value': product_data['quick_status']['buyPrice'] + 0.1}

    # adds npc_sell_price to all items that are in resource_data["items"]
    for item in resource_data["items"]:
        if item['id'] in items[tiers[item['id']]]:
            if "npc_sell_price" in item:
                items[tiers[item['id']]][item['id']]['npc_sell_price'] = item['npc_sell_price']
            else:
                items[tiers[item['id']]][item['id']]['npc_sell_price'] = 0

    # filler item
    for rarity in Rarity:
        items[Rarity[rarity]]['None'] = {'value': 0}

    with open('items.json', 'w', encoding="utf-8") as f:
        json.dump(items, f, indent=4, sort_keys=True)

    with open('tiers.json', 'w', encoding="utf-8") as f:
        json.dump(tiers, f, indent=4, sort_keys=True)

    return items, tiers


def get_auction(urls):
    with ThreadPoolExecutor() as executor:
        for page in executor.map(requests.get, urls):
            for auction in page.json().get('auctions', ()):
                if "bin" in auction:
                    yield auction


def get_items(auctions):
    with ProcessPoolExecutor() as executor:
        auctions_list = []
        future_ids = []
        for auction in auctions:
            auctions_list.append(auction)

            future_ids.append(executor.submit(receive_item_id, auction['item_bytes']))
        items = {rarity: {} for rarity in Rarity}
        for auction, future_id in zip(auctions_list, future_ids):

            item_id = future_id.result()
            if item_id == "PET":
                item_id = auction['item_name']
            items[Rarity[auction['tier']]][item_id] = {
                'value': auction['starting_bid'], "name": auction['item_name']
            }
    return items


def receive_item_id(raw):
    return str(NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))['i'][0]['tag']['ExtraAttributes']['id'])


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

    def pets_profit_calc(self, items, tiers):
        rarity_lower_cost = Pet.pets_lowest_bin(self, items, self.rarity)
        rarity_higher_cost = Pet.pets_lowest_bin(self, items, self.next_rarity)
        kat_flower_cost = items['SPECIAL']['KAT_FLOWER']['value'] * self.kat_flowers_needed
        coins_needed = self.cost
        if rarity_lower_cost is None or rarity_higher_cost is None:  # check if pets have active auctions
            return
        if self.item_needed != "None":  # check if pet needs item to upgrade
            item_price_n_quantity = items[tiers[self.item_needed]][self.item_needed]['value'] * self.item_amount
        else:
            item_price_n_quantity = 0

        money_after_kat = rarity_higher_cost - (
                rarity_lower_cost
                + kat_flower_cost
                + coins_needed
                + item_price_n_quantity
        )
        if money_after_kat > 0:
            print(f"{self.name.format(1)}, {self.rarity} to {self.next_rarity}: {int(money_after_kat)}")
        # else:
        #     print(f"No Profit when converting the Pet: {self.name.format(1)} from {self.rarity} to {self.next_rarity}")

    def pets_lowest_bin(self, items, rarity):
        """
        :returns the lowest bin of a pet of a specific rarity
        not done!!! add  \u2726 and Bal doesnt work
        """
        values = []

        for level in range(100):
            if self.name.format(level) in items[rarity]:
                values.append(items[rarity][self.name.format(level)]['value'])

        try:
            return min(values)
        except ValueError:
            print(f"{self.name.format(1)} of the rarity {rarity} has no auctions")
            return None


@dataclass
class ForgeResult:
    output: str
    input_list: list
    time_tuple: tuple

    def calculate(self, items, tiers):
        time_seconds = (self.time_tuple[0] * 60 + self.time_tuple[1]) * 60 + self.time_tuple[2]
        input_cost = 0.0
        for item, quantity in self.input_list:
            input_cost += items[tiers[item]][item]["value"] * quantity
        profit = items[tiers[self.output]][self.output]["value"] - input_cost
        per_hour = profit / time_seconds * 3600

        print(f" Making {self.output} gives {per_hour:.1f} per hour and {profit:.1f} in total")


if __name__ == '__main__':
    print(f"\n[Finished in {timeit(main, number=1):.1f}]")
