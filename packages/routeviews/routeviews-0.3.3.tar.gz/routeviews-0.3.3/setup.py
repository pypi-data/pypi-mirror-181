import codecs
import os
import sys
from typing import List

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def long_description():
    return f'''{read('docs/user-guide.md')}

# Release Notes

{read('docs/release-notes.md')}
'''


def installation_requirements() -> List[str]:
    install_requires = [
        'ConfigArgParse>=1',
        'humanize>=2',
        'pathvalidate>=2',
        'pytimeparse>=1',
        'PyYAML>=6',
        'rdap>=1',
        'requests>=2',
        'ruamel.yaml>=0.17',
        'tabulate>=0.8',
        'uologging>=0.7.3',
    ]
    if sys.version_info.minor < 7:  # Install dataclasses backport
        install_requires.append('dataclasses>=0.6')
        install_requires.append('netmiko>=3,<4.1',)  # Netmiko 4.1 drops py36 support
    else:
        install_requires.append('netmiko>=3',)

    return install_requires


setup(
    name='routeviews',
    version='0.3.3',
    description='CLI tools that support RouteViews.',
    long_description_content_type='text/markdown',
    long_description=long_description(),
    author='University of Oregon',
    author_email='rleonar7@uoregon.edu',
    license='MIT',
    url='https://github.com/routeviews/routeviews-cli',
    keywords=['RouteViews', 'CLI', 'peeringdb', 'API', 'Integration'],
    package_dir={'': 'src'},
    package_data={'': ['templates/*']},  # templates are part of our package!
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            #
            # Automation tools (`routeviews` prefix)
            #
            'routeviews-template=routeviews.scripts.template:run_main',
            'routeviews-email-peers=routeviews.scripts.get_peers_email:run_main',
            'routeviews-lint=routeviews.scripts.format_ansible_inventory:run_main',
            'routeviews-peer-request=routeviews.scripts.ansible_peering_request:run_main',
            #
            # Monitoring tools (`rvm` prefix)
            #
            # ⚠ Important: These tools make NO changes.
            # Ideally, all these tools support "--influxdb" line protocol option.
            #
            'rvm-latest-mrt=routeviews.scripts.latest_mrt_dump:run_main',
            'rvm-haproxy-stats=routeviews.scripts.haproxy_stats:run_main',
            'rvm-bmp-status=routeviews.scripts.bmp_status:run_main',
            'rvm-bgp-status=routeviews.scripts.bgp_peering_status:run_main',
        ]
    },
    install_requires=installation_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.6',
    ]
)
