def crypto_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "cost": float(item["cost"])
    }


def serialize_dict(entity) -> dict:
    if entity is not None:
        return {**{i: str(entity[i]) for i in entity if i == '_id'}, **{i: entity[i] for i in entity if i != '_id'}}
    return None
