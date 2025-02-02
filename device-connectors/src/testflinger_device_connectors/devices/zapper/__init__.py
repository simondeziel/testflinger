# Copyright (C) 2024 Canonical
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

"""
Package containing modules for implementing Zapper-driven device connectors.

Modules inheriting from the provided abstract class will run Zapper-driven
provisioning procedures via Zapper API. The provisioning logic is implemented
in the Zapper codebase and the connector serves as a pre-processing step,
validating the configuration and preparing the API arguments.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

import rpyc
import yaml

import testflinger_device_connectors
from testflinger_device_connectors.devices import (
    DefaultDevice,
    RecoveryError,
    catch,
)

logger = logging.getLogger(__name__)


class ZapperConnector(ABC, DefaultDevice):
    """
    Abstract base class defining a common interface for Zapper-driven
    device connectors.
    """

    PROVISION_METHOD = ""  # to be defined in the implementation
    ZAPPER_REQUEST_TIMEOUT = 60 * 90
    ZAPPER_SERVICE_PORT = 60000

    @catch(RecoveryError, 46)
    def provision(self, args):
        """Method called when the command is invoked."""
        with open(args.config) as configfile:
            config = yaml.safe_load(configfile)
        testflinger_device_connectors.configure_logging(config)

        (api_args, api_kwargs) = self._validate_configuration(
            args.config, args.job_data
        )

        logger.info("BEGIN provision")
        logger.info("Provisioning device")

        self._run(args.config["controller_host"], *api_args, **api_kwargs)

        logger.info("END provision")

    @abstractmethod
    def _validate_configuration(
        self, config, job_data
    ) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        """
        Validate the job config and data and prepare the arguments
        for the Zapper `provision` API.
        """
        raise NotImplementedError

    def _run(self, zapper_ip, *args, **kwargs):
        """
        Run the Zapper `provision` API via RPyC. The arguments are
        not stricly defined so that the same API can be used by different
        implementations.

        The connector logger is passed as an argument to the Zapper API
        in order to get a real time feedback throughout the whole execution.
        """

        connection = rpyc.connect(
            zapper_ip,
            self.ZAPPER_SERVICE_PORT,
            config={
                "allow_public_attrs": True,
                "sync_request_timeout": self.ZAPPER_REQUEST_TIMEOUT,
            },
        )

        connection.root.provision(
            self.PROVISION_METHOD,
            *args,
            logger=logger,
            **kwargs,
        )
