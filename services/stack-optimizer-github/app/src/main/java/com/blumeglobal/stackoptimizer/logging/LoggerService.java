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
package com.blumeglobal.stackoptimizer.logging;



import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;
import com.blumeglobal.stackoptimizer.error.StackOptimizerErrorCode;
import com.blumeglobal.stackoptimizer.error.StackOptimizerException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.LoggerFactory;
import org.slf4j.impl.StaticLoggerBinder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.logging.LogLevel;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class LoggerService
{
    private static final Map<LogLevel, Level> LEVELS;
    private static final StackOptimizerLogger logger = StackOptimizerLoggerFactory.getLogger(LoggerService.class);

    @Autowired
    private RestTemplate restTemplate;
    static
    {
        Map<LogLevel, Level> levels = new HashMap<>();
        levels.put(LogLevel.TRACE, Level.TRACE);
        levels.put(LogLevel.DEBUG, Level.DEBUG);
        levels.put(LogLevel.INFO, Level.INFO);
        levels.put(LogLevel.WARN, Level.WARN);
        levels.put(LogLevel.ERROR, Level.ERROR);
        levels.put(LogLevel.OFF, Level.OFF);
        LEVELS = Collections.unmodifiableMap(levels);
    }

    public String setLogLevel(String loggerName, LogLevel level)
    {
        Level newLevel = LEVELS.get(level);
        getLogger(loggerName).setLevel(newLevel);
        return newLevel.levelStr;
    }

    public LogLevel getCurrentLogLevel(String loggerName)
    {
        Level currentLevel = getLogger(loggerName).getLevel();
        for (Map.Entry<LogLevel, Level> entry : LEVELS.entrySet())
        {
            if (entry.getValue() == currentLevel)
            {
                return entry.getKey();
            }
        }
        return LogLevel.OFF;
    }

    private Logger getLogger(String name)
    {
        return ((LoggerContext) StaticLoggerBinder.getSingleton().getLoggerFactory())
                .getLogger(StringUtils.isEmpty(name) ? Logger.ROOT_LOGGER_NAME : name);
    }

    public HashMap<String, String> getAllLoggers()
    {
        final String methodName = "getAllLoggers";

        HashMap<String, String> body = new HashMap<String, String>();

        try
        {
            LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();
            for (Logger logger : context.getLoggerList())
            {
                body.put(logger.getName(), logger.getLevel() != null ? logger.getLevel().levelStr : "");
            }

        } catch (Exception exp)
        {
            logger.error(methodName, " Exception Occurred !! ", exp);
            throw new StackOptimizerException(StackOptimizerErrorCode.UNKNOWN_ERROR, exp, null);
        }
        return body;
    }

    private HttpHeaders getHttpHeaders()
    {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        // headers.set("Authorization", "Bearer " + auth.getAttributes().get("token"));
        return headers;
    }
}
