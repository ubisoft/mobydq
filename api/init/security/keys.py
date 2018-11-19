from jwt import jwk_from_pem


def get_public_key():
    """Gets the public key from the docker secrets file"""
    with open('/run/secrets/public_key', 'rb') as fh:
        return jwk_from_pem(fh.read())


def get_private_key():
    """Gets the private key from the docker secrets file"""
    with open('/run/secrets/private_key', 'rb') as fh:
        return jwk_from_pem(fh.read())
