# encoding: utf-8
import pytest

import ckan.plugins as p
import ckan.tests.factories as factories

tk = p.toolkit


@pytest.mark.ckan_config(u'ckan.plugins', u'noanonaccess datastore')
@pytest.mark.usefixtures(u'with_plugins')
@pytest.mark.usefixtures("with_request_context")
class TestNonanonAccessPlugin(object):
    # make sure the plugin is loaded
    def test_plugin_noanonaccess_is_loaded(self):
        p.plugin_loaded("noanonaccess")


    def test_user_should_not_be_able_to_access_general_pages(self, app):
        resp = app.get(tk.url_for(u'home.index'), follow_redirects=False)
        assert resp.status_code == 302
        assert '/user/login?came_from=%2F' in resp.location

        resp = app.get(tk.url_for(u'dataset.search'), follow_redirects=False)
        assert resp.status_code == 302
        assert '/user/login?came_from=%2Fdataset' in resp.location

    @pytest.mark.ckan_config("ckanext.noanonaccess.allowed_paths", "/dataset")
    def test_user_should_be_able_to_access_allowed_pages(self, app):
        resp = app.get(tk.url_for(u'dataset.search'), follow_redirects=False)
        assert resp.status_code == 200
        
    def test_user_should_be_able_to_access_datastore_dump(self, app, monkeypatch, tmpdir, ckan_config):
        monkeypatch.setitem(ckan_config, u"ckan.storage_path", str(tmpdir))
        resp = app.get(tk.url_for(u'datastore.dump', resource_id='jk', follow_redirects=False))
        # datastore dump url should not return 302 but 404
        assert resp.status_code == 404