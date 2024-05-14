# Copyright (c) 2024 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=line-too-long
from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = "Allen Robel"

import inspect
import logging

from ansible_collections.cisco.dcnm.plugins.module_utils.common.api.v1.lan_fabric import \
    LanFabric
from ansible_collections.cisco.dcnm.plugins.module_utils.fabric.fabric_types import \
    FabricTypes


class Fabrics(LanFabric):
    """
    ## V1 API Fabrics - LanFabric().Fabrics()

    ### Description
    Common methods and properties for Fabrics() subclasses.

    ### Path
    -   ``/lan-fabric/rest/control/fabrics/{fabric_name}``
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.fabric_types = FabricTypes()
        self.rest_control_fabrics = f"{self.lan_fabric}/rest/control/fabrics"
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)
        self._build_properties()

    def _build_properties(self):
        """
        - Set the fabric_name property.
        """
        self.properties["fabric_name"] = None
        self.properties["template_name"] = None

    @property
    def fabric_name(self):
        """
        - getter: Return the fabric_name.
        - setter: Set the fabric_name.
        - setter: Raise ``ValueError`` if fabric_name is not valid.
        """
        return self.properties["fabric_name"]

    @fabric_name.setter
    def fabric_name(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.conversion.validate_fabric_name(value)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{error}"
            raise ValueError(msg) from error
        self.properties["fabric_name"] = value

    @property
    def path_fabric_name(self):
        """
        -   Endpoint path property, including fabric_name.
        -   Raise ``ValueError`` if fabric_name is not set and
            ``self.required_properties`` contains "fabric_name".
        """
        method_name = inspect.stack()[0][3]
        if self.fabric_name is None and "fabric_name" in self.required_properties:
            msg = f"{self.class_name}.{method_name}: "
            msg += "fabric_name must be set prior to accessing path."
            raise ValueError(msg)
        return f"{self.rest_control_fabrics}/{self.fabric_name}"

    @property
    def path_fabric_name_template_name(self):
        """
        -   Endpoint path property, including fabric_name and template_name.
        -   Raise ``ValueError`` if fabric_name is not set and
            ``self.required_properties`` contains "fabric_name".
        -   Raise ``ValueError`` if template_name is not set and
            ``self.required_properties`` contains "template_name".
        """
        method_name = inspect.stack()[0][3]
        if self.fabric_name is None and "fabric_name" in self.required_properties:
            msg = f"{self.class_name}.{method_name}: "
            msg += "fabric_name must be set prior to accessing path."
            raise ValueError(msg)
        if self.template_name is None and "template_name" in self.required_properties:
            msg = f"{self.class_name}.{method_name}: "
            msg += "template_name must be set prior to accessing path."
            raise ValueError(msg)
        return f"{self.rest_control_fabrics}/{self.fabric_name}/{self.template_name}"

    @property
    def template_name(self):
        """
        - getter: Return the template_name.
        - setter: Set the template_name.
        - setter: Raise ``ValueError`` if template_name is not a string.
        """
        return self.properties["template_name"]

    @template_name.setter
    def template_name(self, value):
        method_name = inspect.stack()[0][3]
        if value not in self.fabric_types.valid_fabric_template_names:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Invalid template_name: {value}. "
            msg += "Expected one of: "
            msg += f"{', '.join(self.fabric_types.valid_fabric_template_names)}."
            raise ValueError(msg)
        self.properties["template_name"] = value


class EpFabricConfigDeploy(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricConfigDeploy()

    ### Description
    Return endpoint to initiate config-deploy on fabric_name.

     ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.
    -   ``ValueError``: If force_show_run is not boolean.
    -   ``ValueError``: If include_all_msd_switches is not boolean.

    ### Path
    -   ``/fabrics/{fabric_name}/config-deploy``
    -   ``/fabrics/{fabric_name}/config-deploy?forceShowRun={force_show_run}``
    -   ``/fabrics/{fabric_name}/config-deploy?inclAllMSDSwitches={include_all_msd_switches}``

    ### Verb
    -   POST

    ### Parameters
    - force_show_run: boolean
        - set the ``forceShowRun`` value
        - default: False
    - include_all_msd_switches: boolean
        - set the ``inclAllMSDSwitches`` value
        - default: False
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    fabric_config_deploy = EpFabricConfigDeploy()
    fabric_config_deploy.fabric_name = "MyFabric"
    fabric_config_deploy.force_show_run = True
    fabric_config_deploy.include_all_msd_switches = True
    path = fabric_config_deploy.path
    verb = fabric_config_deploy.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "POST"
        self.properties["force_show_run"] = False
        self.properties["include_all_msd_switches"] = False

    @property
    def force_show_run(self):
        """
        - getter: Return the force_show_run value.
        - setter: Set the force_show_run value.
        - setter: Raise ``ValueError`` if force_show_run is not a boolean.
        - Default: False
        """
        return self.properties["force_show_run"]

    @force_show_run.setter
    def force_show_run(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, bool):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Expected boolean for {method_name}. "
            msg += f"Got {value} with type {type(value).__name__}."
            raise ValueError(msg)
        self.properties["force_show_run"] = value

    @property
    def include_all_msd_switches(self):
        """
        - getter: Return the include_all_msd_switches.
        - setter: Set the include_all_msd_switches.
        - setter: Raise ``ValueError`` if include_all_msd_switches is a boolean.
        - Default: False
        """
        return self.properties["include_all_msd_switches"]

    @include_all_msd_switches.setter
    def include_all_msd_switches(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, bool):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Expected boolean for {method_name}. "
            msg += f"Got {value} with type {type(value).__name__}."
            raise ValueError(msg)
        self.properties["include_all_msd_switches"] = value

    @property
    def path(self):
        """
        - Override the path property to mandate fabric_name is set.
        - Raise ``ValueError`` if fabric_name is not set.
        """
        _path = self.path_fabric_name
        _path += "/config-deploy?"
        _path += f"forceShowRun={self.force_show_run}"
        _path += f"&inclAllMSDSwitches={self.include_all_msd_switches}"
        return _path


class EpFabricConfigSave(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricConfigSave()

    ### Description
    Return endpoint to initiate config-save on fabric_name.

    ### Raises
    -  ``ValueError``: If fabric_name is not set.
    -  ``ValueError``: If fabric_name is invalid.
    -  ``ValueError``: If ticket_id is not a string.

    ### Path
    -  ``/fabrics/{fabric_name}/config-save``
    -  ``/fabrics/{fabric_name}/config-save?ticketId={ticket_id}``

    ### Verb
    -   POST

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    -   ticket_id: string
            -   optional unless Change Control is enabled
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    fabric_config_save = EpFabricConfigSave()
    fabric_config_save.fabric_name = "MyFabric"
    fabric_config_save.ticket_id = "MyTicket1234"
    path = fabric_config_save.path
    verb = fabric_config_save.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "POST"
        self.properties["ticket_id"] = None

    @property
    def ticket_id(self):
        """
        - getter: Return the ticket_id.
        - setter: Set the ticket_id.
        - setter: Raise ``ValueError`` if ticket_id is not a string.
        - Default: None
        - Note: ticket_id is optional unless Change Control is enabled.
        """
        return self.properties["ticket_id"]

    @ticket_id.setter
    def ticket_id(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, str):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Expected string for {method_name}. "
            msg += f"Got {value} with type {type(value).__name__}."
            raise ValueError(msg)
        self.properties["ticket_id"] = value

    @property
    def path(self):
        """
        - Endpoint for config-save.
        - Set self.ticket_id if Change Control is enabled.
        - Raise ``ValueError`` if fabric_name is not set.
        """
        _path = self.path_fabric_name
        _path += "/config-save"
        if self.ticket_id:
            _path += f"?ticketId={self.ticket_id}"
        return _path


class EpFabricCreate(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricCreate()

    ### Description
    Return endpoint information.

    ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.
    -   ``ValueError``: If template_name is not set.
    -   ``ValueError``: If template_name is not a valid fabric template name.

    ### Path
    -   ``/rest/control/fabrics/{FABRIC_NAME}/{TEMPLATE_NAME}``

    ### Verb
    -   POST

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    - template_name: string
        - set the ``template_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    instance = EpFabricCreate()
    instance.fabric_name = "MyFabric"
    instance.template_name = "Easy_Fabric"
    path = instance.path
    verb = instance.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self.required_properties.add("template_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "POST"

    @property
    def path(self):
        """
        - Endpoint for fabric create.
        - Raise ``ValueError`` if fabric_name is not set.
        """
        return self.path_fabric_name_template_name


class EpFabricDelete(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricDelete()

    ### Description
    Return endpoint to delete ``fabric_name``.

    ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.

    ### Path
    -   ``/fabrics/{fabric_name}``

    ### Verb
    -   DELETE

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    fabric_delete = EpFabricDelete()
    fabric_delete.fabric_name = "MyFabric"
    path = fabric_delete.path
    verb = fabric_delete.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "DELETE"

    @property
    def path(self):
        """
        - Endpoint for fabric delete.
        - Raise ``ValueError`` if fabric_name is not set.
        """
        return self.path_fabric_name


class EpFabricDetails(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricDetails()

    ### Description
    Return the endpoint to query ``fabric_name`` details.

    ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.

    ### Path
    -   ``/fabrics/{fabric_name}``

    ### Verb
    -   GET

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    fabric_details = EpFabricDelete()
    fabric_details.fabric_name = "MyFabric"
    path = fabric_details.path
    verb = fabric_details.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "GET"

    @property
    def path(self):
        return self.path_fabric_name


class EpFabricFreezeMode(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricFreezeMode()

    ### Description
    Return the endpoint to query ``fabric_name`` freezemode status.

    ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.

    ### Path
    -   ``/fabrics/{fabric_name}/freezemode``

    ### Verb
    -   GET

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    fabric_details = EpFabricDelete()
    fabric_details.fabric_name = "MyFabric"
    path = fabric_details.path
    verb = fabric_details.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "GET"

    @property
    def path(self):
        return f"{self.path_fabric_name}/freezemode"


class EpFabricUpdate(Fabrics):
    """
    ## V1 API - Fabrics().EpFabricUpdate()

    ### Description
    Return endpoint information.

    ### Raises
    -   ``ValueError``: If fabric_name is not set.
    -   ``ValueError``: If fabric_name is invalid.
    -   ``ValueError``: If template_name is not set.
    -   ``ValueError``: If template_name is not a valid fabric template name.

    ### Path
    -   ``/rest/control/fabrics/{FABRIC_NAME}/{TEMPLATE_NAME}``

    ### Verb
    -   PUT

    ### Parameters
    - fabric_name: string
        - set the ``fabric_name`` to be used in the path
        - required
    - template_name: string
        - set the ``template_name`` to be used in the path
        - required
    -   path: retrieve the path for the endpoint
    -   verb: retrieve the verb for the endpoint

    ### Usage
    ```python
    instance = EpFabricUpdate()
    instance.fabric_name = "MyFabric"
    instance.template_name = "Easy_Fabric_IPFM"
    path = instance.path
    verb = instance.verb
    ```
    """

    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.required_properties.add("fabric_name")
        self.required_properties.add("template_name")
        self._build_properties()
        msg = f"ENTERED api.v1.LanFabric.Fabrics.{self.class_name}"
        self.log.debug(msg)

    def _build_properties(self):
        super()._build_properties()
        self.properties["verb"] = "PUT"

    @property
    def path(self):
        """
        - Endpoint for fabric create.
        - Raise ``ValueError`` if fabric_name is not set.
        """
        return self.path_fabric_name_template_name
