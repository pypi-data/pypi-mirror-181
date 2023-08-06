# flask-github-signature

[![Python package](https://github.com/pabluk/flask-github-signature/actions/workflows/python-package.yml/badge.svg)](https://github.com/pabluk/flask-github-signature/actions/workflows/python-package.yml)
[![PyPI](https://img.shields.io/pypi/v/flask-github-signature)](https://pypi.org/project/flask-github-signature/)


A Flask view decorator to verify [Github's webhook signatures](https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks).

# Installation

## Using pip

To get the latest version from pypi.org:

```console
pip install flask-github-signature
```

# Usage

```console
export GH_WEBHOOK_SECRET="xyz"
```

```python
# app.py
from flask import Flask
from flask_github_signature import verify_signature

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
@verify_signature
def webhook():
    return "Payload signature verified."
```

run the previous Flask app with:

```console
flask run
```

and test it with:

```console
curl --request POST \
  --header "X-Hub-Signature-256: sha256=eba50596a17c2c8fbdbc5c68223422fe41d5310bea51ffdc461430bce0386c54" \
  --header "Content-Type: application/json" \
  --data '{}' \
  http://localhost:5000/webhook
```

## Signing a test payload

If you want to test with another payload you can generate a signature using:
```python
>>> import os
>>> from flask_github_signature import compute_signature
>>> 
>>> secret = os.environ["GH_WEBHOOK_SECRET"]
>>> compute_signature(secret, b'{"message": "An example"}')
'04886433fda851ca66181cecbd9c283ba677468ba361b0a0a7ba57a867102b46'
>>> 
```
when using a signature on a header don't forget to append `sha256=` to it.

# Testing

If you want to test, play or contribute to this repo:

```console
git clone git@github.com:pabluk/flask-github-signature.git
cd flask-github-signature/
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -v
```

```console
black --line-length=127 tests/ flask_github_signature/
```
