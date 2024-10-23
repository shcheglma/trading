from fastapi import status, APIRouter, HTTPException
from bson.objectid import ObjectId
from settings import currency_collection
from model import Crypto
from serializer import serializeDict, serializeList

router = APIRouter()
base = "/crypto/"

_notFoundMessage = "Could not find user with the given Id."


async def insert_crypto(data: Crypto):
    result = currency_collection.insert_one(dict(data))
    return serializeDict(currency_collection.find_one({"_id": ObjectId(result.inserted_id)}))


async def update_crypto(id, data: Crypto) -> bool:
    currency_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
    return True


def get_response(done: bool, errorMessage: str):
    if not done:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=errorMessage)
    return None


async def rise_http_exception_if_not_found(result, message: str):
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


async def get_by_id(id):
    return serializeDict(currency_collection.find_one({"_id": ObjectId(id)}))


