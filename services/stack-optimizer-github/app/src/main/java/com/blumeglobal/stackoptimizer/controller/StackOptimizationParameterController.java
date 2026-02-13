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
package com.blumeglobal.stackoptimizer.controller;

import com.blumeglobal.stackoptimizer.config.dto.ApiResponse;
import com.blumeglobal.stackoptimizer.dto.OptimizationParametersDTO;
import com.blumeglobal.stackoptimizer.dto.OptimizationParametersSavedDTO;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import com.blumeglobal.stackoptimizer.metrics.LogEntryAndExit;
import com.blumeglobal.stackoptimizer.metrics.LogExecutionTime;
import com.blumeglobal.stackoptimizer.service.StackOptimizationParameterService;
import io.swagger.annotations.Api;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/stackOptimizationParameter")
@Api(tags = "StackOptimizationParameterService")
public class StackOptimizationParameterController
{
    StackOptimizerLogger stackOptimizerLogger =
            StackOptimizerLoggerFactory.getLogger(StackOptimizationParameterController.class);

    public StackOptimizationParameterController(StackOptimizationParameterService stackOptimizationParameterService)
    {
        this.stackOptimizationParameterService = stackOptimizationParameterService;
    }

    StackOptimizationParameterService stackOptimizationParameterService;

    @PostMapping
    @LogEntryAndExit
    @LogExecutionTime
    public ResponseEntity<ApiResponse<OptimizationParametersSavedDTO>> saveStackOptimizationParameters(
            @RequestBody OptimizationParametersDTO optimizationParametersDTO)
    {
        OptimizationParametersSavedDTO optimizationParametersSavedDTO =
                stackOptimizationParameterService.saveOptimizationParameters(optimizationParametersDTO);
        ApiResponse<OptimizationParametersSavedDTO> apiResponse =
                new ApiResponse.Builder<OptimizationParametersSavedDTO>().status(HttpStatus.OK.value())
                        .data(optimizationParametersSavedDTO).build();
        return ResponseEntity.ok(apiResponse);
    }

    @DeleteMapping("/{id}")
    @LogEntryAndExit
    @LogExecutionTime
    public ResponseEntity<ApiResponse> deleteOptimizationParameters(@PathVariable Long id)
    {
        stackOptimizationParameterService.deleteContainerWatchlist(id);
        ApiResponse<String> apiResponse = new ApiResponse.Builder<String>().status(HttpStatus.OK.value())
                .data("Record deleted successfully").build();
        return ResponseEntity.ok(apiResponse);
    }

    @GetMapping
    @LogEntryAndExit
    @LogExecutionTime
    public ApiResponse<List<OptimizationParametersDTO>> getOptimizationParametersByLocationId(
            @RequestParam String locationUUID)
    {
        List<OptimizationParametersDTO> optimizationParametersList =
                stackOptimizationParameterService.getOptimizationParametersByLocationUUID(locationUUID);
        return new ApiResponse.Builder<List<OptimizationParametersDTO>>().status(HttpStatus.OK.value())
                .data(optimizationParametersList).build();
    }
}
