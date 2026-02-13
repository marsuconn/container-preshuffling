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
package com.blumeglobal.stackoptimizer.model.jpamodel.entities;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name ="optimization_parameters")
@Setter
@Getter
@JsonInclude(JsonInclude.Include.NON_NULL)
@ToString
public class OptimizationParameters extends BaseEntity
{
    @Column(name = "location_uuid")
    private String locationUUID;
    @Column(name = "parameter_name")
    private String parameterName;
    @Column(name = "parameter_value")
    private String parameterValue;
    @Column(name = "value_from")
    private String valueFrom;
    @Column(name = "value_to")
    private String valueTo;
    @Column(name = "value_type")
    private String valueType;
    @Column(name = "uom")
    private String uom;
    @Column(name = "default_value")
    private String defaultValue;
    @Column(name = "description")
    private String description;
}
