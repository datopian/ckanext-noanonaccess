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
    def identify(self):
        try:
            is_anonoumous_user = tk.current_user.is_anonymous
        except Exception:
            # for before ckan v2.10.x
            from ckan.views import _identify_user_default

            _identify_user_default()
            if getattr(tk.c, "user", False):
                is_anonoumous_user = False
            else:
                is_anonoumous_user = True

        # if not anonymous user then no need to check
        if not is_anonoumous_user:
            return
        
        current_path = tk.request.path

        def _get_blueprint_and_view_function():
            if hasattr(tk.request, "blueprint"):
                if current_path is not None:
                    route = current_app.url_map.bind("").match(current_path)
                    endpoint = route[0]
                    if "." not in endpoint:
                        return endpoint
                    blueprint_name, view_function_name = endpoint.split(".", 1)
                    return "%s.%s" % (blueprint_name, view_function_name)
                else:
                    return ""
            else:
                # Backwards compatibility for CKAN < 2.9.x (Pylons routes)
                pylons_mapper = config.get("routes.map", "")
                match = pylons_mapper.routematch(current_path)
                if match:
                    # Extract the controller and action from the matched route
                    controller = match[0]["controller"]
                    action = match[0]["action"]
                    name = match[1].name or controller
                    return "%s.%s" % (name, action)
                else:
                    return ""

        current_blueprint = _get_blueprint_and_view_function()

        # check if the blueprint route is in the allowed list
        allowed_blueprint = [
            "static",  # static files
            "user.login",  # login page
            "user.register",  # register page
            "user.logout",  # logout page
            "user.logged_out_page",  # logged out page redirect
            "user.request_reset",  # request reset page
            "user.perform_reset",  # perform reset page
            "util.internal_redirect",  # internal redirect
            "api.i18n_js_translations",  # i18n js translations
            "webassets.index",  # webassets files eg. js, css files urls
            "api.action",  # api calls
            "_debug_toolbar.static",  # debug toolbar static files
            "resource.download",  # resource download url
            "dataset_resource.download",  # dataset resource download url
            "util.redirect",  # Pylons redirect
            "package.resource_download",  # Pylons resource download url
        ]

        # allow 'dcat' endpoints
        if "dcat" in config.get("ckan.plugins", ""):
            allowed_blueprint.extend(
                [
                    "dcat.read_dataset",
                    "dcat.read_catalog",
                    "dcat.rdf_dataset",
                    "dcat.rdf_catalog",
                    "dcat_json_interface.dcat_json",
                    # pylons url
                    "dcat_dataset.read_catalog"
                    "dcat_dataset.read_dataset"
                    "ckanext.dcat.controllers:DCATController.dcat_json",
                ]
            )

        # allow 'datastore' endpoints
        if "datastore" in config.get("ckan.plugins", ""):
            allowed_blueprint.extend(
                [
                    "datastore.dump",
                    # pylons url
                    "ckanext.datastore.controller:DatastoreController.dump",
                ]
            )

        # allow 's3filestore' endpoints
        if "s3filestore" in config.get("ckan.plugins", ""):
            allowed_blueprint.extend(
                [
                    "s3_resource.resource_download",
                    "s3_uploads.uploaded_file_redirect",
                    # pylons url
                    "resource_download.resource_download",
                    "uploaded_file.uploaded_file_redirect",
                ]
            )

        # allow 'googleanalytics' endpoints
        if "googleanalytics" in config.get("ckan.plugins", ""):
            allowed_blueprint.extend(
                [
                    "google_analytics.action",
                    # Pylons url
                    "ckanext.googleanalytics.controller:GAApiController.action",
                ]
            )

        # allow 'security' endpoints
        if "security" in config.get("ckan.plugins", ""):
            allowed_blueprint.extend(
                [
                    "mfa_user.login",
                    "mfa_user.configure_mfa",
                    "mfa_user.new",
                    # Pylons url
                    "ckanext.security.controllers:SecureUserController.request_reset",
                    "ckanext.security.controllers:SecureUserController.perform_reset",
                    "ckanext.security.controllers:MFAUserController.login",
                    "ckanext.security.controllers:MFAUserController.configure_mfa",
                    "ckanext.security.controllers:MFAUserController.new",
                ]
            )

        # allowed blueprint specified the environment variable
        allowed_blueprints_in_env = config.get(
            "ckanext.noanonaccess.allowed_blueprint", []
        )
        if allowed_blueprints_in_env:
            allowed_blueprint.extend(allowed_blueprints_in_env.split(" "))

        # allow if current blueprint is in allowed blueprint route
        restricted_access = not (current_blueprint in allowed_blueprint)

        # allowed regex path list specified in the environment variable
        allowed_paths = config.get("ckanext.noanonaccess.allowed_paths", [])
        if allowed_paths:
            allowed_paths = allowed_paths.split(" ")

        for path in allowed_paths:
            if re.match(path, current_path):
                restricted_access = False
                break

        if is_anonoumous_user and restricted_access:
            return tk.redirect_to("user.login", came_from=current_path)
