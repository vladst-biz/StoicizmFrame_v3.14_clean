def extract(product):
    return {
        "visual_blocks": len(product.get("visual", [])),
        "diversity": len(set(product.get("visual", [])))
    }