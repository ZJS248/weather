package com.station.dependence.service;

import com.station.dependence.entity.StationByTime;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.List;

public interface StationService {
    List getStations() throws IOException;

    List getTems(String station_id,String start,String end);

    List getAvg(StationByTime station);
}
