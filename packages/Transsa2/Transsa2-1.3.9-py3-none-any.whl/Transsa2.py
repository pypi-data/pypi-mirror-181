#!/usr/bin/env python
# coding: utf-8

# In[1]:


################################### Paquetes ######################################################

import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict
import joblib
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

#################################### Funciones ##############################################


# Función para agregar columnas con indices (ufm2, etc) y cambiar el tipo de
# dato de ciertas columnas
def InsertColumns(D):
    D=D.astype({'antiguedad':'float64','supCSII':'float64','supTSII':'float64','valor':'float64'})
    D.insert(D.shape[1],'ufm2(supCSII)',D.loc[:,'valor']/D.loc[:,'supCSII'], True) 
    D.insert(D.shape[1],'ufm2(supTSII)',D.loc[:,'valor']/D.loc[:,'supTSII'], True)
    D.insert(D.shape[1],'supTSII/supCSII',D.loc[:,'supTSII']/D.loc[:,'supCSII'], True) 
    return D

# Concatenación de tablas de ventas y tasaciones
def tabla_auxiliar(df1,df2,method):
    while (method!="ML" and method!="AVM"):
        print("El método seleccionado no es válido")
        method=input("Ingrese correctamente el método a utilizar (ML o AVM): ")
    if method=="ML":
        df1_aux=df1[['antiguedad','longitud',
           'latitud','supCSII','supTSII','valor','cve_comuna',
           'ufm2(supCSII)','ufm2(supTSII)','supTSII/supCSII']]
        df2_aux=df2[['antiguedad','longitud',
           'latitud','supCSII','supTSII','valor','cve_comuna',
           'ufm2(supCSII)','ufm2(supTSII)','supTSII/supCSII']]
    else:
        df1_aux=df1[['num_','cve_propiedad','rol','cve_comuna','cve_region','ah','ah_hom','zona_eod',
             'zona_jjvv','materialidad','antiguedad','longitud',
             'latitud','supCSII','supTSII','valor']]
        df2_aux=df2[['num_','cve_propiedad','rol','cve_comuna','cve_region','ah','ah_hom','zona_eod',
             'zona_jjvv','materialidad','antiguedad','longitud',
             'latitud','supCSII','supTSII','valor']]
    df1_df2_aux=pd.concat([df1_aux,df2_aux], ignore_index=True, sort=False)
    df1_df2_aux=df1_df2_aux.dropna()
    return df1_df2_aux

# Selección de comuna
def Selec_Comuna(D1,cve):
    comunas=[19,21,22,52]
    while cve not in comunas:
        print('Ingrese alguna de las siguientes comunas: La Reina (19), Las Condes (21), Lo Barnechea (22) o Vitacura (52):')
        cve=int(input())
    if cve==52:
        tol=5000
    else:
        tol=1000
    D_comuna=D1.loc[(D1.loc[:,'cve_comuna']==cve) & (D1.loc[:,'valor']>=tol)]
    return D_comuna

# Eliminación de datos duplicados
def datosduplicados(tabla,T):
    n_inicial = tabla.shape[0];
    tabla2 = tabla.drop_duplicates(subset=['longitud','latitud',
                                          'supCSII','supTSII','valor'])
    
    if T==True:
        print(f'Hay {n_inicial-tabla2.shape[0]} datos duplicados')
        print(f'Al eliminarlos quedan {tabla2.shape[0]} datos')
    return tabla2

#Identificación de atípicos dada una columna
def outliers_col(df,columna,n,a,T,n_i):
    tabla= pd.DataFrame.from_dict({
    'Variable': [],'Cantidad de Atípicos': [],
    'Type': []});
    col = ['Variable','Cantidad de Atípicos','Type'];
    k=0;
    if (a=='zscore'):
        n_outliers = len(df[np.abs(stats.zscore(df[columna])) > 3])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
        
    if (a=='IQR'):
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        n_outliers = len(df[(df[columna] > ul) | (df[columna] < ll)])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    if T==True:
        print(tabulate(tabla, headers=col, tablefmt="fancy_grid"))  
        print('\nSe eliminarán:',k,'datos, y quedarán al menos:',n-k)
        print('en porcentaje con respecto a la cantidad inicial:',(n-k)*100/n_i,'%.\n')     
    return k,tabla

#Eliminación de atípicos dada una columna
def outliers_col_eliminacion(df,columna,a):
    if a=='zscore':
        l=df[np.abs(stats.zscore(df[columna])) > 3].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
                
    if a=='IQR':
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        l=df[(df[columna] > ul) | (df[columna] < ll)].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
    
    df=df.dropna(axis = 0);
    return df

# Gráficas
def grafico_histograma_sns(df,columna,option1,option2):
    plt.figure(figsize = (9,4))
    sns.set_style("whitegrid")
    sns.histplot(data=df[columna],color="#008080",
                 kde=option1,discrete=option2,bins=100);
    plt.xlabel(None)
    plt.title(columna);
    plt.ylabel('Cantidad')
    plt.show() 
    
def grafico_boxplot_jitted(df,columna,jit):
    plt.rcParams['figure.figsize'] = (9,4)
    red_cir = dict(markerfacecolor='r',marker='o',markersize=6)
    sns.set_style("whitegrid")
    
    if(jit=='no'):
         sns.boxplot(y=df[columna],color="#008080",
                     flierprops=red_cir).set_title(columna);  
    else:
        ax=sns.boxplot(x=df[columna],data=df,color="#008080",
                flierprops=red_cir).set_title(columna); 
        ax=sns.stripplot(x=df[columna], data=df, color="orange", jitter=0.15, size=2.5)
        
    plt.xlabel(None)    
    plt.show()

######## Función de gráficos y eliminación iterada de atípicos #######   
#atypicals_be_gone(ven_tas_comuna1,['valor','ufm2(supCSII)','ufm2(supTSII)'],False,'zscore')
def atypicals_be_gone(df,pars,T,metodo):
    ## Gráficos antes de la eliminación
    # Histogramas 1
    print(chr(27)+"[1;34m"+'Histogramas (con atípicos)')
    fig, axs = plt.subplots(3,1,figsize=(9,12));
    colors=['red','blue','orange']
    for j in range(0,len(pars)):
        sns.histplot(data=df,x=pars[j],bins=100,color=colors[j],kde= True,ax=axs[j]);
        axs[j].set_title(pars[j])
        axs[j].set_xlabel(None)
        axs[j].set_ylabel('Cantidad')
        axs[j].grid(True)
    plt.show()
    # Boxplots 1
    print(chr(27)+"[1;32m"+'Boxplots (con atípicos)')
    fig, axs = plt.subplots(3,1,figsize=(9,12));
    red_cir = dict(markerfacecolor='r',marker='o',markersize=6)
    for j in range(0,len(pars)):
        sns.boxplot(x=df[pars[j]],data=df,color="#008080",flierprops=red_cir,ax=axs[j]).set_title(pars[j]);
        sns.stripplot(x=df[pars[j]], data=df, color="orange", jitter=0.15, size=2.5,ax=axs[j])
        axs[j].grid(True)
        axs[j].set_xlabel(None)
    plt.show()
    ## Eliminación de atípicos  
    n_i=df.shape[0]
    for j in range(0,len(pars)):
        w=1
        if T==True:
            print(chr(27)+"[1;30m"+f'Eliminación de atípicos considerando: {pars[j]}',chr(27)+"[0;30m"+'')
        while (w!=0):
            [w,resum]=outliers_col(df,pars[j],df.shape[0],metodo,T,n_i);
            df=outliers_col_eliminacion(df,pars[j],metodo);
            
    ## Gráficos después de la eliminación
    # Histogramas 2
    print(chr(27)+"[1;34m"+'Histogramas (sin atípicos)')
    fig, axs = plt.subplots(3,1,figsize=(9,12));
    colors=['red','blue','orange']
    for j in range(0,len(pars)):
        sns.histplot(data=df,x=pars[j],bins=100,color=colors[j],kde= True,ax=axs[j]);
        axs[j].set_title(pars[j])
        axs[j].set_xlabel(None)
        axs[j].set_ylabel('Cantidad')
        axs[j].grid(True)
    plt.show()
    
    # Boxplots 2
    print(chr(27)+"[1;32m"+'Boxplots (sin atípicos)')
    fig, axs = plt.subplots(3,1,figsize=(9,12));
    red_cir = dict(markerfacecolor='r',marker='o',markersize=6)
    for j in range(0,len(pars)):
        sns.boxplot(x=df[pars[j]],data=df,color="#008080",flierprops=red_cir,ax=axs[j]).set_title(pars[j]);
        sns.stripplot(x=df[pars[j]], data=df, color="orange", jitter=0.15, size=2.5,ax=axs[j])
        axs[j].grid(True)
        axs[j].set_xlabel(None)
    plt.show()
    return df
# Matriz de correlación
def matriz_correlacion(df):
    matriz = df.corr(method='kendall')
    plt.rcParams['figure.figsize'] = (7,7);
    plt.matshow(matriz, cmap='BrBG', vmin=-1, vmax=1)
    plt.xticks(range(df.shape[1]), df.columns, rotation=90)
    plt.yticks(range(df.shape[1]), df.columns)

    for i in range(len(matriz.columns)):
          for j in range(len(matriz.columns)):
                 plt.text(i, j, round(matriz.iloc[i, j], 2),
                 ha="center", va="center")

    plt.colorbar()
    plt.grid(False)
    plt.show()

# Cálcular el tamaño de la muestra
def tam_muestra(ven_tas_comuna1,confianza):
    alpha=1-confianza # Confianza del 90%=0.9
    N=ven_tas_comuna1.shape[0]
    er=10/ven_tas_comuna1['valor'].mean()
    Z=stats.norm.ppf(1-alpha/2)
    COV=ven_tas_comuna1['valor'].std()/ven_tas_comuna1['valor'].mean()
    nmuestra=(N*(COV**2)*(Z**2))/((er**2)*(N-1)+(COV**2)*(Z**2))
    n_muestra=int(nmuestra)
    return n_muestra

def Muestra(df1,df2,cve):
    nn=tam_muestra(df1,0.9)
    n1=int(nn/10)
    N=df1.shape[0]
    n2=int(N/10)
    df3=df1.sort_values(by="valor", ascending= True)
    a=df3.iloc[0:n2,:]
    b=df3.iloc[n2:2*n2,:]
    c=df3.iloc[2*n2:3*n2,:]
    d=df3.iloc[3*n2:4*n2,:]
    e=df3.iloc[4*n2:5*n2,:]
    f=df3.iloc[5*n2:6*n2,:]
    g=df3.iloc[6*n2:7*n2,:]
    h=df3.iloc[7*n2:8*n2,:]
    i=df3.iloc[8*n2:9*n2,:]
    j=df3.iloc[9*n2:N+1,:]
    if n1==n2:
        A=a.sample(n=n1)
        B=b.sample(n=n1)
        C=c.sample(n=n1)
        D=d.sample(n=n1)
        E=e.sample(n=n1)
        F=f.sample(n=n1)
        G=g.sample(n=n1)
        H=h.sample(n=n1)
        I=i.sample(n=n1)
        J=j.sample(n=nn-9*n1)
    else:
        k,n3=0,n1
        while 10*n1+k<nn:
            k=k+1
            n3=n3+1
            A=a.sample(n=n3)
            if 10*n1+k==nn:
                B=b.sample(n=n1)
                C=c.sample(n=n1)
                D=d.sample(n=n1)
                E=e.sample(n=n1)
                F=f.sample(n=n1)
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break   
            k=k+1
            B=b.sample(n=n3)
            if 10*n1+k==nn:
                C=c.sample(n=n1)
                D=d.sample(n=n1)
                E=e.sample(n=n1)
                F=f.sample(n=n1)
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break
            k=k+1
            C=c.sample(n=n3)
            if 10*n1+k==nn:
                D=d.sample(n=n1)
                E=e.sample(n=n1)
                F=f.sample(n=n1)
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break  
            k=k+1
            D=d.sample(n=n3)
            if 10*n1+k==nn:
                E=e.sample(n=n1)
                F=f.sample(n=n1)
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break 
            k=k+1
            E=e.sample(n=n3)
            if 10*n1+k==nn:
                F=f.sample(n=n1)
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break 
            k=k+1
            F=f.sample(n=n3)
            if 10*n1+k==nn:
                G=g.sample(n=n1)
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break
            k=k+1
            G=g.sample(n=n3)
            if 10*n1+k==nn:
                H=h.sample(n=n1)
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break 
            k=k+1
            H=h.sample(n=n3)
            if 10*n1+k==nn:
                I=i.sample(n=n1)
                J=j.sample(n=n1)
                break 
            k=k+1
            I=i.sample(n=n3)
            if 10*n1+k==nn:
                J=j.sample(n=n1)
                break 
            k=k+1
            J=j.sample(n=n3)
    MuestraML=pd.concat([A,B,C,D,E,F,G,H,I,J],sort=False)
    MuestraML=datosduplicados(MuestraML,False)
    MuestraAVM=pd.merge(df2,MuestraML, how="right", 
                        on=["cve_comuna","antiguedad","longitud","latitud","supCSII","supTSII","valor"])
    nombre1='MuestraML'+str(cve)+'.xlsx'
    nombre2='MuestraAVM'+str(cve)+'.xlsx'
    MuestraML.to_excel(nombre1)
    MuestraAVM.to_excel(nombre2)
    return MuestraML,MuestraAVM


def Muestra_Total(A):
    if A=="ML":
        LR = pd.read_excel('MuestraLRML.xlsx');
        LC = pd.read_excel('MuestraLCML.xlsx');
        LB = pd.read_excel('MuestraLBML.xlsx');
        V = pd.read_excel('MuestraVML.xlsx');
        MuestraZOML = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        MuestraZOML.to_excel('MuestraZOML.xlsx')
    elif A=="AVM":
        LR = pd.read_excel('MuestraLRAVM.xlsx');
        LC = pd.read_excel('MuestraLCAVM.xlsx');
        LB = pd.read_excel('MuestraLBAVM.xlsx');
        V = pd.read_excel('MuestraVAVM.xlsx');
        MuestraZOML = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        MuestraZOML.to_excel('MuestraZOAVM.xlsx')
    return MuestraZOML
# Función que hace la indexacion de 10 y 5, además de asignar valores booleanos de acuerdo a dicha indexación

def indexacion(df,mini,maxi):
    years1=[]
    years2=[]
    for i in range(mini,maxi,10):
        years1.append(i)
    for j in range(mini,maxi,5):
        years2.append(j)
    if maxi not in years1:
        years1.append(maxi)
    if maxi not in years2:
        years2.append(maxi)
    conditionlist1=[]
    conditionlist2=[]
    for k in range(0,(len(years1))-2): 
        c=(df['antiguedad'] >=years1[k]) & (df['antiguedad'] <years1[k+1])
        conditionlist1.append(c)
    c=(df['antiguedad'] >=years1[(len(years1))-2]) & (df['antiguedad'] <=years1[(len(years1))-1])
    conditionlist1.append(c)
    L=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","W","X","Y","Z"]
    vectorS1=[]
    vectorS2=[]
    for i in range(0,len(years1)-2):
        vectorS1.append(L[i]+str(years1[i])+"/"+str(years1[i+1]-1))
    vectorS1.append(L[len(years1)-2]+str(years1[len(years1)-2])+"/"+str(years1[len(years1)-1]))
    choicelist1=[]
    for i in range(0,len(vectorS1)):
        choicelist1.append(vectorS1[i][0]+vectorS1[i][3:6]+vectorS1[i][8:10])
    
    for k in range(0,(len(years2))-2): 
        c2=(df['antiguedad'] >=years2[k]) & (df['antiguedad'] <years2[k+1])
        conditionlist2.append(c2)
    c2=(df['antiguedad'] >=years2[(len(years2))-2]) & (df['antiguedad'] <=years2[(len(years2))-1])
    conditionlist2.append(c2)
    for i in range(0,len(years2)-2):
        vectorS2.append(L[i]+str(years2[i])+"/"+str(years2[i+1]-1))
    vectorS2.append(L[len(years2)-2]+str(years2[len(years2)-2])+"/"+str(years2[len(years2)-1]))    
    choicelist2=[]
    for i in range(0,len(vectorS2)):
        choicelist2.append(vectorS2[i][0]+vectorS2[i][3:6]+vectorS2[i][8:10])
    df.insert(df.shape[1],'Index_antiguedad_10',np.select(conditionlist1, choicelist1, default=0))
    df.insert(df.shape[1],'Index_antiguedad_5',np.select(conditionlist2, choicelist2, default=0))
    df2=df.astype({'antiguedad':'float64','supCSII':'float64','supTSII':'float64','valor':'float64'})
    df3=pd.get_dummies(df2)
    return df2,df3
  
  # Gráfica de boxplots

def grafico_boxplot_rcParams(interval,df2):
    if interval==10:
        plt.rcParams['figure.figsize'] = (9,6);
        sns.boxplot(data=df2.sort_values(by=['Index_antiguedad_10'],
                  ascending=True, inplace=False), 
                  x="Index_antiguedad_10", y="valor",
                  showfliers=False,palette="Set2");
        sns.stripplot(data=df2.sort_values(by=['Index_antiguedad_10'], 
                  ascending=True, inplace=False), 
                  x="Index_antiguedad_10", y="valor",
                  linewidth=1.0,palette="Set2");
        plt.xlabel('Década')
        plt.ylabel('Valor UF')
        plt.title('Distribución valor UF por década')
        plt.grid(True, color='lightgrey',linestyle='--')
        plt.show()
    elif interval==5:
        plt.rcParams['figure.figsize'] = (9,5);
        sns.boxplot(
                  data=df2.sort_values(by=['Index_antiguedad_5'], 
                  ascending=True, inplace=False), 
                  x="Index_antiguedad_5", y="valor",
                  showfliers=False,palette="Set2");
        sns.stripplot(data=df2.sort_values(by=['Index_antiguedad_5'], 
                  ascending=True, inplace=False), 
                  x="Index_antiguedad_5", y="valor",
                  linewidth=1.0,palette="Set2");

        plt.xlabel('Periodo 5 años')
        plt.ylabel('Valor UF')
        plt.title('Distribución valor UF cada 5 años')
        plt.grid(True, color='lightgrey',linestyle='--')
        plt.show()

# indexación de las columnas
def indexs(inter,df2):
    col=['antiguedad','longitud','latitud','supCSII','supTSII']
    index=[]
    nombre='Index_antiguedad_'+str(inter)
    if inter==10 or inter==5:
        a=np.array(df2[nombre].unique())
        a.sort()
        for i in range(0,len(a)):
            string=nombre+'_'+a[i]
            index.append(string)
        for k in range(1,len(col)):
            index.append(col[k])
    elif inter==1:
        index=col
    return index

  # Entrenamiento y escalamiento de datos para los modelos
def Entrenamiento(inter, df2, df3, t_s):
    Xrlinter = np.array(df3[indexs(inter,df2)])
    yrlinter = np.array(df3.valor)
    
    Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test = train_test_split(Xrlinter, yrlinter, test_size=t_s)
    return Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test
    
def Escalas(cve, Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test,df2):
    scl1 = StandardScaler().fit(Xtodos_train)
    Xtodos_train = scl1.transform(Xtodos_train)  
    Xtodos_test = scl1.transform(Xtodos_test)
    
    index10=indexs(10,df2)
    i10=len(index10)
    scl10= StandardScaler().fit(Xrl10_train[:,i10-4:i10]) 
    Xrl10_train[:,i10-4:i10]= scl10.transform(Xrl10_train[:,i10-4:i10])   
    Xrl10_test[:,i10-4:i10]= scl10.transform(Xrl10_test[:,i10-4:i10])  
    
    index5=indexs(5,df2)
    i5=len(index5)
    scl5 = StandardScaler().fit(Xrl5_train[:,i5-4:i5]) 
    Xrl5_train[:,i5-4:i5]= scl5.transform(Xrl5_train[:,i5-4:i5])   
    Xrl5_test[:,i5-4:i5]= scl5.transform(Xrl5_test[:,i5-4:i5])
    
    # Se guarda el escalamiento para cada forma con la que se trabajan los datos de entrada
    scaler1_file = "escala1_"+str(cve)+".save"
    joblib.dump(scl1, scaler1_file)
    scaler10_file = "escala10_"+str(cve)+".save"
    joblib.dump(scl10, scaler10_file) 
    scaler5_file = "escala5_"+str(cve)+".save"
    joblib.dump(scl5, scaler5_file) 
    
    return Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test

# Regresion lineal para una indexacion
def Regresion(Xtrain,Xtest,ytrain,ytest,k):
    multi_regr= linear_model.LinearRegression()
    score11 = cross_val_score(multi_regr, Xtrain, ytrain, cv=k)
    multi_regr.fit(Xtrain, ytrain)
    score12 = cross_val_score(multi_regr, Xtest, ytest, cv=k, scoring='r2')
    y_pred13 =cross_val_predict(multi_regr, Xtest, ytest, cv=k)
    return multi_regr,y_pred13

# Regresion lineal para todas las indexaciones
def RegresionIndex(X1train,X1test,y1train,y1test,X2train,X2test,y2train,y2test,X3train,X3test,y3train,y3test,k):
    multi_regr1,y_pred13=Regresion(X1train,X1test,y1train,y1test,k)
    multi_regr2,y_pred16=Regresion(X2train,X2test,y2train,y2test,k)
    multi_regr3,y_pred19=Regresion(X3train,X3test,y3train,y3test,k)
    return multi_regr1,multi_regr2,multi_regr3,y_pred13,y_pred16,y_pred19

#### SELECCIÓN MODELO REGRESIÓN ####

def RegresionEleccion(df2,df3,cve,k):
    c1=0
    c2=0
    c3=0
    for i in range(0,5):
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(1,df2,df3,0.2)
        Xrl10_train, Xrl10_test, yrl10_train, yrl10_test=Entrenamiento(10,df2,df3,0.2)
        Xrl5_train, Xrl5_test, yrl5_train, yrl5_test=Entrenamiento(5,df2,df3,0.2)
        Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test=Escalas(cve, Xtodos_train, Xtodos_test, 
                                                                                          Xrl10_train, Xrl10_test, Xrl5_train, 
                                                                                          Xrl5_test,df2)
        regr1,regr2,regr3,y_pred13,y_pred16,y_pred19=RegresionIndex(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,
                                                                    Xrl10_train,Xrl10_test,yrl10_train,
                                                                    yrl10_test,Xrl5_train,Xrl5_test,yrl5_train,yrl5_test,k)
        E=porcentajeerror(ytodos_test,y_pred13,yrl10_test,y_pred16,yrl5_test,y_pred19)
        a=E["Cantidad_Est_Relativa"][0]
        b=E["Cantidad_Index_10_Relativa"][0]
        c=E["Cantidad_Index_5_Relativa"][0]
        maxi=max(a,b,c)
        if maxi==a:
            c1=c1+1
        if maxi==b:
            c2=c2+1
        if maxi==c:
            c3=c3+1 
    p=max(c1,c2,c3)
    if p==c2:
        print("El método de regresión lineal escogido será con indexación 10. Se procederá a guardarlo")
        joblib.dump(regr2,"Rlineal2_"+str(cve)+".joblib")
        return yrl10_test,y_pred16,regr2
    elif p==c3:
        print("El método de regresión lineal escogido será con indexación 5. Se procederá a guardarlo")
        joblib.dump(regr3,"Rlineal3_"+str(cve)+".joblib")
        return yrl5_test,y_pred19,regr3
    elif p==c1:
        print("El método de regresión lineal escogido será sin indexación. Se procederá a guardarlo")
        joblib.dump(regr1,"Rlineal1_"+str(cve)+".joblib")
        return ytodos_test,y_pred13,regr1

def GraEstModels(a,b,c,d,e,f,g,h):
    xvec=list(a)
    xvec2=list(c)
    xvec3=list(e)
    xvec4=list(g)
    for k in range(0,len(xvec2)):
        xvec.append(xvec2[k])
    for k in range(0,len(xvec3)):
        xvec.append(xvec3[k])
    for k in range(0,len(xvec4)):
        xvec.append(xvec4[k])   
    xmin,xmax=min(xvec)-250,max(xvec)+250
    yvec=list(b)
    yvec2=list(d)
    yvec3=list(f)
    yvec4=list(h)
    for k in range(0,len(yvec2)):
        yvec.append(yvec2[k])
    for k in range(0,len(yvec3)):
        yvec.append(yvec4[k])
    for k in range(0,len(yvec4)):
        yvec.append(yvec4[k])
    ymin,ymax=min(yvec)-250,max(yvec)+250
    red=[xmin,xmax]
    
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(24, 6))
    axs[0].scatter(a,b,color="#008080");
    axs[0].plot(red,red,color="red")
    axs[0].set_xlabel('Valor Observado',size=14)
    axs[0].set_ylabel('Valor Estimado',size=14)
    axs[0].grid(True)
    axs[0].set_xlim(xmin,xmax)
    axs[0].set_ylim(ymin,ymax)
    axs[0].set_title('Regresión Lineal', size= 18)

    axs[1].scatter(c,d,color="#008080");
    axs[1].plot(red,red,color="red")
    axs[1].set_xlabel('Valor Observado',size=14)
    axs[1].set_ylabel('Valor Estimado',size=14)
    axs[1].grid(True)
    axs[1].set_xlim(xmin,xmax)
    axs[1].set_ylim(ymin,ymax)
    axs[1].set_title('ElasticNet', size= 18)
    
    axs[2].scatter(e,f,color="#008080");
    axs[2].plot(red,red,color="red")
    axs[2].set_xlabel('Valor Observado',size=14)
    axs[2].set_ylabel('Valor Estimado',size=14)
    axs[2].grid(True)
    axs[2].set_xlim(xmin,xmax)
    axs[2].set_ylim(ymin,ymax)
    axs[2].set_title('Random Forest', size= 18)
    
    axs[3].scatter(g,h,color="#008080");
    axs[3].plot(red,red,color="red")
    axs[3].set_xlabel('Valor Observado',size=14)
    axs[3].set_ylabel('Valor Estimado',size=14)
    axs[3].grid(True)
    axs[3].set_xlim(xmin,xmax)
    axs[3].set_ylim(ymin,ymax)
    axs[3].set_title('Xtrem Gradient Boosting', size= 18)

    plt.tight_layout();

    ##### Error1 ####

def porcentajeerror(a,b,c,d,e,f):
    r1=100*(b-a)/a;
    rr1=r1.tolist();
    r2=100*(d-c)/c;
    rr2=r2.tolist();
    r3=100*(f-e)/e;
    rr3=r3.tolist();

    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                '%_Est_Acumulado': [],'Cantidad_Est_Relativa': [],
                                '%_Index_10_Acumulado': [],'Cantidad_Index_10_Relativa': [],
                                '%_Index_5_Acumulado': [],'Cantidad_Index_5_Relativa': []});
    col = ['Intervalo','%_Est_Acumulado','Cantidad_Est_Relativa','%_Index_10_Acumulado','Cantidad_Index_10_Relativa',
        '%_Index_5_Acumulado','Cantidad_Index_5_Relativa'];
    cant=[0,0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant[0]
        porcentaje2=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))/len(rr2)
        cantidad2=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))-cant[1]
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[2]
        cant=[cant[0]+cantidad1,cant[1]+cantidad2,cant[2]+cantidad3]

        tablaux = pd.DataFrame([[inter,porcentaje1,cantidad1,porcentaje2,cantidad2,porcentaje3,cantidad3]],
                              columns=['Intervalo','%_Est_Acumulado','Cantidad_Est_Relativa','%_Index_10_Acumulado',
                                      'Cantidad_Index_10_Relativa','%_Index_5_Acumulado','Cantidad_Index_5_Relativa']);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

# ElasticNet para uno

def ELasticNet(Xlrinter_train, Xlrinter_test,yrlinter_train,yrlinter_test,CV):
    ENet_models = {}
    training_scores = []
    test_scores = []
    L1_ratio=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    for l1_ratio in L1_ratio:
        ENet = ElasticNet(alpha=1,l1_ratio=l1_ratio,max_iter=8000).fit(Xlrinter_train, yrlinter_train)
        training_scores.append(ENet.score(Xlrinter_train, yrlinter_train))
        test_scores.append(ENet.score(Xlrinter_test, yrlinter_test))
        ENet_models[l1_ratio] = ENet
    a_aux,a=0,0
    for k in range(0,len(L1_ratio)):
        if test_scores[k]>test_scores[a_aux]:
            a_aux=k
            a=L1_ratio[k]
    ENet=ENet_models[a]
    score21 = cross_val_score(ENet, Xlrinter_train, np.ravel(yrlinter_train), cv=CV)
    ENet.fit(Xlrinter_train, yrlinter_train)
    score22 = cross_val_score(ENet, Xlrinter_test, np.ravel(yrlinter_test), cv=CV, scoring='r2')
    y_pred23 = cross_val_predict(ENet, Xlrinter_test, np.ravel(yrlinter_test), cv=CV)

    return ENet,y_pred23

# Para elegir 
def ELasticNetEleccion(df2,df3,cve):
    c1=0
    c2=0
    c3=0
    for i in range(0,5):
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(1,df2,df3,0.2)
        Xrl10_train, Xrl10_test, yrl10_train, yrl10_test=Entrenamiento(10,df2,df3,0.2)
        Xrl5_train, Xrl5_test, yrl5_train, yrl5_test=Entrenamiento(5,df2,df3,0.2)
        Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test=Escalas(cve, Xtodos_train, Xtodos_test, 
                                                                                          Xrl10_train, Xrl10_test, Xrl5_train, 
                                                                                          Xrl5_test,df2)
        ENet1,y_pred23=ELasticNet(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,10)
        ENet2,y_pred26=ELasticNet(Xrl10_train,Xrl10_test, yrl10_train,yrl10_test,10)
        ENet3,y_pred29=ELasticNet(Xrl5_train,Xrl5_test, yrl5_train,yrl5_test,10)
        
        E=porcentajeerror(ytodos_test,y_pred23,yrl10_test,y_pred26,yrl5_test,y_pred29)
        a=E["Cantidad_Est_Relativa"][0]
        b=E["Cantidad_Index_10_Relativa"][0]
        c=E["Cantidad_Index_5_Relativa"][0]
        maxi=max(a,b,c)
        if maxi==a:
            c1=c1+1
        if maxi==b:
            c2=c2+1
        if maxi==c:
            c3=c3+1 
    p=max(c1,c2,c3)
    
    if p==c2:
        print("El método de ElasticNet  escogido será con indexación 10. Se procederá a guardarlo")
        joblib.dump(ENet2,"ElasticNet2_"+str(cve)+".joblib")
        return yrl10_test,y_pred26,ENet2
    elif p==c3:
        print("El método de ElasticNet escogido será con indexación 5. Se procederá a guardarlo")
        joblib.dump(ENet3,"ElasticNet3_"+str(cve)+".joblib")
        return yrl5_test,y_pred29,ENet3    
    elif p==c1:
        print("El método de ElasticNet escogido será sin indexación. Se procederá a guardarlo")
        joblib.dump(ENet1,"ElasticNet1_"+str(cve)+".joblib")
        return ytodos_test,y_pred23,ENet1

## Random Forest para un par de datos
def RForest(Xtrain,Xtest,ytrain,ytest,k):
    rforest1 = RandomForestRegressor(n_estimators = 600,max_features=5,random_state = 50)
    score41 = cross_val_score(rforest1, Xtrain, np.ravel(ytrain), cv=k)
    rforest1.fit(Xtrain, ytrain)
    score42 = cross_val_score(rforest1, Xtest, np.ravel(ytest), cv=k, scoring='r2')
    y_pred43 = cross_val_predict(rforest1, Xtest, np.ravel(ytest), cv=k)
    return rforest1,y_pred43

## Random Forest para 3 pares de datos 
def RForestIndex(X1train,X1test,y1train,y1test,X2train,X2test,y2train,y2test,X3train,X3test,y3train,y3test,k):
    rforest1,y_pred43=RForest(X1train,X1test,y1train,y1test,k)
    rforest2,y_pred46=RForest(X2train,X2test,y2train,y2test,k)
    rforest3,y_pred49=RForest(X3train,X3test,y3train,y3test,k)
    return rforest1,rforest2, rforest3,y_pred43,y_pred46,y_pred49

## ELECCION RANDOM FOREST ##
def RForestEleccion(df2,df3,cve,k):
    c1=0
    c2=0
    c3=0
    for i in range(0,5):
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(1,df2,df3,0.2)
        Xrl10_train, Xrl10_test, yrl10_train, yrl10_test=Entrenamiento(10,df2,df3,0.2)
        Xrl5_train, Xrl5_test, yrl5_train, yrl5_test=Entrenamiento(5,df2,df3,0.2)
        Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test=Escalas(cve, Xtodos_train, Xtodos_test, 
                                                                                          Xrl10_train, Xrl10_test, Xrl5_train, 
                                                                                          Xrl5_test,df2)
        rforest1,rforest2,rforest3,y_pred43,y_pred46,y_pred49=RForestIndex(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,
                                                                    Xrl10_train,Xrl10_test,yrl10_train,
                                                                    yrl10_test,Xrl5_train,Xrl5_test,yrl5_train,yrl5_test,k)
        E=porcentajeerror(ytodos_test,y_pred43,yrl10_test,y_pred46,yrl5_test,y_pred49)
        a=E["Cantidad_Est_Relativa"][0]
        b=E["Cantidad_Index_10_Relativa"][0]
        c=E["Cantidad_Index_5_Relativa"][0]
        maxi=max(a,b,c)
        if maxi==a:
            c1=c1+1
        if maxi==b:
            c2=c2+1
        if maxi==c:
            c3=c3+1 
    p=max(c1,c2,c3)
    if p==c2:
        print("El método de Random Forest escogido será con indexación 10. Se procederá a guardarlo")
        joblib.dump(rforest1,"RForest1_"+str(cve)+".joblib")
        return yrl10_test,y_pred46,rforest2
    elif p==c3:
        print("El método de Random Forest escogido será con indexación 5. Se procederá a guardarlo")
        joblib.dump(rforest2,"RForest2_"+str(cve)+".joblib")
        return yrl5_test,y_pred49,rforest3
    elif p==c1:
        print("El método de Random Forest escogido será sin indexación. Se procederá a guardarlo")
        joblib.dump(rforest3,"RForest3_"+str(cve)+".joblib")
        return ytodos_test,y_pred43,rforest1

# XGB para un par de datos

def XGB(Xtrain,Xtest,ytrain,ytest,k):
    xg1 = xgb.XGBRegressor(objective ='reg:squarederror', 
                           colsample_bytree = 1, 
                           learning_rate = 0.3,
                           max_depth = 200, alpha = 1, n_estimators = 500)
    score61 = cross_val_score(xg1,Xtrain, np.ravel(ytrain), cv=k)
    xg1.fit(Xtrain,ytrain)
    score62 = cross_val_score(xg1, Xtest, np.ravel(ytest), cv=k, scoring='r2')
    y_pred63 = cross_val_predict(xg1, Xtest, np.ravel(ytest), cv=k)
    return xg1,y_pred63

# XGB para 3 pares de datos

def XGB_Index(X1train,X1test,y1train,y1test,X2train,X2test,y2train,y2test,X3train,X3test,y3train,y3test,k):
    xg1,y_pred63=XGB(X1train,X1test,y1train,y1test,k)
    xg2,y_pred66=XGB(X2train,X2test,y2train,y2test,k)
    xg3,y_pred69=XGB(X3train,X3test,y3train,y3test,k)
    return xg1,xg2,xg3,y_pred63,y_pred66,y_pred69

### ELECCIÓN DE XGB ###
def XGB_Eleccion(df2,df3,cve,k):
    c1=0
    c2=0
    c3=0
    for i in range(0,5):
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(1,df2,df3,0.2)
        Xrl10_train, Xrl10_test, yrl10_train, yrl10_test=Entrenamiento(10,df2,df3,0.2)
        Xrl5_train, Xrl5_test, yrl5_train, yrl5_test=Entrenamiento(5,df2,df3,0.2)
        Xtodos_train, Xtodos_test, Xrl10_train, Xrl10_test, Xrl5_train, Xrl5_test=Escalas(cve, Xtodos_train, Xtodos_test, 
                                                                                          Xrl10_train, Xrl10_test, Xrl5_train, 
                                                                                          Xrl5_test,df2)
        xgb1,xgb2,xgb3,y_pred63,y_pred66,y_pred69=XGB_Index(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,
                                                                    Xrl10_train,Xrl10_test,yrl10_train,
                                                                    yrl10_test,Xrl5_train,Xrl5_test,yrl5_train,yrl5_test,k)
        E=porcentajeerror(ytodos_test,y_pred63,yrl10_test,y_pred66,yrl5_test,y_pred69)
        a=E["Cantidad_Est_Relativa"][0]
        b=E["Cantidad_Index_10_Relativa"][0]
        c=E["Cantidad_Index_5_Relativa"][0]
        maxi=max(a,b,c)
        if maxi==a:
            c1=c1+1
        if maxi==b:
            c2=c2+1
        if maxi==c:
            c3=c3+1 
    p=max(c1,c2,c3)
    if p==c2:
        print("El método de Xtreme Gradient Boosting escogido será con indexación 10. Se procederá a guardarlo")
        joblib.dump(xgb2,"XGB2_"+str(cve)+".joblib")
        return yrl10_test,y_pred66,xgb2
    elif p==c3:
        print("El método de Xtreme Gradient Boosting será con indexación 5. Se procederá a guardarlo")
        joblib.dump(xgb3,"XGB3_"+str(cve)+".joblib")
        return yrl5_test,y_pred69,xgb3
    elif p==c1:
        print("El método de Xtreme Gradient Boosting escogido será sin indexación. Se procederá a guardarlo")
        joblib.dump(xgb1,"XGB1_"+str(cve)+".joblib")
        return ytodos_test,y_pred63,xgb1
    
# Error para los 4 modelos
def porcentajeerror2(a,b,c,d,e,f,g,h):
    r1=100*(b-a)/a;
    rr1=r1.tolist();
    r2=100*(d-c)/c;
    rr2=r2.tolist();
    r3=100*(f-e)/e;
    rr3=r3.tolist();
    r4=100*(g-h)/h;
    rr4=r4.tolist();
    
    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                '%_Est_Regresión': [],'Cantidad_Est_Regresión': [],
                                '%_Est_ElasticNet': [],'Cantidad_Est_ElasticNet': [],
                                '%_Est_RandomForest': [],'Cantidad_Est_RandomForest': [],
                                 '%_Est_XGboosting': [],'Cantidad_Est_XGboosting':[]});
    col = ['Intervalo','%_Est_Regresión','Cantidad_Est_Regresión','%_Est_ElasticNet','Cantidad_Est_ElasticNet',
        '%_Est_RandomForest','Cantidad_Est_RandomForest', '%_Est_XGboosting','Cantidad_Est_XGboosting'];
    cant=[0,0,0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant[0]
        porcentaje2=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))/len(rr2)
        cantidad2=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))-cant[1]
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[2]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[3]
        cant=[cant[0]+cantidad1,cant[1]+cantidad2,cant[2]+cantidad3,cant[3]+cantidad4]
      
        tablaux = pd.DataFrame([[inter,porcentaje1,cantidad1,porcentaje2,cantidad2,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                              columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def Tabla_Estadistica_Error(y11,y12,y21,y22,y31,y32,y41,y42):
    E_regr=[]
    E_ElasticNet=[]
    E_RForest=[]
    E_XGB=[]
    Sobreestimados1=0
    Sobreestimados2=0
    Sobreestimados3=0
    Sobreestimados4=0
    Subestimados1=0
    Subestimados2=0
    Subestimados3=0
    Subestimados4=0
    for i in range(0,len(y11)):
        E_regr.append(y11[i]-y12[i])
        if y11[i]-y12[i]<0:
            Sobreestimados1=Sobreestimados1+1
        elif y11[i]-y12[i]>0:
            Subestimados1=Subestimados1+1
    for i in range(0,len(y21)):
        E_ElasticNet.append(y21[i]-y22[i])
        if y21[i]-y22[i]<0:
            Sobreestimados2=Sobreestimados2+1
        elif y21[i]-y22[i]>0:
            Subestimados2=Subestimados2+1
    for i in range(0,len(y31)):
        E_RForest.append(y31[i]-y32[i])
        if y31[i]-y32[i]<0:
            Sobreestimados3=Sobreestimados3+1
        elif y31[i]-y32[i]>0:
            Subestimados3=Subestimados3+1
    for i in range(0,len(y41)):
        E_XGB.append(y41[i]-y42[i])
        if y41[i]-y42[i]<0:
            Sobreestimados4=Sobreestimados4+1
        elif y41[i]-y42[i]>0:
            Subestimados4=Subestimados4+1
    Sobreestimados=[Sobreestimados1,Sobreestimados2,Sobreestimados3,Sobreestimados4]
    Subestimados=[Subestimados1,Subestimados2,Subestimados3,Subestimados4]
    tabla= pd.DataFrame.from_dict({'Método':[],
                                'Media': [],'Desviación estándar': [],"Rango":[],
                                'Mediana': [],"Cuartil 1": [],
                                "Cuartil 3": [],"Datos sobreestimados":[], "Datos subestimados":[]});
    col = ['Método','Media','Desviación estándar',"Rango",'Mediana','Cuartil 1',"Cuartil 3","Datos sobreestimados",
        "Datos subestimados"];
    inter=["Regresión lineal","Elastic Net","Random Forest", "Xtreme Gradient Boosting"]
    media=[np.mean(E_regr),np.mean(E_ElasticNet),np.mean(E_RForest),np.mean(E_XGB)]
    ds=[np.std(E_regr),np.std(E_ElasticNet),np.std(E_RForest),np.std(E_XGB)] 
    med=[np.percentile(E_regr,50),np.percentile(E_ElasticNet,50),np.percentile(E_RForest,50),np.percentile(E_XGB,50)]
    Cuart1=[np.percentile(E_regr,25),np.percentile(E_ElasticNet,25),np.percentile(E_RForest,25),np.percentile(E_XGB,25)]
    Cuart3=[np.percentile(E_regr,75),np.percentile(E_ElasticNet,75),np.percentile(E_RForest,75),np.percentile(E_XGB,75)]
    Rango=[max(E_regr)-min(E_regr),max(E_ElasticNet)-min(E_ElasticNet),max(E_RForest)-min(E_RForest),max(E_XGB)-min(E_XGB)]
    for i in range(0,4):
        tablaux = pd.DataFrame([[inter[i],media[i],ds[i],Rango[i],med[i],Cuart1[i],Cuart3[i],Sobreestimados[i],Subestimados[i]]],
                                  columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

