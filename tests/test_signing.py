from os import path

import afp

from hexbytes import HexBytes


def test_PrivateKeyAuthenticator():
    authenticator = afp.PrivateKeyAuthenticator(
        "0x93f2348b2b890be53f55344b7b118b53778440eea0dc84a6f86fb6e7f6bd77a6"
    )

    assert authenticator.address == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    assert authenticator.sign_message(b"foobar") == HexBytes(
        "0x32b31738559341bdcdd56ef3bb38dbbb9f218d3ac7b84c0118e364c1e036dc1c07d82f0bc9b2c6428966b7a2a10689ae047b8e765df3b66f5c16e90e20632b681b"
    )


def test_KeyfileAuthenticator():
    keyfile = path.join(path.dirname(__file__), "assets", "test.key")
    authenticator = afp.KeyfileAuthenticator(keyfile, "foobar")

    assert authenticator.address == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    assert authenticator.sign_message(b"foobar") == HexBytes(
        "0x32b31738559341bdcdd56ef3bb38dbbb9f218d3ac7b84c0118e364c1e036dc1c07d82f0bc9b2c6428966b7a2a10689ae047b8e765df3b66f5c16e90e20632b681b"
    )
