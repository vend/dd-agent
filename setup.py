import platform
import sys
from config import *

try:
    from setuptools import setup, find_packages

    # required to build the cython extensions
    from distutils.extension import Extension

except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Extra arguments to pass to the setup function
extra_args = {}

# Prereqs of the build. Won't get installed when deploying the egg.
setup_requires = [
]

# Prereqs of the install. Will install when deploying the egg.
install_requires=[
]

if sys.platform == 'win32':
    import py2exe
    install_requires.extend([
        'tornado==2.3',
        'pywin32==217',
        'wmi==1.4.9',
        'simplejson==2.6.1'
    ])

    class Target(object):
        def __init__(self, **kw):
            self.__dict__.update(kw)
            self.version = get_version()
            self.company_name = "Datadog"
            self.copyright = "2012 Datadog"

    # Create the services
    agent_service = Target(
        name='Datadog Agent',
        description='Sends metrics to Datadog',
        modules=['agent_win32'],
        cmdline_style='pywin32'
    )

    forwarder_service = Target(
        name='Datadog Forwarder',
        description='Buffers metrics from the agent and forwards them to Datadog',
        modules=['forwarder_win32'],
        cmdline_style='pywin32'
    )

    extra_args = {
        'options': {
            'py2exe': {
                'includes': "win32service,win32serviceutil,win32event,simplejson",
                'optimize': 2,
                'compressed': 1,
                'bundle_files': 1,
            },
        },
        'service': [agent_service, forwarder_service],
        'zipfile': None
    }

setup(
    name='datadog-agent',
    version=get_version(),
    description="DevOps' best friend",
    author='DataDog',
    author_email='dev@datadoghq.com',
    url='http://www.datadoghq.com',
    install_requires=install_requires,
    setup_requires=setup_requires,
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    **extra_args
)
