# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsmanager',
 'dsmanager.controller',
 'dsmanager.datamanager',
 'dsmanager.datamanager.datasources',
 'dsmanager.model',
 'dsmanager.view']

package_data = \
{'': ['*']}

install_requires = \
['SharePlum>=0.5.1,<0.6.0',
 'azure-common>=1.1.28,<2.0.0',
 'azure-storage-blob>=12.14.0,<13.0.0',
 'azure-storage-common>=2.1.0,<3.0.0',
 'explainerdashboard>=0.4.0,<0.5.0',
 'ipython>=8.5.0,<9.0.0',
 'numexpr>=2.8.3,<3.0.0',
 'numpy>=1.23.3,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'paramiko>=2.12.0,<3.0.0',
 'pickle-mixin>=1.0.2,<2.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'simple-salesforce>=1.12.2,<2.0.0',
 'snowflake-connector-python>=2.8.0,<3.0.0',
 'snowflake-sqlalchemy>=1.4.2,<2.0.0',
 'sqlalchemy>=1.4.41,<2.0.0',
 'sweetviz>=2.1.4,<3.0.0']

setup_kwargs = {
    'name': 'dsmanager',
    'version': '1.0.8.1',
    'description': 'Template to Kickstart Data Science projects that follows Sklearn standards and brings usefull tools to handle data and models quickly and easily',
    'long_description': '<h1 align="center">DS Template 👨\u200d💻</h1>\n<p>\n  <a href="#" target="_blank">\n  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />\n  </a>\n  <a href="#" target="_blank">\n    <img alt="Documentation" src="https://img.shields.io/badge/documentation-pdoc-orange.svg" />\n  </a>\n  <a href="LICENSE" target="_blank">\n    <img alt="License: Adel Rayane Amrouche" src="https://img.shields.io/badge/License-Adel Rayane Amrouche-yellow.svg" />\n  </a>\n</p>\n\n> Template to Kickstart Data Science projects that follows Sklearn standards and brings usefull tools to handle data and models quickly and easily\n\n## Install\n\n```sh\npip install poetry\npoetry install\n```\n\n## Run tests\n\n```sh\npytest src/\npylint src/\nmypy src/\n```\n\n## Documentation\n\n```sh\npdoc src/\n```\n\n### Usage\n\nThe DS Template has 3 main components:\n- A **DataManager** component\n- A **Controller** component\n- A **Model** component\n\nThe latter depends on the projects type and can be let empty if no model is needed.\n\nThat lets us with both the **controller** and the **data manager**. On the one hand, the **controller** is supposed to be the center of the project and interact with all the components to get the output asked by the user. On the other hand, the **data manager** is working around a json metadata file. This metafile follows a specific schema for both input sources and output sources.\n\n#### Input Sources\n> Sources can take 2 inputs regardless of the type of source and regardless if it is an intput or an output source:\n> - A **type** that can be either **csv**, **excel** or **sql**.\n> - A list of **args** that will be executed by pandas to get access to the source and prepare correctly the dataset.\n>\n> Three kind of **input** sources are handled :\n> - The **local** files that only take a **path** to the source file\n> - The **sharepoint** files that take:\n>   - The **sharepoint** address and the **sites** where the source is\n>   - The **folder** where the file source is\n>   - The **file** source name\n> - The **Sql** sources that take:\n>   - An **username** and a **password** environment variables names\n>   - An **address** of the database and **dialect** of the sql type of database\n>   - A **query** which is not mandatory since sql sources can be handled as a database instead of a simple dataset. You will be then able to query this database like you would do using *sqlalchemy*\n\n*Samples are available in the file **data/metadata.json***\n\n> Two kind of **output** sourcess are handled :\n> - The **local** files that only take a **path** to the source file\n> - The **Sql** sources that take:\n>   - An **username** and a **password** environment variables names\n>   - An **address** of the database and **dialect** of the sql type of database\n>   - A **table_name** where the dataset will be added\n>   - You also might need to include the **schema** and the parameter **if_exists** (either "replace" or append" regarding the way you want to update the table) in the list of **args** \n\n## Author\n\n👤 **Rayane Amrouche**\n\n* Github: [@AARayane](https://github.com/AARayane)\n',
    'author': 'Rayane AMROUCHE',
    'author_email': 'rayaneamrouche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
