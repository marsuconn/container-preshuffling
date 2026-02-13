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
package com.blumeglobal.stackoptimizer.error.handler;

import com.blumeglobal.stackoptimizer.config.dto.ApiResponse;
import com.blumeglobal.stackoptimizer.error.ErrorData;
import com.blumeglobal.stackoptimizer.error.StackOptimizerErrorCode;
import com.blumeglobal.stackoptimizer.error.StackOptimizerException;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import com.blumeglobal.stackoptimizer.metrics.LogEntryAndExit;
import java.util.Arrays;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.servlet.http.HttpServletRequest;
import javax.validation.ConstraintViolationException;
import org.apache.commons.lang3.exception.ExceptionUtils;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestController;

/**
 * Common controller for handling API exceptions.
 */
@ControllerAdvice
@RestController
@Order(Ordered.HIGHEST_PRECEDENCE)
public class StackOptimizerExceptionHandler
{
    private final StackOptimizerLogger logger =
            StackOptimizerLoggerFactory.getLogger(StackOptimizerExceptionHandler.class.getName());

    @ExceptionHandler(StackOptimizerException.class)
    @LogEntryAndExit
    public ResponseEntity<ApiResponse<Void>> handleErrors(StackOptimizerException error)
    {
        String methodName = "handleErrors";
        logger.error(">> handleErrors error: ", error);
        Throwable exception = Optional.ofNullable(error.getException()).orElseGet(RuntimeException::new);
        logger.error(methodName, exception.getMessage(), ExceptionUtils.getStackTrace(exception));
        ErrorData errorData = new ErrorData(error.getErrorCode().name(), error.getErrorCode().getErrorMessage(),
                error.getErrorCode().getErrorMessage() + " "
                        + Optional.ofNullable(error.getCustomErrorMessage()).orElse(""));
        ApiResponse<Void> response = new ApiResponse.Builder<Void>()
                .status(error.getErrorCode().getHttpStatus().value()).error(errorData).build();
        return new ResponseEntity<>(response, error.getErrorCode().getHttpStatus());
    }

    @ExceptionHandler(Exception.class)
    @LogEntryAndExit
    public ResponseEntity<ApiResponse<Void>> handleGeneralErrors(Exception exception, HttpServletRequest request)
    {
        String methodName = "handleGeneralErrors";
        logger.error(methodName, exception);
        logger.error(methodName, exception.getMessage(), ExceptionUtils.getStackTrace(exception));
        StackOptimizerException error =
                new StackOptimizerException(StackOptimizerErrorCode.UNKNOWN_ERROR, exception, null);
        ErrorData errorData = new ErrorData(error.getErrorCode().name(), error.getErrorCode().getErrorMessage(),
                error.getErrorCode().getErrorMessage());
        ApiResponse<Void> response = new ApiResponse.Builder<Void>()
                .status(error.getErrorCode().getHttpStatus().value()).error(errorData).build();
        return new ResponseEntity<>(response, error.getErrorCode().getHttpStatus());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleMissingInputException(MethodArgumentNotValidException exception)
    {
        String methodName = "handleMissingInputException";
        logger.error(methodName, exception);
        logger.error(methodName, exception.getMessage(), ExceptionUtils.getStackTrace(exception));
        StackOptimizerException error = new StackOptimizerException(StackOptimizerErrorCode.REQUIRED_FIELDS_MISSING,
                exception, "Missing fields: " + exception.getFieldErrors().stream().map(FieldError::getField)
                        .collect(Collectors.joining(", ")));
        ErrorData errorData = new ErrorData(error.getErrorCode().name(), error.getErrorCode().getErrorMessage(),
                error.getErrorCode().getErrorMessage() + " " + error.getCustomErrorMessage());
        ApiResponse<Void> response = new ApiResponse.Builder<Void>()
                .status(error.getErrorCode().getHttpStatus().value()).error(errorData).build();
        return new ResponseEntity<>(response, error.getErrorCode().getHttpStatus());
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ApiResponse<Void>> handleMissingInputBodyException(ConstraintViolationException exception)
    {
        String methodName = "handleMissingInputBodyException";
        logger.error(methodName, exception);
        logger.error(methodName, exception.getMessage(), ExceptionUtils.getStackTrace(exception));
        StackOptimizerException error = new StackOptimizerException(
                StackOptimizerErrorCode.REQUEST_BODY_VALIDATION_FAILED, exception, exception.getMessage());
        ErrorData errorData = new ErrorData(error.getErrorCode().name(), error.getErrorCode().getErrorMessage(),
                customizeErrorMessage(error.getCustomErrorMessage()));
        ApiResponse<Void> response = new ApiResponse.Builder<Void>()
                .status(error.getErrorCode().getHttpStatus().value()).error(errorData).build();
        return new ResponseEntity<>(response, error.getErrorCode().getHttpStatus());
    }

    private String customizeErrorMessage(String error)
    {
        try
        {
            error = Arrays.stream(error.split(","))
                    .map(eachError -> eachError.substring(eachError.lastIndexOf(".") + 1)).distinct()
                    .collect(Collectors.joining(", "));
        } catch (Exception e)
        {
        }
        return error;
    }
}
