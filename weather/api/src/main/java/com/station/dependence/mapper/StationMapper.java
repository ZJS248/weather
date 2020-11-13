package com.station.dependence.mapper;

import com.station.dependence.entity.StationByTime;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.Map;
import java.util.List;

@Mapper
public interface StationMapper {
    List<Map> getStations();
    List<Map> getTems(@Param("station_id") String station_id, @Param("start") String start, @Param("end") String end);
    List<Map> getAvg(StationByTime station);
}
