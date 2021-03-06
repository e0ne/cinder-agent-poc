# Copyright 2015 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import functools

from keystonemiddleware import auth_token
from oslo_config import cfg
from oslo_policy import policy

from cinderagent import context
from cinderagent import exceptions

ENFORCER = None


def setup_policy():
    global ENFORCER

    ENFORCER = policy.Enforcer(cfg.CONF)


def enforce(rule):
    def decorator(func):
        @functools.wraps(func)
        def handler(*args, **kwargs):
            ctx = context.ctx()
            ENFORCER.enforce(rule, {}, ctx.to_dict(), do_raise=True,
                             exc=exceptions.Forbidden)

            return func(*args, **kwargs)
        return handler

    return decorator


def wrap(app):
    """Wrap wsgi application with ACL check."""
    return auth_token.AuthProtocol(app, {})
