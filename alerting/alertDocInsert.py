#!/usr/bin/python3

'''
basicPython script to write to OpenSearch
uses some CSV from /python/logFileGenerator
'''
# imports
from datetime import datetime
from faker import Faker
from random import randint
from opensearchpy import OpenSearch
import csv, random, time

# objects
faker = Faker()

# functions
def createRanNum():
    # return a standard log level
    # weighted on a sale of 0-100 so most should be info
    ranNumber = random.randint(0, 100)
    if ranNumber >= 0 and ranNumber <= 70:
        ranNumber = "1"
        # ranNumber = "fatal"
    elif ranNumber >= 71 and ranNumber <= 75:
        ranNumber = "2"
    elif ranNumber >= 76 and ranNumber <= 80:
        ranNumber = "3"
    elif ranNumber >= 81 and ranNumber <= 85:
        ranNumber = "4"
    elif ranNumber >= 86 and ranNumber <= 90:
        ranNumber = "5"
    elif ranNumber >= 91 and ranNumber <= 98:
        ranNumber = "6"   
    else:
        ranNumber = "9" #  + str(ranNumber)   
    return ranNumber

def createLogLevel():
    # return a standard log level
    # weighted on a sale of 0-100 so most should be info
    ranNumber = random.randint(0, 100)
    if ranNumber >= 0 and ranNumber <= 70:
        logLevel = "info"
    elif ranNumber >= 71 and ranNumber <= 75:
        logLevel = "debug"
    elif ranNumber >= 76 and ranNumber <= 80:
        logLevel = "trace"
    elif ranNumber >= 81 and ranNumber <= 85:
        logLevel = "warn"
    elif ranNumber >= 86 and ranNumber <= 90:
        logLevel = "error"
    elif ranNumber >= 91 and ranNumber <= 99:
        logLevel = "critical"    
    else:
        logLevel = "fatal " #  + str(ranNumber)    
    return logLevel
def get_random_item(list_name, random_range):
    '''
    return a random item from a list
    '''
    ran = random.randint(1,random_range)
    return list_name[ran]

def createHttpResponseCode():
    # return response code
    # weighted on a sale of 0-100
    # 200's/300's should be most common
    ranNumber = random.randint(0, 100)
    if ranNumber >= 0 and ranNumber <= 90:
        httpResponse = "1"  # 100/200/300 not important
    elif ranNumber >= 91 and ranNumber <= 97:
        httpResponse = "3"  #400's 
    else:
        httpResponse = "6" # 500   
    return httpResponse

def read_csv(csvFilename, row_number):
    '''
    read a CSV file into a list
    args are filename and row of the desired item
    '''
    with open(csvFilename) as f:
        # list object to return
        return_list = []
        # open the file which returns a pointer to the 1st line
        reader = csv.reader(f)
        # this will move the pointer to the next line so it skips the header line of the CSV
        next(reader)
        for row in reader:
            # print it if you want
            # print(row[row_number])
            # add it to a list
            return_list.append(row[row_number])
    return return_list


if __name__ == '__main__':
    # variables
    host = [{'host': '127.0.0.1', 'port': 9200}]
    auth = ('admin', 'admin')
    ca_certs_path = '/home/bikeride/opensearch/opensearch-2.3.0/config/root-ca.pem'
    target_index = 'test_index1'
    client = OpenSearch(hosts=host,http_compress=True,http_auth=auth,use_ssl=True,verify_certs=True,ssl_assert_hostname=False,ssl_show_warn=False,ca_certs=ca_certs_path)
    # target index to write to
    #target_index = 'test_index1'
    target_index = 'test_index_alert' #  'test_index_ingest'
    
    # generate lists from CSV files
    humanReadableCsv = "/home/bikeride/Documents/csvFiles/Human-to-HumanActionableRequestsDataset.csv"
    messageList = read_csv(humanReadableCsv, 1)
    msgTypeList = read_csv(humanReadableCsv, 0)
    msgDirectionList = read_csv(humanReadableCsv, 2)
    msgValidtyList = read_csv(humanReadableCsv, 3)
    #
    # set up to run for timed run in seconds
    runTime = 6000
    timeToRun = int(time.time() + runTime)
    # for i in range(1000):
    while (int(time.time()) < int(timeToRun)):
        severity = createRanNum()
        loglevel = createLogLevel()
        http_response_code = createHttpResponseCode()
        message = get_random_item(messageList, len(messageList) -1)
        msgType =  get_random_item(msgTypeList, len(msgTypeList) -1)
        msgDirection =  get_random_item(msgDirectionList, len(msgDirectionList) -1)
        msgValidity = get_random_item(msgValidtyList, len(msgValidtyList) -1)
        return_status = faker.boolean()
        hostname = faker.hostname()
        # get a timestamp
        today = datetime.now()
        iso_datetime = today.isoformat()
        # set up the event
        document = {
            'time_stamp' : iso_datetime,
            'msg': message,
            'msg_type': msgType,
            'msg_direction': msgDirection,
            #'msg_validity': msgValidity,
            'severity': severity,
            'return_status': return_status,
            'http_response_code': http_response_code,
            'log_level': loglevel,
            'hostname': hostname
            }
        # send a write request
        response = client.index(
            index = target_index,
            body = document,
            refresh = True
            )
        # print the response if you want
        print(response)
        # short random delay
        time.sleep((random.random()))
