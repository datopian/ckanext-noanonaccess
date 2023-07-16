import logging

import re
import ckan.model as model
import ckan.plugins as plugins
from ckan.plugins.toolkit import config
import ckan.lib.base as base
logger = logging.getLogger(__name__)


class AuthMiddleware(object):
    def __init__(self, app, app_conf):
        self.app = app
    def __call__(self, environ, start_response):

        # Get the dcat_access variable from the config object
        dcat_access = config.get('ckanext.noanonaccess.allow_dcat')
        # List of extensions to be made accessible if dcat_access is True
        ext = ['.jsonld','.xml','.ttl','.n3', '.rdf']
        # List of catalog endpoints                                      
        catalog_endpoint = config.get('ckanext.dcat.catalog_endpoint')
        catalog_endpoints = ['/catalog']                                 
        if catalog_endpoint:                  
            catalog_endpoint = catalog_endpoint.split('/{_format}')      
            catalog_endpoints.append(catalog_endpoint[0])
        # Get feeds_access variable from the config object
        feeds_access = config.get('ckanext.noanonaccess.allow_feeds')
        # we putting only UI behind login so API paths should remain accessible
        # also, allow access to dataset download and uploaded files
        path_info = environ['PATH_INFO']
        if 'repoze.who.identity' in environ or self._get_user_for_apikey(environ):
            # if logged in via browser cookies or API key, all pages accessible
            return self.app(environ, start_response)
        elif dcat_access and (path_info.endswith(tuple(ext)) or path_info.startswith(tuple(catalog_endpoints))):
            # If dcat_acess is enabled in the .env file make dataset and 
            # catalog pages accessible
            return self.app(environ, start_response)
        elif feeds_access and path_info.startswith('/feeds/'):
            # If feeds_acess is enabled in the .env file
            # make RSS feeds page accessible
            return self.app(environ, start_response)
        else:
            # List of paths that are allowed to be accessed without login
            allowed_paths = ['/user/login', '/user/_logout', '/user/reset', '/user/logged_out', '/user/logged_in', 
                             '/user/logged_out_redirect', '/user/register', '/oauth2/callback', '/login/sso']
            
            allowed_regexes_path = [r'/webassets/*', r'/base/*', r'/_debug_toolbar/*', r'/api/*',  
                                r'/datastore/dump/*', r'/uploads/*', r'/download/*']
            
            
            if any(path_info == path for path in allowed_paths) or \
                any(re.match(r_path, path_info) for r_path in allowed_regexes_path):
                return self.app(environ, start_response)
            else:
                # If not logged in, redirect to login page
                url = environ.get('HTTP_X_FORWARDED_PROTO', environ.get('wsgi.url_scheme', 'http'))
                url += '://'
                if environ.get('HTTP_HOST'):
                    url += environ['HTTP_HOST']
                else:
                    url += environ['SERVER_NAME']
                url += '/user/login'
                headers = [
                    ('Location', url),
                    ('Content-Length','0'),
                    ('X-Robots-Tag', 'noindex, nofollow, noarchive')
                    ]
                status = '307 Temporary Redirect'
                start_response(status, headers)
                return [''.encode("utf-8")]

    def _get_user_for_apikey(self, environ):
        # Adapted from https://github.com/ckan/ckan/blob/625b51cdb0f1697add59c7e3faf723a48c8e04fd/ckan/lib/base.py#L396
        apikey_header_name = config.get(base.APIKEY_HEADER_NAME_KEY,
                                        base.APIKEY_HEADER_NAME_DEFAULT)
        apikey = environ.get(apikey_header_name, '')
        if not apikey:
            # For misunderstanding old documentation (now fixed).
            apikey = environ.get('HTTP_AUTHORIZATION', '')
        if not apikey:
            apikey = environ.get('Authorization', '')
            # Forget HTTP Auth credentials (they have spaces).
            if ' ' in apikey:
                apikey = ''
        if not apikey:
            return None
        apikey = unicode(apikey)
        # check if API key is valid by comparing against keys of registered users
        query = model.Session.query(model.User)
        user = query.filter_by(apikey=apikey).first()
        return user


class NoanonaccessPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IMiddleware, inherit=True)

    def make_middleware(self, app, config):
        return AuthMiddleware(app, config)
