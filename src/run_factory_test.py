from contentgenerationmodule import run_factory

if __name__ == "__main__":
    topic = "Как сохранять спокойствие в хаосе"
    result = run_factory(topic)

    print("\n=== ENTRY + SCENE + LEGACY ===\n")
    print(result["scene"])

    print("\n=== TELEGRAM POST ===\n")
    print(result["tg_post"])

    print("\n=== COVER (IMAGE RESPONSE) ===\n")
    print(result["cover"])
