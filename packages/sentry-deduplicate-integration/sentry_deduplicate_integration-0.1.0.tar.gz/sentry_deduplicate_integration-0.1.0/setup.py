# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentry_deduplicate_integration', 'sentry_deduplicate_integration.tests']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'sentry-deduplicate-integration',
    'version': '0.1.0',
    'description': '',
    'long_description': '# sentry-deduplicate-integration\n\nSentry integration to rate-limit duplicated errors, using redis to sync error\ncount and identify duplications.\n\nAdd the integration to your sentry_sdk initialization.\n\n```python\nimport redis\nfrom sentry_deduplicate_integration import SentryDeduplicateIntegration\n\n\nsentry_sdk.init(\n    integrations=[\n        SentryDeduplicateIntegration(\n            redis_factory=redis.Redis,\n            max_events_per_minute=10,\n        ),\n    ],\n)\n```\n\nThe `redis_factory` arg is any function returning a redis client.\n',
    'author': 'Iuri de Silvio',
    'author_email': 'iurisilvio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
