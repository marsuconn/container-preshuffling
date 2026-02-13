package com.blumeglobal.stackoptimizer.model.jpamodel.entities;

import com.blumeglobal.stackoptimizer.model.jpamodel.constants.StackOptimizerJpaConstants;
import com.blumeglobal.core.security.token.config.JwtBean;
import com.blumeglobal.core.security.token.context.JwtContextHolder;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.GenericGenerator;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.ZoneOffset;


/**
 * <h1>BaseEntity</h1>
 * Base class for all entities
 */
@MappedSuperclass
@Getter
@Setter
@NoArgsConstructor
public class BaseEntity extends AbstractBaseEntity implements Serializable
{
    private static final long serialVersionUID = -1185360610331389067L;

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "native")
    @GenericGenerator(name = "native", strategy = "native")
    @Column(name = "id")
    protected Long id;
    @JsonIgnore
    @Column(name = "created_on", updatable = false)
    @CreationTimestamp
    protected LocalDateTime createdOn;
    @JsonIgnore
    @Column(name = "modified_on")
    @UpdateTimestamp
    protected LocalDateTime modifiedOn;
    @Column(name = "created_by")
    protected String createdBy;
    @Column(name = "modified_by")
    protected String modifiedBy;
    @Override
    public String toString() {
        return ToStringBuilder.reflectionToString(this, ToStringStyle.SIMPLE_STYLE);
    }

    @Override
    public boolean equals(Object other) {
        if (other == null) {
            return false;
        }

        if (this.getClass() != other.getClass()) {
            return false;
        }

        BaseEntity otherObject = (BaseEntity) other;

        if (this.getId() == null) {
            return otherObject.getId() == null;
        }

        if (otherObject.getId() == null) {
            return false;
        }

        return this.getId().equals(otherObject.getId());

    }

    @Override
    public int hashCode() {
        return this.getId() == null ? 0 : this.getId().hashCode();
    }

    @PrePersist
    public void onCreate()
    {
        LocalDateTime datetime = LocalDateTime.now(ZoneOffset.UTC);
        this.setCreatedOn(datetime);
        this.setModifiedOn(datetime);

        JwtBean jwtBean = JwtContextHolder.getJwtContext().getJwtBean();
        String username = jwtBean != null && StringUtils.isNotBlank(jwtBean.getUserName()) ? jwtBean.getUserName() : StackOptimizerJpaConstants.SYSTEM;
        setCreatedBy(username);
        setModifiedBy(username);
    }

    @PreUpdate
    public void onUpdate()
    {
        LocalDateTime datetime = LocalDateTime.now(ZoneOffset.UTC);
        this.setModifiedOn(datetime);

        JwtBean jwtBean = JwtContextHolder.getJwtContext().getJwtBean();
        String username = jwtBean != null && StringUtils.isNotBlank(jwtBean.getUserName()) ? jwtBean.getUserName() : StackOptimizerJpaConstants.SYSTEM;
        setModifiedBy(username);
    }
}