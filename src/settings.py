from __future__ import absolute_import, unicode_literals

######################
# CARTRIDGE SETTINGS #
######################

# The following settings are already defined in cartridge.shop.defaults
# with default values, but are common enough to be put here, commented
# out, for conveniently overriding. Please consult the settings
# documentation for a full list of settings Cartridge implements:
# http://cartridge.jupo.org/configuration.html#default-settings

# Sequence of available credit card types for payment.
# SHOP_CARD_TYPES = ("Mastercard", "Visa", "Diners", "Amex")

# Setting to turn on featured images for shop categories. Defaults to False.
SHOP_CATEGORY_USE_FEATURED_IMAGE = True

# Set an alternative OrderForm class for the checkout process.
# SHOP_CHECKOUT_FORM_CLASS = 'cartridge.shop.forms.OrderForm'

# If True, the checkout process is split into separate
# billing/shipping and payment steps.
# SHOP_CHECKOUT_STEPS_SPLIT = True

# If True, the checkout process has a final confirmation step before
# completion.
SHOP_CHECKOUT_STEPS_CONFIRMATION = True

# Controls the formatting of monetary values accord to the locale
# module in the python standard library. If an empty string is
# used, will fall back to the system's locale.
SHOP_CURRENCY_LOCALE = "de_CH"

# Dotted package path and name of the function that
# is called on submit of the billing/shipping checkout step. This
# is where shipping calculation can be performed and set using the
# function ``cartridge.shop.utils.set_shipping``.
# SHOP_HANDLER_BILLING_SHIPPING = \
#                       "cartridge.shop.checkout.default_billship_handler"

# Dotted package path and name of the function that
# is called once an order is successful and all of the order
# object's data has been created. This is where any custom order
# processing should be implemented.
# SHOP_HANDLER_ORDER = "cartridge.shop.checkout.default_order_handler"

# Dotted package path and name of the function that
# is called on submit of the payment checkout step. This is where
# integration with a payment gateway should be implemented.
# SHOP_HANDLER_PAYMENT = "cartridge.shop.checkout.default_payment_handler"

# Sequence of value/name pairs for order statuses.
SHOP_ORDER_STATUS_CHOICES = (
     (1, "Neu"),
     (2, "Bezahlt"),
)

# Sequence of value/name pairs for types of product options,
# eg Size, Colour. NOTE: Increasing the number of these will
# require database migrations!
# SHOP_OPTION_TYPE_CHOICES = (
#     (1, "Size"),
#     (2, "Colour"),
# )

# Sequence of indexes from the SHOP_OPTION_TYPE_CHOICES setting that
# control how the options should be ordered in the admin,
# eg for "Colour" then "Size" given the above:
# SHOP_OPTION_ADMIN_ORDER = (2, 1)

SHOP_USE_RATINGS = False
SHOP_USE_WISHLIST = False
SHOP_PAYMENT_STEP_ENABLED = False
SHOP_DEFAULT_SHIPPING_VALUE = 0

SHOP_ORDER_FROM_EMAIL = "shop@shcbelpa.ch"
SHOP_ORDER_EMAIL_BCC = "webmaster@shcbelpa.ch"

SHOP_PRODUCER_EMAIL = "info@wittwer-mode.ch"
EMAIL_FAIL_SILENTLY = False

EXTRA_MODEL_FIELDS = (
    (
         "cartridge.shop.models.Product.require_number",
         "BooleanField",
         ("Require Player number",),
         {"help_text": 'Check if a player number should be collected when this product is purchased',
          "default": False},
     ),
     (
         "cartridge.shop.models.CartItem.player_number",
         "DecimalField",
         ("Spielernummer",),
         {"blank": True, "null": True, "max_digits": 2, "decimal_places": 0},
     ),
     (
         "cartridge.shop.models.OrderItem.player_number",
         "DecimalField",
         ("Spielernummer",),
         {"blank": True, "null": True, "max_digits": 2, "decimal_places": 0},
     ),
)

######################
# MEZZANINE SETTINGS #
######################

# All logged-in user can edit/view all BlogPosts
OWNABLE_MODELS_ALL_EDITABLE = ('blog.BlogPost',)

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, "Top navigation bar", "pages/menus/dropdown.html"),
#     (2, "Left-hand tree", "pages/menus/tree.html"),
#     (3, "Footer", "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
# )



# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting.
USE_SOUTH = True

# use Django slugify method which handles german Umlauts correct
SLUGIFY = 'django.template.defaultfilters.slugify'

########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    ('Webmaster', 'webmaster@shcbelpa.ch'),
)
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.shcbelpa.ch', '87.230.93.145']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Zurich'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "de"

# Supported languages
_ = lambda s: s
LANGUAGES = (
    ('de', _('Deutsch')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

THUMBNAIL_DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

CACHE_MIDDLEWARE_SECONDS = 300

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "cartridge.shop",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.twitter",
    "sorl.thumbnail",
    "annoying",
    "shcbelpa",
    #"mezzanine.accounts",
    #"mezzanine.mobile",
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
    "shcbelpa.context_processors.gallery_processor",
    "shcbelpa.context_processors.ga_tracking",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    "south",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

###################
# DEPLOY SETTINGS #
###################

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "SSH_USER": "", # SSH username for host deploying to
#     "HOSTS": ALLOWED_HOSTS[:1], # List of hosts to deploy to (eg, first host)
#     "DOMAINS": ALLOWED_HOSTS, # Domains for public site
#     "REPO_URL": "ssh://hg@bitbucket.org/user/project", # Project's repo URL
#     "VIRTUALENV_HOME":  "", # Absolute remote path for virtualenvs
#     "PROJECT_NAME": "", # Unique identifier for project
#     "REQUIREMENTS_PATH": "requirements.txt", # Project's pip requirements
#     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#     "DB_PASS": "", # Live database password
#     "ADMIN_PASS": "", # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }

##################
# SHCBELPA SETTINGS #
##################

HOME_CLUB = 'SHC Belpa 1107'
PICASA_IMGMAX = 1024

##################
# GA SETTINGS #
##################
GA_TRACKING_CODE = None

##################
# DJANGO COMPRESSOR #
##################

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.yuglify.YUglifyCSSFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]



##################
# LOGGING        #
##################
LOGGING_DIR = "%s/../../logs" % PROJECT_ROOT

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true']
        },
        'error_log': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/error.log' % LOGGING_DIR,
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 100,
            'formatter': 'simple',
            'filters': ['require_debug_false']
        },
    },
    'loggers': {
        'shcbelpa': {
            'handlers': ['error_log', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_log', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django': {
            'handlers': ['error_log', 'console'],
            'level': 'WARNING',
            'propagate': True,
        }
    }
}


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

from compressor.conf import CompressorConf
for key, value in CompressorConf().configured_data.iteritems():
    locals()['COMPRESS_' + key] = value
