import os

from django.utils.translation import ugettext_lazy as _

from horizon.utils import secret_key

{% if use_syslog %}
from logging.handlers import SysLogHandler
{% endif %}

from openstack_dashboard import exceptions
from openstack_dashboard.settings import HORIZON_CONFIG

DEBUG = {{ debug }}
TEMPLATE_DEBUG = DEBUG


# WEBROOT is the location relative to Webserver root
# should end with a slash.
WEBROOT = '/'
#LOGIN_URL = WEBROOT + 'auth/login/'
#LOGOUT_URL = WEBROOT + 'auth/logout/'
#
# LOGIN_REDIRECT_URL can be used as an alternative for
# HORIZON_CONFIG.user_home, if user_home is not set.
# Do not set it to '/home/', as this will cause circular redirect loop
#LOGIN_REDIRECT_URL = WEBROOT

# Required for Django 1.5.
# If horizon is running in production (DEBUG is False), set this
# with the list of host/domain names that the application can serve.
# For more information see:
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = ['horizon.example.com', ]

# Set SSL proxy settings:
# For Django 1.4+ pass this header from the proxy after terminating the SSL,
# and don't forget to strip it from the client's request.
# For more information see:
# https://docs.djangoproject.com/en/1.4/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
# https://docs.djangoproject.com/en/1.5/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# If Horizon is being served through SSL, then uncomment the following two
# settings to better secure the cookies from security exploits
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True
{% if ssl_configured %}
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
{% endif %}

# A method to supersede the token timeout with a shorter dashboard session
# timeout in seconds.
SESSION_TIMEOUT = {{ session_timeout }}

# Overrides for OpenStack API versions. Use this setting to force the
# OpenStack dashboard to use a specific API version for a given service API.
# Versions specified here should be integers or floats, not strings.
# NOTE: The version should be formatted as it appears in the URL for the
# service API. For example, The identity service APIs have inconsistent
# use of the decimal point, so valid options would be 2.0 or 3.
#OPENSTACK_API_VERSIONS = {
#    "data-processing": 1.1,
#    "identity": 3,
#    "volume": 2,
#}

# Set this to True if running on multi-domain model. When this is enabled, it
# will require user to enter the Domain name in addition to username for login.
#OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False

# Overrides the default domain used when running on single-domain model
# with Keystone V3. All entities will be created in the default domain.
#OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

# Set Console type:
# valid options are "AUTO"(default), "VNC", "SPICE", "RDP", "SERIAL" or None
# Set to None explicitly if you want to deactivate the console.
#CONSOLE_TYPE = "AUTO"

# Show backdrop element outside the modal, do not close the modal
# after clicking on backdrop.
#HORIZON_CONFIG["modal_backdrop"] = "static"

# Specify a regular expression to validate user passwords.
#HORIZON_CONFIG["password_validator"] = {
#    "regex": '.*',
#    "help_text": _("Your password does not meet the requirements."),
#}

# Disable simplified floating IP address management for deployments with
# multiple floating IP pools or complex network requirements.
#HORIZON_CONFIG["simple_ip_management"] = False

# Turn off browser autocompletion for forms including the login form and
# the database creation workflow if so desired.
#HORIZON_CONFIG["password_autocomplete"] = "off"
{% if allow_password_autocompletion %}
HORIZON_CONFIG["password_autocomplete"] = "on"
{% endif %}

# Setting this to True will disable the reveal button for password fields,
# including on the login form.
#HORIZON_CONFIG["disable_password_reveal"] = False

HORIZON_CONFIG["customization_module"] = "{{ customization_module }}"

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

# Set custom secret key:
# You can either set it to a specific value or you can let horizon generate a
# default secret key that is unique on this machine, e.i. regardless of the
# amount of Python WSGI workers (if used behind Apache+mod_wsgi): However,
# there may be situations where you would want to set this explicitly, e.g.
# when multiple dashboard instances are distributed on different machines
# (usually behind a load-balancer). Either you have to make sure that a session
# gets all requests routed to the same dashboard instance or you set the same
# SECRET_KEY for all of them.
# SECRET_KEY = secret_key.generate_or_read_from_file('/var/lib/openstack-dashboard/secret_key')
SECRET_KEY = "{{ secret }}"

# We recommend you use memcached for development; otherwise after every reload
# of the django development server, you will have to login again. To use
# memcached set CACHES to something like
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#    }
#}

# Send email to the console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Or send them to /dev/null
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Configure these for your outgoing email host
#EMAIL_HOST = 'smtp.my-company.com'
#EMAIL_PORT = 25
#EMAIL_HOST_USER = 'djangomail'
#EMAIL_HOST_PASSWORD = 'top-secret!'

# For multiple regions uncomment this configuration, and add (endpoint, title).
#AVAILABLE_REGIONS = [
#    ('http://cluster1.example.com:5000/v2.0', 'cluster1'),
#    ('http://cluster2.example.com:5000/v2.0', 'cluster2'),
#]
{% if regions|length > 1 -%}
AVAILABLE_REGIONS = [
{% for region in regions -%}
    ('{{ region.endpoint }}', '{{ region.title }}'),
{% endfor -%}
]
{% endif -%}

OPENSTACK_HOST = "{{ service_host }}"
OPENSTACK_KEYSTONE_URL = "{{ service_protocol }}://%s:{{ service_port }}/v2.0" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "{{ default_role }}"
# Enables keystone web single-sign-on if set to True.
#WEBSSO_ENABLED = False

# Determines which authentication choice to show as default.
#WEBSSO_INITIAL_CHOICE = "credentials"

# The list of authentication mechanisms
# which include keystone federation protocols.
# Current supported protocol IDs are 'saml2' and 'oidc'
# which represent SAML 2.0, OpenID Connect respectively.
# Do not remove the mandatory credentials mechanism.
#WEBSSO_CHOICES = (
#    ("credentials", _("Keystone Credentials")),
#    ("oidc", _("OpenID Connect")),
#    ("saml2", _("Security Assertion Markup Language")))

# Disable SSL certificate checks (useful for self-signed certificates):
#OPENSTACK_SSL_NO_VERIFY = True

# The CA certificate to use to verify SSL connections
#OPENSTACK_SSL_CACERT = '/path/to/cacert.pem'

# The OPENSTACK_KEYSTONE_BACKEND settings can be used to identify the
# capabilities of the auth backend for Keystone.
# If Keystone has been configured to use LDAP as the auth backend then set
# can_edit_user to False and name to 'ldap'.
#
# TODO(tres): Remove these once Keystone has an API to identify auth backend.
OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True,
}

# Setting this to True, will add a new "Retrieve Password" action on instance,
# allowing Admin session password retrieval/decryption.
#OPENSTACK_ENABLE_PASSWORD_RETRIEVE = False
{% if password_retrieve %}
OPENSTACK_ENABLE_PASSWORD_RETRIEVE = True
{% endif %}

# The Launch Instance user experience has been significantly enhanced.
# You can choose whether to enable the new launch instance experience,
# the legacy experience, or both. The legacy experience will be removed
# in a future release, but is available as a temporary backup setting to ensure
# compatibility with existing deployments. Further development will not be
# done on the legacy experience. Please report any problems with the new
# experience via the Launchpad tracking system.
#
# Toggle LAUNCH_INSTANCE_LEGACY_ENABLED and LAUNCH_INSTANCE_NG_ENABLED to
# determine the experience to enable.  Set them both to true to enable
# both.
#LAUNCH_INSTANCE_LEGACY_ENABLED = True
#LAUNCH_INSTANCE_NG_ENABLED = False

# The Xen Hypervisor has the ability to set the mount point for volumes
# attached to instances (other Hypervisors currently do not). Setting
# can_set_mount_point to True will add the option to set the mount point
# from the UI.
OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': False,
    'can_set_password': False,
    'requires_keypair': False,
}

# The OPENSTACK_CINDER_FEATURES settings can be used to enable optional
# services provided by cinder that is not exposed by its extension API.
OPENSTACK_CINDER_FEATURES = {
    'enable_backup': {{ cinder_backup }},
}

# The OPENSTACK_NEUTRON_NETWORK settings can be used to enable optional
# services provided by neutron. Options currently available are load
# balancer service, security groups, quotas, VPN service.
OPENSTACK_NEUTRON_NETWORK = {
    'enable_router': True,
    'enable_quotas': True,
    'enable_ipv6': True,
    'enable_distributed_router': {{ neutron_network_dvr }},
    'enable_ha_router': {{ neutron_network_l3ha }},
    'enable_lb': {{ neutron_network_lb }},
    'enable_firewall': {{ neutron_network_firewall }},
    'enable_vpn': {{ neutron_network_vpn }},
    'enable_fip_topology_check': {{ enable_fip_topology_check }},

    # Neutron can be configured with a default Subnet Pool to be used for IPv4
    # subnet-allocation. Specify the label you wish to display in the Address
    # pool selector on the create subnet step if you want to use this feature.
    'default_ipv4_subnet_pool_label': None,

    # Neutron can be configured with a default Subnet Pool to be used for IPv6
    # subnet-allocation. Specify the label you wish to display in the Address
    # pool selector on the create subnet step if you want to use this feature.
    # You must set this to enable IPv6 Prefix Delegation in a PD-capable
    # environment.
    'default_ipv6_subnet_pool_label': None,

    # The profile_support option is used to detect if an external router can be
    # configured via the dashboard. When using specific plugins the
    # profile_support can be turned on if needed.
    {% if support_profile -%}
    'profile_support': '{{ support_profile }}',
    {% else -%}
    'profile_support': None,
    {% endif -%}
    #'profile_support': 'cisco',

    # Set which provider network types are supported. Only the network types
    # in this list will be available to choose from when creating a network.
    # Network types include local, flat, vlan, gre, and vxlan.
    'supported_provider_types': ['*'],

    # Set which VNIC types are supported for port binding. Only the VNIC
    # types in this list will be available to choose from when creating a
    # port.
    # VNIC types include 'normal', 'macvtap' and 'direct'.
    # Set to empty list or None to disable VNIC type selection.
    'supported_vnic_types': ['*']
}

# The OPENSTACK_IMAGE_BACKEND settings can be used to customize features
# in the OpenStack Dashboard related to the Image service, such as the list
# of supported image formats.
#OPENSTACK_IMAGE_BACKEND = {
#    'image_formats': [
#        ('', _('Select format')),
#        ('aki', _('AKI - Amazon Kernel Image')),
#        ('ami', _('AMI - Amazon Machine Image')),
#        ('ari', _('ARI - Amazon Ramdisk Image')),
#        ('docker', _('Docker')),
#        ('iso', _('ISO - Optical Disk Image')),
#        ('ova', _('OVA - Open Virtual Appliance')),
#        ('qcow2', _('QCOW2 - QEMU Emulator')),
#        ('raw', _('Raw')),
#        ('vdi', _('VDI - Virtual Disk Image')),
#        ('vhd', ('VHD - Virtual Hard Disk')),
#        ('vmdk', _('VMDK - Virtual Machine Disk')),
#    ]
#}

# The IMAGE_CUSTOM_PROPERTY_TITLES settings is used to customize the titles for
# image custom property attributes that appear on image detail pages.
IMAGE_CUSTOM_PROPERTY_TITLES = {
    "architecture": _("Architecture"),
    "kernel_id": _("Kernel ID"),
    "ramdisk_id": _("Ramdisk ID"),
    "image_state": _("Euca2ools state"),
    "project_id": _("Project ID"),
    "image_type": _("Image Type"),
}

# The IMAGE_RESERVED_CUSTOM_PROPERTIES setting is used to specify which image
# custom properties should not be displayed in the Image Custom Properties
# table.
IMAGE_RESERVED_CUSTOM_PROPERTIES = []

# OPENSTACK_ENDPOINT_TYPE specifies the endpoint type to use for the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is 'publicURL'.
#OPENSTACK_ENDPOINT_TYPE = "publicURL"
{% if primary_endpoint -%}
OPENSTACK_ENDPOINT_TYPE = "{{ primary_endpoint }}"
{% endif -%}

# SECONDARY_ENDPOINT_TYPE specifies the fallback endpoint type to use in the
# case that OPENSTACK_ENDPOINT_TYPE is not present in the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is None.  This
# value should differ from OPENSTACK_ENDPOINT_TYPE if used.
#SECONDARY_ENDPOINT_TYPE = "publicURL"
{% if secondary_endpoint -%}
SECONDARY_ENDPOINT_TYPE = "{{ secondary_endpoint }}"
{% endif -%}

# The number of objects (Swift containers/objects or images) to display
# on a single page before providing a paging element (a "more" link)
# to paginate results.
API_RESULT_LIMIT = {{ api_result_limit }}
API_RESULT_PAGE_SIZE = 20

# The size of chunk in bytes for downloading objects from Swift
SWIFT_FILE_TRANSFER_CHUNK_SIZE = 512 * 1024

# Specify a maximum number of items to display in a dropdown.
DROPDOWN_MAX_ITEMS = 30

# The timezone of the server. This should correspond with the timezone
# of your entire OpenStack installation, and hopefully be in UTC.
TIME_ZONE = "UTC"

# When launching an instance, the menu of available flavors is
# sorted by RAM usage, ascending. If you would like a different sort order,
# you can provide another flavor attribute as sorting key. Alternatively, you
# can provide a custom callback method to use for sorting. You can also provide
# a flag for reverse sort. For more info, see
# http://docs.python.org/2/library/functions.html#sorted
#CREATE_INSTANCE_FLAVOR_SORT = {
#    'key': 'name',
#     # or
#    'key': my_awesome_callback_method,
#    'reverse': False,
#}

# Set this to True to display an 'Admin Password' field on the Change Password
# form to verify that it is indeed the admin logged-in who wants to change
# the password.
#ENFORCE_PASSWORD_CHECK = False

# Modules that provide /auth routes that can be used to handle different types
# of user authentication. Add auth plugins that require extra route handling to
# this list.
#AUTHENTICATION_URLS = [
#    'openstack_auth.urls',
#]

# The Horizon Policy Enforcement engine uses these values to load per service
# policy rule files. The content of these files should match the files the
# OpenStack services are using to determine role based access control in the
# target installation.

# Path to directory containing policy.json files
#POLICY_FILES_PATH = os.path.join(ROOT_PATH, "conf")

# Map of local copy of service policy files.
# Please insure that your identity policy file matches the one being used on
# your keystone servers. There is an alternate policy file that may be used
# in the Keystone v3 multi-domain case, policy.v3cloudsample.json.
# This file is not included in the Horizon repository by default but can be
# found at
# http://git.openstack.org/cgit/openstack/keystone/tree/etc/ \
# policy.v3cloudsample.json
# Having matching policy files on the Horizon and Keystone servers is essential
# for normal operation. This holds true for all services and their policy files.
#POLICY_FILES = {
#    'identity': 'keystone_policy.json',
#    'compute': 'nova_policy.json',
#    'volume': 'cinder_policy.json',
#    'image': 'glance_policy.json',
#    'orchestration': 'heat_policy.json',
#    'network': 'neutron_policy.json',
#    'telemetry': 'ceilometer_policy.json',
#}

# Trove user and database extension support. By default support for
# creating users and databases on database instances is turned on.
# To disable these extensions set the permission here to something
# unusable such as ["!"].
#TROVE_ADD_USER_PERMS = []
#TROVE_ADD_DATABASE_PERMS = []

# Change this patch to the appropriate static directory containing
# two files: _variables.scss and _styles.scss
#CUSTOM_THEME_PATH = 'themes/default'

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        {% if use_syslog %}
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
        },
        {% endif %}
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_dashboard': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'novaclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'cinderclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'keystoneclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'glanceclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'neutronclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'heatclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'ceilometerclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'troveclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'swiftclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_auth': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'nose.plugins.manager': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'level': 'DEBUG',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['null'],
            'propagate': False,
        },
        'scss': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}

# 'direction' should not be specified for all_tcp/udp/icmp.
# It is specified in the form.
SECURITY_GROUP_RULES = {
    'all_tcp': {
        'name': _('All TCP'),
        'ip_protocol': 'tcp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_udp': {
        'name': _('All UDP'),
        'ip_protocol': 'udp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_icmp': {
        'name': _('All ICMP'),
        'ip_protocol': 'icmp',
        'from_port': '-1',
        'to_port': '-1',
    },
    'ssh': {
        'name': 'SSH',
        'ip_protocol': 'tcp',
        'from_port': '22',
        'to_port': '22',
    },
    'smtp': {
        'name': 'SMTP',
        'ip_protocol': 'tcp',
        'from_port': '25',
        'to_port': '25',
    },
    'dns': {
        'name': 'DNS',
        'ip_protocol': 'tcp',
        'from_port': '53',
        'to_port': '53',
    },
    'http': {
        'name': 'HTTP',
        'ip_protocol': 'tcp',
        'from_port': '80',
        'to_port': '80',
    },
    'pop3': {
        'name': 'POP3',
        'ip_protocol': 'tcp',
        'from_port': '110',
        'to_port': '110',
    },
    'imap': {
        'name': 'IMAP',
        'ip_protocol': 'tcp',
        'from_port': '143',
        'to_port': '143',
    },
    'ldap': {
        'name': 'LDAP',
        'ip_protocol': 'tcp',
        'from_port': '389',
        'to_port': '389',
    },
    'https': {
        'name': 'HTTPS',
        'ip_protocol': 'tcp',
        'from_port': '443',
        'to_port': '443',
    },
    'smtps': {
        'name': 'SMTPS',
        'ip_protocol': 'tcp',
        'from_port': '465',
        'to_port': '465',
    },
    'imaps': {
        'name': 'IMAPS',
        'ip_protocol': 'tcp',
        'from_port': '993',
        'to_port': '993',
    },
    'pop3s': {
        'name': 'POP3S',
        'ip_protocol': 'tcp',
        'from_port': '995',
        'to_port': '995',
    },
    'ms_sql': {
        'name': 'MS SQL',
        'ip_protocol': 'tcp',
        'from_port': '1433',
        'to_port': '1433',
    },
    'mysql': {
        'name': 'MYSQL',
        'ip_protocol': 'tcp',
        'from_port': '3306',
        'to_port': '3306',
    },
    'rdp': {
        'name': 'RDP',
        'ip_protocol': 'tcp',
        'from_port': '3389',
        'to_port': '3389',
    },
}

# Deprecation Notice:
#
# The setting FLAVOR_EXTRA_KEYS has been deprecated.
# Please load extra spec metadata into the Glance Metadata Definition Catalog.
#
# The sample quota definitions can be found in:
# <glance_source>/etc/metadefs/compute-quota.json
#
# The metadata definition catalog supports CLI and API:
#  $glance --os-image-api-version 2 help md-namespace-import
#  $glance-manage db_load_metadefs <directory_with_definition_files>
#
# See Metadata Definitions on: http://docs.openstack.org/developer/glance/

# Indicate to the Sahara data processing service whether or not
# automatic floating IP allocation is in effect.  If it is not
# in effect, the user will be prompted to choose a floating IP
# pool for use in their cluster.  False by default.  You would want
# to set this to True if you were running Nova Networking with
# auto_assign_floating_ip = True.
#SAHARA_AUTO_IP_ALLOCATION_ENABLED = False

# The hash algorithm to use for authentication tokens. This must
# match the hash algorithm that the identity server and the
# auth_token middleware are using. Allowed values are the
# algorithms supported by Python's hashlib library.
#OPENSTACK_TOKEN_HASH_ALGORITHM = 'md5'

# Hashing tokens from Keystone keeps the Horizon session data smaller, but it
# doesn't work in some cases when using PKI tokens.  Uncomment this value and
# set it to False if using PKI tokens and there are 401 errors due to token
# hashing.
#OPENSTACK_TOKEN_HASH_ENABLED = True

# AngularJS requires some settings to be made available to
# the client side. Some settings are required by in-tree / built-in horizon
# features. These settings must be added to REST_API_REQUIRED_SETTINGS in the
# form of ['SETTING_1','SETTING_2'], etc.
#
# You may remove settings from this list for security purposes, but do so at
# the risk of breaking a built-in horizon feature. These settings are required
# for horizon to function properly. Only remove them if you know what you
# are doing. These settings may in the future be moved to be defined within
# the enabled panel configuration.
# You should not add settings to this list for out of tree extensions.
# See: https://wiki.openstack.org/wiki/Horizon/RESTAPI
REST_API_REQUIRED_SETTINGS = ['OPENSTACK_HYPERVISOR_FEATURES']

# Additional settings can be made available to the client side for
# extensibility by specifying them in REST_API_ADDITIONAL_SETTINGS
# !! Please use extreme caution as the settings are transferred via HTTP/S
# and are not encrypted on the browser. This is an experimental API and
# may be deprecated in the future without notice.
#REST_API_ADDITIONAL_SETTINGS = []

###############################################################################
# Ubuntu Settings
###############################################################################

{% if ubuntu_theme %}
# Enable the Ubuntu theme if it is present.
try:
  from ubuntu_theme import *
except ImportError:
  pass
{% elif default_theme %}
CUSTOM_THEME_PATH = 'themes/{{ default_theme }}'
{% endif %}

# Default Ubuntu apache configuration uses /horizon as the application root.
{% if webroot == "/" %}
LOGIN_URL='/auth/login/'
LOGOUT_URL='/auth/logout/'
{% else %}
LOGIN_URL='{{ webroot }}/auth/login/'
LOGOUT_URL='{{ webroot }}/auth/logout/'
{% endif %}
LOGIN_REDIRECT_URL='{{ webroot }}'


# By default, validation of the HTTP Host header is disabled.  Production
# installations should have this set accordingly.  For more information
# see https://docs.djangoproject.com/en/dev/ref/settings/.
ALLOWED_HOSTS = '*'

{{ settings|join('\n\n') }}

# Compress all assets offline as part of packaging installation
#COMPRESS_OFFLINE = True

# DISALLOW_IFRAME_EMBED can be used to prevent Horizon from being embedded
# within an iframe. Legacy browsers are still vulnerable to a Cross-Frame
# Scripting (XFS) vulnerability, so this option allows extra security hardening
# where iframes are not used in deployment. Default setting is True.
# For more information see:
# http://tinyurl.com/anticlickjack
#DISALLOW_IFRAME_EMBED = True
