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



import java.util.function.Supplier;
import org.slf4j.ext.XLogger;

/**
 * Extends Slf4j's ext logger to add deferred logging
 * 
 */
public class Logger extends XLogger
{

    public Logger(org.slf4j.Logger logger)
    {
        super(logger);
    }

    /**
     * Logs an error message if the log level is set to error The caller is not required to check for
     * the current log level using isErrorEnabled() method.
     * 
     * @param message Supplies functional interface with message to log
     */
    public void error(Supplier<String> message)
    {
        if (isErrorEnabled())
        {
            error(message.get());
        }
    }

    /**
     * Logs an warning message if the log level is set to warning or lower. The caller is not required
     * to check for the current log level using isWarnEnabled() method.
     * 
     * @param message Supplies functional interface with message to log
     */
    public void warn(Supplier<String> message)
    {
        if (isWarnEnabled())
        {
            warn(message.get());
        }
    }

    /**
     * Logs an info message if the log level is set to info or lower The caller is not required to check
     * for the current log level using isInfoEnabled() method.
     * 
     * @param message Supplies functional interface with message to log
     */
    public void info(Supplier<String> message)
    {
        if (isInfoEnabled())
        {
            info(message.get());
        }
    }

    /**
     * Logs an info message if the log level is set to debug or lower The caller is not required to
     * check for the current log level using isDebugEnabled() method.
     * 
     * @param message Supplies functional interface with message to log
     */
    public void debug(Supplier<String> message)
    {
        if (isDebugEnabled())
        {
            debug(message.get());
        }
    }

    /**
     * Logs an trace message if the log level is set to trace The caller is not required to check for
     * the current log level using isDebugEnabled() method.
     * 
     * @param message Supplies functional interface with message to log
     */
    public void trace(Supplier<String> message)
    {
        if (isTraceEnabled())
        {
            trace(message.get());
        }
    }

}
