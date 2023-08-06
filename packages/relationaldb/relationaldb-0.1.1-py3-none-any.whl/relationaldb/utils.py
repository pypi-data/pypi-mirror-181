import re

import attrs


# TODO optimize re compile
def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _attr_nothing_factory():
    """Since attr already use attr.NOTHING for no default args,
    we use the hack as factory so that we can use nothing as default"""
    return attrs.NOTHING
