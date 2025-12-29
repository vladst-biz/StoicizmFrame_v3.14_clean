def extract(product):
    return {
        "version": product.get("meta", {}).get("version", "unknown")
    }