try:
    try:
        raise ValueError("An error occurred")
    except ValueError as e:
        raise ValueError("A runtime error occurred") from e
except ValueError as e:
    print(f"Caught an exception: {e}", flush=True)
    raise RuntimeError("A runtime error occurred") from e
