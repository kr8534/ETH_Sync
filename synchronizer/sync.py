import requests
import json
import sys
import base64
import psycopg2
import datetime
import time
import dictDecode

def toHex(num):
    return "0x" + hex(num).split('x')[-1]

def toDate(string):
    tmp = string.split('-')
    return datetime.date(int(tmp[0]),int(tmp[1]), int(tmp[2]))

def decodeBase64(coded_string):
    tmp = base64.b64decode(coded_string)
    rst = tmp.strip('\'').split(',')
    return rst

def decodeHex(coded_string):
    tmp = coded_string.decode("hex")
    rst = tmp.strip('\'').split(',')
    return rst

def insertContract(tx_id, coded_string):
    decoded = coded_string.decode("hex")
    date_list = decoded[7:].split(',')

    c0, c1, c2, c3, c4, c5, c6 = dictDecode.decodeDict(decoded[0:7])

    query = 'INSERT INTO contract (transaction_key, policy_id, policy_type, charge, duration, cust_id, age, gender, insure_date, effective_date, expiry_date) VALUES (\''+ tx_id + '\', \'' + c0 + '\',' + c1 + ',' + c2 + ', \'' + c3 + '\', \'' + c4 + '\', \'' + c5 + '\', \'' + c6 +'\', \'' + date_list[0] + '\', \'' + date_list[1] + '\', \'' + date_list[2] + '\');'

    try:
        con = psycopg2.connect("host='147.47.206.11' port='35432' dbname='zhongan' user='zhongan' password='zhongan'")
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        rst = cur.fetchall()
        
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        print 'Error %s' % e
   
def selectContract():
    try:
        con = psycopg2.connect("host='147.47.206.11' port='35432' dbname='zhongan' user='zhongan' password='zhongan'")
        cur = con.cursor()
        cur.execute("select * from contract2")
        rst = cur.fetchall()
        con.commit()
        print rst
        
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        print 'Error %s' % e
    
def getNumber2(url, method):
    url = url
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(
        {"jsonrpc": "2.0",
         "method": "eth_blockNumber",
         "params":[],
         "id":2018
        })
    if method == 'GET':
        r = requests.get(url, data=data, headers=headers)
    elif method == 'POST':
        r = requests.post(url, data=data, headers=headers)
    elif method == 'PUT':
        r = requests.get(url, data=data, headers=headers)
    else:
        raise Exception()
    rst = json.loads(r.text)
    
    rst_block = rst[u'result']
    decimal_num = int(rst_block, 16)

    return decimal_num

def getTXs(url, method, num):
    url = url
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(
        {"jsonrpc": "2.0",
         "method": "eth_getBlockByNumber",
         "params":[num, True],
         "id":2018
        })
    if method == 'GET':
        r = requests.get(url, data=data, headers=headers)
    elif method == 'POST':
        r = requests.post(url, data=data, headers=headers)
    elif method == 'PUT':
        r = requests.get(url, data=data, headers=headers)
    else:
        raise Exception()

    rst = json.loads(r.text)[u'result']
    txs = rst[u'transactions']
    print txs
    return txs

def parseTX(txs):
    txcount = 0
    for tx in txs:
        txhash = tx[u'hash']
        txfrom = tx[u'from']
        txto = tx[u'to']
        if txto is None:
            break
        hloss = 8 # HEX
        value_str = tx[u'value']
        value_list = value_str.split('x')
        u_input = tx[u'input']
        if len(value_list[1]) <= hloss:
            value_list[1] = '0'
        else:
            value_list[1] = value_list[1][:-8]
        txval = float(int('0x'+value_list[1], 0)) / (1000000000000000000.0 / 0x100000000)
        
        txcount += 1
        print txhash, u_input
        insertContract(txhash, u_input[2:])

if __name__ == "__main__":


    num = getNumber2("http://147.47.206.13:8546", "POST")
    print num

    #txs = getTXs("http://147.47.206.13:8546", "POST", toHex(num)) 

    current = 10954

    while(True):
        num = getNumber2("http://147.47.206.13:8546", "POST")
        if ( num >  current ):
            start_block = current + 1
            end_block = num
            
            for i in range(start_block, end_block + 1):
                block_n = toHex(i)
                txs = getTXs("http://147.47.206.13:8546", "POST", block_n)
                parseTX(txs)

            current = end_block
        else:
            print "no update yet"
        
        time.sleep(1)
