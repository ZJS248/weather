import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate as intp
import pymysql
import os
import copy
from datetime import datetime,timedelta
#格点插值成站点函数
def grid_to_station(grid, station):
    '''
    inputs: 
        grid,形式为：[grid_lon,grid_lat,data] 即[经度网格，纬度网格，数值网格]
        station:[station_lon,station_lat]站点经度, 站点纬度。
    '''    
    lon = grid[0]
    lat = grid[1]
    data = grid[2]
    func=intp.interp2d(lon,lat,data)
    return func(station[0],station[1])
def getTime(filename):
    filetime=filename[:10]#起报时间(字符串)
    hour=filename[-6:-3]#预报时效
    birthtime=datetime.strptime(filetime,"%Y%m%d%H")+timedelta(hours=8)#起报时间
    pretime=birthtime+timedelta(hours=int(hour))#预报时间
    return [birthtime,pretime,int(hour)]
#连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='zjs',
    charset='utf8',
    # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
)
cur = conn.cursor()
stations=[]
query = "select * from station"
result = cur.execute(query)
info = cur.fetchall() 
for point in info:
    stations.append([point[1],point[2],float(point[3]),float(point[4])])#站点id,站点名字,站点经，纬度

result=cur.execute('select birthtime from ec order by birthtime desc LIMIT 1;')
if result==0:
    last_str=datetime.strftime((datetime.now()-timedelta(days=3,hours=8)),'%Y%m%d%H')
else:
    last_time=cur.fetchall()[0][0]
    last_str=datetime.strftime((last_time-timedelta(hours=8)),'%Y%m%d%H')

#读取文件
sql_ec='insert into ec(station_id,station_name,Lon,Lat,TEM,RHU,PRE,PRS,birthtime,pretime) values '
sql_tem='insert into ec_tem(station_id,station_name,Lon,Lat,TEM_Max_24h,TEM_Min_24h,birthtime,pretime) values '
print('running...')
limit=84
for mondir in os.listdir('./data'):
    if mondir<last_str[4:6]:
        continue
    for daydir in os.listdir('./data/'+mondir):
        print(daydir)
        print(last_str)
        print(daydir<=last_str)
        if daydir<=last_str:
            continue
        data={}
        tems={}
        for station in stations:
            print(station[1])
            for file in os.listdir('./data/'+mondir+'/'+daydir+'/PRMSL'):#压强
                times=getTime(file)
                if times[2]>limit:
                    break                
                ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/PRMSL/'+file)
                data[str(times[1])]=data[str(times[1])] if str(times[1]) in data else {}
                data[str(times[1])][station[1]]=data[str(times[1])][station[1]] if station[1] in data[str(times[1])] else {}
                value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                data[str(times[1])][station[1]]['PRS']=value[0]
                
                data[str(times[1])][station[1]]['station_id']=station[0]
                data[str(times[1])][station[1]]['station_name']=station[1]
                data[str(times[1])][station[1]]['Lon']=station[2]
                data[str(times[1])][station[1]]['Lat']=station[3]
                data[str(times[1])][station[1]]['birthtime']=str(times[0])
                data[str(times[1])][station[1]]['pretime']=str(times[1])
                data[str(times[1])][station[1]]['PRE']='0'#设置当时时刻降雨初始值
            for file in os.listdir('./data/'+mondir+'/'+daydir+'/T2'):  #2M温度         
                times=getTime(file)
                if times[2]>limit:
                    break                
                ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/T2/'+file)
                data[str(times[1])]=data[str(times[1])] if str(times[1]) in data else {}
                data[str(times[1])][station[1]]=data[str(times[1])][station[1]] if station[1] in data[str(times[1])] else {}
                value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                data[str(times[1])][station[1]]['TEM']=value[0]
                
            for file in os.listdir('./data/'+mondir+'/'+daydir+'/RAIN03'): #降雨 
                times=getTime(file)
                if times[2]>limit:
                    break
                if times[2]<=72:
                    ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/RAIN03/'+file)
                    data[str(times[1])]=data[str(times[1])] if str(times[1]) in data else {}
                    data[str(times[1])][station[1]]=data[str(times[1])][station[1]] if station[1] in data[str(times[1])] else {}
                    value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                    data[str(times[1])][station[1]]['PRE']=value[0]
                else:
                    break
            for file in os.listdir('./data/'+mondir+'/'+daydir+'/RAIN06'): #降雨 
                times=getTime(file)
                if times[2]>limit:
                    break
                if times[2]>72:
                    ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/RAIN06/'+file)
                    data[str(times[1])]=data[str(times[1])] if str(times[1]) in data else {}
                    data[str(times[1])][station[1]]=data[str(times[1])][station[1]] if station[1] in data[str(times[1])] else {}
                    value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                    data[str(times[1])][station[1]]['PRE']=value[0]
                else:
                    continue
                
            for file in os.listdir('./data/'+mondir+'/'+daydir+'/RH/1000'): #湿度
                times=getTime(file)
                if times[2]>limit:
                    break                
                ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/RH/1000/'+file)
                data[str(times[1])]=data[str(times[1])] if str(times[1]) in data else {}
                data[str(times[1])][station[1]]=data[str(times[1])][station[1]] if station[1] in data[str(times[1])] else {}
                value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                data[str(times[1])][station[1]]['RHU']=value[0]
            '''
            当天最大最小温度⬇
            '''
            t_min=100
            t_max=-273
            for index,file in enumerate(os.listdir('./data/'+mondir+'/'+daydir+'/TMAX2')): #当天最小温度 
                times=getTime(file)
                if times[2]>limit:
                    break
                daytime=datetime.strftime(times[1],"%Y-%m-%d")
                ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/TMAX2/'+file)
                tems[daytime]=tems[daytime] if daytime in tems else {}
                tems[daytime][station[1]]=tems[daytime][station[1]] if station[1] in tems[daytime] else {}
                value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                if np.isnan(value):
                    continue
                if index%4==0 or value>t_max:
                    t_max=value[0]
                tems[daytime][station[1]]['TMAX2']=t_max
                tems[daytime][station[1]]['station_id']=station[0]
                tems[daytime][station[1]]['station_name']=station[1]
                tems[daytime][station[1]]['Lon']=station[2]
                tems[daytime][station[1]]['Lat']=station[3]
                tems[daytime][station[1]]['birthtime']=str(times[0])
                tems[daytime][station[1]]['pretime']=daytime
            for index,file in enumerate(os.listdir('./data/'+mondir+'/'+daydir+'/TMIN2')): #当天最大温度 
                times=getTime(file)
                if times[2]>limit:
                    break
                daytime=datetime.strftime(times[1],"%Y-%m-%d")
                ds=xr.open_dataset('./data/'+mondir+'/'+daydir+'/TMIN2/'+file)
                tems[daytime]=tems[daytime] if daytime in tems else {}
                tems[daytime][station[1]]=tems[daytime][station[1]] if station[1] in tems[daytime] else {}
                value=grid_to_station([ds.lon,ds.lat,ds.Var[0]],[station[2],station[3]])
                if np.isnan(value):
                    continue
                if index%4==0 or value<t_min:
                    t_min=value[0]
                tems[daytime][station[1]]['TMIN2']=t_min
            #break#station
# =============================================================================
#往数据库插入ec预报数据
# =============================================================================        
        insert_ec=[]
        for day in data:
            for point in data[day]:
                station=[]
                station.append(data[day][point]['station_id'])
                station.append(data[day][point]['station_name'])
                station.append(data[day][point]['Lon'])
                station.append(data[day][point]['Lat'])
                station.append(data[day][point]['TEM'])
                station.append(data[day][point]['RHU'])
                station.append(data[day][point]['PRE'])
                station.append(data[day][point]['PRS'])
                station.append(data[day][point]['birthtime'])
                station.append(data[day][point]['pretime'])
                insert_ec.append('('+','.join(("'%s'" %id for id in station))+')')
        # print (sql_ec+','.join(insert_ec))  
        try:
            cur.execute(sql_ec+','.join(insert_ec))
            conn.commit()
            print("插入数据成功;")
        except Exception as e:
            print("插入数据失败:", e)    
# =============================================================================
#往数据库插入温度数据
# =============================================================================
        insert_tem=[]
        for day in tems:
            for point in tems[day]:
                station=[]
                station.append(tems[day][point]['station_id'])
                station.append(tems[day][point]['station_name'])
                station.append(tems[day][point]['Lon'])
                station.append(tems[day][point]['Lat'])
                station.append(tems[day][point]['TMAX2'])
                station.append(tems[day][point]['TMIN2'])
                station.append(tems[day][point]['birthtime'])
                station.append(tems[day][point]['pretime'])
                insert_tem.append('('+','.join(("'%s'" %id for id in station))+')')
        # print (sql_tem+','.join(insert_tem))      
        try:
            cur.execute(sql_tem+','.join(insert_tem))
            conn.commit()
            print("插入数据成功;")
        except Exception as e:
            print("插入数据失败:", e)          
        break#daydir
    break#mondir

