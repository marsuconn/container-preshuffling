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


import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.domain.Page;

@Setter
@Getter
public class PaginationMeta implements Serializable
{

    private static final long serialVersionUID = 4911076807352391702L;
    private Long totalCount;
    private Integer totalPages;
    private Boolean isFirst;
    private Boolean isLast;
    private Integer pageNumber;
    private Integer pageSize;

    public PaginationMeta()
    {
        totalCount = 0L;
        totalPages = 0;
        isFirst = Boolean.TRUE;
        isLast = Boolean.TRUE;
        pageNumber = 0;
        pageSize = 0;
    }

    public static <T> PaginationMeta createPaginationMeta(Page<T> page)
    {
        PaginationMeta paginationMeta = new PaginationMeta();

        paginationMeta.setTotalCount(page.getTotalElements());
        paginationMeta.setTotalPages(page.getTotalPages());
        paginationMeta.setPageSize(page.getSize());
        paginationMeta.setPageNumber(page.getNumber() + 1);
        paginationMeta.setIsFirst(page.isFirst());
        paginationMeta.setIsLast(page.isLast());

        return paginationMeta;
    }
}
