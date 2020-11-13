package com.station.dependence.entity;

public class StationByTime {
    private String station_id;
    private String start;
    private String end;

    public String getEnd() {
        return end;
    }

    public String getStart() {
        return start;
    }

    public String getStation_id() {
        return station_id;
    }

    public void setEnd(String end) {
        this.end = end;
    }

    public void setStart(String start) {
        this.start = start;
    }

    public void setStation_id(String station_id) {
        this.station_id = station_id;
    }
}
