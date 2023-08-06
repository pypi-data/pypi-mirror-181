import pandas as pd 
import os
import json
from pandas import to_datetime
from flask import request, make_response, Flask 
import urllib.parse
import datetime
from pandarallel import pandarallel
import numpy as np
from functools import partial
import traceback
import loggerutility as logger
import re
import sys
import matplotlib
from prophet import Prophet
from DatabaseConnectionUtility import Oracle, SAPHANA, InMemory, Dremio, MySql, ExcelFile, Postgress, MSSQLServer, Tally, ProteusVision, SnowFlake
import requests
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding, serialize
from tensorflow import keras
import googletrans
from googletrans import Translator   
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Input, GlobalMaxPooling1D
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.initializers import Constant
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import joblib

class IncentiveCalculation:

    pandarallel.initialize()
    
    df = None
    detSql = None
    sqlQuery = None
    lookupTableMap = {}
    queryStringMap = {}
    currentDetData = None
    CPU_COUNT = os.cpu_count()
    errorId = ""
    dbDetails = None
    calculationData=""
    val="" 
    group_style =""
    outputType="JSON"
    group=""
    colum=""
    pool = None
    isPool  = 'false'
    minPool = 2
    maxPool = 100
    timeout = 180
    editorId=""
    userId=""
    visualId=""
    tableHeading =""
    argumentList = None
    advancedFormatting=None 
    isColumnChange= 'true'   
    isSqlChange= 'true'      
    transpose="false"
    dataSourceType="S"
    fileName=""
    transId=""
    auth_key=""
    serverUrl=""
    userName=""
    password= "" 
    jsonDataResponse=""
    
    def getConnection(self):
       
        if self.dbDetails != None:
                # Added by SwapnilB for dynamically creating instance of DB class on [ 10-AUG-22 ] [ START ] 
                klass = globals()[self.dbDetails['DB_VENDORE']]
                dbObject = klass()
                self.pool = dbObject.getConnection(self.dbDetails)
                # Added by SwapnilB for dynamically creating instance of DB class on [ 10-AUG-22 ]  [ END ] 
                
        return self.pool

    def getQueryData(self, jsonData=None, isWebsocet=None):
        try:
            con = None
            logger.log(f'\n This code is From queryandprocessdata Package', "0")
            logger.log(f'\n Print time on start : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            
            if isWebsocet == "true":
                print("jsonData in getQueryData:", jsonData, type(jsonData))
                domData = jsonData
            else:
                domData = request.get_data('jsonData', None)
                domData = domData[9:]
            self.calculationData = json.loads(domData)
            logger.log(f'\n Inside getQueryData jsonData : {self.calculationData}', "0")

            if 'isSqlChange' in self.calculationData.keys():
                if self.calculationData.get('isSqlChange') != None:
                    self.isSqlChange = self.calculationData['isSqlChange']

            if 'isColumnChanges' in self.calculationData.keys():
                if self.calculationData.get('isColumnChanges') != None:
                    self.isColumnChange = self.calculationData['isColumnChanges']   

            if 'editorId' in self.calculationData.keys():
                if self.calculationData.get('editorId') != None:
                    self.editorId = self.calculationData['editorId']   

            if 'userId' in self.calculationData.keys():
                if self.calculationData.get('userId') != None:
                    self.userId = self.calculationData['userId']   
            
            if 'visualId' in self.calculationData.keys():
                if self.calculationData.get('visualId') != None:
                    self.editorId = self.calculationData['visualId']   

            if 'tableHeading' in self.calculationData.keys():
                if self.calculationData.get('tableHeading') != None:
                    self.tableHeading = self.calculationData['tableHeading']        
        
            if 'argumentList' in self.calculationData.keys():
                if self.calculationData.get('argumentList') != None:
                    self.argumentList = self.calculationData['argumentList']   
        
            if 'advancedFormatting' in self.calculationData.keys():
                if self.calculationData.get('advancedFormatting') != None:
                    self.advancedFormatting = self.calculationData['advancedFormatting']

            if 'dataSourceType' in self.calculationData.keys():
                if self.calculationData.get('dataSourceType') != None:
                    self.dataSourceType = self.calculationData['dataSourceType']

            sql = self.calculationData['source_sql']
            
            self.dbDetails = self.calculationData['dbDetails']
            self.pool = self.getConnection()

            if self.dbDetails != None:
                if self.dbDetails['DB_VENDORE'] == 'Oracle':
                    if self.isPool == 'true':
                        con = self.pool.acquire()
                    else:
                        con = self.pool
                else:
                    con = self.pool

            if 'update ' in sql or 'delete ' in sql:
                return self.getErrorXml("Invalid SQL" , "Update and Delete operations are not allowed in Visual.")
            else:
                if self.isSqlChange == 'true':
                    logger.log(f'\n Print time for before executing source_sql : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    
                    if self.dataSourceType == "F":          
                        if 'URL' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['URL'] != None:
                            self.fileName = self.calculationData['dbDetails']['URL']

                        if self.fileName[-3:] == "csv" :
                            self.df = pd.read_csv(self.fileName)
                        else:
                        self.df = pd.read_excel(self.fileName)
                        logger.log(f"self.df TYPE_F:::::{self.df}{type(self.df)}","0")
                        
                    elif self.dataSourceType == "R":
                        logger.log(f"inside TYPE_R:::::-->","0")
                        if 'dbDetails' in self.calculationData.keys() and self.calculationData.get('dbDetails') != None:
                            if 'auth_key' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['auth_key'] != None:
                                self.auth_key = self.calculationData['dbDetails']['auth_key']

                            if 'URL' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['URL'] != None:
                                self.serverUrl = self.calculationData['dbDetails']['URL']

                            if 'NAME' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['NAME'] != None:
                                self.userName = self.calculationData['dbDetails']['NAME']

                            if 'KEY' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['KEY'] != None:
                                self.password = self.calculationData['dbDetails']['KEY']

                        if self.auth_key == 'N':               
                            try:
                                response = requests.get(self.serverUrl)
                                if str(response.status_code) == '200':
                                    logger.log(f"{response.url} -- {response} ","0")
                                    self.jsonDataResponse = response.json()
                                    logger.log(f"No-Auth jsonDataResponse : {self.jsonDataResponse}","0")
                                else:
                                    logger.log(f"No-Authentication Type Response: {str(response.status_code)}","0")
                            except Exception as e:
                                trace = traceback.format_exc()
                                descr = str(e)
                                returnErr = self.getErrorXml(descr, trace)
                                logger.log(f'\n Print exception returnSring inside auth_type-N : {returnErr}', "0")
                                return str(returnErr)

                        elif self.auth_key == 'T':      
                            try:
                                response = requests.request("POST",self.serverUrl + "key="+ self.password)
                                if str(response.status_code) == '200':
                                    logger.log(f"{response} ","0")
                                    self.jsonDataResponse = response.json()
                                    logger.log(f"Auth_Type-T jsonDataResponse : {self.jsonDataResponse}","0")
                                else:
                                    logger.log(f"Auth_Type-T Response: {str(response.status_code)}","0")
                                    logger.log(f"Result for token based authentication: {response.json()}","0")
                            except Exception as e:
                                trace = traceback.format_exc()
                                descr = str(e)
                                returnErr = self.getErrorXml(descr, trace)
                                logger.log(f'\n Print exception returnSring inside auth_type-T : {returnErr}', "0")
                                return str(returnErr)

                        elif self.auth_key == 'S':   
                            try:
                                session= requests.Session()
                                formParam = {'USER_CODE': self.userName, 'PASSWORD': self.password, 'DATA_FORMAT':'JSON','APP_ID': 'INSIGHTCON'  }
                                logger.log(f"formParam session login::::{formParam}","0")
                                if "ibase" in self.serverUrl:
                                    self.serverUrl[:self.serverUrl.find("ibase")-1]
                                response = session.post(self.serverUrl +"/ibase/rest/E12ExtService/login?", formParam)
                                if str(response.status_code) == '200':
                                    status = (json.loads(response.text))['Response']['status']
                                    if status == 'success':
                                        logger.log(f"Session based login successful","0")
                                        cookie = response.cookies
                                        tokenId = json.loads((json.loads(response.text))['Response']['results'])['TOKEN_ID'] 
                                        logger.log(f" TYPE_S cookie :::::{cookie} tokenid:::::::{tokenId}","0")
                                        
                                        if 'URL' in self.calculationData['dbDetails'] and self.calculationData.get('dbDetails')['URL'] != None:
                                            self.serverUrl = self.calculationData['dbDetails']['URL']
                                        
                                        formParam = {'TOKEN_ID':tokenId }
                                        logger.log(f"formParam visualList::::{formParam}","0")
                                        response = session.post(self.serverUrl , formParam, cookies=cookie)
                                        self.jsonDataResponse=json.loads(response.text)['Response']['results']
                                        logger.log(f"visualList type-S : {self.jsonDataResponse}","0")
                                        
                                    elif status == 'error':
                                        logger.log(f"visualList type-S : {json.loads(response.text)}","0")
                                        return json.loads(response.text)
                                else:
                                    logger.log(f"Session Based Authentication Response: {str(response.status_code)}","0")
                                
                            except Exception as e:
                                logger.log(f'\n In auth_type-S exception stacktrace : ', "1")
                                trace = traceback.format_exc()
                                descr = str(e)
                                returnErr = self.getErrorXml(descr, trace)
                                logger.log(f'\n Print exception returnSring inside auth_type-S : {returnErr}', "0")
                                return str(returnErr)
                        else:
                            logger.log(f"Invalid auth_key: {self.auth_key}","0")

                        self.df = pd.DataFrame.from_records(self.jsonDataResponse)
                        logger.log(f"self.df in no_auth_key: {self.df}","0")
                    
                    elif self.dataSourceType == "S":
                        self.df = pd.read_sql(sql, con)
                        logger.log(f"self.df type-S read_sql :::::{self.df}{type(self.df)}","0")
                        
                    else:
                        logger.log(f"Invalid dataSourceType:::::{self.dataSourceType}","0")

                    logger.log(f'\n Print time for after executing source_sql : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    self.store(self.df, self.userId, self.editorId, self.visualId, 'sourceSql')
                else:
                    self.df = self.read(self.userId, self.editorId, self.visualId, 'sourceSql')

            self.df.columns = self.df.columns.str.strip().str.lower()
            
            if con:
                if self.dbDetails != None:
                    if self.dbDetails['DB_VENDORE'] == 'Oracle':
                        if self.isPool == 'true' :
                            self.pool.release(con)

            udf_divide = partial(self.udf_divide)
            udf_round = partial(self.udf_round)
            contribution = partial(self.contribution)               # Added by AniketG on [16-Aug-2022] for calculating percentage
            forecast = partial(self.forecast)
            trainemodel = partial(self.trainemodel)
            predict = partial(self.predict)
            translate = partial(self.translate)

            #logger.log(f'\n Print sourcesql result ::: \n {self.df}', "0")

            if not self.df.empty:
                
                if self.isColumnChange == 'true':
      
                    for key in self.calculationData:

                        if key == 'column':
                            detailArr = self.calculationData[key]
                            
                            for detail in detailArr:
                                self.currentDetData = detail

                                if "line_no" in detail:
                                    self.errorId = 'errDetailRow_' + str(detail['line_no'])
                                
                                if detail['calc_type'] == 'S':
                                    logger.log(f'\n Inside getQueryData calc_expression for type SQL : {detail["calc_expression"]}', "0")
                                    self.detSql = detail['calc_expression']
                                    logger.log(f'\n Print time for type SQL before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getSqlResult(row, self.pool, detail), axis=1)
                                    else:
                                        self.df[detail['col_name'].lower().strip()] = self.df.parallel_apply(lambda x : None, axis=1)

                                    logger.log(f'\n Print time for type SQL after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                                elif detail['calc_type'] == 'F':
                                    logger.log(f'\n Inside getQueryData calc_expression for type Forecast : {detail["calc_expression"]}', "0")
                                    expr = detail['col_name'].lower().strip() + '=' + detail['calc_expression'].lower().strip()
                                    logger.log(f'\n Print time for type Forecast before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                            self.df = forecast()
                                        
                                    else:
                                        self.df = self.df.eval(detail['col_name'].lower().strip() + '=' + None)

                                    logger.log(f'\n Print time for type Forecast after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                                elif detail['calc_type'] == 'E':
                                    logger.log(f'\n Inside getQueryData calc_expression for type EXPRESSION : {detail["calc_expression"]}', "0")
                                    expr = detail['col_name'].lower().strip() + '=' + detail['calc_expression'].lower().strip()
                                    logger.log(f'\n Print time for type EXPRESSION before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        self.df = self.df.eval(expr)
                                    else:
                                        self.df = self.df.eval(detail['col_name'].lower().strip() + '=' + None)

                                    logger.log(f'\n Print time for type EXPRESSION after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                                elif detail['calc_type'] == 'L':
                                    logger.log(f'\n Inside getQueryData calc_expression for type LOOKUP : {detail["calc_expression"]}', "0")
                                    self.detSql = detail['calc_expression']
                                    
                                    logger.log(f'\n Print time for type LOOKUP before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getLookUpValue(row, self.pool), axis=1)
                                    else:
                                        self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getLookUpValue(row, self.pool), axis=1)

                                    logger.log(f'\n Print time for type LOOKUP after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                                elif detail['calc_type'] == 'C':
                                    logger.log(f'\n Inside getQueryData calc_expression for type CONDITIONAL EXPRESSION : {detail["calc_expression"]}', "0")
                                    logger.log(f'\n Print time for type CONDITIONAL EXPRESSION before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        exprArr = detail['calc_expression'].lower().split(':')
                                        condition = exprArr[0]
                                        trueExpr = None
                                        falseExpr = None
                                        if exprArr[1] != None:
                                            trueExpr = exprArr[1]
                                        if exprArr[2] != None:
                                            falseExpr = exprArr[2]
                                        self.df[detail['col_name'].lower().strip()] = self.udf_if(self.df, condition, trueExpr, falseExpr)
                                    else:
                                        self.df = self.df.eval(detail['col_name'].lower().strip() + ' = ' + None)

                                    logger.log(f'\n Print time for type CONDITIONAL EXPRESSION after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                elif detail['calc_type'] == 'U':
                                    logger.log(f'\n Inside getQueryData calc_expression for type Cumulative Sum : {detail["calc_expression"]}', "0")
                                    logger.log(f'\n Print time for type Cumulative Sum before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        columnArrList = detail['calc_expression'].lower().split(',')
                                        cumsumColumn = columnArrList[0]
                                        if len(columnArrList) == 1:
                                            self.df[detail['col_name'].lower().strip()] = self.df[cumsumColumn].cumsum()
                                        else:
                                            del columnArrList[0]
                                            self.df[detail['col_name'].lower().strip()] = self.df.groupby(columnArrList)[cumsumColumn].cumsum()
                                    else:
                                        self.df[detail['col_name'].lower().strip()] = self.df.parallel_apply(lambda x : None, axis=1)

                                elif detail['calc_type'] == 'N':
                                    logger.log(f'\n Inside getQueryData UserDefine for type EXPRESSION : {detail["calc_expression"]}', "0")
                                    expr = detail['col_name'].lower().strip() + '=' + detail['calc_expression'].lower().strip()
                                    logger.log(f'\n Print time for type EXPRESSION before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                    
                                    if detail['calc_expression'] != None:
                                        self.df = self.df.eval(expr)
                                    else:
                                        self.df = self.df.eval(detail['col_name'].lower().strip() + '=' + None)

                                    logger.log(f'\n Print time for type EXPRESSION after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                    self.store(self.df, self.userId, self.editorId, self.visualId, 'final')               
                else:
                    self.df = self.read(self.userId, self.editorId, self.visualId, 'final')        
            else:
                returnErr = self.getErrorXml("No records found against the source sql", "")
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)
            
            #logger.log(f'\n End of query datatypes:::\n {self.df.dtypes}', "0")
            self.df.columns = self.df.columns.str.strip().str.lower()
            
            if self.calculationData.get('sorting_col_name'):
                sortingColName = self.calculationData['sorting_col_name']
                if sortingColName != "":
                    sortingColName = sortingColName.lower().strip()
                    self.df.sort_values(by=[sortingColName], inplace=True, ascending=True)
            
            dbDataTypes = self.df.dtypes.to_json()
            #self.df = self.df.to_json(orient='records')
            #logger.log(f'\n End of query data:::\n {self.df}', "0")
            
            if 'visualJson' in self.calculationData.keys():
                if self.calculationData.get('visualJson') != None:
                    visualJson = self.calculationData['visualJson']

            if 'OutputType' in self.calculationData.keys():
                if self.calculationData.get('OutputType') != None:
                    self.outputType = self.calculationData['OutputType']      
            
            if 'columnHeading' in self.calculationData.keys():
                if self.calculationData.get('columnHeading') != None:
                    columnHeading = self.calculationData['columnHeading']        
            
            if 'oldColumnHeading' in self.calculationData.keys():
                if self.calculationData.get('oldColumnHeading') != None:
                    oldColumnHeading = self.calculationData['oldColumnHeading']        

            if self.outputType == 'HTML':
                #logger.log(f'\n Print dataframe at end::: \n {self.df}', "0")
                visualJson1 = json.loads(visualJson)
                columnHeading = columnHeading.split(",")
                self.df.rename(columns=dict(zip(self.df.columns, columnHeading)), inplace=True)
                oldColumnHeading = oldColumnHeading.split(",")
            
                if 'groups' in visualJson1.keys():
                    if len(visualJson1.get('groups')) != 0:    
                        self.group = visualJson1['groups']

                if 'rows' in visualJson1.keys():
                    if len(visualJson1.get('rows')) != 0: 
                        row = visualJson1["rows"]
                
                if 'columns' in visualJson1.keys():
                    if len(visualJson1.get('columns')) != 0:
                        self.colum = visualJson1["columns"]
                
                if 'values' in visualJson1.keys():
                    if len(visualJson1.get('values')) != 0:
                        self.val = visualJson1["values"]
                        
                if len(self.group) != 0:
                    lst=[]
                    for label, df_obj in (self.df).groupby(self.group):
                        sum = df_obj[self.val].sum()
                        df_obj.loc[' '] = sum   
                        lst.append(df_obj)

                    final_df = pd.concat(lst)
                    final_df.loc[final_df[row[0]].isnull(), self.group[0]] = "Total "  
                    final_df.loc[''] = self.df[self.val].sum()
                    final_df.fillna('', inplace=True)
                    final_df.iloc[-1, final_df.columns.get_loc(self.group[0])] = 'Grand Total '
                    self.group_style = True
                    html_str = self.getTableHTML(final_df)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
                elif len(self.colum) == 0:
                    html_str = self.getTableHTML(self.df)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
                else:
                    final_pivot = pd.pivot_table(self.df, index=row, columns=self.colum, values=self.val)
                    html_str = self.getTableHTML(final_pivot)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
            elif self.outputType == "JSON":
                self.df = self.df.to_json(orient='records', date_format='iso')
                #logger.log(f'\n Print dataframe at end::: \n {self.df}', "0")
                data_set = {"dbDataTypesDetails": dbDataTypes, "allData":  self.df }
                logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                #return self.df
                #return data_set 
                return json.dumps(data_set)
            
            elif self.outputType == "XML":               
                xml_Str = self.to_xml(self.df)
                xmlStr = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n' + xml_Str + '\n</root>'
                logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                return xmlStr

            else:
                pass
                
        except Exception as e:
            logger.log(f'\n In getQueryData exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = self.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
            return str(returnErr)
        finally:
            try:
                if self.pool:
                    if self.dbDetails != None:
                        if self.dbDetails['DB_VENDORE'] == 'Oracle':
                            if self.isPool == 'true' :
                                self.pool.close()
                            else:
                                con.close()
                        else:
                            con.close()
            except Exception as e: 
                logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = self.getErrorXml(descr, trace)
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)

    def getLookUpValue(self, row, pool):
        try:
            expr = self.detSql.split(',')
            lookUpTable = str(expr[0].strip())
            lookUpCol = expr[1].strip().lower()
            validateLookup = "false"
            isLookUpDateColValBlank = "false"
            lookupExpLen = len(expr)
            
            if lookupExpLen == 3:
                lookUpDateCol = expr[2].strip().lower()
                lookUpDateColVal = row[lookUpDateCol]
                validateLookup = "true"
                if str(lookUpDateColVal) == None or str(lookUpDateColVal) == '' or str(lookUpDateColVal) == 'NaT':
                    lookUpDateColVal = str('')
                    isLookUpDateColValBlank = "true"

            if lookUpTable != None and lookUpTable.startswith('\''):
                length = len(lookUpTable)
                lookUpTable = lookUpTable[1:length-1]
            else:
                lookUpTable = lookUpTable.lower()
                if  lookUpTable in row:
                    rowVal = row[lookUpTable]
                    lookUpTable = str(rowVal)
                else:
                    lookUpTable = ""
            
            rowVal = row[lookUpCol]

            isLookUpColValBlank = "false"
            if str(rowVal) == None or str(rowVal) == '' or str(rowVal) == 'NaT':
                rowVal = str('')
                isLookUpColValBlank = "true"

            if self.lookupTableMap == None or not ""+str(lookUpTable) in self.lookupTableMap:
                self.setLookUpData( lookUpTable, validateLookup, self.pool )

            if validateLookup == 'true':
                lookUpTable = lookUpTable + '_validate'

            dfLookUpDet = None
            resDataType = str('')
            isdfLookUpDet = "false"
            if self.lookupTableMap != None and ""+str(lookUpTable) in self.lookupTableMap:
                lookUpHeadDetMap = self.lookupTableMap[""+str(lookUpTable)]

                dfLookUpDet = lookUpHeadDetMap["lookUpDet"]

                resDataType = lookUpHeadDetMap["resDataType"]

                query = lookUpHeadDetMap["queryString"]
                if isLookUpDateColValBlank == "false" and isLookUpColValBlank == "false":
                    dfLookUpDet = dfLookUpDet.query( query )
                    isdfLookUpDet = "true"
                else:
                    isdfLookUpDet = "false"
            else:
                isdfLookUpDet = "false"

            if  isdfLookUpDet == "false" or dfLookUpDet.empty:
                if resDataType == 'N':
                    dfLookUpDet = 0
                    dfLookUpDet = pd.to_numeric(dfLookUpDet)
                elif resDataType == 'D':
                    dfLookUpDet = str('')
                    dfLookUpDet = pd.to_datetime(dfLookUpDet)
                elif resDataType == 'S':
                    dfLookUpDet = str('')
                else:
                    dfLookUpDet = str('')

            else:
                dfLookUpDet = dfLookUpDet.iloc[0:1,0:1]
                dfLookUpDet = dfLookUpDet.iat[0,0]

                if resDataType == 'N':
                    dfLookUpDet = pd.to_numeric(dfLookUpDet)
                elif resDataType == 'D':
                    dfLookUpDet = pd.to_datetime(dfLookUpDet)

            return dfLookUpDet
        except Exception as e:
            raise e

    def getSqlResult(self, row, pool, detail):
        try:
            if self.dbDetails != None:
                if self.dbDetails['DATABASETYPE'] == '1':
                    if self.isPool == 'true':
                        con = self.pool.acquire()
                    else:
                        con = self.pool
                elif self.dbDetails['DATABASETYPE'] == '2' or self.dbDetails['DATABASETYPE'] == '3' :
                    con = self.pool

            colDbType = detail['col_datatype']
            self.sqlQuery = self.detSql
            splitColValue = None
            dfSqlResult = None
            newSql = None

            if self.sqlQuery.find("?") != -1:
                newSql = self.sqlQuery.split(':')
                self.sqlQuery = newSql[0]
                sqlInput = newSql[1].lower()
                columns = sqlInput.split(',')
                self.buildSqlQuery(self.sqlQuery, columns, row)

            if 'update ' in self.sqlQuery or 'delete ' in self.sqlQuery:
                return self.getErrorXml("Invalid SQL" , "Update and Delete operations are not allowed in Visual.")
            else:
                dfSqlResult = pd.read_sql(
                    self.sqlQuery, con
                )

            if not dfSqlResult.empty:
                dfSqlResult = dfSqlResult.iloc[0:1,0:1]
                dfSqlResult = dfSqlResult.iat[0,0]
            else:
                if colDbType == 'N':
                    dfSqlResult = 0
                    dfSqlResult = pd.to_numeric(dfSqlResult)
                elif colDbType == 'D':
                    dfSqlResult = str('')
                    dfSqlResult = pd.to_datetime(dfSqlResult)
                else:
                    dfSqlResult = str('')
                    
            return dfSqlResult
        except Exception as e:
            raise e
        finally:
            try:
                if con:
                    if self.dbDetails != None:
                        if self.dbDetails['DATABASETYPE'] == '1':
                            if self.isPool == 'true' :
                                self.pool.release(con)
                        
            except Exception as e :
                logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = self.getErrorXml(descr, trace)
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)

    def buildSqlQuery(self, sql, columns, row):
        ctr = 0
        if sql.find('?') != -1 and len(columns) > 0:
            indexPos = sql.find('?')
            rowVal = str(row[columns[ctr].strip()])

            if str(rowVal) == None or str(rowVal) == 'None': 
                rowVal = str('')

            if len(sql) - 1 != indexPos:
                sql = sql[:indexPos] + "'" + rowVal + "'" + sql[indexPos+1:]
            else:
                sql = sql[:-1] + "'" + rowVal + "'"

            columns.pop(ctr)
            self.sqlQuery = str(sql)
            if(sql.find('?') != -1):
                self.buildSqlQuery(sql, columns, row)

    def getErrorXml(self, descr, trace):

        if  self.currentDetData:
            colName = self.currentDetData['col_name']
            calcType = self.currentDetData['calc_type']
            
            errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error column_name="'''+colName+'''" type="E" column_value="'''+calcType+'''">
                                    <message><![CDATA[Error occurred in calculation of '''+colName+''' column for column type '''+calcType+''']]></message>
                                    <description><![CDATA['''+descr+''']]></description>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                    <errorId>'''+self.errorId+'''</errorId>
                                </error>
                            </Errors>
                        </Root>'''

            return errorXml
        else:
            errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error type="E">
                                    <message><![CDATA['''+descr+''']]></message>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                </error>
                            </Errors>
                        </Root>'''

            return errorXml

    def udf_divide(self, x, y):
        return x/y

    def udf_round(self, value, decimal):
        return round(value, decimal)

    def udf_if(self, df,condition,true_exp, false_exp):
        udf_divide = partial(self.udf_divide)
        udf_round = partial(self.udf_round)
        return np.where(df.eval(condition),df.eval(true_exp),df.eval(false_exp))

    def firstRowColVal(self, df):
        df = df.iloc[0:1,0:1]
        df = df.iat[0,0]
        return df
        
    def setLookUpData(self,lookUpTable,validateLookup, pool):
        try:
            if self.dbDetails != None:
                if self.dbDetails['DATABASETYPE'] == '1':
                    if self.isPool == 'true':
                        con = self.pool.acquire()
                    else:
                        con = self.pool
                elif self.dbDetails['DATABASETYPE'] == '2' or self.dbDetails['DATABASETYPE'] == '3' :
                    con = self.pool

            dfLookUpHead = None
            dfLookUpDet = None
            queryString = ''

            lookUpSql = "SELECT LOOKUP_TYPE, KEY_DATA_TYPE, RESULT_DATA_TYPE FROM GENLOOKUP WHERE LOOKUP_TABLE = '" + lookUpTable + "'"
            dfLookUpHead = pd.read_sql ( lookUpSql, con )

            lookUpDetSql = "SELECT RESULT_VALUE, MIN_KEY_VALUE, MAX_KEY_VALUE, EFF_FROM, VALID_UPTO FROM GENLOOKUP_TABLE WHERE LOOKUP_TABLE = '" + lookUpTable + "'"    
            dfLookUpDet = pd.read_sql( lookUpDetSql, con )

            rowVal = ''
            rowVal = str(rowVal)

            lookUpDateColVal = ''
            lookUpDateColVal = str(lookUpDateColVal)

            if not dfLookUpHead.empty and not dfLookUpDet.empty:
                resDataType = dfLookUpHead['RESULT_DATA_TYPE'].iloc[0]
                lookUpType = dfLookUpHead['LOOKUP_TYPE'].iloc[0]
                keyDataType = dfLookUpHead['KEY_DATA_TYPE'].iloc[0]

                if lookUpType == 'F':
                    if keyDataType == 'N':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_numeric)
                        rowVal = pd.to_numeric(rowVal)

                    elif keyDataType == 'D':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_datetime)
                        rowVal = pd.to_datetime(rowVal)

                    queryString = '@rowVal == MIN_KEY_VALUE'
                elif lookUpType == 'S':
                    if keyDataType == 'N':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_numeric)
                        rowVal = pd.to_numeric(rowVal)

                    elif keyDataType == 'D':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_datetime)
                        rowVal = pd.to_datetime(rowVal)

                if validateLookup == 'true':
                    dfLookUpDet[["EFF_FROM", "VALID_UPTO"]] = dfLookUpDet[["EFF_FROM", "VALID_UPTO"]].apply(pd.to_datetime)
                    lookUpDateColVal = pd.to_datetime(lookUpDateColVal)
                    if lookUpType == 'S':
                        queryString = '(@rowVal >= MIN_KEY_VALUE & @rowVal <= MAX_KEY_VALUE) & (@lookUpDateColVal >= EFF_FROM & @lookUpDateColVal <= VALID_UPTO)'
                    else:
                        queryString = '(@rowVal == MIN_KEY_VALUE) & (@lookUpDateColVal >= EFF_FROM & @lookUpDateColVal <= VALID_UPTO)'
                    lookUpTable = lookUpTable + '_validate'
                else:
                    if lookUpType == 'S':
                        queryString = '@rowVal >= MIN_KEY_VALUE & @rowVal <= MAX_KEY_VALUE'
                    else:
                        queryString = '@rowVal == MIN_KEY_VALUE'

                lookUpHeadDetMap = {}
                lookUpHeadDetMap["lookUpDet"] = dfLookUpDet
                lookUpHeadDetMap["resDataType"] = resDataType
                lookUpHeadDetMap["queryString"] = queryString
                self.lookupTableMap[lookUpTable] = lookUpHeadDetMap
        except Exception as e:
            raise e
        finally:
            if con:
                try:
                    if self.dbDetails != None:
                        if self.dbDetails['DATABASETYPE'] == '1':
                            if self.isPool == 'true' :
                                self.pool.release(con)
                        
                except Exception as e :
                    logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                    trace = traceback.format_exc()
                    descr = str(e)
                    returnErr = self.getErrorXml(descr, trace)
                    logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                    return str(returnErr)

    def is_json(self,a):                                               
        try:
            json.loads(a)
        except Exception as e:
            return False
        return True

    def to_xml(self, dt_frame):
        def row_xml(row):
            xml = ['<Detail>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</Detail>')
            return '\n'.join(xml)
        res = '\n'.join(dt_frame.apply(row_xml, axis=1))
        return(res)

    def format_num(self, str):
        return "text-align:right !important"

    def getTableHTML(self,pivot):
        if self.group_style :
            pivot_style = (pivot).reset_index(drop=True).style.applymap(self.format_num, subset=self.val).format('{:.3f}', na_rep='', subset=self.val)
            
        else:
            pivot_style = (pivot).style.applymap(self.format_num, subset=self.val).format('{:.3f}', na_rep='', subset=self.val)
        
        pivot_style = (pivot_style).set_table_attributes('class= "insight_html_table"')
        html = pivot_style.render()
        # logger.log(f'\n html inside method pivotstyle  : {type(html), html}', "0")                      

        col_dtype = dict(zip((self.calculationData['columnHeading']).split(','), json.loads(self.calculationData['columndataTypes']).values()))
        
        if self.advancedFormatting:
            for i in self.advancedFormatting.keys():
                if col_dtype[i] == 'string' :
                    pivot_style = pivot_style.set_properties(**{'background-color': self.advancedFormatting[i]}, subset=[i])
                else:
                    pivot_style = pivot_style.background_gradient(cmap=self.advancedFormatting[i], subset=[i])
                    
        html = "<h3 class='tableHeading'>"+ self.updateTableHeading(self.tableHeading, self.argumentList)+"</h3>" +  pivot_style.render()
        return html
    
    def store(self, df, userId, editorId, visualId, transpose):
        dir = 'Pickle_files'
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        filename= str(userId) +'_' + str(editorId) + '_' + str(visualId) + '_' + transpose
        df.to_pickle(dir + '/' + filename + '.pkl')
        if os.path.isfile(dir +'/' + filename + '.pkl'):
            logger.log('\n' + transpose + ' Pickle file created','0')   
        else:
            logger.log('\n' + transpose + ' Pickle file created','0')
        return dir +'/' + filename + '.pkl'
    
    def read(self, userId, editorId, visualId, transpose):
        dir = 'Pickle_files'
        if os.path.exists(dir):
            filename= str(userId) +'_' + str(editorId) + '_' + str(visualId) + '_' + transpose
            if os.path.isfile(dir +'/' + filename + '.pkl'):
                df_obj = pd.read_pickle(dir +'/' + filename + '.pkl')
                return df_obj
        else:
            return self.getErrorXml( dir + "directory does not exist","Pickle file directory not found" )  
    
    def replace(self, tableHeading, argumentList):
        left, right = tableHeading[:tableHeading.find("@")], tableHeading[tableHeading.find("@"):]
        key = right[:right.find(" ")]
        
        for i in argumentList.keys():
            if (key[1:]) in i:
                tableHeading = re.sub(key, argumentList[i], tableHeading) 
                break
        if "@" in tableHeading:
            tableHeading = self.replace(tableHeading, argumentList)
        
        return tableHeading

    def updateTableHeading(self, tableHeading, argumentList):    
        if "@" in tableHeading:
            tableHeading = self.replace(tableHeading, argumentList)
        else:
            return tableHeading

        return tableHeading
        
    def contribution(self, x):
        return (x / x.sum()) * 100

    def forecast(self):
        logger.log(f'\nForcast function start time, {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
        convert = json.loads(self.calculationData['columndataTypes'])
        length_of_string_col = 0
        string_list = []
        numeric_list_Int = []
        numeric_list = []
        length_of_dataset = 0
        
        for k in self.calculationData['column']:
            colname = k['col_name']
            expression1 = k['calc_expression']

        periodsof=expression1.split(",")
        per = periodsof[-1].split(")")
        global da
        for m,i in enumerate(convert):
            if convert[i] == 'string':
                string_list.append(i)
            elif convert[i] == 'date':
                da = i
                dateindex = m
            elif convert[i] == 'number':
                numeric_list.append(i)
                numeric_list_Int.append(m)
                pos=m
        
        for num, numbervalue in enumerate(convert):
                if numbervalue == numeric_list[0]:
                    for numbervalue in range(len(self.df)):
                        self.df.at[numbervalue, colname] = self.df[self.df.columns[num]].values[numbervalue]
        
        if len(string_list) != 0:
            new = self.df.filter([i for i in string_list], axis=1)
            drop_dataframe = new.drop_duplicates()    #### for drop duplicate value
            drop_dataframe.index = [i for i in range(0,len(drop_dataframe))]   ####   for contine index   
            for i in range(0,len(drop_dataframe)):
                datestring = []
                y = []
                head = []
                valuesofdataframe = [0]
                logger.log(f'\nForcast New DataFrame creation and finding the same data, start time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
                newo =pd.DataFrame(drop_dataframe.iloc[[i]])
                newo.index=valuesofdataframe
                k=newo.values
                newdataframe = newo.copy()                                                                                                                                            
                newdataframe['marker'] = True
                joined = pd.merge(new, newdataframe, on=[i for i in new], how='left')
                val = joined[pd.notnull(joined['marker'])][new.columns]
                lis = []
                lis = val.index.tolist()
                logger.log(f'\nForcast New DataFrame creation and finding the same data, end time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
                logger.log(f'\nForcast function process start time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
                for ind in lis:
                    datestring.append(self.df[self.df.columns[dateindex]].values[ind])
                    y.append(self.df[self.df.columns[numeric_list_Int[0]]].values[ind])
                    length_of_dataset = length_of_dataset + 1

                if all(item == 0 for item in y) or len(y) < 2:
                    continue

                m = Prophet()
                df_for_prophet = pd.DataFrame(dict(ds=datestring, y=y))
                m.fit(df_for_prophet)
                future = m.make_future_dataframe(periods=int(per[0]))
                forecast = m.predict(future)
                logger.log(f'\nForcast function process End time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
                for l, val in enumerate(forecast["trend"]):
                    df2 = {da: to_datetime([forecast["ds"][l]]), colname: [val]}
                    dd = pd.DataFrame(dict(df2))
                    df3 = pd.concat([newo, dd], axis=1)
                    df4 = df3[~df3[da].isin(datestring)]
                    self.df = self.df.append(df4, ignore_index = True)
                
            self.df.drop_duplicates(subset=da, keep='first', inplace=True)
            logger.log(f'\nForcast function end time :  {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            return self.df

        elif len(string_list) == 0:
            ds = []
            y = []
            for num, numbervalue in enumerate(convert):
                if numbervalue == numeric_list[0]:
                    for numbervalue in range(len(self.df)):
                        pos = num
                        y.append(self.df[self.df.columns[num]].values[numbervalue])

            for num, datevalue in enumerate(convert):
                if convert[datevalue] == "date":
                    d = num
                    date = datevalue
                    for datevalue in range(len(self.df)):
                        ds.append(self.df[self.df.columns[num]].values[datevalue])

            logger.log(f'\nForcast function process start time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            dit = []
            m = Prophet()
            df_for_prophet = pd.DataFrame(dict(ds=ds, y=y))
            m.fit(df_for_prophet)
            future = m.make_future_dataframe(periods=int(per[0]))
            forecast = m.predict(future)
            logger.log(f'\nForcast function process End time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            for l, val in enumerate(forecast["trend"]):
                df2 = {da: forecast["ds"][l],colname: val}
                self.df = self.df.append(df2, ignore_index=True)

            logger.log(f'\nForcast function end time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            self.df  = self.df.drop_duplicates(subset=[da], keep='first', inplace=False, ignore_index=False)
            return self.df

    def trainemodel(self):
        try:
            logger.log(f"inside trainemodel()","0")
            jsonData = request.get_data('jsonData', None)
            logger.log(f"requestParam:::::::{jsonData}{type(jsonData)}","0")
            jsonData = json.loads(jsonData[9:])
            logger.log(f"jsonData: {jsonData}{type(jsonData)}","0")

            modelType = jsonData['modelType']
            logger.log(f"modelType: {modelType}{type(modelType)}","0")
            jsonToDf = jsonData['modelJsonData']
            logger.log(f"jsonToDf: {jsonToDf}{type(jsonToDf)}","0")
            parsed_json = (json.loads(jsonToDf))
            logger.log(f"parsed_json: {parsed_json}{type(parsed_json)}","0")
            df = pd.DataFrame(parsed_json[1:])
            # df = pd.DataFrame(jsonToDf[1:])
            logger.log(f"df: {df}{type(df)}","0")
            input_column_name = json.loads(jsonData['modelParameter'])['input_column_name']
            logger.log(f"input_column_name `1067: {input_column_name}{type(input_column_name)}","0")
            train_column_name = json.loads(jsonData['modelParameter'])['train_column_name']
            logger.log(f"train_column_name: {train_column_name}{type(train_column_name)}","0")
            colNamesLst=[input_column_name, train_column_name]
            if 'Model_name' not in json.loads(jsonData['modelParameter']).keys() or json.loads(jsonData['modelParameter'])["Model_name"] == None:
                modelName = modelType +"_training_model"  
                logger.log(f"modelName if: {modelName}{type(modelName)}","0")               
            else:
                modelName = json.loads(jsonData['modelParameter'])['Model_name'] 
                logger.log(f"modelName: {modelName}{type(modelName)}","0")               

            modelScope = "global" if jsonData['modelScope'] == "G" else "enterprise" 
            logger.log(f"modelScope::{modelScope}","0")
            enterprise_key = jsonData['enterprise_key']
            logger.log(f"enterprise_key::{enterprise_key}","0")

            if modelType == 'Sentiment Analytics':
                logger.log(f"Inside sentimentTraining model","0")      
                review_df = pd.read_csv(self.fileName)         
                review_df = df[colNamesLst]
                logger.log(f'\nreview_df.shape : {review_df.shape}',"0")
                review_df=review_df[review_df[colNamesLst[1]] != "neutral"]  
                review_df[colNamesLst[1]].value_counts()
                sentiment_label=review_df[colNamesLst[1]].factorize()  # creates vector Array
                tweet = review_df[colNamesLst[0]].values
                logger.log(f"tweet : ,{type((tweet))}","0")
                tokenizer = Tokenizer(num_words=5000)
                tokenizer.fit_on_texts(tweet)
                logger.log("tokenizer.word_index::::{tokenizer.word_index}","0")
                encoded_docs = tokenizer.texts_to_sequences(tweet)     
                logger.log(f"encoded_docs:::{encoded_docs}","0")
                padded_sequence = pad_sequences(encoded_docs, maxlen=200)
                logger.log(f"{len(padded_sequence), len(padded_sequence[0])}","0")
                vocab_size = len(tokenizer.word_index) + 1
                embedding_vector_length = 32
                model = Sequential()
                model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
                model.add(SpatialDropout1D(0.25))
                model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
                model.add(Dropout(0.2))
                model.add(Dense(1, activation='sigmoid'))
                model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
                model.fit(padded_sequence,sentiment_label[0], epochs=3, validation_split=0.2, batch_size=32)
            
            elif modelType == 'Classification':
                review_df = df[colNamesLst]
                train_column_name=review_df[colNamesLst[1]]
                input_column_name = review_df[colNamesLst[0]]
                X_train, X_test, y_train, y_test = train_test_split(input_column_name, train_column_name, test_size=10,
                                                    random_state=10)
                svm = Pipeline([
                    ('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LinearSVC()),
                ])
                svm.fit(X_train, y_train)
                logger.log(f'Model Created',"0")
            else:
                logger.log(f'Invalid Model Type',"0")

        except Exception as e:
            logger.log(f'\n In Training model exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = self.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside Training model : {returnErr}', "0")
            raise str(e)
        else:
            flag =""
            if modelType == 'Sentiment Analytics':
                dir = 'models'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                model.save("models/" + modelName)     # to serialize model configuration and save model                  
                with open('models/'+ modelName +'/tokenizer.dictionary', 'wb') as tokenizer_dictionary_file:
                    pickle.dump(tokenizer, tokenizer_dictionary_file)
                    flag = "success"
                    logger.log("Sentiment Model has been trained and saved successfully.","0")
                    
            elif  modelType == 'Classification':
                joblib.dump(svm, 'models/'+modelName+'.pkl')
                flag = "success"
                logger.log("Classification Model has been trained and saved successfully.","0")
                
            else:
                logger.log(f'Invalid Model Type',"0")

            result= self.createModelScope(modelScope, modelName, enterprise_key)
            logger.log(f"ModelScope result::{result}","0")
            
            if flag == "success":
                return "Model has been trained and saved successfully." 


    def predict(self, textColumn, model, modelName):
        logger.log(f"inside predict_sentiment","0")
        logger.log(f"textColum:{textColumn}, model:{model}, modelName:{modelName} ","0")
        predicted_Sentiment=None
        predicted_label_lst=[]
        if model == "sentiment":
            with open('models/'+ modelName +'/tokenizer.dictionary', 'rb') as config_dictionary_file:
                tokenizer = pickle.load(config_dictionary_file)
                logger.log(f"tokenizer:::{tokenizer} {type(tokenizer)}","0")
            logger.log(f"self.df::::{self.df}\n{self.df.shape}","0")
            logger.log(f'\nSentiment prediction start time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            loaded_Model = keras.models.load_model("models/"+ modelName)
            for i,j in textColumn.iteritems():
                tw = tokenizer.texts_to_sequences([j])
                tw = pad_sequences(tw, maxlen=200)
                prediction = int(loaded_Model.predict(tw).round().item())
                predicted_label = "Positive" if prediction==0 else "Negative" 
                logger.log(f"\n\n{j}\n\n Predicted label::::: {predicted_label}","0")
                predicted_label_lst.append(predicted_label)
            
            logger.log(f'\nSentiment prediction end time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',"0")
            predicted_Sentiment = pd.DataFrame(predicted_label_lst, columns=['predicted_sentiment'])
        
        elif model == "textclassification":
            iterater = []
            predictmodel = joblib.load("models/"+modelName+".pkl")
            logger.log(f"predictmodel : {predictmodel}","0")
            return predictmodel.predict(textColumn)
        else:
            raise Exception(f"Invalid model name : '{model}'")
        return predicted_Sentiment

    def translate(self,colname_value,translate_to=None):
        logger.log(f'\n Print time for before executing Translate function : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
        da = Translator()
        ls=[]
        for i in colname_value:
            if i != None:
                logger.log(f'\n Print time for before executing Translate OPERATION : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                ls.append((da.translate(i,dest=translate_to)).text)
                logger.log(f'\n Print time for after executing Translate OPERATION : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")          
            else:
                ls.append("")
                
        logger.log(f'\n Print time for after executing Translate function : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")          
        return ls

    def createModelScope(self, modelScope, modelName,enterprise_key=""):
        if os.path.exists("modelScope.json"):
            logger.log(f"File already exists.","0")
        else:
            with open ("modelScope.json","w") as file:
                fileData={}
                fileData=str(fileData).replace("'", '"')
                logger.log(f"after{str(fileData)}","0")
                file.write(fileData)
                file.close()
                if os.path.exists("modelScope.json"):
                    logger.log(f"File created","0")

        with open ("modelScope.json","r") as file:
            FilejsonData = file.read()
            file.close()
            logger.log(f"FilejsonData::{FilejsonData},{type(FilejsonData)}","0")

            modelScopefileJson=json.loads(FilejsonData)
            logger.log(f"parsedJsonData::{modelScopefileJson},{type(modelScopefileJson)}","0")
        

        if modelScope == "global":
            if modelScope in modelScopefileJson:
                if modelName not in modelScopefileJson[modelScope]:
                    modelScopefileJson[modelScope].append(modelName)
                else:
                    logger.log(f"ModelName exists","0")
                logger.log(f"if::{modelScopefileJson}","0")
            else:
                modelScopefileJson[modelScope] = [modelName]
        elif modelScope == "enterprise":
            if modelScope in modelScopefileJson:
                if enterprise_key not in modelScopefileJson[modelScope]:
                    logger.log(f"enterprise_key if","0")
                    modelScopefileJson[modelScope][enterprise_key]=[modelName]
                else:    
                    logger.log(f"enterprise_key else","0")
                    if not modelName in modelScopefileJson[modelScope][enterprise_key]:
                        modelScopefileJson[modelScope][enterprise_key].append(modelName)
                    else:
                        logger.log(f"ModelName exists","0")
            else:
                modelScopefileJson[modelScope] = {enterprise_key:[modelName]}
        else:
            logger.log(f"Invalid modelScope received:: {modelScope}","0")
        logger.log(f"data: {modelScopefileJson}","0")

        with open ("modelScope.json","w") as file:
                
            modelScopefileJson=str(modelScopefileJson).replace("'", '"')
            logger.log(f"after line 1198 :: {str(modelScopefileJson)}","0")
            file.write(modelScopefileJson)
            file.close()
            logger.log(f"File updated","0")
        
        return "File Updated successfully "
    
        


    
