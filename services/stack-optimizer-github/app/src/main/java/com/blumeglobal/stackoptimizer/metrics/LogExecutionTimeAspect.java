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
package com.blumeglobal.stackoptimizer.metrics;


import com.blumeglobal.stackoptimizer.logging.StackOptimizerLogger;
import com.blumeglobal.stackoptimizer.logging.StackOptimizerLoggerFactory;
import java.lang.reflect.Method;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LogExecutionTimeAspect
{
    private final StackOptimizerLogger logger =
            StackOptimizerLoggerFactory.getLogger(LogExecutionTimeAspect.class.getName());

    @Pointcut("@annotation(com.blumeglobal.stackoptimizer.metrics.LogExecutionTime)")
    public void annotatedFunction()
    {}

    @Pointcut("execution(* com.blumeglobal..*.*(..))")
    public void atAllMethodExecution()
    {}

    @Around("atAllMethodExecution() && annotatedFunction()")
    public Object logExecutionTime(ProceedingJoinPoint call) throws Throwable
    {
        // get log message
        MethodSignature methodSignature = (MethodSignature) call.getSignature();
        Method method = methodSignature.getMethod();
        if (method == null)
        {
            return call.proceed();
        }

        LogExecutionTime myAnnotation = method.getAnnotation(LogExecutionTime.class);
        if (myAnnotation == null)
        {
            return call.proceed();
        }

        // track time
        long startTime = System.nanoTime();

        Object toReturn = call.proceed();

        long endTime = System.nanoTime();
        long duration = (endTime - startTime);
        logger.debug("-- " + method + "() executed in : " + duration + " milliseconds");

        return toReturn;
    }
}
