from jwt import (
    jwk_from_dict,
    jwk_from_pem
)


def get_public_key():
    with open('/run/secrets/public_key', 'rb') as fh:
        return jwk_from_dict(fh.read())


def get_private_key():
    with open('/run/secrets/private_key', 'rb') as fh:
        return jwk_from_pem(fh.read())
