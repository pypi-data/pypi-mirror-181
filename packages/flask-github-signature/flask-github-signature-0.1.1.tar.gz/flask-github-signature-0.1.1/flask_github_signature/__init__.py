"""
A Flask view decorator to verify Github's webhook signatures.

For more details see https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks
"""

import os
import hmac
import logging
from functools import wraps
from flask import request

logger = logging.getLogger(__name__)


def compute_signature(secret, payload):
    """Returns hmac's hexdigest using SHA256"""
    computed = hmac.new(secret.encode("utf-8"), payload, "SHA256")
    return computed.hexdigest()


def get_github_signature(req):
    """Extracts Github's payload signature from request's headers."""
    gh_signature_header = req.headers.get("X-Hub-Signature-256", "")
    if gh_signature_header and gh_signature_header.startswith("sha256="):
        return gh_signature_header.replace("sha256=", "")
    else:
        return None


def signature_is_valid(a, b):
    """Compares 2 signature hashes."""
    return hmac.compare_digest(a, b)


def verify_signature(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        gh_webhook_secret = os.environ.get("GH_WEBHOOK_SECRET")
        if not gh_webhook_secret:
            raise ValueError("No GH_WEBHOOK_SECRET configured.")
        if request.method != "POST":
            msg = "Signature verification is only supported on POST method!"
            logger.error(msg)
            return msg, 400
        if "X-Hub-Signature-256" not in request.headers:
            msg = "Missing signature header!"
            logger.error(msg)
            return msg, 400
        signature_gh = get_github_signature(request)
        if signature_gh is not None:
            payload = request.get_data()
            signature = compute_signature(gh_webhook_secret, payload)
            if signature_is_valid(signature, signature_gh):
                return f(*args, **kwargs)
            else:
                msg = f"Signature don't match: {signature} != {signature_gh}"
                logger.error(msg)
                return msg, 400
        else:
            msg = "Signature content isn't valid!"
            logger.error(msg)
            return msg, 400

    return decorated_function
