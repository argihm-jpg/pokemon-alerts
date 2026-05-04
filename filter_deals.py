MIN_MARKET_PRICE = 10.00
MIN_DISCOUNT = 0.20
TOP_N = 5

# Sets with active secondary market demand
HIGH_DEMAND_SETS = {
    # Modern (Scarlet & Violet era)
    "Surging Sparks",
    "Prismatic Evolutions",
    "Shrouded Fable",
    "Paldean Fates",
    "Scarlet & Violet—151",
    "151",
    "Crown Zenith",
    "Obsidian Flames",
    "Twilight Masquerade",
    "Paradox Rift",
    "Temporal Forces",
    "Stellar Crown",
    "Destined Rivals",
    # Vintage / high collector demand
    "Base Set",
    "Jungle",
    "Fossil",
    "Team Rocket",
    "Gym Heroes",
    "Gym Challenge",
    "Neo Genesis",
    "Neo Discovery",
    "Neo Revelation",
    "Neo Destiny",
    "Legendary Collection",
    "Skyridge",
    "Aquapolis",
    "EX Dragon Frontiers",
    "EX Crystal Guardians",
}

# Premium rarities with consistent resale demand
HIGH_DEMAND_RARITIES = {
    "Illustration Rare",
    "Special Illustration Rare",
    "Hyper Rare",
    "Rare Secret",
    "Trainer Gallery Rare Holo",
    "Rare Ultra",
    "Shiny Ultra Rare",
    "ACE SPEC Rare",
}

# Cards worth alerting on — anything not in this set is bulk with no market potential
VALUABLE_RARITIES = {
    "Rare Holo",
    "Rare Holo EX",
    "Rare Holo GX",
    "Rare Holo V",
    "Rare Holo VMAX",
    "Rare Holo VSTAR",
    "Rare Rainbow",
    "Rare Secret",
    "Rare Shining",
    "Rare Shiny",
    "Rare Shiny GX",
    "Rare Ultra",
    "Amazing Rare",
    "Radiant Rare",
    "Illustration Rare",
    "Special Illustration Rare",
    "Hyper Rare",
    "Trainer Gallery Rare Holo",
    "Double Rare",
    "Shiny Rare",
    "Shiny Ultra Rare",
    "ACE SPEC Rare",
    "LEGEND",
}


def apply_filters(price_entries: list[dict], seen_ids: set[str]) -> list[dict]:
    qualifying = []
    for entry in price_entries:
        if entry["card_id"] in seen_ids:
            continue
        if entry.get("rarity", "") not in VALUABLE_RARITIES:
            continue
        if entry["market_price"] < MIN_MARKET_PRICE:
            continue
        deal_score = (entry["market_price"] - entry["low_price"]) / entry["market_price"]
        if deal_score < MIN_DISCOUNT:
            continue
        in_demand = (
            entry["set_name"] in HIGH_DEMAND_SETS
            or entry.get("rarity", "") in HIGH_DEMAND_RARITIES
        )
        if not in_demand:
            continue
        qualifying.append({**entry, "deal_score": deal_score})

    qualifying.sort(key=lambda x: x["deal_score"], reverse=True)
    return qualifying[:TOP_N]
