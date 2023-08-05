import uuid


def unique_id_str() -> str:
    return str(uuid.uuid1())


def unique_id_int() -> int:
    return uuid.uuid1().int
