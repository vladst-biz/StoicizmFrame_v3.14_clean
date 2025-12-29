def extract(product):
    return {
        "voice_blocks": len(product.get("voice", [])),
        "has_voice": bool(product.get("voice"))
    }