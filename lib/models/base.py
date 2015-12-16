from datetime import datetime
import pymongo

from lib.mongo import get_mongodb


class Model(object):

    def __init__(self):
        self.id = None
        self.created = None
        self.modified = None

    def __unicode__(self):
        return '%s[%s]' % (self.__class__.__name__, self.id)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __repr__(self):
        return self.__str__()

    def _add_timestamps(self, obj):
        self.created = obj['created']
        self.modified = obj['modified']

    def refetch(self):
        return self.find_one({'_id': self.id})

    def insert(self):
        doc = self.to_dict()
        doc['modified'] = datetime.now()
        doc['created'] = doc.get('created', datetime.now())
        self._get_collection().insert(doc)

    def save(self):
        doc = self.to_dict()
        doc['modified'] = datetime.now()
        doc['created'] = self.created
        self._get_collection().update({'_id': self.id}, doc, True)

    def to_dict(self):
        raise NotImplementedError

    @classmethod
    def _get_collection(cls):
        return get_mongodb()[cls.__name__.lower()]

    @classmethod
    def find(cls, *args, **kwargs):
        results = cls._get_collection().find(
            *args,
            sort=[('created', pymongo.DESCENDING)],
            **kwargs)

        objects = []

        for result in results:
            obj = cls.from_dict(result)
            objects.append(obj)

        return objects

    @classmethod
    def find_one(cls, *args, **kwargs):
        doc = cls._get_collection().find_one(*args, **kwargs)
        if doc:
            return cls.from_dict(doc)
        return None

    @classmethod
    def from_dict(cls, result):
        raise NotImplementedError
