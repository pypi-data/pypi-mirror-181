# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantha_streamlit_compare', 'semantha_streamlit_compare.components']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'semantha_sdk==4.1.1', 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'semantha-streamlit-compare',
    'version': '0.2.0',
    'description': 'This is the project for a streamlit component which uses semantha semantic compare.',
    'long_description': '<a href="https://semantha.de"><img src="https://www.semantha.de/wp-content/uploads/semantha.svg" width="380" height="95" align="right" /></a>\n\n# semantha-streamlit-compare: semantha building blocks for Streamlit apps\n\nThis project gives you an idea of how to use our component for building applications with streamlit. And all of this using semantha\'s native capabilities to process semantics in text.\n\ntl;dr: using Streamlit, you can employ semantha\'s semantic comparison with just three lines of code (see below).\n\n## Which Components Are Involved?\nStreamlit.io offers easy GUI implementations. semantha.ai is a semantic processing platform which provides a REST/API for many use cases, end systems, etc.\n\n![alt text](https://user-images.githubusercontent.com/117350133/200347538-367e9478-26cb-4f4a-8e9a-21669cf1695f.jpg  "Streamlit Component Example")\n\n## 🚀 Quickstart\n\nYou can install `semantha-streamlit-compare` from pip:\n\n```bash\npip install semantha-streamlit-compare\n```\n\n\nThen put the following example code in a file.\n\n```python\nfrom semantha_streamlit_compare.components.compare import SemanticCompare\n\ncompare = SemanticCompare()\ncompare.build_input(sentences=("First sentence", "Second sentence"))\n```\n\n## 🎛 Setup, Secret, and API Key\nTo use the component, you need to request a secrets.toml file. You can request that at support@thingsthinking.atlassian.net<br />\nThe file is structured as follows:\n```\n[semantha]\nserver_url="URL_TO_SERVER"\napi_key="YOUR_API_KEY_ISSUED"\ndomain="USAGE_DOMAIN_PROVIDED_TO_YOU"\ndocumenttype="document_with_contradiction_enabled"\n```\n',
    'author': 'thingsTHINKING GmbH',
    'author_email': 'github@thingsthinking.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
