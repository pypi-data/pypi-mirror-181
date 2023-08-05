# shelly-cloud

A python library to access the Shelly cloud API. Refer also to the [Shelly API Docs](https://shelly-api-docs.shelly.cloud/cloud-control-api/communication). This repo provides functionality for:

- Getting devices status
- Getting the status of a single device
- Getting a list of device IDs

## Installing the library locally

Python 3 is recommended for this project.

```bash
python -m pip install -e .
```

> **This is needed for the first time when working with the library/examples/tests.**

## Example usage

```bash
SHELLY_API_URL="https://HOST:PORT" SHELLY_API_TOKEN="REPLACE_ME" python3 examples/simple.py
```

or

```python
from shellyapi.shellyapi import ShellyApi

shelly = ShellyApi('provide_api_url', 'provide_api_token')
# or you can define additional optional parameters
# shelly = ShellyApi('provide_api_url', 'provide_api_token', timeout=10)

print(shelly.get_device_ids())
```

## Development

### Installing required pip packages

```bash
python pip install -r requirenments.txt
pre-commit install -t pre-push
```

### Linting

```bash
pylint shellyapi/*.py tests/*.py examples/*.py
```

### Unit testing

```bash
pytest tests/*.py

# show logs
pytest -o log_cli=true

# code coverage
pytest --durations=10 --cov-report term-missing --cov=shellyapi tests
```
