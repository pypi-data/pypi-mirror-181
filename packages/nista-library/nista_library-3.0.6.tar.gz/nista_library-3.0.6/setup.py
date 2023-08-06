# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_point_client',
 'data_point_client.api',
 'data_point_client.api.data_export',
 'data_point_client.api.data_point',
 'data_point_client.models',
 'nista_library']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'attrs>=20.1.0,<23.0.0',
 'colorama>=0.4.4,<0.5.0',
 'httpx>=0.15.4,<1.0.0',
 'keyring>=23.5.0,<24.0.0',
 'oauth2-client>=1.2.1,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'structlog>=21.0.0,<22.0.0']

setup_kwargs = {
    'name': 'nista-library',
    'version': '3.0.6',
    'description': 'A client library for accessing nista.io',
    'long_description': '[![Gitlab Pipeline](https://gitlab.com/campfiresolutions/public/nista.io-python-library/badges/main/pipeline.svg)](https://gitlab.com/campfiresolutions/public/nista.io-python-library/-/pipelines) [![Python Version](https://img.shields.io/pypi/pyversions/nista-library)](https://pypi.org/project/nista-library/) [![PyPI version](https://img.shields.io/pypi/v/nista-library)](https://pypi.org/project/nista-library/) [![License](https://img.shields.io/pypi/l/nista-library)](https://pypi.org/project/nista-library/) [![Downloads](https://img.shields.io/pypi/dm/nista-library)](https://pypi.org/project/nista-library/)\n\n# nista-library\n\nA client library for accessing nista.io\n\n## Tutorial\n\n### Create new Poetry Project\n\nNavigate to a folder where you want to create your project and type\n\n```shell\npoetry new my-nista-client\ncd my-nista-client\n```\n\n### Add reference to your Project\n\nNavigate to the newly created project and add the PyPI package\n\n```shell\npoetry add nista-library\n```\n\n### Your first DataPoint\n\nCreate a new file you want to use to receive data this demo.py\n\n```python\nfrom nista_library import KeyringNistaConnection, NistaDataPoint, NistaDataPoints\n\nconnection = KeyringNistaConnection()\n\ndata_point_id = "56c5c6ff-3f7d-4532-8fbf-a3795f7b48b8"\ndata_point = NistaDataPoint(connection=connection, data_point_id=data_point_id)\n\ndata_point_data = data_point.get_data_point_data()\n\nprint(data_point_data)\n```\n\nYou need to replace the `DataPointId` with an ID from your nista.io workspace.\n\nFor example the DataPointId of this DataPoint `https://aws.nista.io/secured/dashboard/datapoint/4684d681-8728-4f59-aeb0-ac3f3c573303` is `4684d681-8728-4f59-aeb0-ac3f3c573303`\n\n### Run and Login\n\nRun your file in poetry\'s virtual environment\n\n```console\n$ poetry run python demo.py\n2021-09-02 14:51.58 [info     ] Authentication has been started. Please follow the link to authenticate with your user: [nista_library.nista_connetion] url=https://aws.nista.io/authentication/connect/authorize?client_id=python&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fhome&response_type=code&scope=data-api%20openid%20profile%20offline_access&state=myState\n```\n\nIn order to login copy the `url` into your Browser and Login to nista.io or, if allowed a browser window will open by itself.\n\n### Keystore\n\nOnce you loggedin, the library will try to store your access token in your private keystore. Next time you run your programm, it might request a password to access your keystore again to gain access to nista.io\nPlease take a look at [Keyring](https://pypi.org/project/keyring/) for details.\n\n## Advanced Example\n\n### Show received Data in a plot\n\n```shell\npoetry new my-nista-client\ncd my-nista-client\npoetry add nista-library\npoetry add structlib\npoetry add matplotlib\n```\n\n```python\nimport matplotlib.pyplot as plt\nfrom structlog import get_logger\n\nfrom nista_library import KeyringNistaConnection, NistaDataPoint, NistaDataPoints\n\nlog = get_logger()\n\nconnection = KeyringNistaConnection()\n\ndata_point_id = "56c5c6ff-3f7d-4532-8fbf-a3795f7b48b8"\ndata_point = NistaDataPoint(connection=connection, data_point_id=data_point_id)\n\ndata_point_data = data_point.get_data_point_data()\nlog.info("Data has been received. Plotting")\ndata_point_data.plot()\nplt.show()\n\n```\n\n### Filter by DataPoint Names\n\n```shell\npoetry new my-nista-client\ncd my-nista-client\npoetry add nista-library\npoetry add structlib\npoetry add matplotlib\n```\n\n```python\nimport matplotlib.pyplot as plt\nfrom structlog import get_logger\n\nfrom nista_library import KeyringNistaConnection, NistaDataPoint, NistaDataPoints\n\nlog = get_logger()\n\nconnection = KeyringNistaConnection()\n\ndataPoints = NistaDataPoints(connection=connection)\ndata_point_list = list(dataPoints.get_data_point_list())\n\nfor data_point in data_point_list:\n    log.info(data_point)\n\n# Find Specific Data Points\nfiltered_data_points = filter(\n    lambda data_point: data_point.name.startswith("371880214002"), data_point_list\n)\nfor data_point in filtered_data_points:\n    # get the data\n    data_point_data = data_point.get_data_point_data()\n    log.info(data_point_data)\n    data_point_data.plot()\n    plt.show()\n\n```\n\n## Links\n\n**Website**\n[![nista.io](https://www.nista.io/assets/images/nista-logo-small.svg)](nista.io)\n\n**PyPi**\n[![PyPi](https://pypi.org/static/images/logo-small.95de8436.svg)](https://pypi.org/project/nista-library/)\n\n**GIT Repository**\n[![Gitlab](https://about.gitlab.com/images/icons/logos/slp-logo.svg)](https://gitlab.com/campfiresolutions/public/nista.io-python-library)\n',
    'author': 'Markus Hoffmann',
    'author_email': 'markus.hoffmann@nista.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://nista.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
