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

from os_brick.initiator import connector
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF
logging.register_options(CONF)


global_opts = [
    cfg.StrOpt('rootwrap_config',
               default='/etc/cinderagent/rootwrap.conf',
               help='Path to the rootwrap configuration file to use for '
                    'running commands as root'),
]

CONF.register_opts(global_opts)


def get_root_helper():
    # TODO (e0ne): uncomment and delete debug code
    return 'sudo cinderagent-rootwrap %s' % CONF.rootwrap_config
    # TODO (e0ne): remove it!
    # return 'sudo'


def brick_get_connector(protocol, driver=None,
                        execute=processutils.execute,
                        use_multipath=False,
                        device_scan_attempts=3,
                        *args, **kwargs):
    """Wrapper to get a brick connector object.
    This automatically populates the required protocol as well
    as the root_helper needed to execute commands.
    """

    root_helper = get_root_helper()
    return connector.InitiatorConnector.factory(protocol, root_helper,
                                                driver=driver,
                                                execute=execute,
                                                use_multipath=use_multipath,
                                                device_scan_attempts=
                                                device_scan_attempts,
                                                *args, **kwargs)
