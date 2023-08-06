from typing import Dict, List

import attrs

from .utils import _attr_nothing_factory, camel_to_snake


@attrs.define
class Attribute:
    name: str = attrs.field()
    annotation = attrs.field(default=None)
    kw_only: bool = attrs.field(default=False)
    default = attrs.field(factory=_attr_nothing_factory, kw_only=True)
    required: bool = attrs.field(default=None, kw_only=True)
    in_filter_query: bool = attrs.field(default=False, kw_only=True)
    ref: bool = attrs.field(default=False)
    many: bool = attrs.field(default=False)
    description: str = attrs.field(default=False)
    examples: List[str] = attrs.field(factory=list)
    choices: List[str] = attrs.field(factory=list)
    index: bool = attrs.field(default=False)
    unique: bool = attrs.field(default=False)


@attrs.define
class Entity:
    cls_name: str = attrs.field(kw_only=True)
    name: str = attrs.field(default=None, kw_only=True)
    cls = attrs.field(kw_only=True, default=None)
    attributes: Dict[str, Attribute] = attrs.field(factory=dict, init=False)
    attribute_name = attrs.field(default=None)
    description = attrs.field(default=None)

    def get_kw_only_attributes(self):
        return [e for e in self.attributes.values() if e.kw_only]

    def get_not_kw_only_attributes(self):
        return [e for e in self.attributes.values() if not e.kw_only]

    def get_in_filter_query_attributes(self):
        return [e for e in self.attributes.values() if e.in_filter_query]

    def get_not_in_filter_query_attributes(self):
        return [e for e in self.attributes.values() if not e.in_filter_query]

    @property
    def snakecase_name(self):
        return camel_to_snake(self.cls_name)

    @property
    def camlecase_name(self):
        return self.cls_name

    @property
    def container_name(self):
        return f"{self.cls_name}Container"

    @property
    def normalize_func_name(self):
        return f"_normalize_{self.snakecase_name}"

    @property
    def fromdict_name(self):
        return f"fromdict_{self.snakecase_name}"
