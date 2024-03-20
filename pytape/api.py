# -*- coding: utf-8 -*-
from . import transport, client


def build_headers(authorization_headers, user_agent):
    headers = transport.KeepAliveHeaders(authorization_headers)
    if user_agent is not None:
        headers = transport.UserAgentHeaders(headers, user_agent)
    return headers


def BearerClient(user_key, user_agent=None, domain="https://api.tapeapp.com"):
    auth = transport.BearerAuthorization(user_key)
    return AuthorizingClient(domain, auth, user_agent=user_agent)


def AuthorizingClient(domain, auth, user_agent=None):
    """Creates a Tape client using an auth object."""
    http_transport = transport.HttpTransport(domain, build_headers(auth, user_agent))
    return client.Client(http_transport)
