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
from DB.CRUD import QueryExecute,joindictionary,insertdata
from DB.Query import QueryDashboard
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
    #Distribution about the sample river up
    query=QueryDashboard.sample_upriver()
    data1=QueryExecute.queryexecute(db,query,'River_up')
    
    #Distribution about the sample river down
    query2=QueryDashboard.sample_downriver()
    data2=QueryExecute.queryexecute(db,query2,'River_down')
    
    #Distribution about the dependient variable for the experiment
    query3=QueryDashboard.experiment_dependient_variable()
    data3=QueryExecute.queryexecute(db,query3,'Amoniac_sample')

    #Distribution about the independient variable for the experiment
    query4=QueryDashboard.experiment_independient_variable()
    data4=QueryExecute.queryexecute(db,query4,'Force_sample')
    
    #Get the lineal regression graph for the data base than have the client.
    query5=QueryDashboard.regresion_data()
    data5=QueryExecute.queryexecute_lineal_regression(db,query5,'Force_sample','Amoniac_sample')

    #boxplot from sample amoniac about river up and river down
    query6=QueryDashboard.boxplot_sampleriver()
    data6=QueryExecute.queryexecute_boxplot(db,query6,'River up','River_down')

    #Join the data for make the dashboard
    join=joindictionary([data1,data2,data3,data4,data5,data6])
    return render_template('home.html',data=join)

@app.route('/insert',methods=['GET','POST'])
@login_required
def insert():
    formulario=Forms()
    if request.method=='POST':
        query1=QueryDashboard.regresion_data()
        data1=QueryExecute.queryexecute_lineal_regression(db,query1,'Amoniac_sample','Force_sample')
        a=float(request.form['FORCE_APPLY'])
        data2=QueryExecute.queryexecute_lineal_regression_calculated(db,query1,'Force_apply','Amoniac_sample',a)
        query2=QueryDashboard.querypareto()
        data3=QueryExecute.queryexecute_pareto(db,query2)
        data_total=data1|data2
        data_total=data_total|data3
        return render_template('CRUD/Insert.html',data=data_total,form=formulario)
    
    else:
        query1=QueryDashboard.regresion_data()
        data1=QueryExecute.queryexecute_lineal_regression(db,query1,'Amoniac_sample','Force_sample')
        a=float(0)
        data2=QueryExecute.queryexecute_lineal_regression_calculated(db,query1,'Force_apply','Amoniac_sample',a)
        query2=QueryDashboard.querypareto()
        data3=QueryExecute.queryexecute_pareto(db,query2)
        data_total=data1|data2
        data_total=data_total|data3
        return render_template('CRUD/Insert.html',data=data_total,form=formulario)
    

@app.route('/insert_value',methods=['GET','POST'])
def insert_value():
    if request.method=='POST':
        data_global={
            "ID":request.form['ID'],
            "FORCE_APPLY":request.form['FORCE_APPLY'],
            "QUANTITY_AMONIAC":request.form['QUANTITY_AMONIAC']
        }
        query=QueryDashboard.insertquery(data_global)
        insert_user=insertdata(db,query)
        print(data_global)
        return redirect(url_for('insert'))
    else:
        return redirect(url_for('insert'))

@app.route('/central_limit')
def central_limit():
    query1=QueryDashboard.sample_upriver()
    #queryexecute_central_limit(self,db,query,column,n_data=100)
    data1=QueryExecute.queryexecute(db,query1,'River_up')
    data2=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=10,color="#039255")
    data3=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=20,color="#12B063")
    data4=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=100,color="#12B063")
    data5=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=500,color="#00F980")
    data6=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=1000,color="#0CE149")
    join=joindictionary([data1,data2,data3,data4,data5,data6])
    return render_template('CRUD/Read.html',data=join)

@app.route('/central_limit2')
def central_limit2():
    query1=QueryDashboard.sample_downriver()
    #queryexecute_central_limit(self,db,query,column,n_data=100)
    data1=QueryExecute.queryexecute(db,query1,'River_down')
    data2=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=10,color="#0DA0A0")
    data3=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=20,color="#1FABA3")
    data4=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=100,color="#0FBABA")
    data5=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=500,color="#0AC7C7")
    data6=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=1000,color="#00EEEE")
    join=joindictionary([data1,data2,data3,data4,data5,data6])
    return render_template('CRUD/Read.html',data=join)

@app.route('/central_limit4')
def central_limit4():
    query1=QueryDashboard.experiment_independient_variable()
    #queryexecute_central_limit(self,db,query,column,n_data=100)
    data1=QueryExecute.queryexecute(db,query1,'River_down')
    data2=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=10,color="#0DA0A0")
    data3=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=20,color="#1FABA3")
    data4=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=100,color="#0FBABA")
    data5=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=500,color="#0AC7C7")
    data6=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER DOWN',n_data=1000,color="#00EEEE")
    join=joindictionary([data1,data2,data3,data4,data5,data6])
    return render_template('CRUD/Read.html',data=join)

@app.route('/central_limit3')
def central_limit3():
    query1=QueryDashboard.experiment_dependient_variable()
    #queryexecute_central_limit(self,db,query,column,n_data=100)
    data1=QueryExecute.queryexecute(db,query1,'River_up')
    data2=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=10,color="#039255")
    data3=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=20,color="#12B063")
    data4=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=100,color="#12B063")
    data5=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=500,color="#00F980")
    data6=QueryExecute.queryexecute_central_limit(db,query1,'SAMPLE RIVER UP',n_data=1000,color="#0CE149")
    join=joindictionary([data1,data2,data3,data4,data5,data6])
    return render_template('CRUD/Read.html',data=join)


if __name__=='__main__':
    app.config.from_object(externalobject['Config'])
    app.run()