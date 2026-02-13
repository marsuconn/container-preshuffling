package com.blumeglobal.stackoptimizer.model.dto;

import com.blumeglobal.stackoptimizer.model.util.DateTimeCustomDeserializer;
import com.blumeglobal.stackoptimizer.model.util.DateTimeCustomSerializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.io.Serializable;
import java.time.LocalDateTime;

@Getter
@Setter
@ToString
public class BaseDTO implements Serializable
{
    protected Long id;
    protected String createdBy;
    protected String modifiedBy;
    protected String organization;

    @JsonSerialize(using = DateTimeCustomSerializer.class)
    @JsonDeserialize(using = DateTimeCustomDeserializer.class)
    protected LocalDateTime createdOn;
    @JsonSerialize(using = DateTimeCustomSerializer.class)
    @JsonDeserialize(using = DateTimeCustomDeserializer.class)
    protected LocalDateTime modifiedOn;
}
