# -*- coding: utf-8 -*-
#
# These parameters will be passed to the 'config' attribute of the Flask
# instance used by the Dash app. They must be in UPPER CASE in order to take
# effect. For more information see http://flask.pocoo.org/docs/config.

#
# Config For your app
#

# Your App's title
TITLE = 'HVO Dash'

# URL PREFIX the the app will be mounted at. Must start with '/'
URL_BASE_PATHNAME = '/'

# The ID of the element used to inject each page of the multi-page app into
CONTENT_CONTAINER_ID = 'content'

NAVBAR_CONTAINER_ID = 'navbar'

# Boolean that indicates whether to insert a navigation bar into the
# header/sidebar.
NAVBAR = True

# Ordered iterable of navbar items: tuples of (route, name), where 'route' is a
# string corresponding to path of the route (will be prefixed with
# URL_BASE_PATHNAME) and 'name' is a string corresponding to the name of the
# nav item.
NAV_ITEMS = (
    ('kisum', 'Summit'),
    ('kmerz', 'MERZ'),
    ('klerz', 'LERZ'),
)

# Add you own parameters here

#
# Flask internal parameters
# For list of available params, see: http://flask.pocoo.org/docs/config
#
