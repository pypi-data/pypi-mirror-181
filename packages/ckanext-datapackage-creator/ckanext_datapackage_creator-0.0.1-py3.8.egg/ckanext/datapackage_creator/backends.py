import pydoc
import frictionless

from ckanext.datapackage_creator.settings import settings


class BaseBackend(object):

    def describe(self, resource, *args, **kwargs):
        raise NotImplementedError()

    def validate(self, resource, *args, **kwargs):
        raise NotImplementedError()


class FritionlesseBackend(BaseBackend):

    def describe(self, resource, *args, **kwargs):
        return frictionless.describe(resource, *args, **kwargs)

    def validate(self, resource, *args, **kwargs):
        raise NotImplementedError()


BackendClass = pydoc.locate(settings.get('backend', 'ckanext.datapackage_creator.backends.FritionlesseBackend'))
default = BackendClass()
