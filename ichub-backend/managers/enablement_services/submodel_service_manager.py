#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from typing import Dict, Any
from uuid import UUID
import json
from tractusx_sdk.industry.adapters.submodel_adapter_factory import SubmodelAdapterFactory
from tractusx_sdk.industry.adapters.submodel_adapters.file_system_adapter import FileSystemAdapter

class SubmodelServiceManager:
    """Manager for handling submodel service."""
    file_system: FileSystemAdapter

    def __init__(self):
        # TODO: add needed params here
        self.file_system = SubmodelAdapterFactory.get_file_system(root_path="./data/submodels")

    def upload_twin_aspect_document(self, global_id : UUID, semantic_id: str, payload: Dict[str, Any]):
        """Upload a submodel to the service."""
        # Implementation for uploading a submodel
        content = json.dumps(payload, indent=4)
        print("==========================")
        print("==== Submodel Service ====")
        print("==========================")
        print(f"Uploading submodel with Global ID: {global_id}")
        print(f"Semantic ID: {semantic_id}")
        self.file_system.write(f"{semantic_id}/{global_id}.json",content)
        print(f"==== Start of Payload ====")
        print(content)
        print(f"==== End of Payload ====")
        print("Submodel uploaded successfully (dummy implementation).")
        print()

    def get_twin_aspect_document(self, global_id: UUID, semantic_id: str) -> Dict[str, Any]:
        """Get a submodel from the service."""
        # Implementation for retrieving a submodel
        print(f"Retrieving submodel with Global ID: {global_id}")
        print(f"Semantic ID: {semantic_id}")

        content = self.file_system.read(f"{semantic_id}/{global_id}.json")
        return content
