package com.station.dependence;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.station.dependence.mapper")
public class StationApplication {
    public static void main(String[] args) {
        SpringApplication.run(StationApplication.class, args);
    }
}
