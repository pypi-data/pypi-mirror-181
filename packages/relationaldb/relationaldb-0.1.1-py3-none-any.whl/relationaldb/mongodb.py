import copy
from typing import List

import codeg
from codeg import ClassBlock
from pymongo import MongoClient

from .bases import Attribute, Entity
from .entities import BaseBuilder, BaseContainer, BaseDatabase
from .utils import camel_to_snake


class BaseMongodbContainer(BaseContainer):
    def _add_filter(self, filter_type, **kwargs):
        filters = copy.deepcopy(self.filters)
        for key, value in kwargs.items():
            if value is None:
                continue
            if key not in self.filters:
                filters[key] = {}

            filters[key][filter_type] = value
        return self.__class__(self.entities_manager, filters)

    def __init__(self, entities_manager, filters=None):
        super().__init__(entities_manager, filters)
        self.db = entities_manager.db
        self.entity: Entity = self.entities_manager.entities[self.name]
        self.collection = self.db[self.name]

        fromdict_methode_name = self.entity.fromdict_name
        self.fromdict = getattr(self.entities_manager, fromdict_methode_name)

    def __len__(self):
        return self.collection.count_documents(self.filters)

    def __document_to_instance(self, document):
        document.pop("_id")
        return self.entity.cls(**document)

    def __iter__(self):

        for e in self.collection.find(self.filters):
            yield self.fromdict(e)

    def __getitem__(self, item):
        # FIXME: realy slow to do skip and limit
        #  add index or remove the ability to get the n-th element
        document = self.collection.find(self.filters).skip(item).limit(1)[0]
        return self.fromdict(document)


class BaseMongodbDatabase(BaseDatabase):
    def __init__(
        self,
        dbname,
        host="127.0.0.1",
        port=27017,
        timeout=3000,
        username=None,
        password=None,
    ):
        super().__init__()
        self.mango_client = MongoClient(
            host=host, port=port, serverSelectionTimeoutMS=timeout
        )
        self.db = self.mango_client[dbname]
        self._source_codes = []

    @classmethod
    def __document_to_instance(self, entity, document):
        document.pop("_id")
        return entity.cls(**document)

    @staticmethod
    def _map_args_kwargs_with_attributes(args, kwargs, attributes: List[Attribute]):
        attributes = list(attributes)
        ret = []
        for i, arg in enumerate(args):
            ret.append((attributes[i], arg))

        for k, v in kwargs.items():
            for attr in attributes:
                if attr.name == k:
                    ret.append((attr, v))
        return ret

    def resetdb(self):
        for collection_name in self.db.list_collection_names():
            self.db.drop_collection(collection_name)


class MongodbBuilder(BaseBuilder):
    def __init__(self, conceptor, clsname: str):
        super().__init__(conceptor, clsname)

    def generatecode_imports(self):
        self.cg_script.import_(
            BaseMongodbDatabase, BaseMongodbContainer, frm="relationaldb"
        )

    def generatecode_create_db_cls(self):
        self.cg_db = self.cg_script.cls(self.dbcls_name, BaseMongodbDatabase.__name__)

    def generatecode_db__init__(self):
        attributes_init = [
            Attribute("dbname", annotation=str),
            Attribute("host", annotation=str, default="127.0.0.1"),
            Attribute("port", annotation=int, default=27017),
            Attribute("timeout", annotation=int, default=300),
            Attribute("username", annotation=str, default=None),
            Attribute("password", annotation=str, default=None),
        ]
        self.sb_init = self.cg_db.method("__init__", attributes=attributes_init)
        init_call = codeg.generate_function_call(attributes=attributes_init)
        self.sb_init.line(f"{BaseMongodbDatabase.__name__}.__init__(self, {init_call})")

        # Init containers
        for entity in self.entities.values():
            self.sb_init.line(f"self.{entity.name} = {entity.container_name}(self)")

    def generatecode_db__iter__(self):
        pass

    # ================== #
    # DB Code generation #
    # ================== #
    # Utils functions
    def generatecode_db_normalize_args_entity(self, entity: Entity):
        # Preaparing used variables
        cg = self.cg_db
        var_name = entity.snakecase_name
        in_filter_attributes = entity.get_in_filter_query_attributes()

        # Creating the method
        cg_method = cg.method(
            entity.normalize_func_name, attributes=[Attribute(var_name)]
        )

        # Case X - object is instance of the dataclass -> Error? because we have to return ID not args/kwargs
        # args = "[" + ", ".join([f'{var_name}.{e.name}' for e in not_kw_only_attributes]) + "]"
        # kwargs = "{" + ", ".join([f"'{e.name}':{e.name}" for e in kw_only_attributes]) + "}"
        # cg_method.condition(f"isinstance({var_name}, {entity.cls_name})").ret(f"{args}, {kwargs}")

        # Case 1 - tuple
        cg_method.condition(f"isinstance({var_name}, tuple)").ret(f"{var_name}, {{}}")

        # Case 2 - entity have only one attribute with unambigious and primitif type
        # If attribute is only one type we can add this specific type
        # TODO: add datetime in primitive type?!
        if len(in_filter_attributes) == 1 and in_filter_attributes[0].annotation in [
            str,
            int,
            bool,
            float,
        ]:
            attribute = in_filter_attributes[0]
            cg_method.block(
                f"elif isinstance({var_name}, {attribute.annotation.__name__})"
            ).ret(f"({var_name},), {{}}")

        # Else error!
        cg_method.block("else").line(
            f"raise ValueError('can not normalize {var_name}')"
        )

    def generatecode_db_fromdict_entity(self, entity: Entity):
        # Preaparing used variables
        cg = self.cg_db
        cg_method = cg.method(
            f"fromdict_{entity.snakecase_name}", attributes=[Attribute("document")]
        )
        cg_method.line(f"_id = document.pop('_id')")
        cg_method.line(f"entity = self.entities['{entity.name}']")
        cg_method.line(f"instance = entity.cls(**document)")
        cg_method.line(f"instance.id = _id")
        cg_method.line(
            f"top_self = self"
        )  # top_self reference entities_manager instance
        ref_attributes = [e for e in entity.attributes.values() if e.ref]
        for attribute in ref_attributes:
            ref_entity = self.conceptor._map_clsname_to_entity[
                attribute.annotation.__name__
            ]
            if not attribute.many:
                cg_method.line(
                    f"instance._id_{attribute.name} = instance.{attribute.name}"
                )
                propert_method = cg_method.method(attribute.name)
                propert_method.decorator("property")

                propert_method.condition(
                    f"self._id_{ref_entity.snakecase_name} is None"
                ).ret("None")
                propert_method.line(
                    f"doc = top_self.db['{ref_entity.name}'].find_one({{'_id': self._id_{attribute.name}}})"
                )
                propert_method.ret(
                    f"top_self.fromdict_{ref_entity.snakecase_name}(doc)"
                )
                cg_method.line(
                    f"instance.{attribute.name} = {attribute.name}.__get__(instance)"
                )
            else:
                propert_method = cg_method.method(attribute.name)
                propert_method.decorator("property")
                propert_method.ret(
                    f"{ref_entity.cls_name}Container(top_self).eq({attribute.ref}=self.id)"
                )

            cg_method.line("")

        cg_method.ret("instance")

    def generatecode_db_utils_methods_entity(self, entity: Entity):
        varname = entity.snakecase_name

        cg_method = self.cg_db.method(
            f"_upsert_and_get_id_{varname}", attributes=[Attribute(varname)]
        )
        cg_method.condition(f"isinstance({varname}, {entity.cls_name})").ret(
            f"{varname}.id"
        )

        cg_method.line(f"args, kwargs = self._normalize_{varname}({varname})")
        cg_method.ret(f"self.upsert_{varname}(*args, **kwargs, _retid=True)")

    # Create
    def generatecode_db_new_entity(self, entity: Entity):
        entity_single_name = camel_to_snake(entity.cls_name)
        entity_name = entity.name
        method_name = f"new_{entity_single_name}"
        attributes = entity.attributes.values()

        # Sta building
        sb = self.cg_db
        sb_method_new_entity = sb.method(method_name, attributes=attributes)
        dict_string = (
            "{" + ", ".join([f"'{e.name}': {e.name}" for e in attributes]) + "}"
        )
        sb_method_new_entity.line(f"query = {dict_string}")
        sb_method_new_entity.line(f"collection = self.db['{entity_name}']")
        sb_method_new_entity.line(f"collection.insert_one(query)")
        return sb_method_new_entity

    # Read
    def generatecode_db_firstasdict_entity(self, entity: Entity):
        entity_single_name = camel_to_snake(entity.cls_name)
        entity_name = entity.name
        method_name = f"firstasdict_{entity_single_name}"

        sb = self.cg_db
        sb_method__call__ = sb.method(
            method_name,
            attributes=entity.attributes.values(),
            replace_defaults_with_none=True,
        )  # TODO: add generate stubfile to a method

        # add empty query
        sb_method__call__.line("query = {}")
        sb_method__call__.line("")

        # add parameters to query if not none
        for attr_name, attr in entity.attributes.items():
            sb_method__call__.condition(f"{attr_name} is not None").line(
                f"query['{attr_name}'] = {attr_name}"
            )

        # yield element and convert them to object
        sb_method__call__.line("")
        sb_method__call__.line(f'entity = self.entities["{entity_name}"]')
        sb_method__call__.line(f'return self.db["{entity_name}"].find_one(query)')

        return sb_method__call__

    def generatecode_db_first_entity(self, entity: Entity):
        # FIXME: use firstasdict instead of replaying the code?
        # TODO: add error when first not found and not returning none! (firstasdict also)²
        entity_single_name = camel_to_snake(entity.cls_name)
        entity_name = entity.name
        method_name = f"first_{entity_single_name}"

        sb = self.cg_db
        sb_method__call__ = sb.method(
            method_name,
            attributes=entity.attributes.values(),
            replace_defaults_with_none=True,
        )

        # add empty query
        sb_method__call__.line("query = {}")
        sb_method__call__.line("")

        # add parameters to query if not none
        for attr_name, attr in entity.attributes.items():
            sb_method__call__.condition(f"{attr_name} is not None").line(
                f"query['{attr_name}'] = {attr_name}"
            )

        # yield element and convert them to object
        sb_method__call__.line("")
        sb_method__call__.line(f'entity = self.entities["{entity_name}"]')
        sb_method__call__.line(
            f'entity_as_dict = self.db["{entity_name}"].find_one(query)'
        )
        sb_method__call__.line(f"return self.{entity.fromdict_name}(entity_as_dict)")

        return sb_method__call__

    # Update
    def generatecode_db_upsert_entity(self, entity: Entity):
        # Prepare used variables
        entity_name = entity.name
        method_name = f"upsert_{entity.snakecase_name}"
        attributes = list(entity.attributes.values())
        attributes_in_filter_query = [e for e in attributes if e.in_filter_query]
        attribute_not_in_filter_query = [e for e in attributes if not e.in_filter_query]

        ref_attributes_in_filter_query = [e for e in attributes if e.ref]

        # Building the method
        # Add _retid parameter, to return ID if true
        cg_method = self.cg_db.method(
            method_name,
            attributes=attributes
            + [Attribute("_retid", default=False, annotation=bool)],
        )

        # Normalize all referenced attributes (and create them if they don't exists)
        #  Ex: upsert_animal(owner='john') will call upsert_person('john')
        #  After normalization, the referenced attribute will be the foreing ID to insert
        if ref_attributes_in_filter_query:
            cg_method.comment("Normalize referenced parameters")

        for attribute in ref_attributes_in_filter_query:
            # Get the referenced entity
            ref_entity = self.conceptor._map_clsname_to_entity[
                attribute.annotation.__name__
            ]
            ref_varname = ref_entity.snakecase_name
            # Check if attribute is required or not
            if attribute.required:
                # if required we don't check if none
                cg_method.line(
                    f"{ref_varname} = self._upsert_and_get_id_{ref_varname}({ref_varname})"
                )
            else:
                cg_method.condition(f"{ref_varname} is not None").line(
                    f"{ref_varname} = self._upsert_and_get_id_{ref_varname}({ref_varname})"
                )
            cg_method.line("")

        # Building filter query
        dict_string = (
            "{"
            + ", ".join([f"'{e.name}': {e.name}" for e in attributes_in_filter_query])
            + "}"
        )
        cg_method.line(f"filter_query = {dict_string}")
        cg_method.line(f"set_query = dict(filter_query)")
        cg_method.line("update_query = {'$set': set_query}")
        cg_method.line("")

        # FIXME: don't check not in filter query but required or not?
        for a in attribute_not_in_filter_query:
            cg_method.condition(f"{a.name} is not None").line(
                f"set_query['{a.name}'] = {a.name}"
            )
        cg_method.line("")

        cg_method.line(f"collection = self.db['{entity_name}']")
        cg_method.line(
            f"ret = collection.update_one(filter_query, update_query, upsert=True)"
        )
        cg_method.line("")

        # Get return ID if param _retid is True
        cg_method.comment(f"Get upserted ID if _retid is True")
        ret_condition = cg_method.condition("_retid")
        x = ret_condition.condition("ret.upserted_id")
        x.ret("ret.upserted_id")
        ret_condition.ret(f"self.db['{entity.name}'].find_one(filter_query)['_id']")
        return cg_method

    # delete
    def generatecode_db_deletefirst_entity(self, entity: Entity):
        entity_single_name = camel_to_snake(entity.cls_name)
        entity_name = entity.name
        method_name = f"deletefirst_{entity_single_name}"

        sb = self.cg_db
        sb_method__call__ = sb.method(
            method_name,
            attributes=entity.attributes.values(),
            replace_defaults_with_none=True,
        )

        # add empty query
        sb_method__call__.line("query = {}")
        sb_method__call__.line("")

        # add parameters to query if not none
        for attr_name, attr in entity.attributes.items():
            sb_method__call__.condition(f"{attr_name} is not None").line(
                f"query['{attr_name}'] = {attr_name}"
            )

        # yield element and convert them to object
        sb_method__call__.line("")
        sb_method__call__.line(f'self.db["{entity_name}"].delete_one(query)')

        return sb_method__call__

    def generatecode_db_delete_entities(self, entity: Entity):
        method_name = f"delete_{entity.name}"

        sb = self.cg_db
        sb_method__call__ = sb.method(
            method_name,
            attributes=entity.attributes.values(),
            replace_defaults_with_none=True,
        )

        # add empty query
        sb_method__call__.line("query = {}")
        sb_method__call__.line("")

        # add parameters to query if not none
        for attr_name, attr in entity.attributes.items():
            sb_method__call__.condition(f"{attr_name} is not None").line(
                f"query['{attr_name}'] = {attr_name}"
            )

        # yield element and convert them to object
        sb_method__call__.line("")
        sb_method__call__.line(f'd = self.db["{entity.name}"].delete_many(query)')

        return sb_method__call__

    # ========================= #
    # Container Code generation #
    # ========================= #
    def generatecode_create_container_cls(self, entity: Entity):
        cg_cls = self.cg_script.cls(
            entity.container_name, BaseMongodbContainer.__name__
        )
        cg_cls.line(f"name: str = '{entity.name}'")
        return cg_cls

    def generatecode_container__iter__(self, entity: Entity, cg: ClassBlock):
        """Method is already present in base container"""
        pass

    def generatecode_container__len__(self, entity: Entity, cg: ClassBlock):
        """Method is already present in base container"""
        pass

    def generatecode_container__call__(self, entity: Entity, sb: ClassBlock):
        sb.line("__call__ = eq")

    def generatecode_container__getitem__(self, entity: Entity, cg: ClassBlock):
        pass

    def _generatecode_container_filters(
        self, entity: Entity, cg: ClassBlock, operator, method_name=None
    ):
        cg_method = cg.method(
            operator,
            attributes=entity.attributes.values(),
            replace_defaults_with_none=True,
        )
        funcall = codeg.generate_function_call(
            attributes=entity.attributes.values(), kw_only=True
        )
        cg_method.ret(f"self._add_filter('${operator}', {funcall})")

    def generatecode_container__lt__(self, entity: Entity, cg: ClassBlock):
        self._generatecode_container_filters(entity, cg, "lt")

    def generatecode_container__gt__(self, entity: Entity, cg: ClassBlock):
        self._generatecode_container_filters(entity, cg, "gt")

    def generatecode_container__eq__(self, entity: Entity, cg: ClassBlock):
        self._generatecode_container_filters(entity, cg, "eq")

    def generatecode_container__ne__(self, entity: Entity, cg: ClassBlock):
        self._generatecode_container_filters(entity, cg, "ne")
