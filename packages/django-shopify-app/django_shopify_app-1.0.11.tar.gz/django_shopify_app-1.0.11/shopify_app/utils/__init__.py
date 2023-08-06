import importlib
from django.apps import apps
from django.conf import settings


def get_shop_model():
    Model = apps.get_model(settings.SHOPIFY_SHOP_MODEL)
    return Model


def get_function_from_string(string):
    func_name = string.rsplit('.')[-1]
    location = string.replace(f'.{func_name}', "")
    module = importlib.import_module(location)
    if not hasattr(module, func_name):
        raise AttributeError(
            f"Module {module} does not have function {func_name}"
        )
    func = getattr(module, func_name)
    return func
