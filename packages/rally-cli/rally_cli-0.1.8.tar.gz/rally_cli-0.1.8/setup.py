# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rallycli',
 'rallycli.apis',
 'rallycli.errors',
 'rallycli.models',
 'rallycli.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'aiologger>=0.7.0,<0.8.0',
 'click>=8.1.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'dateparser>=1.1.4,<2.0.0',
 'feedparser>=6.0.10,<7.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-box>=6.1.0,<7.0.0',
 'pytz>=2022.6,<2023.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'simplejson>=3.18.0,<4.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'treelib>=1.6.1,<2.0.0',
 'urllib3>=1.26.13,<2.0.0']

setup_kwargs = {
    'name': 'rally-cli',
    'version': '0.1.8',
    'description': 'Rally software API Client',
    'long_description': '# rally-cly:Rally API Client\n\n## Install\n\nFrom code repo dir:\n\n```shell\npip install --user --editable .\n```\n\n## Use\n> RallyTypeGeneric class is used for all models with no specific model Class\n```python\nfrom typing import List\nfrom rallycli import RallyAPI\nfrom rallycli.models import RallyTypeGeneric, type_names, US, Feature, User\n\nrally_api = RallyAPI(key_based_auth=True,\n                     external_key="<your_external_key_here>",\n                     baseurl="https://eu1.rallydev.com/",\n                     workspace="/workspace/<workspace_OID_here>")\n\nproject_ref: str = "/project/<your_project_OID_here>"\n\n## getting the project\nproject: RallyTypeGeneric = rally_api.project_api.get_project_by_ref(project_ref)\n## getting project releases\nreleases: List[RallyTypeGeneric] = rally_api.timebox_api.get_releases_for_project(project_ref=project._ref)\n## getting project iterations\niterations: List[RallyTypeGeneric] = rally_api.timebox_api.get_active_iterations_for_project(project_ref=project._ref)\n## create UserStory\nus: US = US()\nus.Name = f"Autocreated Us {n}"\nus.Project = project_ref\nus.Description = f"Test US {n} para rallycli python module. By {rally_api.user_api.get_this_user().EmailAddress}"\nus.Owner = rally_api.user_api.get_this_user()\nus.Release = releases[0]._ref\nus.Iteration = iterations[0]._ref\n\ncreated_us: US = rally_api.artifact_api.create_artifact(us, type_names.US)\nprint(created_us)\n\nfeature: Feature = rally_api.artifact_api.get_artifact_by_formattedid("FE1")\nprint(feature.Name)\n\n# Get all disabled users using 4 parallel threads\nusers: List[User] = rally_api.query("( Disabled = true)", "user", fetch="Username",model_class=User, \n                                    threads=4, pagesize=80)\n```\n\n',
    'author': 'J. Andres Guerrero',
    'author_email': 'juguerre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
