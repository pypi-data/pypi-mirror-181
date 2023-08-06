import abc
import re
from pathlib import Path
from typing import Dict, List, Type  # noqa: TYP001

import attr
import codeg
import coloring
from codeg import ClassBlock

from .bases import Attribute, Entity
from .exceptions import ObjectNotFound


def camel_to_snake(name):
    # TODO: understand this code!
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


ATTR_METADATA_KEY = "koalak"


def attr_metadata(in_filter_query=None, ref=None):
    return {ATTR_METADATA_KEY: {"in_filter_query": in_filter_query, "ref": ref}}


def attribute(
    # attrs attribute
    *,
    type=None,
    default=attr.NOTHING,
    validator=None,
    repr=True,
    cmp=None,
    hash=None,
    init=True,
    metadata=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    # entities attribute
    unique=None,
    nullable=None,
    target=None,
    ref=None,
    in_filter_query=None,
):
    koalak_metadata = attr_metadata(in_filter_query=in_filter_query, ref=ref)
    if not metadata:
        metadata = {}
    metadata.update(koalak_metadata)
    attrib = attr.ib(  # noqa
        default=default,
        validator=validator,
        repr=repr,
        cmp=cmp,
        hash=hash,
        init=init,
        metadata=metadata,
        type=type,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
    )
    if ref:
        coloring.print_green(attrib)
    return attrib


class BaseBuilder(abc.ABC):
    def __init__(self, conceptor: "Conceptor", dbcls_name: str):
        """BaseBuilder is the cls to subcls for creating new implementations.
        It's role is to build the DatabaseClass and a container for each entity"""
        self.dbcls_name = dbcls_name
        self.conceptor = conceptor
        self.entities = conceptor.entities
        self.cg_script = codeg.script()
        self.cg_db: codeg.ClassBlock

    def build(self, globals=None, locals=None) -> "BaseDatabase":
        """Build the Database"""

        # add imports
        self.generatecode_imports()

        # Create cls in the script
        self.generatecode_create_db_cls()

        # add init in cls
        self.generatecode_db__init__()

        for entity in self.entities.values():
            # Add Database methods for each entity
            self.cg_db.comment(f"{entity.name} related methods", title=True)
            self.generatecode_db_first_entity(entity)
            self.generatecode_db_firstasdict_entity(entity)
            self.generatecode_db_new_entity(entity)
            self.generatecode_db_upsert_entity(entity)
            self.generatecode_db_deletefirst_entity(entity)
            self.generatecode_db_delete_entities(entity)

            # Utils DB function
            self.generatecode_db_normalize_args_entity(entity)
            self.generatecode_db_fromdict_entity(entity)
            self.generatecode_db_utils_methods_entity(entity)

            # Build the container
            cls_container = self.generatecode_create_container_cls(entity)
            self.generatecode_container__iter__(entity, cls_container)

            self.generatecode_container__getitem__(entity, cls_container)
            self.generatecode_container__len__(entity, cls_container)
            self.generatecode_container__lt__(entity, cls_container)
            self.generatecode_container__gt__(entity, cls_container)
            self.generatecode_container__eq__(entity, cls_container)
            self.generatecode_container__ne__(entity, cls_container)
            self.generatecode_container__call__(entity, cls_container)

        # coloring.print_blue(self.cg_script.generate_code(format_with_black=False))
        locals = self.cg_script.build(globals=globals, locals=locals)
        cls = locals[self.dbcls_name]
        setattr(cls, "entities", self.entities)
        for entity in self.entities.values():
            setattr(locals[entity.container_name], "entity", entity)
        return locals[self.dbcls_name]

    @abc.abstractmethod
    def generatecode_imports(self):
        """Imports needed for the code to compile"""
        pass

    @abc.abstractmethod
    def generatecode_create_db_cls(self):
        """Creates the cls and its bases (without any methods)"""
        pass

    @abc.abstractmethod
    def generatecode_db__init__(self):
        pass

    @abc.abstractmethod
    def generatecode_db__iter__(self):
        # TOOD: testme
        pass

    # ================== #
    # DB Code generation #
    # ================== #
    # Utils functions
    @abc.abstractmethod
    def generatecode_db_normalize_args_entity(self, entity: Entity):
        pass

    def generatecode_db_utils_methods_entity(self, entity: Entity):
        """Generate utils methods for an entity, private methods used"""
        pass

    @abc.abstractmethod
    def generatecode_db_fromdict_entity(self, entity: Entity):
        pass

    # Create
    @abc.abstractmethod
    def generatecode_db_new_entity(self, entity: Entity):
        pass

    # Read
    @abc.abstractmethod
    def generatecode_db_firstasdict_entity(self, entity: Entity):
        pass

    @abc.abstractmethod
    def generatecode_db_first_entity(self, entity: Entity):
        pass

    # Update
    @abc.abstractmethod
    def generatecode_db_upsert_entity(self, entity: Entity):
        pass

    # Delete
    @abc.abstractmethod
    def generatecode_db_deletefirst_entity(self, entity: Entity):
        pass

    @abc.abstractmethod
    def generatecode_db_delete_entities(self, entity: Entity):
        pass

    # ========================= #
    # Container Code generation #
    # ========================= #
    @abc.abstractmethod
    def generatecode_create_container_cls(self, entity: Entity):
        pass

    @abc.abstractmethod
    def generatecode_container__iter__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__len__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__call__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__lt__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__gt__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__eq__(self, entity: Entity, cg: ClassBlock):
        pass

    @abc.abstractmethod
    def generatecode_container__ne__(self, entity: Entity, cg: ClassBlock):
        pass


class Conceptor(abc.ABC):
    """Base class to design the database. Responsible to register the entities"""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.builder = None
        self._built = False
        self._cg = None
        self._globals = {}
        self._map_clsname_to_entity = {}

    def __len__(self):
        return self.entities.__len__()

    def __getitem__(self, item):
        return self.entities.__getitem__(item)

    attr_metadata = staticmethod(attr_metadata)
    attribute = staticmethod(attribute)

    def entity(self, entity_name):
        """Register new entity"""
        # FIXME: if entity name match keyword! keep keyword and entity will be accesible trhoug [] syntax
        def decorator(cls):
            # ======================================= #
            # decorate cls with attr (if not already) #
            # ======================================= #
            # add cls to globals
            self._globals[cls.__name__] = cls

            if not hasattr(cls, "__attrs_attrs__"):
                cls = attr.s(cls)
                current_entity = Entity(
                    name=entity_name,
                    cls=cls,
                    cls_name=cls.__name__,
                    attribute_name=camel_to_snake(cls.__name__),
                )
                self.entities[entity_name] = current_entity

                # add attributes
                current_attributes = current_entity.attributes
                for attr_attribute in cls.__attrs_attrs__:
                    # Add annotation to autocomplte
                    attr_attribute: attr.Attribute
                    required = attr_attribute.default is attr.NOTHING
                    in_filter_query = attr_attribute.metadata.get(
                        ATTR_METADATA_KEY, {}
                    ).get("in_filter_query")
                    ref = attr_attribute.metadata.get(ATTR_METADATA_KEY, {}).get("ref")
                    current_attributes[attr_attribute.name] = Attribute(
                        attr_attribute.name,
                        annotation=attr_attribute.type,
                        kw_only=attr_attribute.kw_only,
                        required=required,
                        default=attr_attribute.default,
                        in_filter_query=in_filter_query,
                        ref=ref,
                    )

                # create empty list
                # self._add_entity_methods(current_entity)

            else:
                raise ValueError(
                    f"Class {cls.__name__} must not be decorated with attr.s use db.entities instead!"
                )

            # add new_method
            # self._add_new_method(cls)
            return cls

        return decorator

    def init(self):
        # Add cls mapping
        for entity in self.entities.values():
            self._map_clsname_to_entity[entity.cls_name] = entity

        classes = [e.cls for e in self.entities.values()]
        for entity in self.entities.values():
            for attribute in entity.attributes.values():
                if attribute.annotation in classes:
                    print(
                        "IN cls",
                        entity.name,
                        attribute.annotation,
                        attribute.name,
                        attribute.ref,
                    )
                    if (
                        not attribute.ref
                    ):  # since type is an annotation make attribute true
                        attribute.ref = True

                    if isinstance(attribute.ref, str):
                        print("AAAAAAAAAAAAAAAAAAA")
                        # ref_entity = self._map_clsname_to_entity[attribute.annotation.__name__]
                        # ref_entity.attributes[attribute.ref] = Attribute(attribute.ref, many=True, ref=attribute.name, annotation=ref_entity.cls)
                        # FIXME: if we add an attribute, it will be added, so we must have 2 attribues
                        #  attributes that will be built, and references attributes?
        for entity in self.entities.values():
            print(entity)
            for a in entity.attributes.values():
                print("\t", a)

    def build(self, builder: Type[BaseBuilder], clsdb_name=None):
        self.init()
        if clsdb_name is None:
            clsdb_name = "EntitiesManager"
        builder = builder(self, clsdb_name)
        built = builder.build(globals=self._globals, locals=self._globals)
        self._built = True
        self._cg = builder.cg_script
        built.conceptor = self
        built.builder = builder
        return built

    def mongodb(self, clsname: str = "EntitiesManager"):  # -> Type["MongodbEntities"]:
        from .mongodb import MongodbBuilder

        return self.build(MongodbBuilder)

    def create_stubfile(self, *, __file__: str):
        path = Path(__file__)
        if not path.exists():
            raise FileNotFoundError(
                f"File {__file__} not found to create it's stub file"
            )

        if not __file__.endswith(".py"):
            raise ValueError(f".py file must be provided")

        pyi_file = __file__.replace(".py", ".pyi")
        pyi_code = self._cg.generate_stubcode()
        if not Path(pyi_file).exists() or open(pyi_file).read() != pyi_code:
            print("Adding stub file")
            with open(pyi_file, "w") as f:
                f.write(pyi_code)

    def create_codefile(self, *, __file__: str):
        path = Path(__file__)
        if not path.exists():
            raise FileNotFoundError(
                f"File {__file__} not found to create it's stub file"
            )

        if not __file__.endswith(".py"):
            raise ValueError(f".py file must be provided")

        pyi_file = __file__.replace(".py", "_codegen.py")
        pyi_code = self._cg.generate_code()
        if not Path(pyi_file).exists() or open(pyi_file).read() != pyi_code:
            print("Adding code file")
            with open(pyi_file, "w") as f:
                f.write(pyi_code)


class BaseDatabase(abc.ABC):
    """Base class with CRUD operations on all the entities"""

    pass
    # def __init__(self, entities: Dict[str, Entity]):
    #    self.entities: Dict[str, Entity] = entities


class A:
    def __init__(self):
        self.filters = {}
        """
        container.like(name='lol').gt(age=23).gt(money=1000).like('lol')
        {
        }
        """
        query = {"age": {"$gt": 23}, "money": {"$gt": 500}}
        filters = {"name": {}}

    def gt(self, name=None, age=None, money=None, sexe=None):
        self._add_filter("$gt", name=name, age=age, money=money, sexe=sexe)

        return self

    def lt(self, name=None, age=None, money=None, sexe=None):
        self._add_filter("$lt", name=name, age=age, money=money, sexe=sexe)
        return self


class BaseContainer(abc.ABC):
    """Base class that contains all instances of one entity."""

    name: str

    def __init__(self, entities_manager, filters=None):
        if filters is None:
            filters = {}
        self.entities_manager = entities_manager
        self.filters = filters

    def first(self):
        for e in self:
            return e
        raise ObjectNotFound("Object not found")
        # TODO: raise error

    def __len__(self):
        length = 0
        for _ in self:
            length += 1
        return length

    def __getitem__(self, item):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    # filters
    def like(self):
        pass

    def ilike(self):
        pass

    # Operators
    def gt(self):
        pass

    def lt(self):
        pass

    def eq(self):
        pass

    def ne(self):
        pass

    def ge(self):
        pass

    def le(self):
        pass

    # Converters
    def asdict(self):
        pass

    def aslist(self):
        pass

    # Helper functions to use in debug/interpreter
    def list(self):
        return list(self)

    def print(self):
        for e in self:
            print(e)


@staticmethod
def _map_args_kwargs_with_attributes(args, kwargs, attributes: List[Attribute]):
    attributes = list(attributes)
    ret = []
    for i, arg in enumerate(args):
        ret.append((attributes[i], arg))

    for k, v in kwargs.items():
        for attribute in attributes:
            if attribute.name == k:
                ret.append((attr, v))
    return ret
