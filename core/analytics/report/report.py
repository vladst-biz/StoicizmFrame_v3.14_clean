def build_report(metrics: dict) -> str:
    lines = []
    for section, values in metrics.items():
        lines.append(f"[{section}]")
        for key, value in values.items():
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)