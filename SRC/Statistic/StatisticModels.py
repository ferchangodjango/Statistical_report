import pingouin as pgn
from scipy import stats
import pandas as pd
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure

def lineal_regression_calculated(data,column1,column2,variable,widht=500,heigth=300):

    #Calculo de la regresion lineal.
    rls=pgn.linear_regression(X=data[column1],y=data[column2],as_dataframe=False)
    b0=rls['coef'][0]
    b1=rls['coef'][1]

    data['Y_Estimada']=b0+b1*data[column1]
    
    
    #Calculo de la media y el numero de datos en la columna.
    x_media=(data[column1].mean())
    n=len(data[column1])
    #Calculo del estadistico t para los intervalos de confianza y predicción respectivamente.
    alpha=0.05
    stadistic=abs(stats.t.ppf(alpha/2,df=n-2))
    #Calculo de Sxx
    data['Error']=+data[column2]-data['Y_Estimada']
    data['Error_Sqr']=+(data['Error'])**2
    s_sqr=(data['Error_Sqr'].sum())/(n-2)
    s=s_sqr**0.5
    data['xx']=(data[column1]-x_media)**2
    #Constante
    Sxx=data['xx'].sum()
    
    data['LIPI']=data['Y_Estimada']-stadistic*s*((1/n)+((data[column1]-x_media)**2/Sxx))**0.5
    data['LSPI']=data['Y_Estimada']+stadistic*s*((1/n)+((data[column1]-x_media)**2/Sxx))**0.5

    data['LIPIF']=data['Y_Estimada']-stadistic*s*(1+(1/n)+((data[column1]-x_media)**2/Sxx))**0.5
    data['LSPIF']=data['Y_Estimada']+stadistic*s*(1+(1/n)+((data[column1]-x_media)**2/Sxx))**0.5


    min_value=int(data[column1].min())-1
    max_value=int(data[column1].max())+1
    #Ecuación de regresión lineal simple
    x=variable
    Y_estimada=(float(b0)+float(b1)*x)
    
    #Ecuación de limite infererior y superior de predicción inside (lipi & lspi)
    LIPI=(Y_estimada-stadistic*s*((1/n)+((x-x_media)**2/Sxx))**0.5)
    LSPI=(Y_estimada+stadistic*s*((1/n)+((x-x_media)**2/Sxx))**0.5)

    #Ecuación de limite infererior y superior de predicción future (lipif & lspif)
    LIPIF=(Y_estimada-stadistic*s*(1+(1/n)+((x-x_media)**2/Sxx))**0.5)
    LSPIF=(Y_estimada+stadistic*s*(1+(1/n)+((x-x_media)**2/Sxx))**0.5)
    
    x1=[LIPI,LSPI]
    x2=[LIPIF,LSPIF]
    y1=[1,1]
    y2=[2,2]

    figure1=figure(
        title="Intervals graph",
        plot_width=widht,plot_height=heigth,
        toolbar_location='below')

    figure1.xgrid.grid_line_color=None
    figure1.xaxis.major_label_text_font_size='15px'
    figure1.toolbar.autohide=True

    figure1.line(x1,y1,color='green')
    figure1.line(x2,y2,color='blue')
    figure1.varea(x=x1,
                  y1=y1,
                  y2=y2,alpha=0.5)
    figure1.varea(x=x2,
                  y1=y1,
                  y2=y2,alpha=0.5)

    script,div=components(figure1)
    js_resources=INLINE.render_js()
    css_resources=INLINE.render_css()


    data={
        "Y_estimada":round(Y_estimada,3),
        "LIPI":round(LIPI,3),
        "LSPI":round(LSPI,3),
        "LIPIF":round(LIPIF,3),
        "LSPIF":round(LSPIF,3),
        "script2":script,
        "div2":div,
        "js_resources2":js_resources,
        "css_resources2":css_resources
      }
    
    return data