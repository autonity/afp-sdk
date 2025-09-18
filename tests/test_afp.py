from os import path

import pytest

import afp
from afp.constants import defaults
from afp.exceptions import ConfigurationError


def test_AFP_constructor__creates_KeyFileAuthenticator_from_defaults(
    monkeypatch,
):
    keyfile = path.join(path.dirname(__file__), "assets", "test.key")
    monkeypatch.setattr(defaults, "KEYFILE", keyfile)
    monkeypatch.setattr(defaults, "KEYFILE_PASSWORD", "foobar")

    app = afp.AFP()
    assert isinstance(app.config.authenticator, afp.KeyfileAuthenticator)
    assert (
        app.config.authenticator.address == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    )


def test_AFP_constructor__creates_PrivateKeyAuthenticator_from_defaults(
    monkeypatch,
):
    private_key = "0x93f2348b2b890be53f55344b7b118b53778440eea0dc84a6f86fb6e7f6bd77a6"
    monkeypatch.setattr(defaults, "PRIVATE_KEY", private_key)

    app = afp.AFP()
    assert isinstance(app.config.authenticator, afp.PrivateKeyAuthenticator)
    assert (
        app.config.authenticator.address == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    )


def test_AFP_constructor__raises_error_for_ambiguous_defaults(monkeypatch):
    monkeypatch.setattr(defaults, "KEYFILE", "baz")
    monkeypatch.setattr(defaults, "PRIVATE_KEY", "0x")

    with pytest.raises(ConfigurationError):
        afp.AFP()
