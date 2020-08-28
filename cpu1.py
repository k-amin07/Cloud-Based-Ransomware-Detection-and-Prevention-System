# https://github.com/giampaolo/psutil
import psutil
import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib.parse import urlencode
from urllib.request import urlopen
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import zipfile
from win10toast import ToastNotifier
import win32api
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
import time
from decimal import *
from os.path import expanduser


def get_drives():
    drives = expanduser("~")
    return drives


def upload(data):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file5 = drive.CreateFile()
    file5.SetContentFile(data)
    file5.Upload()  # Upload the file.


def process_info():
    #file = open("results.json", "a")
    url = 'https://fyp-cbrdp.herokuapp.com/process'
    machineID = 'undefined'
    while(1):

        processes = psutil.pids()
        length = len(psutil.pids())
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_usage = psutil.cpu_percent(interval=1)
        i=0
        try:
            while (i < length):
                try:
                    p = psutil.Process(processes[i])
                    attr = p.as_dict(
                        attrs=['io_counters', 'memory_percent', 'name'])

                    io_counterss = str(attr['io_counters'])
                    mem_percent = str(attr['memory_percent'])
                    p_name = str(attr['name'])

                    # disk input output counters till next comment
                    counters = io_counterss.split("(")
                    io_counterss = counters[1]
                    counters = io_counterss.split(")")
                    io_counterss = counters[0]
                    counters = io_counterss.split(",")
                    one = counters[0]
                    two = counters[1]
                    three = counters[2]
                    four = counters[3]

                    one = one.split("=")
                    two = two.split("=")
                    three = three.split("=")
                    four = four.split("=")

                    read_count = one[1]
                    write_count = two[1]
                    read_bytes = three[1]
                    write_bytes = four[1]

                    # end of above comments
                    names_list.append(p_name)
                    mem_percent_list.append(float(mem_percent))
                    read_bytes_list.append(int(read_bytes))
                    read_count_list.append(int(read_count))
                    write_bytes_list.append(int(write_bytes))
                    write_count_list.append(int(write_count))
                    i=i+1
                except Exception as error:
                    i=i+1
                    print(error)


            total_names=len(names_list)
            mem_percent=sum(mem_percent_list)
            read_bytes=sum(read_bytes_list)
            read_count=sum(read_count_list)
            write_bytes=sum(write_bytes_list)
            write_count=sum(write_count_list)

            names_list.clear()
            mem_percent_list.clear()
            read_bytes_list.clear()
            read_count_list.clear()
            write_bytes_list.clear()
            write_count_list.clear()


            dictionary['total_process']=total_names
            dictionary['memory_percent']=mem_percent
            dictionary['read_bytes']=read_bytes
            dictionary['read_count']=read_count
            dictionary['write_bytes']=write_bytes
            dictionary['write_count']=write_count
            dictionary['cpu_usage']=cpu_usage
            dictionary['ransomware_active']=0
            json_data = json.dumps(dictionary, ensure_ascii=False, indent=4)
            data = json.loads(json_data)
            payload = data
            try:
                r = requests.post(url, data=payload)
                print(r.status_code)
            except Exception as error:
                print(error)
                i = i + 1

        except Exception as error:
                i = i + 1


def machine_id():
    machineID = os.popen('wmic DISKDRIVE get SerialNumber').read()
    machineID_list = machineID.split("\n")
    # print(machineID)
    i = 1
    while (i < len(machineID_list)):
        if machineID_list[i]:
            machineID = machineID_list[i]
            i = i + 1
        else:
            i = i + 1
    # print(machineID)
    machineID = machineID.split(" ")
    machineID = machineID[0]
    return machineID


def get_processHistory():
    machineID = 'undefined'
    url = 'https://fyp-cbrdp.herokuapp.com/getAllProcess'
    dic = dict()
    dic['id'] = machineID
    json_data = json.dumps(dic, ensure_ascii=False)
    python_obj = json.loads(json_data)
    payload = python_obj
    try:
        r = requests.post(url, data=payload)

    except Exception as error:
        print(error)

    json_data = r.content
    data = json.loads(json_data)
    history_data = json.dumps(data, indent=2, sort_keys=True)
    return history_data


def data_local_storage():
    #storing from online server to csv file
    csv_file = open('info.csv', 'w', newline='')
    fieldnames = ['id', 'memory_percent', 'name_to_int' , 'name', 'num_handles', 'num_threads', 'read_bytes', 'read_count',
                  'write_bytes', 'write_count', 'cpu_usage', 'num_connections', 'ransomware_active']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    process = get_processHistory()
    process_dict = dict()
    process_dict = json.loads(process)
    keys1 = list(process_dict.keys())

    i = 0
    process_name_list = []
    while (i < len(keys1)):
        temp1 = keys1[i]
        p_name = process_dict[temp1]
        process_name_list.append(p_name['name'])
        i = i + 1

    # converting name into integers

    name_set = set(process_name_list)
    unique_name = list(name_set)
    name_integer_mapping = dict()
    modified_names = []

    for i in range(0, len(unique_name)):
        temp = unique_name[i]
        name_integer_mapping[temp] = i

    name_int_mapping_file=open("name_int_mapping_file.txt","w")
    json.dump(name_integer_mapping,name_int_mapping_file)
    name_int_mapping_file.close()
    # writing names to integer mapping in csv file
    i = 0
    while (i < len(keys1)):
        temp1 = keys1[i]
        process_info_dict = process_dict[temp1]   #multiple process info to single process info conversion
        temp2 = process_info_dict['name']

        process_info_dict['name_to_int'] = name_integer_mapping[temp2]
        writer.writerow(process_info_dict)
        i = i + 1


def temp():
    #pushing from json file to online server
    url = 'https://fyp-cbrdp.herokuapp.com/process'
    file = open("results.json").read()
    list_of_json = file.split("}")

    for i in range(0, len(list_of_json)):
        temp = list_of_json[i] + '}'
        # print(temp)
        try:
            dictionary = json.loads(temp)
            payload = dictionary

            try:
                r = requests.post(url, data=payload)
                print(r.status_code)
            except Exception as error:
                print(error)

        except Exception as error:
            print(error)


#ignored because used in initial data gathering
def temp2():
    #retre
    csv_file = open('data.csv', 'w', newline='')
    fieldnames = ['total_process', 'memory_percent', 'read_bytes', 'read_count',
                  'write_bytes', 'write_count', 'cpu_usage', 'ransomware_active']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    dictionary=dict()
    file=open("info.csv","r")
    reader=csv.reader(file)

    ram_percent=[]
    byte_read=[]
    byte_write=[]
    count_read=[]
    count_write=[]
    cpu_usage=[]
    process_count=0
    flag=0
    ransomware_flag=0

    for row in reader:
        if row[2]=='3':
            if flag==1:
                dictionary['memory_percent']=sum(ram_percent)
                dictionary['read_bytes']=sum(byte_read)
                dictionary['write_bytes']=sum(byte_write)
                dictionary['read_count']=sum(count_read)
                dictionary['write_count']=sum(count_write)
                dictionary['cpu_usage']=sum(cpu_usage)
                dictionary['total_process']=process_count
                dictionary['ransomware_active']=ransomware_flag
                writer.writerow(dictionary)
                process_count=0


                ram_percent.clear()
                byte_read.clear()
                byte_write.clear()
                count_read.clear()
                count_write.clear()
                cpu_usage.clear()
        else:
            process_count=process_count+1
            #print(row[1])
            ram_percent.append(Decimal(row[1]))
            byte_read.append(int(row[6]))
            byte_write.append(int(row[8]))
            count_read.append(int(row[7]))
            count_write.append(int(row[9]))
            cpu_usage.append(Decimal(row[10]))
            ransomware_flag=int(row[12])
            flag=1

def local():
    #for the formation of a csv file from a json file of the data which is gathered during testing. because many ransomwares do not encrypt the json files
    json_file=open("temp.json","r").read()
    csv_file=open("datas.csv","w",newline='')
    fields=['total_process', 'memory_percent', 'read_bytes', 'read_count',
                  'write_bytes', 'write_count', 'cpu_usage', 'ransomware_active']
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()


    list_of_json = json_file.split("}")

    for i in range(0, len(list_of_json)):
        temp = list_of_json[i] + '}'
        # print(temp)
        try:
            dictionary = json.loads(temp)
            writer.writerow(dictionary)
        except Exception as error:
            print(error)


def machine_learning():
    json_file=open("temp.json","w")

    #reading the data
    dataset = pd.read_csv('data.csv')

    X = dataset.iloc[:, [0, 1, 2, 3, 4, 5, 6]].values
    y = dataset.iloc[:, 7].values
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    #
    sc = StandardScaler()
    X_train = sc.fit_transform(X)
    X_test = sc.transform(X_test)

    #classifying the data using decision tree classifier
    classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)


    dictionary=dict()
    names_list=[]
    mem_percent_list=[]
    read_bytes_list=[]
    read_count_list=[]
    write_bytes_list=[]
    write_count_list=[]
    array=[]

    while(1):
        #getting the live data from computer
        processes = psutil.pids()
        length = len(psutil.pids())

        #cpu usage data
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_usage = psutil.cpu_percent(interval=1)

        i=0
        try:
            while (i < length):
                try:

                    #getting process data
                    p = psutil.Process(processes[i])
                    attr = p.as_dict(
                        attrs=['io_counters', 'memory_percent', 'name'])

                    io_counterss = str(attr['io_counters'])
                    mem_percent = str(attr['memory_percent'])
                    p_name = str(attr['name'])

                    # disk input output counters till next comment
                    counters = io_counterss.split("(")
                    io_counterss = counters[1]
                    counters = io_counterss.split(")")
                    io_counterss = counters[0]
                    counters = io_counterss.split(",")
                    one = counters[0]
                    two = counters[1]
                    three = counters[2]
                    four = counters[3]

                    one = one.split("=")
                    two = two.split("=")
                    three = three.split("=")
                    four = four.split("=")

                    read_count = one[1]
                    write_count = two[1]
                    read_bytes = three[1]
                    write_bytes = four[1]

                    # parsing the data into readable format
                    names_list.append(p_name)
                    mem_percent_list.append(float(mem_percent))
                    read_bytes_list.append(int(read_bytes))
                    read_count_list.append(int(read_count))
                    write_bytes_list.append(int(write_bytes))
                    write_count_list.append(int(write_count))
                    i=i+1
                except Exception as error:
                    i=i+1
                    print(error)


            #summing the data for a single moment
            total_names=len(names_list)
            mem_percent=sum(mem_percent_list)
            read_bytes=sum(read_bytes_list)
            read_count=sum(read_count_list)
            write_bytes=sum(write_bytes_list)
            write_count=sum(write_count_list)

            names_list.clear()
            mem_percent_list.clear()
            read_bytes_list.clear()
            read_count_list.clear()
            write_bytes_list.clear()
            write_count_list.clear()

            #forming an array of data of single moment
            array.append(total_names)
            array.append(mem_percent)
            array.append(read_bytes)
            array.append(read_count)
            array.append(write_bytes)
            array.append(write_count)
            array.append(cpu_usage)

            #forming numpy array of the above array
            numpy_array=np.array(array).reshape(1,7)
            numpy_array=sc.transform(numpy_array)
            array.clear()

            #predicting from the classifier
            y_pred = classifier.predict(numpy_array)
            print(y_pred)

            #pushing the notification if the ransomware is found active
            if y_pred==1:
                toaster = ToastNotifier()
                toaster.show_toast("Ransomware Attack Detected", "Check the task manager to kill unknown process",
                                   duration=3)



        except Exception as error:
            print(error)



def data_push():
    #pushing from a csv file to online server
    dictionary=dict()
    url = 'https://fyp-cbrdp.herokuapp.com/process'
    machineID = 'Ahsans VM'

    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            dictionary['machineID']=machineID
            dictionary['total_process']=line[0]
            dictionary['memory_percent']=line[1]
            dictionary['read_bytes']=line[2]
            dictionary['read_count']=line[3]
            dictionary['write_bytes']=line[4]
            dictionary['write_count']=line[5]
            dictionary['cpu_usage']=line[6]
            dictionary['ransomware_active']=line[7]
            json_data = json.dumps(dictionary, ensure_ascii=False, indent=4)
            data = json.loads(json_data)
            payload = data
            try:
                r = requests.post(url, data=payload)
                print(r.status_code)
            except Exception as error:
                print(error)







#machine_learning()
