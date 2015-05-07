# Copyright 2013 OpenStack Foundation.
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

import sys

import flask
from oslo_config import cfg
from oslo_log import log as logging

from cinderagent import api
# from cinderagent import policy

CONF = cfg.CONF
CONF(sys.argv[1:], project='cinderagent', version='1.0')

logging.setup(CONF, 'cinderagent')
app = flask.Flask(__name__)
app.register_blueprint(api.cinder_agent_api)

# NOTE(e0ne): uncomment it to enable keystone authentication
# app.wsgi_app = policy.wrap(app.wsgi_app)

if __name__ == '__main__':
    app.debug = CONF.debug
    app.run(host='0.0.0.0')
