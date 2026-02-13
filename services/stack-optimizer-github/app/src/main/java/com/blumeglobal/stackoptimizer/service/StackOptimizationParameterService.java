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
package com.blumeglobal.stackoptimizer.service;

import com.blumeglobal.stackoptimizer.dto.OptimizationParametersDTO;
import com.blumeglobal.stackoptimizer.dto.OptimizationParametersSavedDTO;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import com.blumeglobal.stackoptimizer.metrics.LogEntryAndExit;
import com.blumeglobal.stackoptimizer.model.jpamodel.entities.OptimizationParameters;
import com.blumeglobal.stackoptimizer.repository.OptimizationParametersRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class StackOptimizationParameterService
{
    public StackOptimizationParameterService(OptimizationParametersRepository optimizationParametersRepository)
    {
        this.optimizationParametersRepository = optimizationParametersRepository;
    }

    OptimizationParametersRepository optimizationParametersRepository;

    private StackOptimizerLogger logger =
            StackOptimizerLoggerFactory.getLogger(StackOptimizationParameterService.class);

    @LogEntryAndExit
    public List<OptimizationParametersDTO> getOptimizationParametersByLocationUUID(String locationUUID)
    {
        return optimizationParametersRepository.findAllByLocationUUID(locationUUID).stream()
                .map(this::getOptimizationParametersDTO).collect(Collectors.toList());
    }

    private OptimizationParametersDTO getOptimizationParametersDTO(OptimizationParameters optimizationParameters)
    {
        OptimizationParametersDTO optimizationParametersDTO =
                OptimizationParametersDTO.convertToDTO(optimizationParameters);
        return optimizationParametersDTO;
    }

    @LogEntryAndExit
    @Transactional(transactionManager = "stackOptimizerTxMan")
    public OptimizationParametersSavedDTO saveOptimizationParameters(
            OptimizationParametersDTO optimizationParametersDTO)
    {
        OptimizationParameters optimizationParameters =
                OptimizationParametersDTO.convertToEntity(optimizationParametersDTO);
        optimizationParameters = optimizationParametersRepository.save(optimizationParameters);
        OptimizationParametersSavedDTO optimizationParametersSavedDTO = new OptimizationParametersSavedDTO();
        optimizationParametersSavedDTO.setOptimizationParameters(optimizationParameters);
        return optimizationParametersSavedDTO;
    }

    @LogEntryAndExit
    public void deleteContainerWatchlist(Long id)
    {
        optimizationParametersRepository.deleteById(id);
    }
}
