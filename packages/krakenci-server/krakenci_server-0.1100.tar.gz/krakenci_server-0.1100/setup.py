# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kraken',
 'kraken.migrations',
 'kraken.migrations.versions',
 'kraken.server',
 'kraken.server.bg',
 'kraken.server.cloud']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.1.0,<2.0.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'Flask>=1.1.4,<2.0.0',
 'MarkupSafe==2.0.1',
 'RestrictedPython==5.0',
 'SQLAlchemy>=1.4.25,<2.0.0',
 'alembic>=1.7.3,<2.0.0',
 'apscheduler>=3.8.0,<4.0.0',
 'azure-identity>=1.6.1,<2.0.0',
 'azure-mgmt-compute>=23.0.0,<24.0.0',
 'azure-mgmt-monitor>=2.0.0,<3.0.0',
 'azure-mgmt-network>=19.0.0,<20.0.0',
 'azure-mgmt-resource>=19.0.0,<20.0.0',
 'azure-mgmt-storage>=18.0.0,<19.0.0',
 'azure-mgmt-subscription>=1.0.0,<2.0.0',
 'boto3>=1.18.52,<2.0.0',
 'casbin>=1.17.1,<2.0.0',
 'clickhouse-driver>=0.2.2,<0.3.0',
 'connexion>=2.13.1,<3.0.0',
 'giturlparse>=0.10.0,<0.11.0',
 'gunicorn>=20.1.0,<21.0.0',
 'jsonschema>=4.5.0,<5.0.0',
 'kubernetes>=20.13.0,<21.0.0',
 'minio>=7.1.0,<8.0.0',
 'passlib>=1.7.4,<2.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-ldap>=3.4.3,<4.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'rq>=1.10.0,<2.0.0',
 'sentry-sdk[flask]>=1.5.0,<2.0.0',
 'swagger-ui-bundle>=0.0.9,<0.0.10',
 'tzlocal==2.1']

entry_points = \
{'console_scripts': ['kkdbmigrate = kraken.migrations.apply:main',
                     'kkplanner = kraken.server.planner:main',
                     'kkqneck = kraken.server.qneck:main',
                     'kkrq = kraken.server.kkrq:main',
                     'kkscheduler = kraken.server.scheduler:main',
                     'kkwatchdog = kraken.server.watchdog:main']}

setup_kwargs = {
    'name': 'krakenci-server',
    'version': '0.1100',
    'description': 'Kraken CI server.',
    'long_description': '# Kraken CI\n\n![Release Version](https://img.shields.io/github/v/release/Kraken-CI/kraken)\n![Release Date](https://img.shields.io/github/release-date/Kraken-CI/kraken)\n\n![Kraken Build](https://lab.kraken.ci/bk/branch-badge/2)\n![Kraken Tests](https://lab.kraken.ci/bk/branch-badge/2/tests)\n![Kraken Issues](https://lab.kraken.ci/bk/branch-badge/2/issues)\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/be770bd29e374ece9e6f2782a1de99fc)](https://www.codacy.com/gh/Kraken-CI/kraken/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Kraken-CI/kraken&amp;utm_campaign=Badge_Grade)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Kraken-CI/kraken.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Kraken-CI/kraken/context:python)\n[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/Kraken-CI/kraken.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Kraken-CI/kraken/context:javascript)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/Kraken-CI/kraken.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Kraken-CI/kraken/alerts/)\n[![codebeat badge](https://codebeat.co/badges/556ac028-2390-4093-839e-a509f5678cf1)](https://codebeat.co/projects/github-com-kraken-ci-kraken-master)\n\n[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4758/badge)](https://bestpractices.coreinfrastructure.org/projects/4758)\n[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/kraken-ci)](https://artifacthub.io/packages/search?repo=kraken-ci)\n\n\n<!-- ABOUT THE PROJECT -->\n## About Kraken CI\n\n![Kraken CI Results Page](https://kraken.ci/img/slide-branch-results.png)\n\nKraken CI is a modern, open-source, on-premise CI/CD system\nthat is highly scalable and focused on testing.\n\nMore information can be found on https://kraken.ci\n\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nQuick start guide is here: https://kraken.ci/docs/quick-start\n\nFull installation manual: https://kraken.ci/docs/installation\n\nAnd here is developers guide: https://kraken.ci/docs/dev-guide\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nGuides can be found here: https://kraken.ci/docs/guide-intro\n\nDemo site is available here: https://lab.kraken.ci/\n\n\n<!-- ROADMAP -->\n## Roadmap\n\nSee the [open issues](https://github.com/kraken-ci/kraken/issues) for a list of proposed features (and known issues).\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nDetails on https://kraken.ci/docs/contrib-kraken\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the Apache 2.0 License. See `LICENSE` for more information.\n\n\n<!-- CONTACT -->\n## Contact\n\nMichal Nowikowski - godfryd@gmail.com\n\nProject Link: [https://kraken.ci](https://kraken.ci)\n',
    'author': 'Michal Nowikowski',
    'author_email': 'godfryd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kraken.ci/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
