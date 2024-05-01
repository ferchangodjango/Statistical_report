from flask import jsonify
import pandas as pd
from Graphs.Graphs import histogram_plot,lineal_regression,Box_Plot,Pareto
from bokeh.embed import components
from bokeh.resources import INLINE
from Statistic.StatisticModels import lineal_regression_calculated
import random
import numpy as np

def insertdata(db,query):

    try:
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()

        return jsonify({"mesage":"Insert data Ok!"})
    except Exception as ex:
        raise Exception(ex)
    
class QueryExecute():
    @classmethod
    def queryexecute(self,db,query,column1):

        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    column1:row[0]}
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME[column1]=DATA_FRAME[column1].astype(float)
        
            #Get the DataFrame
            m1=DATA_FRAME[column1].mean()
            std1=DATA_FRAME[column1].std()

            histogram=histogram_plot(DATA_FRAME,column1,column1,'normal',m=m1,std=std1,ancho=500,alto=500)
            
            #Get the components about the DataFrame
            script,div=components(histogram)
            js_resources=INLINE.render_js()
            css_resources=INLINE.render_css()
            data={
                "script":script,
                "div":div,
                "js_resources":js_resources,
                "css_resources":css_resources
            }
            
            return data
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def queryexecute_lineal_regression(self,db,query,column1,column2):

        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    column1:row[0],
                    column2:row[1]}
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME[column1]=DATA_FRAME[column1].astype(float)
            DATA_FRAME[column2]=DATA_FRAME[column2].astype(float)
        



            graph=lineal_regression(DATA_FRAME,column1,column2,widht=500,heigth=500)
            
            #Get the components about the DataFrame
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
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def queryexecute_boxplot(self,db,query,column1,column2):

        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    'Data':row[0],
                    'Index':column1
                    }
                answers.append(row_answer)

            for row in answer:
                row_answer={
                    'Data':row[1],
                    'Index':column2
                    }
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME['Data']=DATA_FRAME['Data'].astype(float)
        



            graph=Box_Plot(DATA_FRAME,'Index','Data',width=500,height=500)
            
            #Get the components about the DataFrame
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
        
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def queryexecute_pareto(self,db,query):
        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    'ID_ENGINIEER':row[0],
                    'QUANTITY':row[1]}
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME['ID_ENGINIEER']=DATA_FRAME['ID_ENGINIEER'].astype(str)
            DATA_FRAME['QUANTITY']=DATA_FRAME['QUANTITY'].astype(float)
        

            pareto=Pareto(DATA_FRAME,'ID_ENGINIEER','QUANTITY')
            
            #Get the components about the DataFrame
            script,div=components(pareto)
            js_resources=INLINE.render_js()
            css_resources=INLINE.render_css()
            data={
                "script3":script,
                "div3":div,
                "js_resources3":js_resources,
                "css_resources3":css_resources
            }
            
            return data
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def queryexecute_central_limit(self,db,query,column,n_data=100,color="#008080"):
        """ This function return a components from a histogram, for test the central limit
        theory"""
        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    column:row[0]
                    }
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME[column]=DATA_FRAME[column].astype(float)

            #Limit central logic
            #Get a sample from the size describe for the follow ecuation
            p=0.5
            z=1.96
            e=0.05
            N=DATA_FRAME[column].count()
            n=(N*z**2)*p*(1-p)/((N-1)*e+(z**2)*p*(1-p))
            k1=int(round(n,0))
            n_datacheck=int(n_data)
            list_dataframe_values=list(DATA_FRAME[column])

            #Get a mean of a sample from the original dataframe, and add this in a list
            a=[np.array(random.sample(list_dataframe_values,k=k1)).mean() for i in range(n_datacheck)]
            #Get a second data frame
            data={
            column:a
            }
            df_2=pd.DataFrame(data)

            #Get a histogram from the second data frame
            graph=histogram_plot(df_2,column,'normality_test','normal',m=df_2[column].mean(),std=df_2[column].std(),ancho=500,alto=500,color=color)
             
            #Get the components about the DataFrame
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
        
        except Exception as ex:
            raise Exception(ex)
        
    

    @classmethod
    def queryexecute_lineal_regression_calculated(self,db,query,column1,column2,variable):
        try:
            #get the connection
            cursor=db.connection.cursor()
            cursor.execute(query)
            #get the DataFrame
            answer=cursor.fetchall()
            answers=[]
            for row in answer:
                row_answer={
                    column1:row[0],
                    column2:row[1]}
                answers.append(row_answer)

            JSONIFY_TOTAL=jsonify({
                "TABLA":answers,
                "message":"Get data ok!!"
                })
            JSON_TOTAL=JSONIFY_TOTAL.get_json()
            DATA_FRAME=pd.json_normalize(JSON_TOTAL['TABLA'])
            DATA_FRAME[column1]=DATA_FRAME[column1].astype(float)
            DATA_FRAME[column2]=DATA_FRAME[column2].astype(float)
        



            data=lineal_regression_calculated(DATA_FRAME,column1,column2,variable)
            return data
        except Exception as ex:
            raise Exception(ex)


def joindictionary(dictionary_list):
    keys_list=list(dictionary_list[0].keys())
    for i in range(len(dictionary_list)):
        for j in keys_list:
            dictionary_list[i][j+str(i+1)]=dictionary_list[i].pop(j)
    dictionary_master={}
    for i in range(len(dictionary_list)):
        dictionary_master=dictionary_master|dictionary_list[i]
    
    return dictionary_master