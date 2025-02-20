/********************************************************************************
 * Eclipse Tractus-X - Industry Core Hub Frontend
 *
 * Copyright (c) 2025 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the
 * License for the specific language govern in permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
********************************************************************************/

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import carPartsData from "../data/sample-data.json";
import { Cards } from '@catena-x/portal-shared-components';

interface CarPart {
  uuid: string;
  PartInstanceID: string;
  Name: string;
  Status: string;
  SingleLevelBom: string;
  Manufacturer: string;
  Material: string;
  WeightKg: number;
  Category: string;
  Description: string;
  Image: string;
}

function ProductsList() {
    const [carParts, setCarParts] = useState<CarPart[]>([]);
    const navigate = useNavigate();
  
    useEffect(() => {
      setCarParts(carPartsData);
    }, []);

    const handleButtonClick = (part: CarPart) => {
      navigate(`/product/${part.uuid}`);  // Navigate to the details page
    };
  
    return (
      <Cards
        buttonText="VIEW"
        items={carParts.map((part) => ({
          key: part.Name,
          title: part.Name,
          subtitle: part.Manufacturer,
          description: part.Description,
          image: {
            alt: part.Name,
            src: part.Image
          },
          onButtonClick: () => handleButtonClick(part),
          boxClickable: true
        }))}
        variant="expanded"
      />
    );
  }

export default ProductsList;
