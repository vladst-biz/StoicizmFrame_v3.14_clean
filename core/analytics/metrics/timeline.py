def extract(product):
    return {
        "timeline_length": len(product.get("timeline", []))
    }