from flask import jsonify
import pandas as pd
from bokeh.embed import components
from bokeh.resources import INLINE
import random
import numpy as np

class ManageResources():
    @classmethod
    def queryExecute(self,db,query,insert=False):
        """ This function in case than insert is false only execute a Query, and return a 
        DataFrame with the values of Query, the arguments are the data base
        and the Query than need to execute, id insert isn´t false only execute the Query"""
        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            if insert==False:
                #get the DataFrame
                answer=cursor.fetchall()
                answerDataFrame=pd.DataFrame(answer)
                db.connection.commit()
                return answerDataFrame
            else:
                db.connection.commit()
                return jsonify({"mesage":"Insert data Ok!"})
            
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def extractResource(self,graph):
        """ This function is for extract the script, div, JS_resources and CSS_resources
        from bokeh graphs, for can render in the diferentes templates."""
        script,div=components(graph)
        js_resources=INLINE.render_js()
        css_resources=INLINE.render_css()
        data={
            "script":script,
            "div":div,
            "js_resources":js_resources,
            "css_resources":css_resources
        }
        return data
    
    @classmethod
    def joinDictionary(self,dictionary_list):
        """
        This function Join a list of dictionary for create a 
        big dictionary than can render in the HTML templates, specific a dictionary
        with this keys:
        data={
            "script":script,
            "div":div,
            "js_resources":js_resources,
            "css_resources":css_resources
        } 
        This function is specific for join this kind of dictionary
        """
        keys_list=list(dictionary_list[0].keys())
        for i in range(len(dictionary_list)):
            for j in keys_list:
                dictionary_list[i][j+str(i+1)]=dictionary_list[i].pop(j)
        dictionary_master={}
        for i in range(len(dictionary_list)):
            dictionary_master=dictionary_master|dictionary_list[i]
        return dictionary_master

    @classmethod
    def changeName(self,data,*args):
        """
        This function changes the name from the data frame,and return a new data with the name
        changed, the argumentes than need is the data, and the names
        """
        columnsName=list(data.columns)
        for i in range(len(args)):
            data=data.rename(columns={columnsName[i]:args[i]})
        return data
    
    @classmethod
    def concatColumns(self,data):
        names=list(data.columns)
        datas=[]
        for i in range(len(names)):
            newData=pd.DataFrame(data.loc[:,names[i]])
            newData=newData.rename(columns={names[i]:"Values"})
            newData["Name"]=names[i]
            datas.append(newData)
        dataConcat=pd.concat(datas)
        dataConcat=dataConcat.reset_index(drop=True)
        return dataConcat
            

def centralLimit(dataFrame,column,numberSample):
    """ This function return a data frame where was aplied the
    limit central theorem with the numberSample than you specific in the function"""
    #Limit central logic
    #Get a sample from the sizeData describe for the follow ecuation
    proportion=0.5
    statiscZ=1.96
    error=0.05
    sizeData=dataFrame[column].count()
    sizeSample=(sizeData*statiscZ**2)*proportion*(1-proportion)/((sizeData-1)*error+(statiscZ**2)*proportion*(1-proportion))
    sizeSample=int(round(sizeSample,0))
    numberSample=int(numberSample)
    list_dataframe_values=list(dataFrame[column])
    #Get a mean of a sample from the original dataframe, and add this in a list
    meanSample=[np.array(random.sample(list_dataframe_values,k=sizeSample)).mean() for i in range(numberSample)]
    #Get a second data frame
    data={
    column:meanSample
    }
    sampleDataFrame=pd.DataFrame(data)
    return sampleDataFrame