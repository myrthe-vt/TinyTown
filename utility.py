def safe_cast_to_int(data):
    if data is None:
        return 0
    else:
        return int(data)    