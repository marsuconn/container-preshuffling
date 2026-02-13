package com.blumeglobal.stackoptimizer.model.util;


import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;

import java.io.IOException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.List;

/**
 * Custom deserializer for {@link LocalDateTime}
 */
public class DateTimeCustomDeserializer extends JsonDeserializer<LocalDateTime>
{
    private String DATE_FORMAT_YYYY_MM_DD_HH_MM_SS = "yyyy-MM-dd HH:mm:ss";
    private List<String> DATE_FORMATS = Arrays.asList(DATE_FORMAT_YYYY_MM_DD_HH_MM_SS);

    @Override
    public LocalDateTime deserialize(JsonParser p, DeserializationContext context) throws IOException
    {
        LocalDateTime localDateTime = null;
        try {
            localDateTime =   parseDate(p.getValueAsString());
        }catch(Exception e)
        {
           throw new IOException(e.getMessage());
        }
        return  localDateTime;
    }


    public  LocalDateTime parseDate(String date) throws Exception {
        try
        {
            return LocalDateTime.parse(date, DateTimeFormatter.ISO_DATE_TIME);
        } catch (Exception e)
        {
            // no logging required here. log at the end
        }

        for (String dateFormat : DATE_FORMATS)
        {
            try
            {
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern(dateFormat);
                return LocalDateTime.parse(date, formatter);
            } catch (Exception e)
            {
                // no logging required here. log at the end
            }
        }

        try
        {
            long epoc = Long.parseLong(date);
            return getLocalDateTimeAtUTCofMilliseconds(epoc);
        } catch (NumberFormatException e)
        {
            // no logging required here. log at the end
        }

        throw new Exception(
                "Un-parsable date: " + date + " Supported formats are");
    }

    public  LocalDateTime getLocalDateTimeAtUTCofMilliseconds(Long epochMilliseconds)
    {
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(epochMilliseconds), ZoneOffset.UTC);
    }

}
