#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlparse, urljoin, parse_qsl


def parse_url(url):
    parsed_url = urlparse(url)  # http://url.com/page.php?id=1&foo=bar
    base_url = urljoin(
        '%s://%s' % (parsed_url.scheme, parsed_url.netloc), parsed_url.path
    )  # http://url.com/page.php
    url_params = parse_qsl(parsed_url.query)  # [('id', '1'), ('foo', 'bar')]
    return base_url, url_params


def encode_url(base_url, params, target_param, injection):
    req_params = []
    for param, value in params:
        if param == target_param:
            payload = value + injection  # 1'
            new_param = (param, payload)  # ('id', "1'")
            req_params.append(new_param)
        else:  # parametre non testé, ajout tel quel
            new_param = (param, value)  # ('id', '1')
            req_params.append(new_param)
    encoded_params = urlencode(req_params)  # id=1%27&foo=bar
    test_url = base_url + '?' + encoded_params  # http://url.com/page.php?id=1%27&foo=bar
    return test_url, payload

if len(sys.argv) != 3:
    print "USAGE: %s URL TARGET_PARAMETER" % sys.argv[0]
    sys.exit(1)

_, url, target_param = sys.argv
sql_errors = {
    'MySQL': 'error in your SQL syntax',
    'Oracle': 'ORA-01756',
    'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
    'MSSQL_Uqm': 'Unclosed quotation mark',
    'MS-Access_ODBC': 'ODBC Microsoft Access Driver'
}
base_url, url_params = parse_url(url)
print "Testing %s (tested param: %s)" % (url, target_param)
for injection in ["'", '"', "')", '")']:
    test_url, payload = encode_url(base_url, url_params, target_param, injection)
    html = urlopen(test_url).read()
    for dbms in sql_errors:
        if sql_errors[dbms] in html:
            print "Potential %s SQL injection detected!" % dbms
            print " - Payload: %s" % payload
