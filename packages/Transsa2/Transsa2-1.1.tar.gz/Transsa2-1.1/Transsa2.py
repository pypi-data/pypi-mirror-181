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
    plt.rcParams['figure.figsize'] = (6,3)
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

# Muestreo y guardado de archivos .xlsx
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
    h=df3.iloc[7*nn:9*nn,:]
    i=df3.iloc[8*n2:2*nn,:]
    j=df3.iloc[9*n2:-1,:]
    A=a.sample(n=n1)
    B=b.sample(n=n1)
    C=c.sample(n=n1)
    D=d.sample(n=n1)
    E=e.sample(n=n1)
    F=f.sample(n=n1)
    G=g.sample(n=n1)
    H=h.sample(n=n1)
    I=i.sample(n=n1)
    J=j.sample(n=n1)
    MuestraML=pd.concat([A,B,C,D,E,F,G,H,I,J],sort=False)
    MuestraML=datosduplicados(MuestraML,False)
    MuestraAVM=pd.merge(ven_tas_aux,MuestraAVM, how="right", 
                        on=["cve_comuna","antiguedad","longitud","latitud","supCSII","supTSII","valor"])
    if cve==19:
        MuestraML.to_excel("MuestraLRML.xlsx")
        MuestraAVM.to_excel("MuestraLRAVM.xlsx")
    elif cve==21:
        MuestraML.to_excel("MuestraLCML.xlsx")
        MuestraAVM.to_excel("MuestraLCAVM.xlsx")
    elif cve==22:
        MuestraML.to_excel("MuestraLBML.xlsx")
        MuestraAVM.to_excel("MuestraLBAVM.xlsx")
    elif cve==52:
        MuestraML.to_excel("MuestraVML.xlsx")
        MuestraAVM.to_excel("MuestraVAVM.xlsx")
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

