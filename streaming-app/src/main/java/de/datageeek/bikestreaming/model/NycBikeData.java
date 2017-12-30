package de.datageeek.bikestreaming.model;

import lombok.Data;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public @Data class NycBikeData {
    private static final String TIME_STAMP_PATTERN = "yyyy-MM-dd hh:mm:ss a";

    private int key;
    private int id;
    private String stationName;
    private int availableDocks;
    private int totalDocks;
    private double latitude;
    private double longitude;
    private String statusValue;
    private int statusKey;
    private int availableBikes;
    private String lastCommunicationTime;

    public String getIdAsString() {
        return String.valueOf(id);
    }

    public long getTimestampInMillis() {
        ZoneId nyc = ZoneId.of("America/New_York");
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(TIME_STAMP_PATTERN);
        LocalDateTime time = LocalDateTime.parse(lastCommunicationTime, formatter);
        ZonedDateTime timeNyc = ZonedDateTime.of(time, nyc);
        return timeNyc.toInstant().toEpochMilli();
    }

}

