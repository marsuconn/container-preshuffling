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



import java.text.MessageFormat;

// todo: morr - A new logging module is comming on line in core-architecture/core-logger. Where did
// this logger extention come from?
public class StackOptimizerLogger extends Logger
{
    public StackOptimizerLogger(org.slf4j.Logger logger)
    {
        super(logger);
    }

    private static final String METHOD_ENTRY_FORMAT = "MethodEntry : {0} () >> ";

    private static final String METHOD_EXIT_FORMAT = "MethodExit : {0} () << ";

    private static final String INPUT_ATTRIBUTE_FORMAT =
            " [Input attribute : {0} : {1}, and other input attributes : {2}]";

    private static final String INFO_ATTRIBUTE_FORMAT = " [Info attribute : {0}]";

    private static final String DEBUG_ATTRIBUTE_FORMAT = " [Debug attribute : {0}]";

    private static final String RESPONSE_ATTRIBUTE_FORMAT =
            " [Response attribute : {0} : {1}, and other attributes : {2}]";

    private static final String INPUT_OBJECT = "Input Object";

    private static final String RETURN_OBJECT = "Return Object";

    private static final String METHOD_INFO_FORMAT = "Info : Method : {0} () >> ";

    private static final String METHOD_DEBUG_FORMAT = "Debug : Method : {0} () >> ";

    private static final String METHOD_ERROR_FORMAT = "Error : Method : {0} () >> ";

    /**
     * Logger method for method entry
     *
     * @param methodName - method name
     * @param inputObject - input object to the method
     * @param message - string - custom message
     * @param object - any extra object if required to log
     */
    public void methodEntry(String methodName, String message, Object inputObject, Object... object)
    {
        if (isInfoEnabled())
        {
            info(MessageFormat.format(METHOD_ENTRY_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer()) + MessageFormat.format(INPUT_ATTRIBUTE_FORMAT,
                            INPUT_OBJECT, inputObject, getObjectArrayToString(object)));
        }
    }

    /**
     * Logger method for method exit
     *
     * @param methodName - method name
     * @param returnObject - return object from the method.
     * @param message - string - custom message
     * @param object - any extra object if required to log
     */
    public void methodExit(String methodName, String message, Object returnObject, Object... object)
    {
        if (isInfoEnabled())
        {
            debug(MessageFormat.format(METHOD_EXIT_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer()) + MessageFormat.format(RESPONSE_ATTRIBUTE_FORMAT,
                            RETURN_OBJECT, returnObject, getObjectArrayToString(object)));
        }
    }

    /**
     * Logger method for info
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param object - any object if required to log
     */
    public void info(String methodName, String message, Object object)
    {
        if (isInfoEnabled())
        {
            info(MessageFormat.format(METHOD_INFO_FORMAT, methodName) + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(INFO_ATTRIBUTE_FORMAT, object));
        }
    }

    /**
     * Logger method for info
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param object - any extra object if required to log
     */
    public void info(String methodName, String message, Object... object)
    {
        if (isInfoEnabled())
        {
            info(MessageFormat.format(METHOD_INFO_FORMAT, methodName) + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(INFO_ATTRIBUTE_FORMAT, getObjectArrayToString(object)));
        }
    }

    /**
     * Logger method for debug
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param object - any extra object if required to log
     */
    public void debug(String methodName, String message, Object... object)
    {
        if (isInfoEnabled())
        {
            debug(MessageFormat.format(METHOD_DEBUG_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(DEBUG_ATTRIBUTE_FORMAT, getObjectArrayToString(object)));
        }
    }

    /**
     * Logger method for debug
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param object - any object if required to log
     */
    public void debug(String methodName, String message, Object object)
    {
        if (isInfoEnabled())
        {
            debug(MessageFormat.format(METHOD_DEBUG_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(DEBUG_ATTRIBUTE_FORMAT, object));
        }
    }

    /**
     * Logger method for error
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param e - throw
     * @param object - any extra object if required to log
     */
    public void error(String methodName, String message, Throwable e, Object... object)
    {
        if (isErrorEnabled())
        {
            error(MessageFormat.format(METHOD_ERROR_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(DEBUG_ATTRIBUTE_FORMAT, getObjectArrayToString(object)), e);
        }
    }

    /**
     * Logger method for error
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param e - throw
     */
    public void error(String methodName, String message, Throwable e)
    {
        if (isErrorEnabled())
        {
            error(MessageFormat.format(METHOD_ERROR_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer()), e);
        }
    }

    /**
     * Logger method for error
     *
     * @param methodName - method name
     * @param message - string - custom message
     * @param obj - throw
     */
    public void error(String methodName, String message, Object obj)
    {
        if (isErrorEnabled())
        {
            error(MessageFormat.format(METHOD_ERROR_FORMAT, methodName)
                    + (message != null ? message : new StringBuffer())
                    + MessageFormat.format(DEBUG_ATTRIBUTE_FORMAT, getObjectArrayToString(obj)));
        }
    }

    /**
     * toString method for variable number of arguments
     *
     * @param object
     * @return
     */
    private String getObjectArrayToString(Object... object)
    {
        String toString = null;
        if (object != null)
        {
            for (Object element : object)
            {
                if (toString == null)
                {
                    toString = element != null ? element.toString() : "null";
                }
                else
                {
                    toString = toString + ", " + (element != null ? element.toString() : "null");
                }
            }
        }
        return toString;
    }

}
