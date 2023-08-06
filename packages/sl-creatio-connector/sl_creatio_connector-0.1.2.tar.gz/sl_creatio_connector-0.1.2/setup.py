# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sl_creatio_connector']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'sl-creatio-connector',
    'version': '0.1.2',
    'description': 'Creatio (aka BPMonline) ODATA API helper',
    'long_description': '# <p align="center">Simple logic\'s Creatio ODATA connector</p>\n<p align="center">Connector to integrate <a href="https://academy.creatio.com/docs/developer/integrations_and_api/data_services/odata/overview">Creatio ODATA API</a>.</p>\n<p><a href="https://documenter.getpostman.com/view/10204500/SztHX5Qb">Creatio ODATA API postman documentation</a></p>\n\n## Getting started\n\nThis connector tested for ODATA3 and ODATA4 protocols (including .net core version)\n\n```bash\n$ pip install sl_creatio_connector\n```\n\n```python\n\nfrom sl_creatio_connector.creatio import Creatio\nfrom sl_creatio_connector.constants import ODATA_version\n\n# get collection\ndef get_contact_leads():\n    cr = Creatio(\n        creatio_host=\'http://creatio.mydomen.com:5000\',\n        login=\'Supervisor\',\n        password=\'Supervisor\',\n        odata_version=ODATA_version.v4core\n    )\n    parameters = [\n        "filter=Contact eq \'Marady Esther\'"\n    ]\n    collection = cr.get_object_collection(\n        object_name=\'Lead\',\n        parameters= parameters,\n    )\n    assert len(collection) == 0\n\ndef create_and_delete_contact():\n    cr = Creatio(\n        creatio_host=\'http://creatio.mydomen.com:5000\',\n        login=\'Supervisor\',\n        password=\'Supervisor\',\n        odata_version=ODATA_version.v4core\n    )\n    data = {\n        \'Name\': "Test name"\n    }\n    created_contact = cr.create_object(\n        \'Contact\',\n        data= data,\n    )\n    created_id = created_contact[\'Id\']\n    status_code = cr.delete_object(\'Contact\', created_id).status_code\n\n```\n\n\n',
    'author': 'sumarokov-vp',
    'author_email': 'sumarokov.vp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
