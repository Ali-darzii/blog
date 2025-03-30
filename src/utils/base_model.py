from typing import List
import pymongo
from Blog.settings import MONGO_DB
from bson import ObjectId
from django.db import models


class Manager:

    def __init__(self):
        self._model_instance = None
        self._model_class = None
        self._meta = None


    def __get__(self, instance, owner):
        new_manager = self.__class__()
        new_manager._model_instance = instance  # None for class access
        new_manager._model_class = owner
        new_manager._meta = owner._meta
        return new_manager

    def _get_collection(self):
        """ Name of the instance collection """
        return MONGO_DB["__" + self._model_class.__name__.lower()]

    @classmethod
    def _get_all_collections(cls):
        """ Return all collections in collection """
        return MONGO_DB.list_collection_names()

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

    def create(self, **kwargs):
        """
        Insert instance into collection
        it's just model_obj.save() with field validation
        """

        obj = self._model_class(**kwargs)
        obj.full_clean()
        obj.save()
        return obj

    def all(self, sort: List[str]):
        """
        Return all documents in collection
        sort like ["username"] or for DESCENDING ["-username"]
        """
        collection = self._get_collection()
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
        collection = self._get_collection()
        data = collection.find_one(kwargs)
        return self._object_id_convertor(**data)


class BaseModel(models.Model):
    object_id = None
    id = None

    mongo_object = Manager()

    @classmethod
    def _get_collection(cls):
        """ Name of the instance collection """
        return MONGO_DB["__" + cls.__name__.lower()]

    def to_dict(self):
        """ Return dict representation of instance except id"""

        return {
            f.name: getattr(self, f.attname, None)
            for f in self._meta.fields
        }

    def save(self, **kwargs):
        collection = self._get_collection()
        attr = self.to_dict()
        attr.pop("id")
        self.object_id = collection.insert_one(attr).inserted_id
        self.id = str(self.object_id)
        return self




    class Meta:
        abstract = True