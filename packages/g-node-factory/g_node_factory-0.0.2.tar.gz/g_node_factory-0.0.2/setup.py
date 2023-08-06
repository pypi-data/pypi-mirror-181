# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gnf',
 'gnf.data_classes',
 'gnf.dev_utils',
 'gnf.django_related',
 'gnf.django_related.migrations',
 'gnf.enums',
 'gnf.schemata']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'django>=4.1.2,<5.0.0',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.85.1,<0.86.0',
 'pendulum>=2.1.2,<3.0.0',
 'pika>=1.3.1,<2.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'py-algorand-sdk>=1.19.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyteal>=0.19.0,<0.20.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.5,<2023.0',
 'requests-async>=0.6.2,<0.7.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'uvicorn[standard]>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['g-node-factory = gnf.__main__:main']}

setup_kwargs = {
    'name': 'g-node-factory',
    'version': '0.0.2',
    'description': 'G Node Factory',
    'long_description': "# G Node Factory\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nThe GNodeFactory is an actor in a larger Transactive Energy Management (TEM) system. Within that system, it has the authority for creating and updating GNodes. Among other things, it has the authority for creating and updating `TerminalAssets`, which represent the devices capable of transacting on electricity markets within the TEM.\n\nThis repo has been developed through the generous funding of a grant provided by the [Algorand Foundation](https://www.algorand.foundation/). For more context, please read our Algorand [Milestone 1 writeup](docs/wiki/milestone-1.md) and Milestone 2 deck. For design specifications for the repo, go [here](docs/wiki/design-specifications.md). For a very short description of what GNodes are and why we need a factory for them, skip to [Background](#Background) below.\n\n## Local Demo setup\n\n**PREP**\n\n1. Clone this repo\n\n   - Using python 3.10.\\* or greater, create virtual env inside this repo\n\n     ```\n     python -m venv venv\n     source venv/bin/activate\n     pip install -e .\n     ```\n\n2. In sister directories, clone and make virtual envs for these two repos:\n\n   - [https://github.com/thegridelectric/gridworks-marketmaker](https://github.com/thegridelectric/gridworks-marketmaker) (MarketMaker GNode repo)\n   - [https://github.com/thegridelectric/gridworks-atn-spaceheat](https://github.com/thegridelectric/gridworks-atn-spaceheat) (AtomicTNode GNode repo)\n\n   For now, each of these needs a separate virtual env.\n\n3. Start the Algorand sandbox in a **sibling directory**\n\n   a. Clone [Algorand Sandbox](https://github.com/algorand/sandbox) into sibling directory\n\n   ```\n   - YourDemoFolder\n     |\n     -- g-node-factory\n     -- sandbox\n   ```\n\n   b. Start the Algorand sandbox. From the `YourDemoFolder/sandbox` directory\n\n   ```\n   ./sandbox up dev\n   ```\n\n4. Install [docker](https://docs.docker.com/get-docker/)\n\n**RUNNING A SIMULATION OF 4 TERMINAL ASSETS**\n\n**Note**: if your machine is x86, substitute `docker-demo-arm.yml` for `docker-demo-x86.yml` in the instructions below. If you are not sure, try one. If rabbit fails to load try the other.\n\n1. In a terminal for `g-node-factory`, start the dockerized APIS:\n\n   ```\n   ./1prep.sh\n   ```\n\n   - Check at:\n     - [http://localhost:8001/docs](http://localhost:8001/docs) - Api for the dockerized TaValidator\n     - [http://localhost:7997/get-time/](http://localhost:7997/get-time/) - Api for the dockerized TaValidator\n\n2. In that same terminal, start the final gnf API (not in docker yet):\n\n   ```\n   ./2prep.sh\n   ```\n\n3. In a terminal for `gridworks-marketmaker`:\n\n   ```\n   python demo.py\n   ```\n\n   - Check that `d1.isone.ver.keene-Fxxx` shows up in [rabbitmq](http://d1-1.electricity.works:15672/#/queues) passwd/username: smqPublic\n\n4. In a new terminal window for `g-node-factory` repo:\n\n   ```\n   python demo.py\n   ```\n\n## Testing\n\npytest -v\n\n## Configuration and secrets\n\nThe repo uses dotenv and `.env` files. Look at `src/gnf/config` for default values. These are overwritten with values from a\ngit ignored top-level `.env` file. All dev examples are intended to run without needing to create\na `.env` file.\n\n## Code derivation tools\n\nThe primary derivation tool used for this is [ssot.me](https://explore.ssot.me/app/#!/home), developed by EJ Alexandra of [An Abstract Level LLC](https://effortlessapi.com/pages/effortlessapi/blog). All of the xslt code in `CodeGeneration` uses this tool.\n\nThe `ssotme` cli and its upstream `ssotme` service pull data from our [private airtable](https://airtable.com/appgibWM6WZW20bBx/tblRducbzl15OWmwv/viwIvHvZcrMELIP3x?blocks=hide) down into an odxml file and a json file, and then references local `.xslt` scripts in order to derive code. The `.xslt` allows for two toggles - one where files are always overwritten, and one where the derivation tools will leave files alone once any hand-written code is added. Mostly that toggle is set to `always overwrite` since we are working with immutable schemata. Note that the `ssotme cli` requires an internet connection to work, since it needs to access the upstream `ssotme` service.\n\nIf you want to add enums or schema, you will need access to the `ssotme cli` and the airtable. Contact Jessica for this.\n\n## Background\n\nWhat are GNodes and why do we need a factory for them?\n\nThe GNodeFactory stands at the boundary between the physical world and the world of code, maintaining a high fidelity connection between the physical components of real-world electric grids and code objects (GNodes) representing them.\n\nThe goal of GNodeFactory is to support transactive devices, especially transactive loads, in taking on the mantle of balancing the electric grid in a renewable future. This requires establishing a link of trust between the the physical reality of a transactive device, and the GNode acting as its online representation. The GNodeFactory does this by issuing NFTs that certify the gps location, metering, and device type of the transactive device prior to activating the corresponding GNode.\n\nThis link of trust allows us to [redefine demand response](docs/wiki/redefining-demand-response.md).\n\nGNodes come in several flavors (see [this enum](src/gnf/enums/core_g_node_role.py)), and the first flavor to understand is a [TerminalAsset](docs/wiki/terminal-asset.md).\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/thegridelectric/g-node-factory/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/thegridelectric/g-node-factory/blob/main/LICENSE\n[contributor guide]: https://github.com/thegridelectric/g-node-factory/blob/main/CONTRIBUTING.md\n[command-line reference]: https://g-node-factory.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jessica Millar',
    'author_email': 'jmillar@gridworks-consulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thegridelectric/g-node-factory',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
