# -*- coding: utf-8 -*-
'''
The match module allows for match routines to be run and determine target specs
'''
from __future__ import absolute_import

# Import python libs
import inspect
import logging
import sys

# Import salt libs
import salt.minion
import salt.utils
from salt.defaults import DEFAULT_TARGET_DELIM
from salt.ext.six import string_types

__func_alias__ = {
    'list_': 'list'
}

log = logging.getLogger(__name__)


def compound(tgt, minion_id=None):
    '''
    Return True if the minion ID matches the given compound target

    minion_id
        Specify the minion ID to match against the target expression

        .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' match.compound 'L@cheese,foo and *'
    '''
    opts = {'grains': __grains__}
    if minion_id is not None:
        if not isinstance(minion_id, string_types):
            minion_id = str(minion_id)
    else:
        minion_id = __grains__['id']
    opts['id'] = minion_id
    matcher = salt.minion.Matcher(opts, __salt__)
    try:
        return matcher.compound_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def ipcidr(tgt):
    '''
    Return True if the minion matches the given ipcidr target

    CLI Example:

    .. code-block:: bash

        salt '*' match.ipcidr '192.168.44.0/24'

    delimiter
    Pillar Example:

    .. code-block:: yaml
       '172.16.0.0/12':
         - match: ipcidr
         - nodeclass: internal

    '''
    matcher = salt.minion.Matcher({'grains': __grains__}, __salt__)
    try:
        return matcher.ipcidr_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def pillar(tgt, delimiter=DEFAULT_TARGET_DELIM, delim=None):
    '''
    Return True if the minion matches the given pillar target. The
    ``delimiter`` argument can be used to specify a different delimiter.

    CLI Example:

    .. code-block:: bash

        salt '*' match.pillar 'cheese:foo'
        salt '*' match.pillar 'clone_url|https://github.com/saltstack/salt.git' delimiter='|'

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 2014.7.0

    delim
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 0.16.4
        .. deprecated:: 2014.7.0
    '''
    if delim is not None:
        salt.utils.warn_until(
            'Beryllium',
            'The \'delim\' argument to match.pillar has been deprecated and '
            'will be removed in a future release. Please use \'delimiter\' '
            'instead.'
        )
        delimiter = delim

    matcher = salt.minion.Matcher({'pillar': __pillar__}, __salt__)
    try:
        return matcher.pillar_match(tgt, delimiter=delimiter)
    except Exception as exc:
        log.exception(exc)
        return False


def data(tgt):
    '''
    Return True if the minion matches the given data target

    CLI Example:

    .. code-block:: bash

        salt '*' match.data 'spam:eggs'
    '''
    matcher = salt.minion.Matcher(__opts__, __salt__)
    try:
        return matcher.data_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def grain_pcre(tgt, delimiter=DEFAULT_TARGET_DELIM, delim=None):
    '''
    Return True if the minion matches the given grain_pcre target. The
    ``delimiter`` argument can be used to specify a different delimiter.

    CLI Example:

    .. code-block:: bash

        salt '*' match.grain_pcre 'os:Fedo.*'
        salt '*' match.grain_pcre 'ipv6|2001:.*' delimiter='|'

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 2014.7.0

    delim
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 0.16.4
        .. deprecated:: 2014.7.0
    '''
    if delim is not None:
        salt.utils.warn_until(
            'Beryllium',
            'The \'delim\' argument to match.grain_pcre has been deprecated '
            'and will be removed in a future release. Please use '
            '\'delimiter\' instead.'
        )
        delimiter = delim

    matcher = salt.minion.Matcher({'grains': __grains__}, __salt__)
    try:
        return matcher.grain_pcre_match(tgt, delimiter=delimiter)
    except Exception as exc:
        log.exception(exc)
        return False


def grain(tgt, delimiter=DEFAULT_TARGET_DELIM, delim=None):
    '''
    Return True if the minion matches the given grain target. The ``delimiter``
    argument can be used to specify a different delimiter.

    CLI Example:

    .. code-block:: bash

        salt '*' match.grain 'os:Ubuntu'
        salt '*' match.grain 'ipv6|2001:db8::ff00:42:8329' delimiter='|'

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 2014.7.0

    delim
        Specify an alternate delimiter to use when traversing a nested dict

        .. versionadded:: 0.16.4
        .. deprecated:: 2014.7.0
    '''
    if delim is not None:
        salt.utils.warn_until(
            'Beryllium',
            'The \'delim\' argument to match.grain has been deprecated and '
            'will be removed in a future release. Please use \'delimiter\' '
            'instead.'
        )
        delimiter = delim

    matcher = salt.minion.Matcher({'grains': __grains__}, __salt__)
    try:
        return matcher.grain_match(tgt, delimiter=delimiter)
    except Exception as exc:
        log.exception(exc)
        return False


def list_(tgt, minion_id=None):
    '''
    Return True if the minion ID matches the given list target

    minion_id
        Specify the minion ID to match against the target expression

        .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' match.list 'server1,server2'
    '''
    if minion_id is not None:
        if not isinstance(minion_id, string_types):
            minion_id = str(minion_id)
    else:
        minion_id = __grains__['id']
    matcher = salt.minion.Matcher({'id': minion_id}, __salt__)
    try:
        return matcher.list_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def pcre(tgt, minion_id=None):
    '''
    Return True if the minion ID matches the given pcre target

    minion_id
        Specify the minion ID to match against the target expression

        .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' match.pcre '.*'
    '''
    if minion_id is not None:
        if not isinstance(minion_id, string_types):
            minion_id = str(minion_id)
    else:
        minion_id = __grains__['id']
    matcher = salt.minion.Matcher({'id': minion_id}, __salt__)
    try:
        return matcher.pcre_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def glob(tgt, minion_id=None):
    '''
    Return True if the minion ID matches the given glob target

    minion_id
        Specify the minion ID to match against the target expression

        .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' match.glob '*'
    '''
    if minion_id is not None:
        if not isinstance(minion_id, string_types):
            minion_id = str(minion_id)
    else:
        minion_id = __grains__['id']
    matcher = salt.minion.Matcher({'id': minion_id}, __salt__)
    try:
        return matcher.glob_match(tgt)
    except Exception as exc:
        log.exception(exc)
        return False


def filter_by(lookup, expr_form='compound', minion_id=None):
    '''
    Return the first match in a dictionary of target patterns

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' match.filter_by '{foo*: Foo!, bar*: Bar!}' minion_id=bar03

    Pillar Example:

    .. code-block:: yaml

        {% set roles = salt['match.filter_by']({
            'web*': ['app', 'caching'],
            'db*': ['db'],
        }) %}
    '''
    expr_funcs = dict(inspect.getmembers(sys.modules[__name__],
        predicate=inspect.isfunction))

    for key in lookup:
        if minion_id and expr_funcs[expr_form](key, minion_id):
            return lookup[key]
        elif expr_funcs[expr_form](key, minion_id):
            return lookup[key]

    return None
