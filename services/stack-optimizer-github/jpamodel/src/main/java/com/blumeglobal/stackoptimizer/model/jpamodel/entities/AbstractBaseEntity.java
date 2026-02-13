package com.blumeglobal.stackoptimizer.model.jpamodel.entities;

import java.io.Serializable;

public abstract class AbstractBaseEntity implements Serializable {

    private static final long serialVersionUID = 3972492520934707989L;

    /**
     * Return string representation of a class
     * @return string representation
     */
    public abstract String toString();

    /**
     * To check if two objects are equal
     * @param o object to be checked for equality
     * @return true/false based on equality
     */
    public abstract boolean equals(Object o);

    /**
     * Returns hashcode of the object
     * @return hashcode of the object
     */
    public abstract int hashCode();

}