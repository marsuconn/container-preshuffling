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


import com.blumeglobal.stackoptimizer.logging.LoggerService;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import java.util.HashMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.logging.LogLevel;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/logger")
@Api(tags = "LoggingService")
public class LoggerController
{

    private static final StackOptimizerLogger logger = StackOptimizerLoggerFactory.getLogger(LoggerController.class);

    @Autowired
    private LoggerService loggerService;

    @SuppressWarnings({"unchecked", "rawtypes"})
    @PostMapping(value = "/{loggerName}/{logLevel}", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiOperation(value = "Update the Logging level", produces = "application/json", consumes = "application/json")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "The POST call is Successful"),
            @ApiResponse(code = 500, message = "The POST call is Failed"),
            @ApiResponse(code = 404, message = "The API could not be found"),
            @ApiResponse(code = 400, message = "Invalid input")})
    public ResponseEntity<?> updateLogLevel(@PathVariable(value = "loggerName") String loggerName,
            @PathVariable("logLevel") String logLevel)
    {
        final String methodName = "updateLogLevel";
        logger.methodEntry(methodName, "loggerName = ", loggerName, "logLevel = " + logLevel);
        ResponseEntity responseEntity = null;
        HashMap<String, String> body = new HashMap<String, String>();
        try
        {
            String oldLogLevel = loggerService.getCurrentLogLevel(loggerName).toString();
            String newLogLevel = loggerService.setLogLevel(loggerName, LogLevel.valueOf(logLevel));
            body.put("OldLogLevel", oldLogLevel);
            body.put("NewLogLevel", newLogLevel);
            responseEntity = new ResponseEntity(body, HttpStatus.OK);
        } catch (Exception exp)
        {
            logger.error(methodName, "ErrorStackTrace ", exp);
            body.put("ErrorStackTrace", exp.toString());
            responseEntity = new ResponseEntity(body, HttpStatus.INTERNAL_SERVER_ERROR);
        }
        logger.methodExit(methodName, "Exit : body = ", body);
        return responseEntity;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    @GetMapping(value = "/getAllLoggers", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiOperation(value = "Get All Logging level", produces = "application/json", consumes = "application/json")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "The GET call is Successful"),
            @ApiResponse(code = 500, message = "The GET call is Failed"),
            @ApiResponse(code = 404, message = "The API could not be found"),
            @ApiResponse(code = 400, message = "Invalid input")})
    public ResponseEntity<?> getAllLoggers()
    {
        final String methodName = "getAllLoggers";
        logger.methodEntry(methodName, "Entry ", null);
        ResponseEntity responseEntity = null;
        HashMap<String, String> body = new HashMap<String, String>();
        try
        {
            body = loggerService.getAllLoggers();
            responseEntity = new ResponseEntity(body, HttpStatus.OK);
        } catch (Exception exp)
        {
            logger.error(methodName, "ErrorStackTrace ", exp);
            body.put("ErrorStackTrace", exp.toString());
            responseEntity = new ResponseEntity(body, HttpStatus.INTERNAL_SERVER_ERROR);
        }
        logger.methodExit(methodName, "Exit ", null);
        return responseEntity;
    }
}
