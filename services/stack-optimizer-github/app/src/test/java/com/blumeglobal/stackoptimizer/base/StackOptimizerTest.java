/*
 * Copyright (c) 2021, Blume Global and/or its affiliates. All rights reserved.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This code is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 only, as
 * published by the Free Software Foundation.  Blume Global designates this
 * particular file as subject to the "Classpath" exception as provided
 * by Blume Global in the LICENSE file that accompanied this code.
 *
 * This code is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * version 2 for more details (a copy is included in the LICENSE file that
 * accompanied this code).
 *
 * You should have received a copy of the GNU General Public License version
 * 2 along with this work; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * Please contact Blume Global, 7901 Stoneridge Dr Suite 400, Pleasanton, CA 94588 USA
 * or visit www.blumeglobal.com if you need additional information or have any
 * questions.
 */
package com.blumeglobal.stackoptimizer.base;

import com.blumeglobal.stackoptimizer.config.dto.ApiResponse;
import com.blumeglobal.stackoptimizer.controller.StackOptimizationParameterController;
import com.blumeglobal.stackoptimizer.dto.OptimizationParametersDTO;
import com.blumeglobal.stackoptimizer.dto.OptimizationParametersSavedDTO;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.ResponseEntity;

public class StackOptimizerTest extends AbstractIntegrationTest
{

    private final StackOptimizerLogger logger = StackOptimizerLoggerFactory.getLogger(StackOptimizerTest.class);

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    StackOptimizationParameterController stackOptimizationParameterController;

    /*
     * create optimization parameters , get optimization parameters , update optimization parameters get
     * optimization parameters , delete optimization parameters and then get optimization parameters the
     * list should be empty
     */
    @Test
    public void testStackOptimizationParameter() throws IOException
    {
        String optimizationParametersPath = "testData/OptimizationParametersDTO.json";
        OptimizationParametersDTO optimizationParametersDTO =
                objectMapper.readValue(new ClassPathResource(optimizationParametersPath).getFile(),
                        new TypeReference<OptimizationParametersDTO>() {});
        ResponseEntity<ApiResponse<OptimizationParametersSavedDTO>> response =
                stackOptimizationParameterController.saveStackOptimizationParameters(optimizationParametersDTO);
        Assertions.assertEquals(response.getBody().getData().getOptimizationParameters().getParameterName(),
                optimizationParametersDTO.getParameterName());
        Assertions.assertNotNull(stackOptimizationParameterController
                .getOptimizationParametersByLocationId(optimizationParametersDTO.getLocationUUID()).getData());
        optimizationParametersDTO.setParameterValue("Drop");
        optimizationParametersDTO.setId(response.getBody().getData().getOptimizationParameters().getId());
        optimizationParametersDTO.setCreatedBy(response.getBody().getData().getOptimizationParameters().getCreatedBy());
        response = stackOptimizationParameterController.saveStackOptimizationParameters(optimizationParametersDTO);
        Assertions.assertEquals(response.getBody().getData().getOptimizationParameters().getParameterValue(), "Drop");
        Assertions.assertEquals(1, stackOptimizationParameterController
                .getOptimizationParametersByLocationId(optimizationParametersDTO.getLocationUUID()).getData().size());
        Assertions.assertEquals("Record deleted successfully", stackOptimizationParameterController
                .deleteOptimizationParameters(optimizationParametersDTO.getId()).getBody().getData());
        Assertions.assertTrue(stackOptimizationParameterController
                .getOptimizationParametersByLocationId(optimizationParametersDTO.getLocationUUID()).getData()
                .isEmpty());
    }
}
