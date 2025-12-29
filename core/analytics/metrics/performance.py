def extract(product):
    return {
        "export_ready": product.get("meta", {}).get("export") == "ready"
    }