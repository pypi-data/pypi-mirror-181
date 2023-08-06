# G Node Factory

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

The GNodeFactory is an actor in a larger Transactive Energy Management (TEM) system. Within that system, it has the authority for creating and updating GNodes. Among other things, it has the authority for creating and updating `TerminalAssets`, which represent the devices capable of transacting on electricity markets within the TEM.

This repo has been developed through the generous funding of a grant provided by the [Algorand Foundation](https://www.algorand.foundation/). For more context, please read our Algorand [Milestone 1 writeup](docs/wiki/milestone-1.md) and Milestone 2 deck. For design specifications for the repo, go [here](docs/wiki/design-specifications.md). For a very short description of what GNodes are and why we need a factory for them, skip to [Background](#Background) below.

## Local Demo setup

**PREP**

1. Clone this repo

   - Using python 3.10.\* or greater, create virtual env inside this repo

     ```
     python -m venv venv
     source venv/bin/activate
     pip install -e .
     ```

2. In sister directories, clone and make virtual envs for these two repos:

   - [https://github.com/thegridelectric/gridworks-marketmaker](https://github.com/thegridelectric/gridworks-marketmaker) (MarketMaker GNode repo)
   - [https://github.com/thegridelectric/gridworks-atn-spaceheat](https://github.com/thegridelectric/gridworks-atn-spaceheat) (AtomicTNode GNode repo)

   For now, each of these needs a separate virtual env.

3. Start the Algorand sandbox in a **sibling directory**

   a. Clone [Algorand Sandbox](https://github.com/algorand/sandbox) into sibling directory

   ```
   - YourDemoFolder
     |
     -- g-node-factory
     -- sandbox
   ```

   b. Start the Algorand sandbox. From the `YourDemoFolder/sandbox` directory

   ```
   ./sandbox up dev
   ```

4. Install [docker](https://docs.docker.com/get-docker/)

**RUNNING A SIMULATION OF 4 TERMINAL ASSETS**

**Note**: if your machine is x86, substitute `docker-demo-arm.yml` for `docker-demo-x86.yml` in the instructions below. If you are not sure, try one. If rabbit fails to load try the other.

1. In a terminal for `g-node-factory`, start the dockerized APIS:

   ```
   ./1prep.sh
   ```

   - Check at:
     - [http://localhost:8001/docs](http://localhost:8001/docs) - Api for the dockerized TaValidator
     - [http://localhost:7997/get-time/](http://localhost:7997/get-time/) - Api for the dockerized TaValidator

2. In that same terminal, start the final gnf API (not in docker yet):

   ```
   ./2prep.sh
   ```

3. In a terminal for `gridworks-marketmaker`:

   ```
   python demo.py
   ```

   - Check that `d1.isone.ver.keene-Fxxx` shows up in [rabbitmq](http://d1-1.electricity.works:15672/#/queues) passwd/username: smqPublic

4. In a new terminal window for `g-node-factory` repo:

   ```
   python demo.py
   ```

## Testing

pytest -v

## Configuration and secrets

The repo uses dotenv and `.env` files. Look at `src/gnf/config` for default values. These are overwritten with values from a
git ignored top-level `.env` file. All dev examples are intended to run without needing to create
a `.env` file.

## Code derivation tools

The primary derivation tool used for this is [ssot.me](https://explore.ssot.me/app/#!/home), developed by EJ Alexandra of [An Abstract Level LLC](https://effortlessapi.com/pages/effortlessapi/blog). All of the xslt code in `CodeGeneration` uses this tool.

The `ssotme` cli and its upstream `ssotme` service pull data from our [private airtable](https://airtable.com/appgibWM6WZW20bBx/tblRducbzl15OWmwv/viwIvHvZcrMELIP3x?blocks=hide) down into an odxml file and a json file, and then references local `.xslt` scripts in order to derive code. The `.xslt` allows for two toggles - one where files are always overwritten, and one where the derivation tools will leave files alone once any hand-written code is added. Mostly that toggle is set to `always overwrite` since we are working with immutable schemata. Note that the `ssotme cli` requires an internet connection to work, since it needs to access the upstream `ssotme` service.

If you want to add enums or schema, you will need access to the `ssotme cli` and the airtable. Contact Jessica for this.

## Background

What are GNodes and why do we need a factory for them?

The GNodeFactory stands at the boundary between the physical world and the world of code, maintaining a high fidelity connection between the physical components of real-world electric grids and code objects (GNodes) representing them.

The goal of GNodeFactory is to support transactive devices, especially transactive loads, in taking on the mantle of balancing the electric grid in a renewable future. This requires establishing a link of trust between the the physical reality of a transactive device, and the GNode acting as its online representation. The GNodeFactory does this by issuing NFTs that certify the gps location, metering, and device type of the transactive device prior to activating the corresponding GNode.

This link of trust allows us to [redefine demand response](docs/wiki/redefining-demand-response.md).

GNodes come in several flavors (see [this enum](src/gnf/enums/core_g_node_role.py)), and the first flavor to understand is a [TerminalAsset](docs/wiki/terminal-asset.md).

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/g-node-factory/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/g-node-factory/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/g-node-factory/blob/main/CONTRIBUTING.md
[command-line reference]: https://g-node-factory.readthedocs.io/en/latest/usage.html
