![tests](https://github.com/alvarojimenez95/orchestrator-py/actions/workflows/tests.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/django)

# Python-Orchestrator

A library build to handle the [Orchestrator API](https://docs.uipath.com/orchestrator/reference/api-references).

This is a work in progress.

## Quick Start

---

To initialize the class provide an instance of the `Orchestrator` object with the following credentials:

- `client_id`: your client id.
- `refresh_token`: a refresh token.
- `tenant_name`: your account logical name.

```py
from orchestrator import Orchestrator

client = Orchestrator()
```

In order to authenticate, you need to call one of the three authentication methods allowed:

- `from_oauth_credentials`:

  ```py
  from orchestrator import Orchestrator

  client = Orchestrator().from_oauth_credentials(
          client_id = "CLIENT_ID",
          refresh_token = "REFRESH_TOKEN",
          tenant_name = "TENANT_NAME",
          organization = "ORGANIZATION")
  ```

- `from_custom_credentials`

  ```py
  from orchestrator import Orchestrator

  client = Orchestrator().from_custom_credentials(
          client_id = "CLIENT_ID",
          refresh_token = "REFRESH_TOKEN",
          tenant_name = "TENANT_NAME",
          organization = "ORGANIZATION"
        )
  ```

  The authentication type (_cloud_, _custom_) together with the necessary parameters can be passed directly to the Orchestrator instance as well:

  ```py
  from orchestrator import Orchestrator

  client = Orchestrator(
        auth = "cloud",
        client_id = "CLIENT_ID",
        refresh_token = "REFRESH_TOKEN",
        tenant_name = "TENANT_NAME",
        organization = "ORGANIZATION"
    )

  ```

From an Orchestrator client, we can access different information about the folder, the queues, the assets of your cloud account. The following methods return properties of the folders of your Orchestrator account:

```py
folders = client.get_folders() # returns all folders
folder = client.get_folder(1263510) # returns a single folder by id
```

From a folder, one can access several entities that belong to
a given folder in the Orchestrator cloud, such as queues, assets or process schedules:

```py
# returns a single queue by id
queue = folder.get_queue(12456)
```
