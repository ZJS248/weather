package com.station.dependence.controller;

import com.station.dependence.entity.GridLayer;
import com.station.dependence.entity.StationByTime;
import com.station.dependence.service.StationService;
import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ucar.ma2.InvalidRangeException;
import ucar.nc2.Attribute;
import ucar.nc2.NetcdfFile;
import ucar.nc2.Variable;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.List;
import java.util.Map;


@RestController
@RequestMapping("")
public class StationController {
    @Autowired
    private StationService stationService;
    @GetMapping("view/stationlist")
    public List getStations() throws IOException {
        List stations = stationService.getStations();
        return stations;
    }
    @GetMapping("view/templist")
    public List getTems(String station_id,String start,String end){
        List tems= stationService.getTems(station_id,start,end);
        return tems;
    }
    @PostMapping("view/avglist")
    public List getAVGTem(@RequestBody StationByTime station){
        List avgTem=stationService.getAvg(station);
        return avgTem;
    }
    @GetMapping("view/axisTime")
    public String getFileName(String date){

        File file = new File("C:\\Users\\ZJS\\Desktop\\新建文件夹\\代码\\python\\预报读取\\ec\\data");		//获取其file对象
        File[] fs = file.listFiles();	//遍历path下的文件和目录，放在File数组中
        File dir = new File(String.valueOf(fs[fs.length-1]));
        File[] root = dir.listFiles();
        String filehead=String.valueOf(root[root.length-1]).split("\\\\")[String.valueOf(root[root.length-1]).split("\\\\").length-1];
        return filehead;
    }
    @GetMapping("view/temGrid")
    public GridLayer getGrid(String date) throws IOException, InvalidRangeException {
        File file = new File("C:\\Users\\ZJS\\Desktop\\新建文件夹\\代码\\python\\预报读取\\ec\\data");		//获取其file对象
        File[] fs = file.listFiles();	//遍历path下的文件和目录，放在File数组中
        File dir = new File(String.valueOf(fs[fs.length-1]));
        File[] root = dir.listFiles();
        String filehead=String.valueOf(root[root.length-1]).split("\\\\")[String.valueOf(root[root.length-1]).split("\\\\").length-1];

        NetcdfFile nc= NetcdfFile.open(root[root.length-1]+"\\T2\\"+date+".nc");
        Variable lons=nc.findVariable("lon");
        Variable lats=nc.findVariable("lat");
        Variable time=nc.findVariable("time");
        Variable var=nc.findVariable("Var");
        Double add_offset= (Double) var.findAttribute("add_offset").getNumericValue();
        Double scale_factor= (Double) var.findAttribute("scale_factor").getNumericValue();
        short[] values = (short[]) var.read().copyTo1DJavaArray();
        Double[] vals=new Double[values.length];
        for(int i=0;i<values.length;i++){
            vals[i]= ((values[i]*scale_factor)+add_offset);
        }
        GridLayer grid=new GridLayer();
        grid.setLonsize(lons.getSize());
        grid.setLatsize(lats.getSize());
        grid.setStartlon(lons.read(String.valueOf(0)).getDouble(0));
        grid.setEndlon(lons.read(String.valueOf(lons.getSize()-1)).getDouble(0));
        grid.setStartlat(lats.read(String.valueOf(0)).getDouble(0));
        grid.setEndlat(lats.read(String.valueOf(lats.getSize()-1)).getDouble(0));
        grid.setData(vals);
        grid.setlegendValue(new double[]{-40.0, -34.285714285714285, -28.57142857142857, -22.857142857142858, -17.142857142857142, -11.428571428571427, -5.714285714285715, 0.0, 5.714285714285715, 11.42857142857143, 17.142857142857146, 22.85714285714286, 28.57142857142857, 34.28571428571429, 40.0, 45.71428571428572});
        grid.setLegendColor(new String[]{"#0000ff", "#1900e6", "#3200cd", "#4b00b4", "#64009b", "#7d0082", "#960069", "#af0050", "#c80037", "#e1001e", "#fa0005"});
        grid.setPolygonExtent("-9.999992,0.000000,80.000008,180.000000");
        grid.setMissingValue(0);
        return grid;
    }
}
