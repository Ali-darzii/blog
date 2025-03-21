from typing import List

import pymongo

from Blog.settings import MONGO_DB
import json
from bson import ObjectId


class BaseModel:
    id = None
    _id = None

    @classmethod
    def _get_collection(cls):
        """ Name of the instance collection """
        return MONGO_DB["__" + cls.__name__.lower()]

    def to_dict(self):
        """ Return dict representation of instance except _id"""
        return {key: value for key, value in self.__dict__.items() if key != "_id"}

    def insert_one(self):
        """
        Insert instance into collection
        When id remain None it means somthing went wrong!
        """
        collection = self._get_collection()
        self._id = collection.insert_one(self.to_dict()).inserted_id
        self.id = str(self._id)

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
    def get_all(cls, sort:List[str]):
        """
        Return all documents in collection
        sort like ["username"] or for DESCENDING ["-username"]
        """
        collection = cls._get_collection()
        documents = collection.find()
        for item in sort:
            if item[0] == "-":
                item.replace("-","")
                documents.sort(item, pymongo.ASCENDING)
            else:
                documents.sort(item, pymongo.DESCENDING)

        return [cls._object_id_convertor(**document) for document in documents]

    @classmethod
    def find_one(cls, **kwargs):
        """ Return one filtered document """
        kwargs = cls._object_id_convertor(**kwargs)
        collection = cls._get_collection()
        data = collection.find_one(kwargs)
        return cls._object_id_convertor(**data)


    @classmethod
    def get_all_collections(cls):
        """ Return all collections in collection """
        return MONGO_DB.list_collection_names()

