import abc
import os

import codeg
import jinja2
from bson.objectid import ObjectId
from pymongo import MongoClient

# The template used to generate code dynamically

HERE = os.path.dirname(__file__)

TEMPLATE_PATH = os.path.join(HERE, "data", "mongodb_template.jinja2")
TEMPLATE = open(TEMPLATE_PATH).read()

TEMPLATE_STUBFILE = """
from relationaldb import BaseMongodbDatabase, BaseObjects


class {{db_cls_name}}(BaseMongodbDatabase):

    {% for entity in entities %}
    {{entity.cls_name}}: {{entity.cls_name}}Objects{% endfor %}

    def __init__(
        self,
        dbname: str,
        host: str = "127.0.0.1",
        port: int = 27017,
        timeout: int = 300,
        username: str = None,
        password: str = None,
    ):  ...



{% for entity in entities %}
class {{entity.cls_name}}Objects(BaseObjects):
    collection_name: str

    def find_asdict({{entity.method_signature_as_none}}):
        ...


    def first_asdict({{entity.method_signature_as_none}}):
        ...

    def first({{entity.method_signature_as_none}}):
        ...

    def insert_one({{entity.method_signature}}):
        ...

    def feed({{entity.method_signature}}, _retid: bool = False):
        ...

    # ====== #
    # DELETE #
    # ====== #
    def delete_first({{entity.method_signature_as_none}}):
       ...

    def delete_many({{entity.method_signature_as_none}}):
        ...


{% endfor %}
"""


class Database:
    pass


class BaseObjects(abc.ABC):
    collection_name: str = None

    def __init__(self, db):
        mongodb = db.mongodb

        self.db = db
        self.mongodb = mongodb
        self.collection = mongodb[self.collection_name]
        self.cls = self.db.entities[
            self.collection_name
        ].cls  # FIXME: probably bug here
        self.filters = {}

        # aliases
        self.new = self.insert_one
        self.filter_asdict = self.find_asdict
        self.delete_first = self.delete_one
        self.find_one_asdict = self.first_asdict
        self.delete_one = self.delete_first

    def from_dict(self, document: dict):
        _id = document.pop("_id")
        instance = self.cls(**document)
        instance.id = _id
        return instance

    # Insert
    @abc.abstractmethod
    def insert_one(self, *args, **kwargs):
        pass

    def insert_many(self, iterable):
        pass

    # Read
    def __iter__(self):
        return self.find()

    @abc.abstractmethod
    def find_asdict(self):
        yield from self.collection.find()

    def get(self, id):
        return self.from_dict(self.get_asdict(id))

    def get_asdict(self, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection.find_one({"_id": id})

    def first(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def first_asdict(self, *args, **kwargs):
        pass

    def __len__(self):
        return self.collection.count_documents(self.filters)

    def __getitem__(self, item):
        return self.from_dict(self.index_asdict(item))

    def index_asdict(self, item):
        # FIXME: realy slow to do skip and limit
        #  add index or remove the ability to get the n-th element
        return self.collection.find(self.filters).skip(item).limit(1)[0]

    # Update
    def update_many(self, *args, **kwargs):
        pass

    def update_one(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def feed(self, *args, **kwargs):
        pass

    # Delete
    @abc.abstractmethod
    def delete_one(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def delete_many(self, *args, **kwargs):
        pass

    def list(self) -> list:
        return list(self)

    aslist = list

    def print(self):
        for e in self:
            print(e)


class BaseMongodbDatabase:
    def __init__(
        self,
        dbname: str,
        host: str = "127.0.0.1",
        port: int = 27017,
        timeout: int = 3000,
        username: str = None,
        password: str = None,
    ):
        super().__init__()
        self.mango_client = MongoClient(
            host=host, port=port, serverSelectionTimeoutMS=timeout
        )
        self.mongodb = self.mango_client[dbname]

    def resetdb(self):
        for collection_name in self.mongodb.list_collection_names():
            self.mongodb.drop_collection(collection_name)


class MongodbBuilder:
    def __init__(self, conception, name):
        self.conception = conception

        self.name = name

        entities = []
        for entity in self.conception.entities.values():
            attributes = entity.attributes.values()
            in_filter_query_attributes = [e for e in attributes if e.in_filter_query]
            ref_attributes = [e for e in attributes if e.ref]
            not_in_filter_query_attributes = [
                e for e in attributes if not e.in_filter_query
            ]

            # Case 2 - entity have only one attribute with unambigious and primitif type
            # If attribute is only one type we can add this specific type
            # TODO: add datetime in primitive type?!
            if len(in_filter_query_attributes) == 1 and in_filter_query_attributes[
                0
            ].annotation in [str, int, bool, float]:
                one_argument_normalization = in_filter_query_attributes[
                    0
                ].annotation.__name__
            else:
                one_argument_normalization = False

            entities.append(
                {
                    "cls_name": entity.cls_name,
                    "name": entity.name,
                    "method_signature": codeg.generate_function_signature(
                        attributes, add_self=True
                    ),
                    "method_signature_as_none": codeg.generate_function_signature(
                        attributes, add_self=True, replace_defaults_with_none=True
                    ),
                    "attributes": attributes,
                    "in_filter_query_attributes": in_filter_query_attributes,
                    "not_in_filter_query_attributes": not_in_filter_query_attributes,
                    "one_argument_normalization": one_argument_normalization,
                    "ref_attributes": ref_attributes,
                }
            )

        self.context = {"entities": entities, "db_cls_name": name}

    def _render(self, string, context):
        jinja_environment = jinja2.Environment(undefined=jinja2.StrictUndefined)
        return jinja_environment.from_string(string).render(context)

    def generate_code(self):
        code = self._render(TEMPLATE, self.context)
        return codeg.format_string_with_black(code)

    def generate_stub_code(self):
        code = self._render(TEMPLATE_STUBFILE, self.context)
        return codeg.format_string_with_black(code)

    def build(self):
        code = self.generate_code()
        _globals = {}
        for e in self.conception.entities.values():
            _globals[e.cls_name] = e.cls
        cls_db = codeg.build(code, globals=_globals, locals=_globals)[self.name]
        cls_db.entities = self.conception.entities
        return cls_db
