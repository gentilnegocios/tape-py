#!/usr/bin/env python
"""
Unit tests for pytape.resources.Record (via pytape.client.Client). Works
by mocking httplib2, and making assertions about how pytape calls
it.
"""

import json

from mock import Mock
from nose.tools import eq_

from tests.utils import check_client_method, get_client_and_http, URL_BASE


def test_find():
    record_id = 9590591

    client, check_assertions = check_client_method()
    result = client.Record.find(record_id)
    check_assertions(result, 'GET', '/v1/record/%s' % record_id)
