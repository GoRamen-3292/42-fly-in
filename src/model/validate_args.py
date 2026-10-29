def validate_hub_name(name: str) -> str:
    """
    hubの名前が正しい形式であることを検証する関数

    Args:
        name (str): The name to verify.
    Raises:
        ValueError: If the name is invalid.
    """
    if "-" in name:
        raise ValueError(
            "Hub name cannot contain '-' character. "
            "It uses '-' as a separator for hub names in connections.")
    elif any(c.isspace() for c in name):
        raise ValueError(
            "Hub name cannot contain spaces. "
            "It uses spaces as a separator for hub names in connections.")
    return name


def validate_metadata(name: str, value: str) -> str:
    """
    メタデータの文字列の値が正しい形式であることを検証する関数
    """
    if "=" in value or any(c.isspace() for c in value):
        raise ValueError(
            f"{name} must not contain spaces or equal signs."
        )
    elif not value:
        raise ValueError(
            f"{name} must not be empty."
        )
    return value
