import base64
from itertools import takewhile
import json
import re

from .utils import gnupg

UID_EMAIL_PROG = re.compile(r".*<([^@>]+@[^>]+)>.*")

KEY_HEADER = "-----BEGIN PGP PUBLIC KEY BLOCK-----"
KEY_FOOTER = "-----END PGP PUBLIC KEY BLOCK-----"
MSG_HEADER = "-----BEGIN PGP SIGNED MESSAGE-----"
SIG_HEADER = "-----BEGIN PGP SIGNATURE-----"
SIG_FOOTER = "-----END PGP SIGNATURE-----"
HASH_PROG = re.compile(r"Hash: (.+)")


def resolve_email(email: str) -> str:
    if not email:
        with gnupg() as gpg:
            private_keys = gpg.list_keys(True)
            if private_keys and private_keys[0]["uids"]:
                for uid in private_keys[0]["uids"]:
                    m = UID_EMAIL_PROG.match(uid)
                    if not m or not m.group(1):
                        continue
                    return m.group(1)
    return email


def resolve_fingerprint(email):
    with gnupg() as gpg:
        for key in gpg.list_keys():
            for uid in key["uids"]:
                m = UID_EMAIL_PROG.match(uid)
                if not m:
                    continue
                if m.group(1) and m.group(1) == email:
                    return key["fingerprint"], email
    raise Exception("No public key found")


def resolve_public_key(email):
    with gnupg() as gpg:
        for key in gpg.list_keys():
            for uid in key["uids"]:
                m = UID_EMAIL_PROG.match(uid)
                if not m:
                    continue
                if m.group(1) and m.group(1) == email:
                    return gpg.export_keys(key["fingerprint"]), email
    raise Exception("No public key found")


def resolve_public_key_by_fingerprint(fingerprint):
    with gnupg() as gpg:
        for key in gpg.list_keys():
            if key["fingerprint"] == fingerprint:
                return gpg.export_keys(key["fingerprint"])
    raise Exception("No public key found")


def sign_value(email, value):
    with gnupg() as gpg:
        for key in gpg.list_keys():
            for uid in key["uids"]:
                m = UID_EMAIL_PROG.match(uid)
                if not m:
                    continue
                if m.group(1) and m.group(1) == email:
                    return str(gpg.sign(value, keyid=key["fingerprint"]))
    raise Exception("No public key found")


def parse_signed_value(signed_value):
    lines_iter = iter(signed_value.splitlines())
    assert next(lines_iter) == MSG_HEADER
    m = HASH_PROG.match(next(lines_iter))
    assert m is not None
    hash = m.group(1)
    assert not next(lines_iter)
    payload = "".join(takewhile(lambda x: x != SIG_HEADER, lines_iter))
    assert not next(lines_iter)
    signature = "".join(takewhile(lambda x: x != SIG_FOOTER, lines_iter))
    return {
        "header": {
            "hash": hash,
        },
        "payload": payload,
        "signature": signature,
    }


def build_token(email: str) -> str:
    fingerprint, email = resolve_fingerprint(resolve_email(email))
    payload = {"email": email, "fingerprint": fingerprint}
    payload_str = json.dumps(payload)
    signed_value = sign_value(email, payload_str)
    parsed = parse_signed_value(signed_value)
    header_token = base64.urlsafe_b64encode(json.dumps(parsed["header"]).encode()).decode()
    payload_token = base64.urlsafe_b64encode(payload_str.encode()).decode()
    signature_token = base64.urlsafe_b64encode(parsed["signature"].encode()).decode()
    return ".".join((header_token, payload_token, signature_token))
