# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nqsdk', 'nqsdk.abstract', 'nqsdk.dummy', 'nqsdk.validation']

package_data = \
{'': ['*'], 'nqsdk.dummy': ['resources/*']}

install_requires = \
['djangorestframework>=3,<4',
 'email-validator>=1,<2',
 'jsonschema>=4,<5',
 'phonenumbers>=8,<9',
 'pytz',
 'requests>=2,<3']

setup_kwargs = {
    'name': 'nqsdk',
    'version': '1.0.0a12',
    'description': 'NQ SDK',
    'long_description': "# NQ SDK\n\n## Abstract Provider Classes\n\nConstruct your provider class using base provider class `nqsdk.abstract.provider.Provider` and appropriate mixin classes depending on what functionality is supported by your provider.\n\nAll abstract methods must be implemented.\n\n## `nqsdk.abstract.provider.Provider`\n\nBase provider class. All providers must be inherited from it.\n\n## `nqsdk.abstract.provider.HealthCheckMixin`\n\nUse if your provider supports health check requests.\n\n## `nqsdk.abstract.provider.BalanceCheckMixin`\n\nUse if your provider supports user's balance check requests.\n\n## `nqsdk.abstract.provider.DeliveryCheckMixin`\n\nUse if your provider supports delivery check requests.\n\n## `nqsdk.abstract.provider.AckCheckMixin`\n\nUse if your provider supports ack check requests.\n\n## `nqsdk.abstract.provider.CallbackHandleMixin`\n\nUse if your provider supports callbacks from your API with no difference b/w `message delivered` & `message ack` events. E.g. all events are sent to the same URL & provider can distinguish them from callback's payload.\n\n## `nqsdk.abstract.provider.DeliveryHandleMixin`\n\nUse if your provider supports `message delivered` event callbacks sent to a specific URL provided by NQ service.\n\n## `nqsdk.abstract.provider.AckHandleMixin`\n\nUse if your provider supports `message ack` event callbacks sent to a specific URL provided by NQ service.\n\n## Dummy Provider\n\n`nqsdk.dummy.provider.DummyProvider` is a dummy implementation of NQ Provider Interface. It does nothing but can be used for tests.\n\nYou can find it at `dummy/provider.py`.\n\n## Tests\n\nRun tests locally:\n\n```shell script\n./scripts/tests\n```\n",
    'author': 'Inqana Ltd.',
    'author_email': 'develop@inqana.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
