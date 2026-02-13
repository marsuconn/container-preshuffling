package com.blumeglobal.stackoptimizer.model.jpamodel.config;

import com.blumeglobal.core.architecture.properties.YamlPropertySourceFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource(ignoreResourceNotFound=true,
        value = {"classpath:jpa-application.yml",
                "classpath:jpa-application-${spring.profiles.active}.yml"}, factory = YamlPropertySourceFactory.class)
public class StackOptimizerJpaConfiguration
{
}
