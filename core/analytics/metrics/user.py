def extract(product):
    return {
        "user_patterns": product.get("meta", {}).get("user_patterns", [])
    }