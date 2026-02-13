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

import com.blumeglobal.core.mongo.test.mockdata.MockDataMongoService;
import com.blumeglobal.core.mysql.test.mockdata.MockDataService;
import com.blumeglobal.core.mysql.test.wiper.TestDataWiper;
import com.blumeglobal.core.test.config.BlumeSpringRunner;
import com.blumeglobal.stackoptimizer.StackOptimizerApplication;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.sql.DataSource;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.ConfigDataApplicationContextInitializer;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.transaction.support.TransactionTemplate;

@RunWith(BlumeSpringRunner.class)
@SpringBootTest(classes = {StackOptimizerApplication.class})
@ContextConfiguration(initializers = {ConfigDataApplicationContextInitializer.class})
@Configuration
@ActiveProfiles("test")
// @EmbeddedKafka(partitions = 1, brokerProperties = { "listeners=PLAINTEXT://localhost:9092",
// "port=9092" })
// @PropertySource(value = "classpath:test-mysql-datasource.yaml", factory =
// YamlPropertySourceFactory.class)
public abstract class AbstractIntegrationTest
{


    Logger logger = LoggerFactory.getLogger(this.getClass());

    // @Autowired()
    // public BlumeMysqlConfigurations mysqlConfigs;

    // @Autowired
    // @Qualifier("jpaConfigurator")
    // public BlumeMysqlJpaConfigurator jpaConfigurator;

    @Autowired
    @Qualifier("stackOptimizerDataSource")
    public DataSource ds;

    @PersistenceContext(unitName = "stackOptimizer")
    public EntityManager em;

    @Autowired
    @Qualifier("stackOptimizerTxTemplate")
    public TransactionTemplate txTemp;

    @Autowired
    @Qualifier("stackOptimizerJdbcTemplate")
    public NamedParameterJdbcTemplate jdbcTemp;

    @Autowired
    public MockDataService mockSrv;

    @Autowired
    public MockDataMongoService mockDataMongoService;

    @Autowired
    public TestDataWiper wiper;

    @Before
    public void cleanSchema()
    {
        wiper.truncateAllTables(jdbcTemp, txTemp);
    }
}
