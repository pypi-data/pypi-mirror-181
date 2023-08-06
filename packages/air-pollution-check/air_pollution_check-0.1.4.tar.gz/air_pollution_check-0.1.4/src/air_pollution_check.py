import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean






 # function 1 - output dataframe
def pollution_level(x):
    """
    This function can add in the overall level to the dataframe.
    
    Parameter
    ----------
    x: dataframe, usually created by the transfer_df function.
    
    Examples
    ----------
    >>> pollution_level(x)
    'dataframe'
    """
    for i in x['no2']:
        if 0 <= i <= 50:
            x['no2_level'] = 5
        if 50 < i <= 100:
            x['no2_level'] = 4
        if 100<i<=200:
            x['no2_level'] = 3
        if 200<i<=400:
            x['no2_level'] = 2
        if 400 < i:
            x['no2_level'] = 1
    for j in x['pm10']:
        if 0 <= j <= 25:
            x['pm10_level'] = 5
        if 25 < j <= 50:
            x['pm10_level'] = 4
        if 50 < j <= 90:
            x['pm10_level'] = 3
        if 90 < j <= 180:
            x['pm10_level'] = 2
        if 180 < j:
            x['pm10_level'] = 1
    for z in x['o3']:
        if 0 <= z <= 60:
            x['o3_level'] = 5
        if 60 < z <= 120:
            x['o3_level'] = 4
        if 120 < z <= 180:
            x['o3_level'] = 3
        if 180 < z <= 240:
            x['o3_level'] = 2
        if 240 < z:
            x['o3_level'] = 1       
    for p in x['pm2_5']:
        if 0 <= p <= 15:
            x['pm2.5_level'] = 5
        if 15 < p <= 30:
            x['pm2.5_level'] = 4
        if 30 < p <= 55:
            x['pm2.5_level'] = 3
        if 55 < p <= 110:
            x['pm2.5_level'] = 2
        if 110 < p:
            x['pm2.5_level'] = 1        
    x['total_level'] = (x['no2_level']+x['pm10_level']+x['o3_level']+x['pm2.5_level'])       
    x["avg_level"] = x['total_level']/4
    for v in x["avg_level"]:
        if 4 < v <= 5:
            x['avg_level'] = 'good'
        if 3 < v<= 4:
            x['avg_level'] = 'fair'
        if 2 < v <= 3:
            x['avg_level'] = 'moderate'
        if 1 < v <= 2:
            x['avg_level'] = 'poor'
        if 0 <= v <= 1:
            x['avg_level'] = 'very poor'   
    return x


def transfer_df(lat, lon, x = 'current', start = 1606488670, end = 1606747870):
    """
    This function can transfer the air pollution data output into dataframes.
    
    Parameter
    ----------
    lat: Geographical coordinates (latitude)
    lon: Geographical coordinates (lontitude)
    x: can only be 'current', 'forcast', and 'history', to determine whether you want to view the level in the past or in the future.
    
    Examples
    ----------
    >>> transfer_df(10,10)
    'dataframe'
    """   
    assert x != ['current','forcast','history'], "Your function cannot be called because CFT has to equals to 'current', 'forcast', or 'history'." 
    assert lon < 181, "Your lontitude has above the range."
    assert lat < 91, "Your latitude has abouve the range."
    assert start != int, "Your start value has to be integers."
    assert end != int, "Your end value has to be integers."
    
    key = '8acef062b251740191e9cbf7dff998b9'
    if x == 'current':
        r = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}')
        r_text = r.text
        response = json.loads(r_text)
        re = response['list']
        current_info = []
        for i in re:
            current_info.append(i['components'])   
        current_list = []
        for info in response['list']:
            current_list.append(info)
        current_df = pd.DataFrame(data=current_info)
        current_df['lat'] = lat
        current_df['lon'] = lon
        x = current_df
        return pollution_level(x)    
    if x == 'forcast':
        r_forcast = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={key}')
        r_forcast_text = r_forcast.text
        response2 = json.loads(r_forcast_text)
        re2 = response2['list']
        future_info = []
        for i in re2:
            future_info.append(i['components'])
    
        future_list = []
        for info in response['list']:
            future_list.append(info)

        future_df = pd.DataFrame(data=future_info)
        future_df['lat'] = lat
        future_df['lon'] = lon
        x = future_df
        return pollution_level(x)    
    if x == 'history':
        r_hist = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={key}')
        r_hist_text = r_hist.text
        response3 = json.loads(r_hist_text)
        re3 = response3['list']        
        history_info = []
        for i in re3:
            history_info.append(i['components'])    
        history_list = []
        for info in response['list']:
            history_list.append(info)
        history_df = pd.DataFrame(data=history_info)
        history_df['lat'] = lat
        history_df['lon'] = lon
        x = history_df
        return pollution_level(x)
    
 



 # function 2 - overall pollution level
def current_pollution(x):
    x = pollution_level(x)
    x = int(x['total_level'] / 4)
    if x == 5:
        x = 'good'
    if x == 4:
        x = 'fair'
    if x == 3:
        x = 'moderate'
    if x == 2:
        x = 'poor'
    if x == 1:
        x = 'very poor'
    return x

def FutureAndHist_pollution(y):
    future_df = pollution_level(y)
    future_total_avg = sum(future_df['total_level'])/len(future_df)
    future_avg = int(future_total_avg / 4)
    if future_avg == 5:
        future_avg = 'good'
    if future_avg == 4:
        future_avg = 'fair'
    if future_avg == 3:
        future_avg = 'moderate'
    if future_avg == 2:
        future_avg = 'poor'
    if future_avg == 1:
        future_avg = 'very poor'
    return future_avg


def overall_pollution_level(lat, lon, CFT = 'current', start = 0, end = 0):
    """
    This function can help to detect your current, future, or history overall air pollution level.
    
    Parameter
    ----------
    lat: Geographical coordinates (latitude)
    lon: Geographical coordinates (lontitude)
    CFT: can only be 'current', 'forcast', and 'history', to determine whether you want to view the level in the past or in the future.
    start: Start date (unix time, UTC time zone), e.g. start=1606488670, only used when CFT = 'history'
    end: End date (unix time, UTC time zone), e.g. end=1606747870, only used when CFT = 'history'
    
    Examples
    ----------
    >>> overall_pollution_level(lon=180,lat=88.7,CFT='history', start = 1606488670, end = 1606747870)
    'good'
    """
    
    
    assert CFT != ['current','forcast','history'], "Your function cannot be called because CFT has to equals to 'current', 'forcast', or 'history'." 
    assert lon < 181, "Your lontitude has above the range."
    assert lat < 91, "Your latitude has abouve the range."
    
    key = '8acef062b251740191e9cbf7dff998b9'
    
    if CFT == 'current':
        r = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}')
        r_text = r.text
        response = json.loads(r_text)
        re = response['list']
        current_info = []
        for i in re:
            current_info.append(i['components'])
    
        current_list = []
        for info in response['list']:
            current_list.append(info)

        current_df = pd.DataFrame(data=current_info)
        current_df['lat'] = lat
        current_df['lon'] = lon
        current_level = current_pollution(current_df)
        return "current overall air pollution level for lon = {} and lat = {} is {}.".format(lat, lon, current_level)
    
    if CFT == 'forcast':
        r_forcast = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={key}')
        r_forcast_text = r_forcast.text

        response2 = json.loads(r_forcast_text)
        re2 = response2['list']
        future_info = []
        for i in re2:
            future_info.append(i['components'])
    
        future_list = []
        for info in response2['list']:
            future_list.append(info)

        future_df = pd.DataFrame(data=future_info)
        future_df['lat'] = lat
        future_df['lon'] = lon
        future_level = FutureAndHist_pollution(future_df)
        return "future overall air pollution level for lon = {} and lat = {} is {}.".format(lat, lon, future_level)
    
    if CFT == 'history':
        r_hist = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={key}')
        r_hist_text = r_hist.text

        response3 = json.loads(r_hist_text)
        re3 = response3['list']
    
        history_info = []
        for i in re3:
            history_info.append(i['components'])
    
        history_list = []
        for info in response3['list']:
            history_list.append(info)

        history_df = pd.DataFrame(data=history_info)
        history_df['lat'] = lat
        history_df['lon'] = lon
        history_level = FutureAndHist_pollution(history_df)
        return "history overall air pollution level for lon = {} and lat = {} from {} to {} is {}.".format(lat, lon, start, end, history_level)



    
    
# function 3 - visualization
def visualization(lat, lon, CFT = 'overall', start = 1606488670, end = 1606747870):
    """
    This function can visualize the future, history, or overall air pollution level among time, it is created for having a overlook of the pollution chages.
    
    Parameter
    ----------
    lat: Geographical coordinates (latitude)
    lon: Geographical coordinates (lontitude)
    CFT: can only be 'current', 'forcast', and 'history', to determine whether you want to view the level in the past or in the future.
    start: Start date (unix time, UTC time zone), e.g. start=1606488670, only used when CFT = 'history'
    end: End date (unix time, UTC time zone), e.g. end=1606747870, only used when CFT = 'history'
    
    Examples
    ----------
    >>> visualization(lat = 10, lon = 10)
    'graph'
    """
    
    assert CFT != ['overall','forcast','history'], "Your function cannot be called because CFT has to equals to 'current', 'forcast', or 'history'." 
    assert lon < 181, "Your lontitude has above the range."
    assert lat < 91, "Your latitude has abouve the range."
    assert start != int, "Your start value has to be integers."
    assert end != int, "Your end value has to be integers."
    
    key = '8acef062b251740191e9cbf7dff998b9'
    
    if CFT == 'overall':
        r_forcast = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={key}')
        r_forcast_text = r_forcast.text
        response2 = json.loads(r_forcast_text)
        re2 = response2['list']
        future_info = []
        for i in re2:
            future_info.append(i['components'])
        future_list = []
        for info in response2['list']:
            future_list.append(info)
        future_df = pd.DataFrame(data=future_info)
        future_df['lat'] = lat
        future_df['lon'] = lon
        
        r = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}')
        r_text = r.text
        response = json.loads(r_text)
        re = response['list']
        current_info = []
        for i in re:
            current_info.append(i['components'])
        current_list = []
        for info in response['list']:
            current_list.append(info)
        current_df = pd.DataFrame(data=current_info)
        current_df['lat'] = lat
        current_df['lon'] = lon
        
        r_hist = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={key}')
        r_hist_text = r_hist.text
        response3 = json.loads(r_hist_text)
        re3 = response3['list']
        history_info = []
        for i in re3:
            history_info.append(i['components'])
        history_list = []
        for info in response3['list']:
            history_list.append(info)
        history_df = pd.DataFrame(data=history_info)
        history_df['lat'] = lat
        history_df['lon'] = lon
        
        history_level = pollution_level(history_df)
        forcast_level = pollution_level(future_df)
        current_level = pollution_level(current_df)
        
        overall = pd.concat([history_level, current_level, forcast_level], ignore_index = True)
        
        plt.plot(overall['co'],label = 'co')
        plt.plot(overall['no'], label = 'no')
        plt.plot(overall['no2'], label = 'no2')
        plt.plot(overall['o3'], label = 'o3')
        plt.plot(overall['so2'], label = 'so2')
        plt.plot(overall['pm2_5'], label = 'pm2_5')
        plt.plot(overall['pm10'], label = 'pm10')
        plt.plot(overall['nh3'], label = 'nh3')
        plt.xlabel("days")
        plt.ylabel("Pollutant concentration in μg/m3")
        plt.legend()
        plt.show()

        
    if CFT == 'history':
        r_hist = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={key}')
        r_hist_text = r_hist.text
        response3 = json.loads(r_hist_text)
        re3 = response3['list']
        history_info = []
        for i in re3:
            history_info.append(i['components'])
        history_list = []
        for info in response3['list']:
            history_list.append(info)
        history_df = pd.DataFrame(data=history_info)
        history_df['lat'] = lat
        history_df['lon'] = lon
        
        history_level = pollution_level(history_df)
        
        plt.plot(history_level['co'],label = 'co')
        plt.plot(history_level['no'], label = 'no')
        plt.plot(history_level['no2'], label = 'no2')
        plt.plot(history_level['o3'], label = 'o3')
        plt.plot(history_level['so2'], label = 'so2')
        plt.plot(history_level['pm2_5'], label = 'pm2_5')
        plt.plot(history_level['pm10'], label = 'pm10')
        plt.plot(history_level['nh3'], label = 'nh3')
        plt.xlabel("days")
        plt.ylabel("Pollutant concentration in μg/m3")
        plt.legend()
        plt.show()
        
        
    if CFT == 'forcast':
        r_forcast = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={key}')
        r_forcast_text = r_forcast.text
        response2 = json.loads(r_forcast_text)
        re2 = response2['list']
        future_info = []
        for i in re2:
            future_info.append(i['components'])
        future_list = []
        for info in response2['list']:
            future_list.append(info)
        future_df = pd.DataFrame(data=future_info)
        future_df['lat'] = lat
        future_df['lon'] = lon
        
        forcast_level = pollution_level(future_df)
        
        plt.plot(forcast_level['co'],label = 'co')
        plt.plot(forcast_level['no'], label = 'no')
        plt.plot(forcast_level['no2'], label = 'no2')
        plt.plot(forcast_level['o3'], label = 'o3')
        plt.plot(forcast_level['so2'], label = 'so2')
        plt.plot(forcast_level['pm2_5'], label = 'pm2_5')
        plt.plot(forcast_level['pm10'], label = 'pm10')
        plt.plot(forcast_level['nh3'], label = 'nh3')
        plt.xlabel("days")
        plt.ylabel("Pollutant concentration in μg/m3")
        plt.legend()
        plt.show()
        
        
        

        
# function 4: comparison
def air_comparison_v1(lat, lon, start = 1606488670, end = 1606747870, col = "no"):
    
    assert lon < 181, "Your lontitude has above the range."
    assert lat < 91, "Your latitude has abouve the range."
    assert start != int, "Your start value has to be integers."
    assert end != int, "Your end value has to be integers."
    
    future_level = transfer_df(lat,lon)
    history_level = transfer_df(lat,lon,start,end)
        
    if mean(forcast_level[col]) > mean(hist_pollution_level[col]):
        return f'The {col} for this location will be increasing in the future'
    if mean(forcast_level[col]) < mean(hist_pollution_level[col]):
        return f'The {col} for this location will be decreasing in the future'
    if mean(forcast_level[col]) == mean(hist_pollution_level[col]):
        return f'The {col} for this location will stay the same in the future'
    
def comparison(lat, lon, start = 1606488670, end = 1606747870):
    
    assert lon < 181, "Your lontitude has above the range."
    assert lat < 91, "Your latitude has abouve the range."
    assert start != int, "Your start value has to be integers."
    assert end != int, "Your end value has to be integers."
    
    col_list = ['co','no','no2','o3','so2','pm2_5','pm10','nh3','total_level']
    x = []
    for i in col_list:
        x.append(air_comparison_v1(lat, lon, start = 1606488670, end = 1606747870, col = i))
    return x
    
