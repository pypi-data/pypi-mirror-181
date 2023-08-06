'''Functional tests for controllers/package.py.'''
import json
import pytest
import responses

import datapackage_creator
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as toolkit


responses.add_passthru(toolkit.config['solr_url'])


@pytest.mark.ckan_config('ckan.plugins', 'datapackage_creator')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestDatapackageBlueprint():
    '''Functional tests for the DataPackage Blueprint.'''

    def test_tabular_file(self, app):
        pass

    def test_not_tabular_file(self, app):
        pass
