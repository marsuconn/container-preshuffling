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
package com.blumeglobal.stackoptimizer.config;


import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.MapperFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableHandlerMethodArgumentResolver;
import org.springframework.data.web.SortHandlerMethodArgumentResolver;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@ComponentScan({"com.blumeglobal.*"})
@EnableWebMvc
@Order(2)
public class CustomizedWebConfig implements WebMvcConfigurer
{

    private static final String PAGE = "page-number";
    private static final String SIZE = "page-size";
    private static final String SORT = "order-by";
    private static final Integer DEFAULT_PAGE_NUMBER = 0;

    @Value("${pagination.default.page-size}")
    private Integer defaultPageSize;
    @Value("${pagination.default.max-page-size}")
    private Integer maxPageSize;

    @Bean
    public RestTemplate restTemplate()
    {
        SimpleClientHttpRequestFactory httpRequestFactory = getSimpleClientHttpRequestFactory();
        RestTemplate restTemplate = new RestTemplate(httpRequestFactory);
        restTemplate.getMessageConverters().add(0, mappingJacksonHttpMessageConverter());
        return restTemplate;
    }

    private SimpleClientHttpRequestFactory getSimpleClientHttpRequestFactory()
    {
        SimpleClientHttpRequestFactory httpRequestFactory = new SimpleClientHttpRequestFactory();
        httpRequestFactory.setConnectTimeout(15000);
        httpRequestFactory.setReadTimeout(15000);
        return httpRequestFactory;
    }

    @Bean
    public MappingJackson2HttpMessageConverter mappingJacksonHttpMessageConverter()
    {
        MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
        converter.setObjectMapper(objectMapper());
        return converter;
    }

    @Bean
    public ObjectMapper objectMapper()
    {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        objectMapper.configure(MapperFeature.ACCEPT_CASE_INSENSITIVE_ENUMS, true);
        return objectMapper;
    }

    @Bean
    public ExecutorService executorService()
    {
        return Executors.newFixedThreadPool(10);
    }

    /**
     * Pagination settings
     *
     * @param argumentResolvers
     */
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers)
    {
        // set sorting query parameters
        SortHandlerMethodArgumentResolver sortResolver = new SortHandlerMethodArgumentResolver();
        sortResolver.setSortParameter(SORT);

        // set pagination query parameters
        PageableHandlerMethodArgumentResolver pageResolver = new PageableHandlerMethodArgumentResolver(sortResolver);
        Pageable defaultPageable = PageRequest.of(DEFAULT_PAGE_NUMBER, defaultPageSize);

        pageResolver.setOneIndexedParameters(true); // set 1-indexed page-number in query parameter
        pageResolver.setPageParameterName(PAGE);
        pageResolver.setSizeParameterName(SIZE);
        pageResolver.setMaxPageSize(maxPageSize);
        pageResolver.setFallbackPageable(defaultPageable); // default pagination

        argumentResolvers.add(pageResolver);

        WebMvcConfigurer.super.addArgumentResolvers(argumentResolvers);
    }
}
