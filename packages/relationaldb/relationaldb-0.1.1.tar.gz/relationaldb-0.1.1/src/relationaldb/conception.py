import re
from pathlib import Path
from typing import Dict, List, Union

import attr
from koalak.decorators import optionalargs

from .bases import Attribute, Entity


def camel_to_snake(name):
    # TODO: understand this code!
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


ATTR_METADATA_KEY = "relationaldb"


def attr_metadata(
    in_filter_query: bool = None,
    ref=None,
    description: str = None,
    examples: Union[str, List[str]] = None,
    index: bool = None,
    unique: bool = None,
):
    if examples is None:
        examples = []
    elif isinstance(examples, str):
        examples = [examples]

    if index is None:
        index = False
    if unique is None:
        unique = False
    return {
        ATTR_METADATA_KEY: {
            "in_filter_query": in_filter_query,
            "ref": ref,
            "description": description,
            "examples": examples,
            "unique": unique,
            "index": index,
        }
    }


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
    in_filter_query: bool = None,
    ref=None,
    description: str = None,
    examples: Union[str, List[str]] = None,
    index: bool = None,
    unique: bool = None,
):
    relationaldb_metadata = attr_metadata(
        in_filter_query=in_filter_query,
        unique=unique,
        ref=ref,
        examples=examples,
        index=index,
        description=description,
    )
    if not metadata:
        metadata = {}
    metadata.update(relationaldb_metadata)
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
    return attrib


field = attribute


class Conceptor:
    """Base class to design the database. Responsible to register the entities"""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.collections = self.entities
        self.builder = None
        self._built = False
        self._initialized = False
        self._built_cls = None
        self._cg = None
        self._map_clsname_to_entity = {}

    def __len__(self):
        return self.entities.__len__()

    def __getitem__(self, item):
        return self.entities.__getitem__(item)

    attr_metadata = staticmethod(attr_metadata)
    attribute = staticmethod(attribute)
    field = attribute

    @optionalargs(firstarg=str)
    def entity(self, cls, entity_name: str = None, *, description: str = None):
        """Register new entity"""
        # FIXME: if entity name match keyword! keep keyword and entity will be accesible trhoug [] syntax
        # FIXME: study the case if the entity is already built

        if self._initialized:
            raise ValueError(f"Can not add new entities to already initialize class")

        # ======================================= #
        # decorate cls with attr (if not already) #
        # ======================================= #
        if entity_name is None:
            entity_name = cls.__name__
        if not hasattr(cls, "__attrs_attrs__"):
            cls = attr.s(cls)

            current_entity = Entity(
                name=entity_name,
                cls=cls,
                cls_name=cls.__name__,
                attribute_name=camel_to_snake(cls.__name__),
                description=description,
            )
            self.entities[entity_name] = current_entity

            # add attributes
            current_attributes = current_entity.attributes
            for attr_attribute in cls.__attrs_attrs__:
                # Add annotation for autocomplete
                attr_attribute: attr.Attribute

                required = attr_attribute.default is attr.NOTHING
                relationaldb_attr_metadata = attr_attribute.metadata.get(
                    ATTR_METADATA_KEY, {}
                )

                current_attributes[attr_attribute.name] = Attribute(
                    attr_attribute.name,
                    annotation=attr_attribute.type,
                    kw_only=attr_attribute.kw_only,
                    required=required,
                    default=attr_attribute.default,
                    **relationaldb_attr_metadata,
                )

        else:
            raise ValueError(
                f"Class {cls.__name__} must not be decorated with attrs.define use db.define instead!"
            )

        return cls

    define = entity

    def init(self):
        if self._initialized:
            raise ValueError(f"Already initialized")
        self._initialized = True

        # Add cls mapping
        for entity in self.entities.values():
            self._map_clsname_to_entity[entity.cls_name] = entity

        classes = [e.cls for e in self.entities.values()]
        for entity in self.entities.values():
            for attribute in entity.attributes.values():
                if attribute.annotation in classes:
                    """print(
                        "IN cls",
                        entity.name,
                        attribute.annotation,
                        attribute.name,
                        attribute.ref,
                    )"""
                    if (
                        not attribute.ref
                    ):  # since type is an annotation make attribute true
                        cls_name = attribute.annotation.__name__
                        attribute.ref = self._map_clsname_to_entity[cls_name]

                    if isinstance(attribute.ref, str):
                        pass
                        # ref_entity = self._map_clsname_to_entity[attribute.annotation.__name__]
                        # ref_entity.attributes[attribute.ref] = Attribute(attribute.ref, many=True,
                        # ref=attribute.name, annotation=ref_entity.cls)
                        # FIXME: if we add an attribute, it will be added, so we must have 2 attribues
                        #  attributes that will be built, and references attributes?

    def build(self, name="BaseDatabase"):
        self.init()

        from .mongodb_builder import MongodbBuilder

        mongodb_builder = MongodbBuilder(self, name)
        self._code = mongodb_builder.generate_code()
        self._stubcode = mongodb_builder.generate_stub_code()

        self._built = True
        self._built_cls = mongodb_builder.build()
        return self._built_cls

    def mongodb(
        self,
        dbname: str,
        host: str = "127.0.0.1",
        port: int = 27017,
        timeout: int = 3000,
        username: str = None,
        password: str = None,
    ):
        # TODO: refactor and add None to every thing
        if not self._built:
            self.build()

        return self._built_cls(
            dbname=dbname,
            host=host,
            port=port,
            timeout=timeout,
            username=username,
            password=password,
        )

    def create_stubfile(self, *, __file__: str):
        path = Path(__file__)
        if not path.exists():
            raise FileNotFoundError(
                f"File {__file__} not found to create it's stub file"
            )

        if not __file__.endswith(".py"):
            raise ValueError(f".py file must be provided")

        pyi_file = __file__.replace(".py", ".pyi")

        pyi_code = self._stubcode
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
        pyi_code = self._code
        if not Path(pyi_file).exists() or open(pyi_file).read() != pyi_code:
            print("Adding code file")
            with open(pyi_file, "w") as f:
                f.write(pyi_code)
