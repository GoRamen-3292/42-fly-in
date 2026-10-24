from ..model import Connection, Hub, HubType, SimulationConfig


def parse_line(line: str, config: SimulationConfig) -> None:
    """1行のパースをする関数"""
    if line.startswith("#") or not line:
        return

    try:
        key, value = line.split(":")
        key = key.strip()
        value = value.strip()

        if key in HubType.__members__.values():
            config.hubs.append(_parse_hub_line(HubType(key), value, config))
        elif key == "connection":
            _parse_connection_line(value, config)
        elif key == "nb_drones":
            if config.nb_drones is not None:
                raise ValueError("nb_drones is already set")
            config.nb_drones = int(value)
    except ValueError:
        raise ValueError(f"Invalid line format: {line}")


def _parse_hub_line(hub_type: HubType, value: str,
                    config: SimulationConfig) -> Hub:
    """hubの行をパースする関数"""
    values = value.split()

    if len(values) >= 3:
        name, x, y = values[:3]
        options = values[3:] if len(values) > 3 else []
    else:
        raise ValueError(f"Too few args for line ==N==: {value}")

    d: dict[str, str] = _parse_options(" ".join(options))

    zone = d.get("zone", Hub.model_fields["zone"].default)
    max_drones = int(
        d.get("max_drones", Hub.model_fields["max_drones"].default))
    return Hub(
        hub_type=hub_type,
        name=name,
        coordinate=(int(x), int(y)),
        zone=zone,
        max_drones=max_drones,
        color=d.get("color")
    )


def _parse_options(options: str) -> dict[str, str]:
    """オプションのパースをする関数"""
    result: dict[str, str] = {}
    options = options.strip().strip("[]")
    for option in options.split():
        key, value = (x.strip() for x in option.split("="))
        result[key] = value

    return result


def _parse_connection_line(value: str, config: SimulationConfig) -> Connection:
    """connectionの行をパースする関数"""
    # ここでvalueを解析してConnectionを作成し、configに追加する処理を書く
    raise NotImplementedError("Connection parsing is not implemented yet.")
