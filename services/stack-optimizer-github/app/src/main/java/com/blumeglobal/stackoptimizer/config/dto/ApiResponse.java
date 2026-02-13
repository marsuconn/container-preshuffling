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
package com.blumeglobal.stackoptimizer.config.dto;


import com.blumeglobal.stackoptimizer.error.ErrorData;
import java.io.Serializable;
import lombok.Getter;
import lombok.ToString;

/**
 * This class represents the general response structure of the api.
 * 
 * @param <T> response data
 */
@Getter
@ToString
public final class ApiResponse<T> implements Serializable
{

    /**
     * HTTP status.
     */
    private Integer status;

    /**
     * Error data.
     */
    private ErrorData error;

    /**
     * Response data.
     */
    private T data;

    private ApiResponse(final Builder<T> builder)
    {
        this.status = builder.status;
        this.error = builder.error;
        this.data = builder.data;
    }

    /**
     * Builder for {@link ApiResponse}.
     * 
     * @param <T> response data type
     */
    public static final class Builder<T>
    {

        /**
         * Status value.
         */
        private Integer status;

        /**
         * Error value.
         */
        private ErrorData error;

        /**
         * Data value.
         */
        private T data;

        /**
         * Set HTTP status.
         * 
         * @param statusValue value for status
         * @return builder
         */
        public Builder<T> status(final Integer statusValue)
        {
            this.status = statusValue;

            return this;
        }

        /**
         * Set error data.
         * 
         * @param errorValue value for error
         * @return builder
         */
        public Builder<T> error(final ErrorData errorValue)
        {
            this.error = errorValue;

            return this;
        }

        /**
         * Set response data.
         * 
         * @param dataValue value for data
         * @return builder
         */
        public Builder<T> data(final T dataValue)
        {
            this.data = dataValue;

            return this;
        }

        /**
         * @return instance of {@link ApiResponse}.
         */
        public ApiResponse<T> build()
        {
            return new ApiResponse<>(this);
        }
    }
}
