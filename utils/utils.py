def get_root_node_key(data: dict):
    for key, value in data.items():
        if value == (None, None):
            return key
    return False


