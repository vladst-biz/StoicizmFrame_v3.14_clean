def extract(product):
    return {
        "publish_ready": product.get("meta", {}).get("export") == "ready"
    }