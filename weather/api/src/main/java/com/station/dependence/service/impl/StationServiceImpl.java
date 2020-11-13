package com.station.dependence.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.station.dependence.entity.StationByTime;
import com.station.dependence.mapper.StationMapper;
import com.station.dependence.service.StationService;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.List;

@Service
public class StationServiceImpl implements StationService {
    @Autowired
    private StationMapper stationMapper;

    @Override
    public List getStations() throws IOException {
//        List stations=stationMapper.getStations();
        String str=strJSON("C:\\Users\\ZJS\\Desktop\\prepare\\weather\\api\\src\\main\\resources\\json\\station.json");
        JSONObject obj = JSON.parseObject(str);
        List stations= (List) obj.get("RECORDS");
        return stations;
    }
    @Override
    public List getTems(String station_id,String start,String end){
        List tems=stationMapper.getTems(station_id,start,end);
        return tems;
    }

    @Override
    public List getAvg(StationByTime station) {
        List avgTem=stationMapper.getAvg(station);
        return avgTem;
    }
    public String strJSON(String path) throws IOException {
        File file = new File(path);
        InputStreamReader reader = new InputStreamReader(new FileInputStream(file));
        BufferedReader br = new BufferedReader(reader);
        String line = "";
        line = br.readLine();
        String str = "";
        while(line != null) {
            str+=(line);
            line = br.readLine();
        }
        return str;
    }
}
