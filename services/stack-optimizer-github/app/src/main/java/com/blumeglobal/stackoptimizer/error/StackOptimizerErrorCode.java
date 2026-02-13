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
package com.blumeglobal.stackoptimizer.error;



import lombok.Getter;
import lombok.ToString;
import org.springframework.http.HttpStatus;

@Getter
@ToString
public enum StackOptimizerErrorCode
{
    REQUIRED_FIELDS_MISSING("Some of the required inputs are missing", HttpStatus.BAD_REQUEST),
    REQUEST_BODY_VALIDATION_FAILED("Invalid request.", HttpStatus.BAD_REQUEST),
    UNKNOWN_ERROR("An internal server error occurred", HttpStatus.INTERNAL_SERVER_ERROR);

    private final String errorMessage;
    private final HttpStatus httpStatus;

    StackOptimizerErrorCode(String errorMessage, HttpStatus httpStatus)
    {
        this.errorMessage = errorMessage;
        this.httpStatus = httpStatus;
    }
}
