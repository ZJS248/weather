package com.station.dependence.entity;

public class GridLayer {
    private double startlon;
    private double endlon;
    private double startlat;
    private double endlat;
    private String nlon;
    private String nlat;
    private long lonsize;
    private long latsize;
    private Double[] data;
    private String[] legendColor;
    private double[] legendValue;
    private String polygonExtent;
    private String date;
    private int missingValue;

    public int getMissingValue() {
        return missingValue;
    }

    public void setMissingValue(int missingValue) {
        this.missingValue = missingValue;
    }

    public double getStartlon() {
        return startlon;
    }

    public void setStartlon(double startlon) {
        this.startlon = startlon;
    }

    public double getEndlon() {
        return endlon;
    }

    public void setEndlon(double endlon) {
        this.endlon = endlon;
    }

    public double getStartlat() {
        return startlat;
    }

    public void setStartlat(double startlat) {
        this.startlat = startlat;
    }

    public double getEndlat() {
        return endlat;
    }

    public void setEndlat(double endlat) {
        this.endlat = endlat;
    }

    public String getNlon() {
        return nlon;
    }

    public void setNlon(String nlon) {
        this.nlon = nlon;
    }

    public String getNlat() {
        return nlat;
    }

    public void setNlat(String nlat) {
        this.nlat = nlat;
    }

    public long getLonsize() {
        return lonsize;
    }

    public void setLonsize(long lonsize) {
        this.lonsize = lonsize;
    }

    public long getLatsize() {
        return latsize;
    }

    public void setLatsize(long latsize) {
        this.latsize = latsize;
    }

    public Double[] getData() {
        return data;
    }

    public void setData(Double[] data) {
        this.data = data;
    }

    public String[] getLegendColor() {
        return legendColor;
    }

    public void setLegendColor(String[] legendColor) {
        this.legendColor = legendColor;
    }

    public double[] getlegendValue() {
        return legendValue;
    }

    public void setlegendValue(double[] lengendValue) {
        this.legendValue = lengendValue;
    }

    public String getPolygonExtent() {
        return polygonExtent;
    }

    public void setPolygonExtent(String polygonExtent) {
        this.polygonExtent = polygonExtent;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }
}
