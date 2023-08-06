# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csp', 'csp.management', 'csp.management.commands', 'csp.migrations']

package_data = \
{'': ['*'], 'csp': ['fixtures/*', 'templates/csp/*']}

install_requires = \
['django>=3.2,<5.0', 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'django-csp-plus',
    'version': '0.9.0',
    'description': 'CSP tracking and violation report endpoint.',
    'long_description': '# Django CSP Plus\n\nDjango app for building CSP and tracking violations.\n\nThis project is based on the excellent `django-csp` project from MDN,\nwith a couple of alterations:\n\n1. It includes a violation report tracker\n2. It stores rules in a model, so they can be edited at runtime\n\nThe `nonce` pattern has been lifted directly.\n\n## History\n\nThe original reason for forking this from the original was the desire to\nhave the violation reporting with the same Django project as the source\npages. I\'m sure there is / was an excellent reason for not doing so in\nthe original, but it\'s not explained, and Django seems like a great fit\nfor an HTTP endpoint that can parse JSON requests and store the data\nsomewhere.\n\nThe second reason was the experience we had with Sqreen - a fantastic\nsecurity app that we used from their beta launch through to their\nacquisition by Datadog. They have/had a great violation report tool that\nallowed you to see how many violations had occurred, and to\nautomatically add the valid domains to the working CSP, making CSP\ntrivial to manage (and requiring no restarts).\n\nIt felt like this is something we could add to the Django admin\nrelatively easily ("convert this violation report into a rule").\n\nThe final push was the desire to manage the rules at runtime - running a\nlarge commercial site you never quite know what the marketing team has\njust added to the site, and having to redeploy to unblock their new tool\nwas a pain.\n\nWe ended with these requirements:\n\n1. Design time base rules\n2. Runtime configurable rules\n3. Builtin violation reporting\n4. Support for nonces\n5. Ability to exclude specific requests / responses\n\n## Implementation\n\nWe have split the middleware in two - `CspNonceMiddleware`, which adds\nthe `request.csp_nonce` attribute, and `CspHeaderMiddleware`, which adds\nthe header. Most sites will want both, but you can run one without the\nother.\n\nThe baseline, static, configuration of rules is a dict in `settings.py`.\nThis can then be enriched with dynamic rules stored in the `CspRule`\nmodel.\n\nYou can add two special placeholders in the rules: `{nonce}` and\n`{report-uri}`; if present these will be replaced with the current\n`request.csp_nonce` and the local violation report URL on each request.\nThe CSP is cached for all requests with the placeholder text in (so it\'s\nthe same for all users / requests).\n\n## Settings\n\n### `CSP_ENABLED`\n\n`bool`, default = `False`\n\nKill switch for the middleware. Defaults to `False` (disabled).\n\n### `CSP_REPORT_ONLY`\n\n`bool`, default = `True`\n\nSet to `True` to run in report-only mode. Defaults to `True`.\n\n### `CSP_REPORT_SAMPLING`\n\n`float`, default = `1.0`\n\nFloat (0.0-1.0) - used as a percentage of responses on which to include\nthe `report-uri` directive. This can be used to turn down the noise -\nonce you have a stable CSP there is no point having every single request\ninclude the reporting directive - you need a trickle not a flood.\n\n### `CSP_REPORT_THROTTLING`\n\n`float`, default = `0.0`\n\nFloat (0.0-1.0) - used as a percentage of reporting violation requests\nto throttle (throw away). This is used to control potentially malicious\nviolation reporting. The reporting endpoint is public, and accepts JSON\npayloads, so is open to abuse (sending very large, or malformed JSON)\nand is a potential DOS vulnerability. If you set this value to 1.0 then\nall inbound reporting requests are thrown away without processing. Use\nin extremis.\n\n### `CSP_CACHE_TIMEOUT`\n\n`int`, default = `600`\n\nThe cache timeout for the templated CSP. Defaults to 5 min (600s).\n\n### `CSP_FILTER_REQUEST_FUNC`\n\n`Callable[[HttpRequest], bool]` - defaults to returning `True` for all\nrequests\n\nA callable that takes `HttpRequest` and returns a bool - if False, the\nmiddleware will not add the response header. Defaults to return `True`\nfor all requests.\n\n### `CSP_FILTER_RESPONSE_FUNC`\n\n`Callable[[HttpResponse], bool]` - defaults to `True` for all\n`text/html` responses.\n\nCallable that takes `HttpResponse` and returns a bool - if `False` the\nmiddleware will not add the response header. Defaults to a function that\nfilters only responses with `Content-Type: text/html` - which results in\nstatic content / JSON responses _not_ getting the CSP header.\n\n### `CSP_DEFAULTS`\n\n`dict[str, list[str]]`\n\nThe default (baseline) CSP as a dict of `{directive: values}`. This is\nextended by the runtime rules (i.e. not overwritten). Defaults to:\n\n```python\n{\n    "default-src": ["\'none\'"],\n    "base-uri": ["\'self\'"],\n    "connect-src": ["\'self\'"],\n    "form-action": ["\'self\'"],\n    "font-src": ["\'self\'"],\n    "img-src": ["\'self\'"],\n    "script-src": ["\'self\'"],\n    "style-src": ["\'self\'"],\n    "report-uri": ["{report_uri}"],\n}\n```\n\nNote the `{report-uri}` value in the default - this is cached as-is,\nwith the local report URL injected into it at runtime.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-csp-plus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
