def extract(product):
    return {
        "complete": "timeline" in product and "visual" in product and "voice" in product
    }