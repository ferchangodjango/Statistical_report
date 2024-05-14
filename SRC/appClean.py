from flask import Flask,request,render_template,url_for,redirect,flash
from config import externalobject
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_required,login_user,logout_user
#Entities
from Models.entities.User import User
from Models.Models import ModelUser
#Forms
from Forms.forms import Forms
#CRUD
from DB.ManageResources import ManageResources,centralLimit
from DB.Query import QueryDashboard
#Statistic
from Statistic.StatisticModels import lineal_regression_calculated
#Graphs
from Graphs.Graphs import histogram_plot,lineal_regression,Box_Plot,Pareto,limits_regression
#Seguridd
from flask_wtf.csrf import CSRFProtect

app=Flask(__name__)
db=MySQL(app)
loginmanager=LoginManager(app)
csrf=CSRFProtect(app)

@loginmanager.user_loader
def get_by_id(id):
    return ModelUser.get_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    """This is the login function, and validate the credential from access to the website"""
    if request.method=='POST':
        user=User(None,request.form['username'],request.form['password'])
        user_logged=ModelUser.logged_user(db,user)
        if user_logged !=None:
            if user_logged.PASSWORD:
                login_user(user_logged)
                return redirect(url_for('home'))
            else:
                flash('Invalid Password')
                return render_template('Auth/login.html')
        else :
            flash('User not found')
            return render_template('Auth/login.html')
    else:
        return render_template('Auth/login.html')

@app.route('/home')
@login_required
def home():
    """This function return a view from the main Lay Out"""

    #Get the data for sample river up and river down
    querySampleRiver=QueryDashboard.boxplot_sampleriver()
    DataSampleRiver=ManageResources.queryExecute(db,querySampleRiver)
    DataSampleRiver=ManageResources.changeName(DataSampleRiver,'SAMPLE_RIVER_UP','SAMPLE_RIVER_DOWN')
    histogramRiverUp=histogram_plot(DataSampleRiver,'SAMPLE_RIVER_UP','Sample of amoniac river Up','normal',width=500,height=400)
    histogramRiverDown=histogram_plot(DataSampleRiver,'SAMPLE_RIVER_DOWN','Sample of amoniac river down','normal',width=500,height=400)

    #Get graph for regression data
    queryExperimentData=QueryDashboard.regresion_data()
    DataExperiment=ManageResources.queryExecute(db,queryExperimentData)
    DataExperiment=ManageResources.changeName(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE')
    HistogramDataExperimentForce=histogram_plot(DataExperiment,'FORCE_SAMPLE','Quantity force apply','normal',width=500,height=400)
    HistogramDataExperimentAmoniac=histogram_plot(DataExperiment,'AMONIAC_SAMPLE','Percentage of amoniac','normal',width=500,height=400)

    #Get lineal regression graph
    RegressionExperiment=lineal_regression(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE',widht=500,heigth=400)

    #Get the box plot graph
    DataSampleRiverConcat=ManageResources.concatColumns(DataSampleRiver)
    BoxPlotSampleRiver=Box_Plot(DataSampleRiverConcat,"Name","Values",width=500,height=400)

    #Get the resources
    ResourceshistogramRiverUp=ManageResources.extractResource(histogramRiverUp)
    ResourceshistogramRiverDown=ManageResources.extractResource(histogramRiverDown)
    ResourcesHistogramDataExperimentForce=ManageResources.extractResource(HistogramDataExperimentForce)
    ResourcesHistogramDataExperimentAmoniac=ManageResources.extractResource(HistogramDataExperimentAmoniac)
    ResoucesLinealRegression=ManageResources.extractResource(RegressionExperiment)
    ResoucesBoxPlot=ManageResources.extractResource(BoxPlotSampleRiver)

    #Join the data for make the dashboard
    join=ManageResources.joinDictionary([ResourceshistogramRiverUp,
                                         ResourceshistogramRiverDown,
                                         ResourcesHistogramDataExperimentForce,
                                         ResourcesHistogramDataExperimentAmoniac,
                                         ResoucesLinealRegression,
                                         ResoucesBoxPlot])
    
    return render_template('homeClean.html',data=join)


@app.route('/insert',methods=['GET','POST'])
@login_required
def insert():
    formulario=Forms()
    if request.method=='POST':
        
        #calculated and show the regression lineal
        #Get the Query from the lineal regression and get the DataFrame
        queryExperimentData=QueryDashboard.regresion_data()
        DataExperiment=ManageResources.queryExecute(db,queryExperimentData)
        DataExperiment=ManageResources.changeName(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE')
        #Get the graph from this lineal regression
        RegressionExperiment=lineal_regression(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE',widht=500,heigth=400)
        #Get the resources from the graph(Data resources)
        ResoucesLinealRegression=ManageResources.extractResource(RegressionExperiment)

        #calculated and show the Pareto
        ProductivitytScients=QueryDashboard.querypareto()
        DataProductivitytScients=ManageResources.queryExecute(db,ProductivitytScients)
        DataProductivitytScients=ManageResources.changeName(DataProductivitytScients,'ID_ENGINIEER','QUANTITY')

        DataProductivitytScients['ID_ENGINIEER']=DataProductivitytScients['ID_ENGINIEER'].astype(str)
        DataProductivitytScients['QUANTITY']=DataProductivitytScients['QUANTITY'].astype(float)
        #(Data resources)
        ParetoProductivitytScients=Pareto(DataProductivitytScients,'ID_ENGINIEER','QUANTITY',color="#9B59B6",width=500,height=300)
        ResourcesPareto=ManageResources.extractResource(ParetoProductivitytScients)

        #Calulated the estimation from the value that the user to want
        #Get the value than user want to calculated the estimation
        independientValue=float(request.form['FORCE_APPLY'])
        #Calulated the estimation for that value(Data resources).
        linealRegresionCalulated=lineal_regression_calculated(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE',independientValue)

        #Define the values for the next graph
        LPI=[linealRegresionCalulated["LIPI"],linealRegresionCalulated["LSPI"]]
        LPIF=[linealRegresionCalulated["LIPIF"],linealRegresionCalulated["LSPIF"]]

        GraphLimitsRegression=limits_regression(LPI,LPIF,widht=500,heigth=200)
        ResourcesGraphLimitsRegression=ManageResources.extractResource(GraphLimitsRegression)


        #Join Resources
        joinGraphsInsert=ManageResources.joinDictionary([ResoucesLinealRegression,ResourcesGraphLimitsRegression,ResourcesPareto])
        LocalDataInsert=joinGraphsInsert|linealRegresionCalulated
        return render_template('CRUD/Insert.html',data=LocalDataInsert,form=formulario)
    
    else:

        #calculated and show the regression lineal
        #Get the Query from the lineal regression and get the DataFrame
        queryExperimentData=QueryDashboard.regresion_data()
        DataExperiment=ManageResources.queryExecute(db,queryExperimentData)
        DataExperiment=ManageResources.changeName(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE')
        #Get the graph from this lineal regression
        RegressionExperiment=lineal_regression(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE',widht=500,heigth=400)
        #Get the resources from the graph(Data resources)
        ResoucesLinealRegression=ManageResources.extractResource(RegressionExperiment)

        #calculated and show the Pareto
        ProductivitytScients=QueryDashboard.querypareto()
        DataProductivitytScients=ManageResources.queryExecute(db,ProductivitytScients)
        DataProductivitytScients=ManageResources.changeName(DataProductivitytScients,'ID_ENGINIEER','QUANTITY')
        DataProductivitytScients['ID_ENGINIEER']=DataProductivitytScients['ID_ENGINIEER'].astype(str)
        DataProductivitytScients['QUANTITY']=DataProductivitytScients['QUANTITY'].astype(float)
        #(Data resources)
        ParetoProductivitytScients=Pareto(DataProductivitytScients,'ID_ENGINIEER','QUANTITY',color="#9B59B6",width=500,height=300)
        ResourcesPareto=ManageResources.extractResource(ParetoProductivitytScients)

        #Calulated the estimation from the value that the user to want
        #Get the value than user want to calculated the estimation
        independientValue=0
        #Calulated the estimation for that value(Data resources).
        linealRegresionCalulated=lineal_regression_calculated(DataExperiment,'FORCE_SAMPLE','AMONIAC_SAMPLE',independientValue)

        #Define the values for the next graph
        LPI=[linealRegresionCalulated["LIPI"],linealRegresionCalulated["LSPI"]]
        LPIF=[linealRegresionCalulated["LIPIF"],linealRegresionCalulated["LSPIF"]]

        GraphLimitsRegression=limits_regression(LPI,LPIF,widht=500,heigth=200)
        ResourcesGraphLimitsRegression=ManageResources.extractResource(GraphLimitsRegression)


        #Join Resources
        joinGraphsInsert=ManageResources.joinDictionary([ResoucesLinealRegression,ResourcesGraphLimitsRegression,ResourcesPareto])
        LocalDataInsert=joinGraphsInsert|linealRegresionCalulated
        return render_template('CRUD/Insert.html',data=LocalDataInsert,form=formulario)


@app.route('/insert_value',methods=['GET','POST'])
def insert_value():
    if request.method=='POST':
        data_global={
            "ID":request.form['ID'],
            "FORCE_APPLY":request.form['FORCE_APPLY'],
            "QUANTITY_AMONIAC":request.form['QUANTITY_AMONIAC']
        }
        query=QueryDashboard.insertquery(data_global)
        insert_user=ManageResources.queryExecute(db,query,insert=True)
        print(data_global)
        return redirect(url_for('insert'))
    else:
        return redirect(url_for('insert'))


@app.route('/AmoniacRiverUp_centralLimit')
def AmoniacRiverUp_centralLimit():
    """This function create a view for demostrate the limit central theorem"""
    #Execute the query and get the data
    query=QueryDashboard.boxplot_sampleriver()
    Data=ManageResources.queryExecute(db,query)
    Data=ManageResources.changeName(Data,'SAMPLE_RIVER_UP','SAMPLE_RIVER_DOWN')
    Histogram=histogram_plot(Data,'SAMPLE_RIVER_UP','Sample of amoniac river Up','normal',width=500,height=400)

    #def centralLimit(dataFrame,column,numberSample):
    ListNumberSample=[10,20,100,500,1000]
    ListColor=["#039255","#12B063","#12B063","#00F980","#0CE149"]
    ListHistograms=[]
    ListResourcesHistogram=[]
    ListHistograms.append(Histogram)

    #Get all the graphs
    for i in range(len(ListNumberSample)):
        DataCentralLimit=centralLimit(Data,'SAMPLE_RIVER_UP',ListNumberSample[i])
        HistogramCentralLimit=histogram_plot(DataCentralLimit,'SAMPLE_RIVER_UP','Sample of amoniac river Up','normal',width=500,height=400,color=ListColor[i])
        ListHistograms.append(HistogramCentralLimit)

    for j in range(len(ListHistograms)):
        Resourceshistogram=ManageResources.extractResource(ListHistograms[j])
        ListResourcesHistogram.append(Resourceshistogram)
        
    join=ManageResources.joinDictionary(ListResourcesHistogram)
    return render_template('CRUD/Read.html',data=join)

@app.route('/AmoniacRiverDown_centralLimit')
def AmoniacRiverDown_centralLimit():
    """This function create a view for demostrate the limit central theorem"""
    #Execute the query and get the data
    query=QueryDashboard.boxplot_sampleriver()
    Data=ManageResources.queryExecute(db,query)
    Data=ManageResources.changeName(Data,'SAMPLE_RIVER_UP','SAMPLE_RIVER_DOWN')
    Histogram=histogram_plot(Data,'SAMPLE_RIVER_DOWN','Sample of amoniac river Up','normal',width=500,height=400)

    #def centralLimit(dataFrame,column,numberSample):
    ListNumberSample=[10,20,100,500,1000]
    ListColor=["#039255","#12B063","#12B063","#00F980","#0CE149"]
    ListHistograms=[]
    ListResourcesHistogram=[]
    ListHistograms.append(Histogram)

    #Get all the graphs
    for i in range(len(ListNumberSample)):
        DataCentralLimit=centralLimit(Data,'SAMPLE_RIVER_DOWN',ListNumberSample[i])
        HistogramCentralLimit=histogram_plot(DataCentralLimit,'SAMPLE_RIVER_DOWN','Sample of amoniac river down','normal',width=500,height=400,color=ListColor[i])
        ListHistograms.append(HistogramCentralLimit)

    for j in range(len(ListHistograms)):
        Resourceshistogram=ManageResources.extractResource(ListHistograms[j])
        ListResourcesHistogram.append(Resourceshistogram)
        
    join=ManageResources.joinDictionary(ListResourcesHistogram)
    return render_template('CRUD/Read.html',data=join)

@app.route('/Force_centralLimit')
def Force_centralLimit():
    """This function create a view for demostrate the limit central theorem"""
    #Execute the query and get the data
    Query=QueryDashboard.regresion_data()
    Data=ManageResources.queryExecute(db,Query)
    Data=ManageResources.changeName(Data,'FORCE_SAMPLE','AMONIAC_SAMPLE')
    Histogram=histogram_plot(Data,'FORCE_SAMPLE','Quantity force apply','normal',width=500,height=400)
    

    #def centralLimit(dataFrame,column,numberSample):
    ListNumberSample=[10,20,100,500,1000]
    ListColor=["#039255","#12B063","#12B063","#00F980","#0CE149"]
    ListHistograms=[]
    ListResourcesHistogram=[]
    ListHistograms.append(Histogram)

    #Get all the graphs
    for i in range(len(ListNumberSample)):

        DataCentralLimit=centralLimit(Data,'FORCE_SAMPLE',ListNumberSample[i])
        HistogramCentralLimit=histogram_plot(DataCentralLimit,'FORCE_SAMPLE','Quantity force apply','normal',width=500,height=400,color=ListColor[i])
        ListHistograms.append(HistogramCentralLimit)

    for j in range(len(ListHistograms)):
        Resourceshistogram=ManageResources.extractResource(ListHistograms[j])
        ListResourcesHistogram.append(Resourceshistogram)
        
    join=ManageResources.joinDictionary(ListResourcesHistogram)
    return render_template('CRUD/Read.html',data=join)

@app.route('/AmoniacExperiment_centralLimit')
def AmoniacExperiment_centralLimit():
    """This function create a view for demostrate the limit central theorem"""
    #Execute the query and get the data
    Query=QueryDashboard.regresion_data()
    Data=ManageResources.queryExecute(db,Query)
    Data=ManageResources.changeName(Data,'FORCE_SAMPLE','AMONIAC_SAMPLE')
    Histogram=histogram_plot(Data,'AMONIAC_SAMPLE','Percentage of amoniac','normal',width=500,height=400)
    

    #def centralLimit(dataFrame,column,numberSample):
    ListNumberSample=[10,20,100,500,1000]
    ListColor=["#039255","#12B063","#12B063","#00F980","#0CE149"]
    ListHistograms=[]
    ListResourcesHistogram=[]
    ListHistograms.append(Histogram)

    #Get all the graphs
    for i in range(len(ListNumberSample)):

        DataCentralLimit=centralLimit(Data,'AMONIAC_SAMPLE',ListNumberSample[i])
        HistogramCentralLimit=histogram_plot(DataCentralLimit,'AMONIAC_SAMPLE','Percentage of amoniac','normal',width=500,height=400,color=ListColor[i])
        ListHistograms.append(HistogramCentralLimit)

    for j in range(len(ListHistograms)):
        Resourceshistogram=ManageResources.extractResource(ListHistograms[j])
        ListResourcesHistogram.append(Resourceshistogram)
        
    join=ManageResources.joinDictionary(ListResourcesHistogram)
    return render_template('CRUD/Read.html',data=join)

if __name__=='__main__':
    app.config.from_object(externalobject['Config'])
    app.run()