#################################################################################
# Eclipse Tractus-X - Dataspace SDK
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


## Authorization Managment from Eclipse Tractus-X Simple Wallet (Renamed to tools)
## Author: Mathias Brunkow Moser
## License: Apache License, Version 2.0
## Source: https://github.com/eclipse-tractusx/digital-product-pass/blob/main/dpp-verification/simple-wallet/utilities/httpUtils.py

from fastapi import Request

class authManager:
    api_key: str
    api_key_header: str
    auth_enabled: bool
    
    def __init__(self, api_key:str="password", api_key_header:str = "X-Api-Key", auth_enabled:bool = False):
        self.api_key = api_key
        self.api_key_header = api_key_header
        self.auth_enabled = auth_enabled
    
    def is_authenticated(self, request: Request):
        
        ## If auth is not enabled then is authenticated
        if(not self.auth_enabled):
            return True
        
        api_key_from_header = request.headers.get(self.api_key_header, None)
        
        ## User not authenticated
        if(api_key_from_header is None):
            return False
        
        ## This is the  only case that the user is authenticated
        if(api_key_from_header == self.api_key):
            return True
        
        return False