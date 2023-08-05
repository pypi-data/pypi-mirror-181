# MCLI (MosaicML Command Line Interface)

## Understanding MCLI

MCLI is a command line interface for the Mosaic Cloud.

To understand MCLI use cases, read the [customer-facing docs](https://mcli.docs.mosaicml.com/) and go through installation and tutorials.

There is also documentation specific to [internal use cases](https://internal.mcli.docs.mosaicml.com).

## Development environment setup

### Pre-requisites

**Git**

We’re using git and GitHub for source control. In case your dev box does not have git installed, [this is a good resource on installing git](https://github.com/git-guides/install-git#install-git) (and it has [even more resources](https://github.com/git-guides/) to help get started with git concepts and commands).

**Python**

MCLI is developed with Python3. To install Python, start [here](https://www.python.org/downloads/).

### Setup steps

**Clone repository**

Clone the repo from GitHub and cd into the newly created project dir

```bash
$ git clone git@github.com:mosaicml/mosaicml-cli.git
$ cd mosaicml-cli
```

**Create a virtual environment**

Run this command from the project root:

```bash
$ python -m venv venv
```

Note that the virtual environment files will be stored in a folder named "venv" under the current directory, and this folder is ignored by git via .gitignore

**Activate your new virtual environment**

```bash
$ source venv/bin/activate
```

You will now see your terminal prompt being updated to start with the virtual environment name in parenthesis: "(venv)". This is how you know you are working in an activated virtual environment!

**Update pip to the latest version**

```bash
$ pip install --upgrade pip
```

**Install mcli dependencies (including dev dependencies)**

Here we're using the -e flag to indicate this module is "editable", meaning changes to the source directory will immediately affect the installed package without requiring to re-install.

```bash
$ pip install -e ".[all]"
```

**Give `mcli` a quick test**

Check you have local mcli installed by running the commend below, and ensuring you get the same version as in the file [`mcli/version.py`](https://github.com/mosaicml/mosaicml-cli/blob/dev/mcli/version.py)

```bash
$ mcli version
```

**Run `mcli` tests**

Run tests to make sure setup in in order. All tests should either pass or configured to be ignored.

```bash
# Runs all unit tests
$ pytest

# Runs all integration tests
$ pytest --integration
```

**And… you are done!**

A few notes for later on:

- To exit the virtual environment later on: `$ deactivate`
- To get back into your virtual environment: `$ source venv/bin/activate`

## Running against mcloud as a developer

There are currently 4 MCLI Modes. To use a mode other than the default `PROD`, set your local environment variable `MCLI_MODE` or specify the mode when you run MCLI commands (e.g. `MCLI_MODE=DEV mcli get runs`)

| Mode       | Used By         | MAPI Endpoint                        | Use cases                                              | API Key                                                    |
| ---------- | --------------- | ------------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------- |
| `PROD`     | Default         | N/A                                  | Demos, simulating customer behavior, integration tests | N/A                                                        |
| `INTERNAL` | Internal users  | https://api.mosaicml.com/graphql     | Internal/alpha features in a prod-like environment     | Create one [here](https://cloud.mosaicml.com/account#)     |
| `DEV`      | Developers only | https://dev.api.mosaicml.com/graphql | Test against dev branch of mcloud                      | Create one [here](https://dev.cloud.mosaicml.com/account#) |
| `LOCAL`    | Developers only | http://localhost:3001/graphql        | Test local mcloud changes                              | test.mosaicml-secret-testing-api-key                       |

Note for each, you need to set an api key to talk to MAPI:

```bash
mcli set api-key <value>
```

**Running in `LOCAL` mode**
For local mode, you'll need to spin up the following services manually. You'll need 4 different terminal shells:

1. Postgres database (http://localhost:5432), local aws (http://localhost:4566), and MAPI graphql (http://localhost:3001/graphql)

```bash
# Inside mcloud/mapi
yarn dev:localstack
yarn dev:db
yarn dev:gql
```

2. Worker init container, logging agent, orchestration redis & minio, orchestrator

```bash
# Inside mcloud
make build
make db-dev
make orch-dev
```

3. Worker

```bash
# Inside mcloud
make worker-dev
```
If you have a kube config that you want to use that is not in the default kube config location, set the `KUBERNETES_CONFIG_PATH` environment variable to the path of your specified kube config.

4. Logger (http://localhost:50053)

```bash
# Inside mcloud
make mlog-dev
```

Refer to the [MAPI](https://github.com/mosaicml/mcloud/tree/dev/mapi) and [main mcloud](https://github.com/mosaicml/mcloud) documentation for more information.
