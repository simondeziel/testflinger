# Copyright (C) 2017-2023 Canonical
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Noprovision support code."""

import logging

import yaml
from testflinger_device_connectors.devices import (
    DefaultDevice,
    RecoveryError,
    catch,
)

import testflinger_device_connectors
from testflinger_device_connectors import logmsg
from testflinger_device_connectors.devices.noprovision.noprovision import (
    Noprovision,
)


class DeviceConnector(DefaultDevice):
    @catch(RecoveryError, 46)
    def provision(self, args):
        with open(args.config) as configfile:
            config = yaml.safe_load(configfile)
        testflinger_device_connectors.configure_logging(config)
        device = Noprovision(args.config)
        test_username = testflinger_device_connectors.get_test_username(
            args.job_data
        )
        logmsg(logging.INFO, "BEGIN provision")
        device.ensure_test_image(test_username)
        logmsg(logging.INFO, "END provision")
