import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import csv
import time
from datetime import datetime
from plotly.tools import FigureFactory as FF

weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',
           'Sunday']

def get_dosed_history_current(data):
    for i in range(len(data)-1, -1, -1):
        try:
            dosed = data[i][2]
            if str(dosed) == '1':
                return 'YES'
            else:
                return 'NO'
        except:
            pass

    return 'NO'

def get_last_csv_datetime(data):
    for i in range(len(data)-1, -1, -1):
        try:
            last_hour = data[i][1]
            last_hour = datetime.strptime(last_hour, '%Y-%m-%d %H:%M:%S')
            return last_hour
        except:
            pass

    return ''

def get_average_values_from_hour(data, required_hour):
    sum_ph = 0
    sum_fc = 0
    count = 0
    required_hour = str(required_hour)

    for i in range(len(data)-1, -1, -1):
        try:
            current_hour = str(datetime.strptime(data[i][1], '%Y-%m-%d %H:%M:%S').hour)
            if current_hour != required_hour:
                break

            sum_ph += round(float(data[i][2]),2)
            sum_fc += round(float(data[i][4]),2)
            count += 1
        except:
            pass

    try:
        avg_ph = round(sum_ph / float(count), 2)
    except:
        avg_ph = 0

    try:
        avg_fc = round(sum_fc / float(count), 2)
    except:
        avg_fc = 0

    return avg_ph, avg_fc

def get_attention_value(avg_ph, avg_fc):
    attention = 'SAFE'

    if avg_ph > 7.8:             #pH > Upper Limit
        attention = 'ATTENTION'

    elif avg_fc > 3:             #FC > Upper Limit
        attention = 'ATTENTION'

    elif avg_ph < 7.2:             #pH < Lower Limit
        attention = 'ATTENTION'

    elif avg_fc < 1:             #FC < Lower Limit
        attention = 'ATTENTION'

    return attention

def make_table():
    print('make table')
    username = 'dosauto'
    api_key = 'fjfbcaeknd'
    py.sign_in(username, api_key)

    today = time.strftime('%A')
    #Generate a matrix 'arr' from the CSV file
    with open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'rU') as f:
        reader_dose = csv.reader((line.replace('\0','') for line in f), delimiter = '\t')
        dose_arr = list(reader_dose)

    # Get the dosed history of current hour
    hasDosed = get_dosed_history_current(dose_arr)

    with open('/home/pi/Desktop/'+ today +'.csv', 'rU') as inp:
        reader = csv.reader((line.replace('\0','') for line in inp), delimiter = '\t')
        data = list(reader)

    # A DateTime object
    last_csv_datetime = get_last_csv_datetime(data)
    if isinstance(last_csv_datetime, str):
        print("Failed to get data from {}".format('/home/pi/Desktop/'+ today +'.csv'))
        return

    avg_ph, avg_fc = get_average_values_from_hour(data, last_csv_datetime.hour)

    attention_value = get_attention_value(avg_ph, avg_fc)

    colorscale =[[0, '#272D31'], [.5, 'ffffff'], [1, '#ffffff']]
    font = []
    font.append('#FCFCFC')              #White font for header

    if attention_value=='ATTENTION':
        font.append('#ff0000')      #Red font for 'DANGER'
    else:
        #font.append('#00ff00')      #Green font for 'SAFE'
        font.append('#006400')	#Darkgreen font for 'SAFE'

    avg_arr = [['Date', 'Time','pH','FC','Dose','SAFE/ATTENTION']]
    avg_arr.append([
        last_csv_datetime.strftime("%d/%m"), str(last_csv_datetime.hour) + ":00", avg_ph, avg_fc, hasDosed, attention_value
    ])

    table = FF.create_table(avg_arr, name=today, colorscale=colorscale, font_colors=font)
    table.layout.update({'title':today})

    #Increase the font size
    for i in range(len(table.layout.annotations)):
        table.layout.annotations[i].font.size = 14

    py.plot(table, filename ='Dosing_Table', auto_open = False)

def get_average_values_for_whole_day(data):
    sum_ph = 0
    sum_fc = 0
    count = 0
    current_date = ""

    for row in data:
        try:
            if current_date == "":
                current_date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

            sum_ph += round(float(row[2]),2)
            sum_fc += round(float(row[4]),2)
            count += 1
        except:
            pass

    try:
        avg_ph = round(sum_ph / float(count), 2)
    except:
        avg_ph = 0

    try:
        avg_fc = round(sum_fc / float(count), 2)
    except:
        avg_fc = 0

    return {
            'date': current_date,
            'ph': avg_ph,
            'fc': avg_fc
            }


def get_dict_all_averages():
    data_as_list = []

    for day in weekday:
        try:
            with open('/home/pi/Desktop/'+ day +'.csv', 'r') as inp:
                reader = csv.reader((line.replace('\0','') for line in inp), delimiter = '\t')
                data = list(reader)

            data_object = get_average_values_for_whole_day(data)
            data_as_list.append(data_object)
        except:
            pass

    # Sort the list by dates
    data_as_list.sort(key=lambda obj: obj['date'])

    return data_as_list

def make_line():
    today = time.strftime('%A')
    print('make line')
    username = 'dosauto'
    api_key = 'fjfbcaeknd'
    py.sign_in(username, api_key)

    data = get_dict_all_averages()

    # If the array is empty
    if not data:
        print("Failed to get data from {}".format('/home/pi/Desktop/'+ today +'.csv'))
        return

    # Create the lists for the line chart
    upper_y_ph = []
    lower_y_ph = []
    upper_y_cl = []
    lower_y_cl = []
    pH = []
    FC = []
    time_list = []

    for obj in data:
        pH.append(obj['ph'])
        FC.append(obj['fc'])
        time_list.append(datetime.strftime(obj['date'], '%a, %d/%m'))
        upper_y_ph.append(7.6)
        lower_y_ph.append(7.2)
        upper_y_cl.append(3)
        lower_y_cl.append(1)

    trace_pH = go.Scatter(
        x = time_list,
        y = pH,
        name = 'pH',
        xaxis='x1', yaxis='y1',
        line = dict(
            width = 3)
    )

    trace_FC = go.Scatter(
        x = time_list,
        y = FC,
        name = 'FC',
        xaxis='x2', yaxis='y2',
        line = dict(
            width = 3)
    )
    trace_upperlim_ph = go.Scatter(
        x = time_list,
        y = upper_y_ph,
        name = 'Upper Limit',
        showlegend = False,
        xaxis='x1', yaxis='y1',
        line = dict(
            color = ('rgb(128, 0, 128)'),
            width = 1,
            dash = 'dash')
    )
    trace_lowerlim_ph = go.Scatter(
        x = time_list,
        y = lower_y_ph,
        name = 'Lower Limit',
        showlegend = False,
        xaxis='x1', yaxis='y1',
        line = dict(
            color = ('rgb(128, 0, 128)'),
            width = 1,
            dash = 'dash')
    )
    trace_upperlim_cl = go.Scatter(
        x = time_list,
        y = upper_y_cl,
        name = 'Upper Limit',
        showlegend = False,
        xaxis='x2', yaxis='y2',
        line = dict(
            color = ('rgb(128, 0, 128)'),
            width = 1,
            dash = 'dash')
    )
    trace_lowerlim_cl = go.Scatter(
        x = time_list,
        y = lower_y_cl,
        name = 'Lower Limit',
        showlegend = False,
        xaxis='x2', yaxis='y2',
        line = dict(
            color = ('rgb(128, 0, 128)'),
            width = 1,
            dash = 'dash')
    )

    figure = plotly.tools.make_subplots(rows=2, cols = 1)

    figure.append_trace(trace_pH, 1,1)
    figure.append_trace(trace_upperlim_ph, 1,1)
    figure.append_trace(trace_lowerlim_ph, 1,1)
    figure.append_trace(trace_FC, 2,1)
    figure.append_trace(trace_upperlim_cl, 2,1)
    figure.append_trace(trace_lowerlim_cl, 2,1)

    py.plot(figure, filename ='Line Graph', auto_open= False)
