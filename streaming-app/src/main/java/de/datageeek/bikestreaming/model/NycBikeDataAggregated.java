package de.datageeek.bikestreaming.model;
import lombok.Data;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public @Data class NycBikeDataAggregated {
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
    private int year;
    private String month;
    private String weekDay;
    private int hour;
    private int sum;
    private int count;
    private double avgAvailableBikes;
    private long aggTimeStart;
    private long aggTimeEnd;

    public NycBikeDataAggregated add(NycBikeData value) {
        this.key = value.getKey();
        this.id = value.getId();
        this.stationName = value.getStationName();
        this.availableDocks = value.getAvailableDocks();
        this.totalDocks = value.getTotalDocks();
        this.latitude = value.getLatitude();
        this.longitude = value.getLongitude();
        this.statusValue = value.getStatusValue();
        this.statusKey = value.getStatusKey();
        this.availableBikes = value.getAvailableBikes();
        this.lastCommunicationTime = value.getLastCommunicationTime();
        this.count= this.count+1;
        this.sum = this.sum + availableBikes;
        return this;
    }

    public NycBikeDataAggregated computeAvgBikes() {
        this.avgAvailableBikes = (double) this.sum / this.count;
        return this;
    }

    public NycBikeDataAggregated setDateFields(){
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(TIME_STAMP_PATTERN);
        LocalDateTime date = LocalDateTime.parse(lastCommunicationTime, formatter);
        this.year = date.getYear();
        this.month = date.getMonth().toString();
        this.weekDay = date.getDayOfWeek().toString();
        this.hour = date.getHour();
        return this;
    }

    public NycBikeDataAggregated setWindowStartAndEnd(long aggTimeStart, long aggTimeEnd) {
        this.aggTimeStart = aggTimeStart;
        this.aggTimeEnd = aggTimeEnd;
        return this;
    }
}


