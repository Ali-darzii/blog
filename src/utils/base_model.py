from typing import List
import pymongo
from Blog.settings import MONGO_DB
from bson import ObjectId
from django.db import models


class Manger:
    id = None
    object_id = None

    def __init__(self, collection):
        self._collection = collection

    def to_dict(self):
        """ Return dict representation of instance except _id"""
        return {key: value for key, value in self.__dict__.items() if key != "object_id" or not key.startswith("_")}

    @classmethod
    def _object_id_convertor(cls, **kwargs):
        for key, value in kwargs.items():
            if key == "_id":
                if not isinstance(value, ObjectId):
                    kwargs[key] = ObjectId(value)
                    break
                else:
                    kwargs[key] = str(value)
                    break
        return kwargs

    @classmethod
    def get_all_collections(cls):
        """ Return all collections in collection """
        return MONGO_DB.list_collection_names()

    def create(self):
        """
        Insert instance into collection
        When id remain None it means somthing went wrong!
        """
        collection = self._collection()
        self.object_id = collection.insert_one(self.to_dict()).inserted_id
        self.id = str(self.object_id)

    def all(self, sort: List[str]):
        """
        Return all documents in collection
        sort like ["username"] or for DESCENDING ["-username"]
        """
        collection = self._collection
        documents = collection.find()
        for item in sort:
            if item[0] == "-":
                item.replace("-", "")
                documents.sort(item, pymongo.ASCENDING)
            else:
                documents.sort(item, pymongo.DESCENDING)

        return [self._object_id_convertor(**document) for document in documents]

    def get(self, **kwargs):
        """ Return first filtered document """
        kwargs = self._object_id_convertor(**kwargs)
        collection = self._collection
        data = collection.find_one(kwargs)
        return self._object_id_convertor(**data)


class BaseModel(models.Model):

    @classmethod
    def _get_collection(cls):
        """ Name of the instance collection """
        print("__" + cls.__name__.lower())
        return MONGO_DB["__" + cls.__name__.lower()]

    @property
    def objects(self):
        return Manger(self._get_collection())

    def save(self, **kwargs):
        print(self._meta._non_pk_concrete_field_names)

    class Meta:
        abstract = True