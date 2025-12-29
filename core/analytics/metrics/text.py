def extract(product):
    return {
        "length": len(product.get("timeline", [])),
        "has_voice": "voice" in product,
        "has_visual": "visual" in product
    }