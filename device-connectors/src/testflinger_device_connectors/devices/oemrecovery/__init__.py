# Copyright (C) 2018-2023 Canonical
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

"""Ubuntu OEM Recovery provisioner support code."""

import logging

from testflinger_device_connectors.devices import (
    DefaultDevice,
    RecoveryError,
    catch,
)
from testflinger_device_connectors.devices.oemrecovery.oemrecovery import (
    OemRecovery,
)

logger = logging.getLogger(__name__)


class DeviceConnector(DefaultDevice):
    """Tool for provisioning baremetal with a given image."""

    @catch(RecoveryError, 46)
    def provision(self, args):
        """Method called when the command is invoked."""
        device = OemRecovery(args.config, args.job_data)
        logger.info("BEGIN provision")
        logger.info("Provisioning device")
        device.provision()
        logger.info("END provision")
