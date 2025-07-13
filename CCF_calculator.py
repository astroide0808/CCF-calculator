import cdsapi
import xarray as xr
import numpy as np
import ast
import copy as cp
import math
from datetime import date 
day_coeff = []
latitude = int(input("latitude?="))
longitude = int(input("longitude?="))
starting_date = str(input("input the starting day,month and year in this format : [D,M,Y]"))
ending_date = (input("input the ending day,month and year in this format : [D,M,Y]"))
def date_transform(List):
    i = 0
    List = list(List)
    while List[i] != "]" and i+1 < len(List):
        i += 1
        if List[i] == "0" and (List[i-1] == "," or List[i-1] == "[" ):
            List[i] = ""
    List = ''.join(List)
    return ast.literal_eval(List)
#adapts the visual notations to code
starting_date = date_transform(starting_date)
ending_date = date_transform(ending_date)
temp_date = starting_date
start = 0
day,month,year = temp_date[0],temp_date[1],temp_date[2]
CCF_period = []
CCF_final = 0
def days_between(d1, d2):
    d1 = date(d1[2], d1[1], d1[0])
    d2 = date(d2[2], d2[1], d2[0])
    return abs((d2 - d1).days)
def Daylight(lat,date):
    theta_o = ((days_between([1,1,date[2]],date)-172.5)/365)*2*math.pi
    rad_lat = math.radians(latitude)
    orientation = math.radians(23.4)
    condition = math.atan(1/math.tan(orientation))
    if (rad_lat < condition or rad_lat > -condition) == False :
        theta_1 = -math.acos(-(1/math.tan(rad_lat))*(1/math.tan(orientation)))
        theta_2 = -math.acos((1/math.tan(rad_lat))*(1/math.tan(orientation)))
        theta_3 = math.acos((1/math.tan(rad_lat))*(1/math.tan(orientation)))
        theta_4 = math.acos(-(1/math.tan(rad_lat))*(1/math.tan(orientation)))
    T_var = math.acos(-math.tan(rad_lat)*math.tan(orientation)*math.cos(theta_o))
    if (rad_lat < condition or rad_lat > -condition) :
        return round((24*T_var)/math.pi)
    elif ((theta_o > theta_1 and theta_o < theta_2) or (theta_o > theta_3 and theta_o < theta_4)) :
        return round((24*T_var)/math.pi)
    elif (theta_o > theta_2 and theta_o < theta_3):
        return 24
    else :
        return 0


cycle_d = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]]
if year%4 == 0 :
    cycle_d[1].append(29)
def CCF(date):
    Time_interval = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
                 "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

    Day_period = Daylight(latitude, starting_date)
    if Day_period == 0 :
        return "null"
    Day_p1 = (24 - Day_period) / 2
    Day_p2 = (24 - Day_period) / 2 + 12
    # honestly i copy and pasted line 56
    New_Time_interval = []
    for k, time in enumerate(Time_interval):
        if k < Day_p1 or k > Day_p2:
            New_Time_interval.append(time)
    month = date[1]
    day = date[0]
    year = date[2]
    if month > 9 :
        m = str(month)
    else :
        m = "0"+ str(month)
    if day > 9 :
        d = str(day)
    else :
        d = "0"+ str(day)
    dataset = "reanalysis-era5-pressure-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["fraction_of_cloud_cover"],
        "year": [str(year)],
        "month": [str(m)],
        "day": [str(d)],
        "time": New_Time_interval,
        "pressure_level": [
            "100", "125", "150",
            "175", "200", "225",
            "250", "300", "350",
            "400", "450", "500",
            "550", "600", "650",
            "700", "750", "775",
            "800", "825", "850",
            "875", "900", "925",
            "950", "975", "1000"
        ],
        "data_format": "grib",
        "download_format": "unarchived",
        "area": [latitude+1, longitude-1, latitude-1, longitude+1],  # [N, W, S, E]
    }
    client = cdsapi.Client()
    client.retrieve(dataset, request,target="download.grib")
    # Step 2: Load with xarray + cfgrib
    ds = xr.open_dataset("download.grib", engine="cfgrib", backend_kwargs={"indexpath": ""})
    # Step 3: Access cloud fraction data
    cloud = ds["cc"]  # Replace with correct key if it's not 'cc'
    # Step 4: Extract array
    cloud_array = cloud.values
    np.savetxt("cloud_cover.txt", cloud_array.flatten(), fmt="%.4f")
    # Initial variables
    h = []
    v = []
    CCF_alt_list = []
    CCF_global = 0
    CCF_time = []
    dimension = cloud_array.shape
    # creation of an I matrix of varying dimension using loops
    for i in range(dimension[3]):
        h.append(1)
    for e in range(dimension[2]):
        v.append(h)
    v = np.array(v)
    #daily CCF calculator
    for i in range(dimension[0]):
        product = v
        for b in range(dimension[1]):
            product = product*(v-np.array(cloud_array[i][b]))
        CCF_alt_list = v-product
        CCF_alt_list = np.array(CCF_alt_list)
        CCF_list = 0
        for e in range(CCF_alt_list.shape[0]):
            for a in range(CCF_alt_list.shape[1]):
                CCF_list = CCF_list + CCF_alt_list[e][a]
        CCF_time.append(CCF_list/(dimension[2]*dimension[3]))
    CCF_day = 0
    av = 0
    for i in range(dimension[0]):
        av = av + CCF_time[i]
    CCF_day = av/dimension[0]
    day_coeff.append(dimension[2])
    print(dimension[2])
    return CCF_day*(dimension[2])
while temp_date != ending_date:
    
    if start == 0 :
        start = 1
        C = CCF(temp_date)
        if C == "null" :
            pass
        else :
            CCF_period.append(C)
    
    day += 1
    if day > len(cycle_d[month-1]) :
        day = 1
        month += 1
        if month > 12 :
            month = 1
            year += 1
            if year%4 == 0 :
                if 29 in cycle_d[1] :
                    pass
                else :
                    cycle_d[1].append(29)
            else :
                cycle_d[1].remove(29)
    temp_date = [day, month,year]
    if start == 1 :
        C = CCF(temp_date)
        if C == "null" :
            pass
        else :
            CCF_period.append(C)

#calculates the finals cloud cover factor (CCF)
print(CCF_period)
for i in range(0,len(CCF_period)):
    CCF_final += CCF_period[i]
CCF_final = CCF_final/sum(day_coeff)
print("The CCF of a latitude of",latitude,"and longitude of",longitude,"between",starting_date,"and",ending_date,"is equal to",CCF_final*100,"%")
    
    
