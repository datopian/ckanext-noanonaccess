import logging

import re
from flask import current_app

import ckan.plugins as plugins
from ckan.plugins import toolkit as tk 
from ckan.plugins.toolkit import config

log = logging.getLogger(__name__)

class NoanonaccessPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthenticator, inherit=True)

    # IAuthenticator
    def identify(self, ):
        try:
            is_anonoumous_user = tk.current_user.is_anonymous 
        except:
            # for before ckan v2.10.x
            from ckan.views import _identify_user_default
            _identify_user_default()
            if getattr(tk.c, 'user', False):
                is_anonoumous_user = False
            else:
                is_anonoumous_user = True
                
        current_path = tk.request.path

        def _get_blueprint_and_view_function():
            if current_path is not None:
                path = tk.request.path
                route = current_app.url_map.bind('').match(path)
                endpoint = route[0]
                if '.' not in endpoint:
                    return endpoint
                blueprint_name, view_function_name = endpoint.split('.', 1)
                return '%s.%s' % (blueprint_name, view_function_name)
            else:
                return ''
                        
        current_blueprint = _get_blueprint_and_view_function()

        # check if the blueprint route is in the allowed list
        allowed_blueprint = [
            'static', # static files
            'user.login', # login page
            'user.register', # register page
            'user.logout', # logout page
            'user.logged_out_page', # logged out page redirect
            'user.request_reset', # request reset page
            'user.perform_reset', # perform reset page
            'util.internal_redirect', # internal redirect
            'api.i18n_js_translations', # i18n js translations
            'webassets.index', # webassets files eg. js, css files urls
            'api.action', # api calls
            '_debug_toolbar.static', # debug toolbar static files
            'resource.download', # resource download url
            'dataset_resource.download', # dataset resource download url
            's3_uploads.uploaded_file_redirect', # s3 uploads redirect
        ]    
       
        # allow 'dcat' endpoints
        if 'dcat' in config.get('ckan.plugins', ''):
            allowed_blueprint.append('dcat.read_catalog') # dcat metadata urls 
            allowed_blueprint.append('dcat.read_dataset')
            allowed_blueprint.append('dcat_json_interface.dcat_json')

        # allow 'datastore' endpoints
        if 'datastore' in config.get('ckan.plugins', ''):
            allowed_blueprint.append('datastore.dump') # datastore dump

        # allow 's3filestore' endpoints
        if 's3filestore' in config.get('ckan.plugins', ''):
            allowed_blueprint.append('s3_resource.resource_download')

        # allow 'googleanalytics' endpoints
        if 'googleanalytics' in config.get('ckan.plugins', ''):
            allowed_blueprint.append('google_analytics.action')

        # allow if current blueprint is in allowed blueprint route 
        restricted_access = not(current_blueprint in allowed_blueprint)
        

        # allowed regex path list 
        allowed_paths = config.get('ckanext.noanonaccess.allowed_paths', [])
        if allowed_paths:
            allowed_paths = allowed_paths.split(' ')
       
        for path in allowed_paths:
            if re.match(path, current_path):
                restricted_access = False
                break

        if is_anonoumous_user and restricted_access:
            return tk.redirect_to('user.login', came_from=current_path)