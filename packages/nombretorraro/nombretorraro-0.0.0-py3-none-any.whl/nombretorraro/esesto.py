#Arrays, matrices y estructuras
import pandas as pd
import numpy as np

#Visualización
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
%matplotlib inline
import seaborn as sns
import folium
import plotly as py
import plotly.graph_objects as go
import plotly.express as px

#WebScrapping
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Manejo de mi directorio personal
from multiprocessing.sharedctypes import Value
import requests
import io
from datetime import datetime as dt
from PIL import Image
import time
import os

#Preprocesamiento
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


#Feature Selection
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA

#Modelos
from sklearn.preprocessing import PowerTransformer, QuantileTransformer, StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.compose import make_column_transformer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle

#Metricas
from sklearn.metrics import silhouette_score, confusion_matrix, accuracy_score, mean_squared_error, classification_report

#Ensembles
from sklearn.ensemble import IsolationForest, RandomForestRegressor, GradientBoostingClassifier, RandomForestClassifier

#DeepLearning
from sklearn.neural_network import MLPRegressor

#Pipelines
from sklearn.pipeline import make_pipeline

#Otros
import concurrent.futures as cf
import functools

#Librerias secundarias
import shutil
import cv2

from datetime import date
from unidecode import unidecode
from collections import Counter

def visualize_data(x, y):
   '''
    SE NECESITA:
        1. Importar el dataset
        2. Tener claras las siguientes variables:
            x = lista o indice X
            y = lista o indice Y
    '''
   plt.plot(x, y)
   plt.xlabel('X values')
   plt.ylabel('Y values')
   plt.show()

def s_temporal(df, a, y):
    '''
    SE NECESITA:
        1. Importar el dataset
        2. Tener claras las siguientes variables:
            df = El dataframe a utilizar
            a = la medida que se quiere utilizar, ya sea M, W o A
            y = Nombre del eje Y
    '''

    plot = df.resample(a).sum()
    if a == 'M':
        a = 'Meses'
    elif a == 'A':
        a = 'Años'
    elif a == 'W':
        a = 'Semanal'
    plot.plot(xlabel=a, ylabel=y)

def comparacion_stemporal(train, test, prediction, lower_series, upper_series):
    '''
            SE NECESITA:
            1. Importar el dataset
            2. Tener claras las siguientes variables:
            train = datos de train que se utilizan para el modelo
            test = datos de test que se utilizan para poner en practica el modelo
            prediction = la prediccion que se hace del resultado
            lower_series = serie de panda que se basa en la predicción y toma en cuenta pd.Series([:, 0] , test.index)
            upper_series = serie de panda que se basa en la predicción y toma en cuenta pd.Series([:, 1] , test.index)
    '''
    plt.figure(figsize=(15,15))
    plt.plot(train, label='train', lw= 2)
    plt.plot(test, label='actual', lw= 2)
    plt.plot(prediction, label='prediction', lw= 2)
    plt.fill_between(lower_series.index, lower_series, upper_series, color= 'k', alpha=.15)
    plt.title("Prediction vs Actual Numbers")
    plt.legend(loc = 'upper left', fontsize=10)
    plt.show()

def candle_plot(df):
    '''
     Grafica de velas chinas para ver evolución de precios del mercado bursatil, se requieren los parametros del
     precio de entrada "Open", pico más alto del dia "High", el pico de bajada del dia "Low", y el precio del cierre
     "Close", necesitas tener el DataFrame con esas columnas definidas.
    '''
    fig = py.Figure(data=[py.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    fig.show()

def grafica_creator(df):
    # Se inicializa la figura de plotly
    fig = py.Figure()
    name = str(df['Codigo empresa'].unique())
    # Aquí se agregan los diferentes Scatter, o graficas lineales, que se hace un deploy de 4 graficas manejadas por Botones

    fig.add_trace(
        py.Scatter(x=list(df.index),
                   y=list(df.High),
                   name="High",
                   line=dict(color="#33CFA5")))

    fig.add_trace(
        py.Scatter(x=list(df.index),
                   y=[df.High.mean()] * len(df.index),
                   name="High Average",
                   visible=False,
                   line=dict(color="#33CFA5", dash="dash")))

    fig.add_trace(
        py.Scatter(x=list(df.index),
                   y=list(df.Low),
                   name="Low",
                   line=dict(color="#F06A6A")))

    fig.add_trace(
        py.Scatter(x=list(df.index),
                   y=[df.Low.mean()] * len(df.index),
                   name="Low Average",
                   visible=False,
                   line=dict(color="#F06A6A", dash="dash")))

    # Se agregan las anotaciones, y se crean los botones para cada una de las tablas
    # Las Anotaciones son basicamente el valor promedio, y los umbrales
    high_annotations = [dict(x="2019-01-01",
                             y=df.High.mean(),
                             xref="x", yref="y",
                             text="High Average:f" % df.High.mean(),
                            ax = 0, ay = -40),
                        dict(x=df.High.idxmax(),
                             y=df.High.max(),
                             xref="x", yref="y",
                             text="High Max:f" % df.High.max(),
                            ax = 0, ay = -40)]
    low_annotations = [dict(x="2019-01-01",
                            y=df.Low.mean(),
                            xref="x", yref="y",
                            text="Low Average:f" % df.Low.mean(),
                            ax = 0, ay = 40),
                        dict(x=df.High.idxmin(),
                             y=df.Low.min(),
                             xref="x", yref="y",
                             text="Low Min:f" % df.Low.min(),
                            ax = 0, ay = 40)]
    # Aquí están los botones que permiten manipular si solo quieres ver los valores maximos, minimos, ambos.
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="None",
                         method="update",
                         args=[{"visible": [True, False, True, False]},
                               {"title": name,
                                "annotations": []}]),
                    dict(label="High",
                         method="update",
                         args=[{"visible": [True, True, False, False]},
                               {"title": name,
                                "annotations": high_annotations}]),
                    dict(label="Low",
                         method="update",
                         args=[{"visible": [False, False, True, True]},
                               {"title": name,
                                "annotations": low_annotations}]),
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True, True]},
                               {"title": name,
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text=name)

    fig.show()

def grid_creator(data, x, y, hue):
    '''
    Esta funcion permite crear diferentes graficos dependiendo de los parametros que se van pidiend,
    cada una de las graficas sigue un parametro sencillo, primero el data frame, luego el eje x, luego el y,
    por ultimo el hue, te permite ingresar los valores mediante un input para que puedas elegir las columnas
    de tu preferencia

    '''
    fig = plt.figure(constrained_layout=True, figsize=(20,10))
    grid = gridspec.GridSpec(ncols=6, nrows=2, figure=fig)

    #bar plot Horizontal
    ax1 = fig.add_subplot(grid[0, :2])
    ax1.set_title(input(str))
    sns.countplot(data, x= data[input(str)],y=data[input],hue =data[input(str)] , ax=ax1,) #Paid no paid

    #bar plot Vertical
    ax2 = fig.add_subplot(grid[1, :2])
    ax2.set_title('Purpose segmented by Fully Paid/Charged Off')
    bar = sns.barplot(data, x= data[input(str)],y=data[input],hue =data[input(str)] , ax=ax2)
    bar.set_xticklabels(bar.get_xticklabels(),  rotation=90, horizontalalignment='right') #fixing the Names

    #box plot Credit Score
    ax3 = fig.add_subplot(grid[:, 2])
    ax3.set_title('Credit Score')
    sns.boxplot(data.loc[:,input(str)], orient='v', ax = ax3)


    #box plot Monthly payment
    ax4 = fig.add_subplot(grid[:,3])
    ax4.set_title(input('Introduce el titulo de tu Boxplot'))
    sns.boxplot(data[input(str)], orient='v' ,ax=ax4)

    return plt.show()

def Line_Line_bar_party(x, y, y1, label_x="x",
                        label_y="y",
                        label_y1="y1",
                        plotsize=(20, 12),
                        barcolor="grey",
                        linecolor_y="green",
                        linecolor_y1="b"):
    """

    Esta función muestra 3 gráficas, 2 lineales y
    1 lineal combinada con barras, agrupando las vistas comparativas

    Para esta función debes tener instalado las librerias
    de MATPLOTLIB/NUMPY/PANDAS


    Parameters
    ----------
        x : np.array
            eje x
        y : np.array
            eje y
        y1 : np.array
            eje y1
        label_x : str
            Etiqueta del eje x
        label_y : str
            Etiqueta del eje y
        label_y1 : str
            Etiqueta del eje y1
        plotsize : Tuple()
            Tamaño del primer plano
        barcolor : str
            Color de las barras
        linecolor_y : str
            Color de las lineas
        linecolor_y1 : str
            Color de las lineas y1

    Returns
    -------
        Vista comparativa de 2 productos
        según sus ventas, cantidades, compras, o algo asi.

    Notes
    ------

        Función para visualizar la comparación de 2
        columnas, con comportamientos
        similares.

        Ejemplo:
                Tengo 2 productos, y quiero visualizar
                cuanto se ha vendido
                de cada uno en 1 año.

        Francisco Quintero :)


        """


    # Se establece el tamaño de la gráfica y el estilo
    plt.style.use("seaborn-white")
    plt.figure(figsize=plotsize)

    # 1er Linechart con dots
    plt.subplot(2, 3, 1)
    plt.plot(x, y, '-ok');
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.plot(x, y, linestyle="--");

    # 2do Linechart con dots
    plt.subplot(2, 3, 2)
    plt.plot(x, y1, '--');
    plt.xlabel(label_x)
    plt.ylabel(label_y1)
    plt.plot(x, y1, linestyle="--");

    # Linechart+barchart
    plt.subplot(233)
    plt.bar(x, y, color=barcolor)
    plt.plot(x, y, linestyle="--")
    plt.plot(x, y, linestyle="--", color=linecolor_y, label=label_y)
    plt.plot(x, y1, linestyle="--", color=linecolor_y1, label=label_y1)
    plt.xlabel(label_x)
    plt.ylabel(label_y + "_" + label_y1)
    plt.legend(loc="upper right")
    plt.locator_params(axis="x", nbins=len(x))

    plt.show();
    return


def balanced_target(X_train,
                    y_train):
    """
    Esta función realiza un balance del target TRAIN con el
    método SMOTE() y muestra 2 gráficas con el antes y después.

    Para esta función debes tener instalado las librerias
    de MATPLOTLIB/NUMPY/PANDAS/SKLEARN/IMBLEARN


    Recibe los siguientes parámetros:

    Parameters
    ----------
        x_train : np.array
            datos para train
        y_train : np.array
            target para train

    Returns
    -------
        Target balanceado y gráficas

    Notes
    -------

        Para esta función, X_train, y_train deben estar codificados.
        La función fue creada con la finalidad de ahorrar pasos y tener mejor visibilidad
        de el preprocesado en Machine Learning

        Francisco Quintero :)
        """

    smote = SMOTE()

    conteo_balance_target = y_train.value_counts()

    if conteo_balance_target[0] != conteo_balance_target[1]:
        X_train1, y_train = smote.fit_resample(X_train, y_train)
        y_train_balanced = y_train.value_counts()

        plt.figure(figsize=(5, 5))
        plt.subplot(2, 2, 1)
        plt.pie(conteo_balance_target.values,
                labels=conteo_balance_target.index,
                autopct='%1.2f%%')
        p = plt.gcf()
        plt.show()

        plt.figure(figsize=(5, 5))
        plt.subplot(2, 2, 2)
        plt.pie(y_train_balanced.values,
                labels=y_train_balanced.index,
                autopct='%1.2f%%')
        p = plt.gcf()
        plt.show()

        return y_train


def feature_importances_visualization(best_estimator,
                                      X_train,
                                      plotsize=(20, 10)):
    """
    Esta función sirve para visualizar
    el feature importances de un modelo previamente
    entrenado y seleccionado de un GridSearchCV

    Para esta función debes tener instalado las librerias
    de MATPLOTLIB/PANDAS/SKLEARN

    Recibe los siguientes parámetros:

    Parameters
    ----------
        best_estimator : sklearn.model_selection._search.GridSearchCV
            modelo entrenado y seleccionado de un GridSearchCV
        X_train : np.array
            datos para train
        plotsize : Tuple()
            Tamaño del primer plano

    Returns
    -------
        Visualización de los Features importances del modelo entrenado y seleccionado
        de un GridSearchCV mediante un Barchart

    Notes
    -------
        La función fue creada para visualizar cuales son las variables mas usadas
        por un modelo entrenado y seleccionado de un GridSearchCV.

    Francisco Quintero :)
        """


    mejor_estimador = best_estimator.best_estimator_
    fe_i = mejor_estimador.feature_importances_
    df = pd.DataFrame(fe_i, index=X_train.columns).sort_values(0, ascending=False) * 100
    df = df.rename(columns={0: 'Feature_importances'})

    return plt.figure(figsize=plotsize), plt.bar(df.index, df.Feature_importances);

def matrices_comparadas(y, x_test_scaled, y_test, nombre_modelo, y_2, x_test_scaled_2, y_test_2, nombre_modelo_2, size):
    """" Esta función crea dos matrices de confusión y las representa en la misma imagen, para poder compararlas.
    Parámetros:
    y= Target completo para poder sacar las etiquetas del primer modelo
    x_test_scaled= Los parámetros de x_test del primer modelo. NOTA: pueden ser sin escalar, eso no afecta a la función.
    y_test= Target una vez hecho el train_test_split del primer modelo
    nombre_modelo= Primer modelo del que se van a sacar los parámetros
    y_2= Target completo para poder sacar las etiquetas del segundo modelo
    x_test_scaled= Los parámetros de x_test del segundo modelo. NOTA: pueden ser sin escalar, eso no afecta a la función.
    y_test= Target una vez hecho el train_test_split del segundo modelo
    nombre_modelo= Segundo modelo del que se van a sacar los parámetros
    size= tamaño en el cual queremos sacar la imagen. Debe introducirse como tupla, como por ejemplo (7,7)
    """
    fig, (ax1, ax2) = plt.subplots(1,2)
    #primera matriz
    plt.figure(figsize=size)
    cm_labels = np.unique(y)
    predictions = nombre_modelo.predict(x_test_scaled)
    cm_array = confusion_matrix(y_test, predictions)
    cm_array_df = pd.DataFrame(cm_array, index=cm_labels, columns=cm_labels)
    sns.heatmap(cm_array_df, annot=True, annot_kws={"size": 12}, cmap='rocket_r', cbar=False, ax=ax1)
    #segunda matriz
    cm_labels_2 = np.unique(y_2)
    predictions_2 = nombre_modelo_2.predict(x_test_scaled_2)
    cm_array_2 = confusion_matrix(y_test_2, predictions_2)
    cm_array_df_2 = pd.DataFrame(cm_array_2, index=cm_labels_2, columns=cm_labels_2)
    sns.heatmap(cm_array_df, annot=True, annot_kws={"size": 12}, cmap='rocket_r', cbar=False, ax=ax2)
    return plt.show()


def plot_matriz_confusion(y, x_test_scaled, y_test, nombre_modelo, size):
    """" Esta función crea una matriz de confusión y la representa visualmente de una forma elegante y sobria.

    y= Target completo para poder sacar las etiquetas de nuestro modelo
    x_test_scaled= Los parámetros de x_test de nuestro modelo. NOTA: pueden ser sin escalar, eso no afecta a la función.
    y_test= Target una vez hecho el train_test_split del modelo
    nombre_modelo= Modelo del que se van a sacar los parámetros
    size= tamaño en el cual queremos sacar la imagen. Debe introducirse como tupla, como por ejemplo (7,7)
    """
    plt.figure(figsize=size)
    cm_labels = np.unique(y)
    predictions = nombre_modelo.predict(x_test_scaled)
    cm_array = confusion_matrix(y_test, predictions)
    cm_array_df = pd.DataFrame(cm_array, index=cm_labels, columns=cm_labels)
    return sns.heatmap(cm_array_df, annot=True, annot_kws={"size": 12}, cmap='rocket_r', cbar=False)

def piechart_etiquetado(data, size):
    """Esta función nos crea un pie chart con sus correspondientes etiquetas porcentuales, para
    poder saber el % de cada categoría de una forma más sencilla.

    Parámetros:
    data: el dataframe del que vamos a sacar los valores, debe tener las etiquetas como índices y una única columna
    para que la función opere correctamente.
    size: Tamaño que deseamos para la figura. Sus valores deben introducirse como una tupla, como por ejemplo (7,7).
    """
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.figure(figsize=size)
    plt.pie(data.values,
            labels=data.index,
            autopct='%1.2f%%')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    return plt.show()

def test_transformers(df, cols):  # pasamos como argumentos el dataframe y la lista de columnas
    '''Para esta función necesitamos un dataframe con columnas numéricas
    a las que queramos transformar su distribución hacia una más normal tipo Gauss.
    Esta transformación es necesaria en modelos no supervisados basados en distancias como K-Means,
    previa al estandarizado de los datos.

    Lo ideal antes de pasar los argumentos a la función es tener declaradas dos variables: una que recoja el df
    y otra que nombre las columnas con los datos a transformar en forma de lista.

    Ejemplo:
    # dataframe con los datos sin transformar
    df = pd.read_csv('dataframe_ejemplo')

    # recogemos los nombres de las columnas del dataframe que transformar
    columnas = ["Col1", "Col2", "Col3"]


    PowerTransformer() # instancia del transformador PowerTransformers con los parámetros por defecto (toma valores positivos y negativos)

    QuantileTransformer(output_distribution='normal') # en QT cambiamos el output a normal para ese tipo de distribución


    La función definida sirve para visualizar las posibles distribuciones de los datos, NO guarda los datos transformados.
    Su puesta en marcha responde más a una necesidad de visualizar tal distribución y elegir el mejor preprocesado.

    Para más información sobre estas transformaciones, visita la web
    https://machinelearningmastery.com/quantile-transforms-for-machine-learning/

    Cita necesaria a Yashowardhan Shinde.
    Su perfil en medium: https://yashowardhanshinde.medium.com/
    '''
    # importamos las librerias necesarias para la ejecución de la función

    pt = PowerTransformer()  # instancia del transformador PowerTransformers con los parámetros por defecto (toma valores positivos y negativos)
    qt = QuantileTransformer(
        output_distribution='normal')  # en QT cambiamos el output a normal para ese tipo de distribución

    # definimos el tamaño del plot, pero es recomendable modificarlo para más de 3 columnas

    fig = plt.figure(figsize=(30, 15))
# definimos j para que la función vaya graficando los plots en cada distribución
    j = 1

    for i in cols:
        # definimos n para que se creen 3 subplots (3 graficos) por cada columna
        n = len(cols)

        # convertimos cada columna a un array de una dimensión
        array = np.array(df[i]).reshape(-1, 1)

        # aplicamos las transformaciones
        y = pt.fit_transform(array)
        x = qt.fit_transform(array)

        # Graficamos la distribución original y cada transformación por cada columna:
        plt.subplot(n, 3, j)
        sns.histplot(array, bins=50, kde=True)
        plt.title(f"Original Distribution for {i}")
        plt.subplot(n, 3, j + 1)
        sns.histplot(x, bins=50, kde=True)
        plt.title(f"Quantile Transform for {i}")
        plt.subplot(n, 3, j + 2)
        sns.histplot(y, bins=50, kde=True)
        plt.title(f"Power Transform for {i}")

        # definimos j como los saltos de cada fin del bucle for para la siguiente fila
        # como en este caso son tres subplots por cada columna del dataframe, j añade 3 en cada vuelta
        j += 3
        # ya podemos usar nuestra función con el dataframe y nuestras columnas
        #test_transformers(df, columnas)

def report_plot(tree_entrenado, X_test, y_test, columnas_X):
    '''Funcion que toma de argumento el modelo y retorna el classification report y el gráfico del decission tree
    sirve para comparar distintos arboles, o modificaciones del mismo sin tener que ejecutar el bloque de código entero
    (ej. prunned tree de un DecisionTree ya creado).

    Para su ejecución se necesita el modelo ya entrenado (modelo.fit(X_train, y_train)) como argumento,
    por lo que la división en train y test también deberá darse previa al llamado de la función.

    Para más información sobre las métricas del Classification Report visita la documentación de la librería sci-kit learn al respecto.
    '''

    model_preds = tree_entrenado.predict(X_test)
    print(classification_report(y_test, model_preds))
    print('\n')
    plt.figure(figsize=(12, 8), dpi=150)
    plot_tree(tree_entrenado, filled=True, feature_names=columnas_X);

def bar_plot(df, columna):
    '''Ideal para columnas categoricas con no mas de 10 categorías.

    Esta función devuelve, con una sola línea de código: un plot dentro de un figsize=(15,6),
    un gráfico de barras con los colores de una paleta preseleccionada de colores, la frecuencia de dichos valores
    dentro del dataset, el título del gráfico, una etiqueta para el eje y, e imprime en pantalla un value counts
    de la columna que le hemos pasado a la función.

    En caso de querer usar la función con más de una columna, se recomienda usarla en un bucle for de la siguiente manera:

    for x in ['Col1', 'Col2', 'Col3', ...]:
        bar_plot(x)

        >> el output sería lo descrito anteriormente mostrado de forma consecutiva para cada columna.

    Si se requiere más información, visita la documentación de matplotlib en
    https://matplotlib.org/stable/index.html

    Agradecimientos a Enes Besinci,
    visita su perfil en kaggle en https://www.kaggle.com/code/enesbeinci/k-means-ile-m-teri-ki-ilik-analizi
    '''

    var = df[columna]
    varV = var.value_counts()
    plt.figure(figsize=(15, 6))
    plt.bar(varV.index, varV, color=mcolors.TABLEAU_COLORS)
    plt.xticks(varV.index)
    plt.ylabel("Frecuencia")
    plt.title(columna)
    plt.show()
    print("{}: \n {}".format(columna, varV))

def mapa_folium(df, geojson, key, coord, legend="Mapa"):
    """Esta función se apoya en la librería Folium para visualizar la distribución geográfica de los datos
    presentes en un dataset. Habrá que indicarle las coordenadas donde se inizializa el mapa, así como un archivo
    Json que almacene las geometrías GeoJson de las localidades del mapa.

    Se requiere la instalación de las librerías Pandas y Folium.

    --> df: dataframe que pasaremos a la función y que queremos visualizar. Deberá constar de dos columnas,
    la primera con los lugares del mapa que queremos mostrar y la segunda con los datos que queremos visualizar.
    --> geojson: archivo Json con las geometrías de las localidades que queremos mostrar.
    --> key: string, variable del Json geojson con la que vincularemos los datos. Deberá comenzar siempre por "feature"
    y estar escrita en nomenclatura javascript como por ejemplo "feature.id" o "featura.properties.statename".
    --> coord: tupla, coordenadas en [ejeX, ejeY] en las que queremos inicializar el mapa.
    --> legend: string, argumento opcional que indicará el título de la leyenda que siguen los datos mostrados en el mapa.
    """

    mapa = folium.Map(location=coord, zoom_start=4)

    tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
    for tile in tiles:
        folium.TileLayer(tile).add_to(mapa)

    mapa.choropleth(
        geo_data=geojson,
        name='choropleth',
        data=df,
        columns=df.keys(),
        key_on=key,
        fill_color='BuPu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend
    )
    folium.LayerControl().add_to(mapa)

    return mapa

def vis_line(df, ejex, ejey, group="", type=0):
    """Esta función nos permite visualizar los datos contenidos en un dataset mediante un line chart. Habrá que indicarle
    que columnas serán los ejes x e y del gráfico, así como indicarle por qué columna queremos agrupar los datos en caso que queramos,
    además también de poder elegir el tipo de line chart que queremos usar.

    Se requiere la instalación las librerías Plotly y Pandas.

    --> df: este será el dataframe que pasaremos a la función con la información que queremos visualizar en el gráfico.
    --> ejex: string, indicaremos la columna que queremos usar en el gráfico como eje X para representar los datos.
    --> ejey: string, indicaremos la columna que queremos usar en el gráfico como eje Y para representar los datos.
    --> group: string, es un argumento opcional que nos permite deicidir si queremos agrupar los datos o no. En caso de querer
    agruparlos tendremos que indicar el nombre de la columna por la cual queramos agruparlos.
    --> type: int, argumento opcional que nos permite decidir que tipo de line chart queremos utilizar, 0 para líneas y marcadores,
    1 para solo líneas y 2 u otro número para solo marcadores. Por defecto está activada la opción 0 para líneas y marcadores.
    """
    fig = go.Figure()
    if group != "":
        grupos = df[group].unique()
        if type==0:
            for grupo in grupos:
                x = df[df[group].values == grupo][ejex]
                y = df[df[group].values == grupo][ejey]
                fig.add_trace(go.Scatter(x=x, y=y,
                mode="lines+markers",
                name=grupo
                    ))
        elif type==1:
            for grupo in grupos:
                x = df[df[group].values == grupo][ejex]
                y = df[df[group].values == grupo][ejey]
                fig.add_trace(go.Scatter(x=x, y=y,
                mode="lines",
                name=grupo
                    ))
        else:
            for grupo in grupos:
                x = df[df[group].values == grupo][ejex]
                y = df[df[group].values == grupo][ejey]
                fig.add_trace(go.Scatter(x=x, y=y,
                mode="markers",
                name=grupo
                    ))

    else:
        if type == 0:
            fig.add_trace(go.Scatter(x=df[ejex], y=df[ejey],
                                     mode="lines+markers"))
        elif type == 1:
            fig.add_trace(go.Scatter(x=df[ejex], y=df[ejey],
                                     mode="lines"))
        else:
            fig.add_trace(go.Scatter(x=df[ejex], y=df[ejey],
                                     mode="markers"))
    return fig

def matrix_sca (df, dimensiones, agrupar, titulo="Scatter Matrix"):
    """Esta función nos permite crear una matriz de Scatterplots para realizar una comparativa de los valores de las
    variables de un dataset utilizando la librería Pyplot.express.

    Se requiere la instalación de las librerías Pyplot y Pandas

    --> df: dataframe que pasaremos a la función con la información que queremos comparar
    --> dimensiones: lista con los nombres de las columnas con cuyos datos queremos hacer una comparativa
    --> agrupar: string, nombre de la columna con la cual queremos agrupar los datos
    --> titulo: string, argumento opcional con el título que queremos poner a la gráfica. Por defecto será 'Scatter Matrix'
    """
    fig = px.scatter_matrix(df,
        dimensions=dimensiones,
        color=agrupar,
        title=titulo,
        labels=dimensiones)
    fig.update_traces(diagonal_visible=False)

    return fig

def pca_visualization(df):
    """Escala los datos del dataframe original y aplica un PCA para reducir el numero de columnas original a 3 columnas.
    Teniendo 3 columnas / componentes principales, los datos pueden ser representados en un grafico de dispersión 3D.

    Args:
        df (DataFrame): Base de datos original sin la columna target

    Returns:
        3D Scatter Plot: Gráfico de dispersión 3D tras aplicar el PCA
        Varianza explicada acumulada para 3 componentes principales: Devuelve la suma de la varianza
        explicada para 3 componentes principales. Esto informa de cuánta información se está perdiendo con el PCA.
    """

    scal = StandardScaler()
    X_scal = scal.fit_transform(df)

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scal)

    principalDf = pd.DataFrame(data=X_pca, columns=['P1', 'P2', 'P3'])

    xdata = principalDf['P1']
    ydata = principalDf['P2']
    zdata = principalDf['P3']

    trace1 = go.Scatter3d(x=xdata,
                          y=ydata,
                          z=zdata,
                          mode='markers',
                          marker=dict(size=5, color='rgb(255,0,0)'))

    data = [trace1]
    layout = go.Layout(margin=dict(l=0,
                                   r=0,
                                   b=0,
                                   t=0))

    fig = go.Figure(data=data, layout=layout)

    expl = pca.explained_variance_ratio_
    print('Cumulative explained variance with 3 principal components:', round(np.sum(expl[0:3]), 2))
    iplot(fig)


def my_pca(n_components, df):
    """Escala los datos del DataFrame original y aplica un PCA con el numero de componentes principales deseado.

        Args:
            df (DataFrame): Base de datos original sin la columna target

        Returns:
            Varianza explicada acumulada : Devuelve la suma de la varianza explicada para los componentes principales deseados.
    """

    scal = StandardScaler()
    X_scal = scal.fit_transform(df)

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scal)

    expl = pca.explained_variance_ratio_
    print('Varianza acumulada', np.cumsum(expl))

    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of components')
    plt.ylabel('Cumulative explained variance')
    plt.xticks(np.arange(0, n_components, step=1))


def my_kmeans(n_clusters, df):
    """Escala los datos del DataFrame original y aplica un KMeans con el numero de clusters deseado.

        Args:
            df (DataFrame): Base de datos original sin la columna target

        Returns:
            Inercias para cada modelo de KMeans y un grafico para visualizar los resultados
            Silhouette scores para cada modelo de Kmeans y un grafico para visualizar los resultados

    """

    scal = StandardScaler()
    X_scal = scal.fit_transform(df)

    kmeans_per_k = [KMeans(n_clusters=k, random_state=42).fit(X_scal) for k in range(2, n_clusters + 1)]
    inertias = [model.inertia_ for model in kmeans_per_k]

    plt.figure(figsize=(8, 3.5))

    plt.plot(range(2, n_clusters + 1), inertias, "bo-")
    plt.xlabel("$k$", fontsize=14)
    plt.ylabel("Inertia", fontsize=14)
    plt.show()

    silhouette_scores = [silhouette_score(X_scal, model.labels_) for model in kmeans_per_k]
    plt.figure(figsize=(8, 3))
    plt.plot(range(2, n_clusters + 1), silhouette_scores, "bo-")
    plt.xlabel("$k$", fontsize=14)
    plt.ylabel("Silhouette score", fontsize=14)

    return inertias, silhouette_scores


################################### FUNCIÓN DE DETECCIÓN DE ANOMALÍAS ################################################
def anomalias_var(feature):
    '''Función para detectar las anomalías/outliers de las distintas variables (columnas/features)
       de un dataset mediante un modelo de Isolation Forest.

       Sólo tiene un argumento de entrada:
         feature --> Ha de ser un VECTOR COLUMNA. Ejemplo: feature = df[["nombre_col"]]

       La función te devuelve un dataframe con los valores de la variable que el modelo considera anómalos'''

    model = IsolationForest(max_samples=len(feature), random_state=13)
    anomalias = model.fit_predict(feature)

    return feature[anomalias == -1]


#################################### FUNCIÓN DE FEATURE IMPORTANCE ###################################################
def FeatureImportance_rf(X, y, n):
    '''Función para plasmar el Feature Importance (ordenado de mayor a menor) de un dataset
       con valores numéricos, haciendo uso de un Random Forest Regressor.

       Los argumentos de entrada son:
            X --> el conjunto de variables (features) de tu dataset. Ha de tener formato dataframe o un np.array 2D
            y --> el target; con formato pd.Series o np.array 1D
            n --> nº de estimadores de los que quieres dotar al modelo Random Forest

        La función te devolverá un dataframe con 2 columnas:
            Relevancia --> indica el % de transcendencia que tiene una variable en relación al target.
            Variable --> indica el nombre de la columna (string)
    '''
    nombres = X.columns

    rf = RandomForestRegressor(n_estimators=n, random_state=13)
    rf.fit(X, y)

    decimales = rf.feature_importances_
    decimales = sorted(decimales, reverse=True)

    puntuacion = zip(map(lambda f: "{:.2%}".format(f), decimales), nombres)

    return pd.DataFrame(puntuacion, columns=['Relevancia', 'Variable'])


######################################## FUNCIÓN DE FEATURE SELECTION ##########################################
def FeatureSelection_var(X, min_var):
    '''Función para elegir el nº de variables adecuado para la cantidad de observaciones de un dataset
       según el filtro de varianza.

       Válida para aprendizaje NO SUPERVISADO (no hace falta el target).
       Ideal para datasets con pocas observaciones (filas) y muchas variables (columnas)

       La función primero te calcula el nº de variables adecuado para las filas halladas siguiendo la
       "rule of thumb";seguidamente, te aplica un preprocesado en el que te estandariza tus datos y
       y realiza un filtro de varianza (VarianceThreshold), por el que, por debajo de un mínimo valor de
       varianza te desecha las variables que no lo cumplan.

       La función te devuelve un nuevo conjunto de datos (dataset sin target) estandarizado y únicamente con
       aquellas columnas que superen el valor mínimo de varianza, siempre que éstas sean una cantidad igual o
       inferior al número adecuado de variables indicado por la "rule of thumb". En caso de que todas las
       variables tuvieran una varianza superior al valor mínimo y éstas fueran demasiadas, la función iría
       subiendo automáticamente ese umbral mínimo hasta que se redujeran las columnas.

       Como argumentos de entrada se tienen:
            X --> dataset (sin target) de valores numéricos
            min_var --> valor mínimo de varianza que deseamos que tengan las variables del dataset

       '''
    f = len(X)
    N = 5 * np.log10(f)

    var_pipe = make_pipeline(StandardScaler(), VarianceThreshold(min_var))
    selector = var_pipe.fit(X)
    variables = selector.get_feature_names_out()
    pipelado = var_pipe.transform(X)
    columnas = pipelado.shape[1]

    while columnas > N:
        min_var += 0.1
        var_pipe = make_pipeline(StandardScaler(), VarianceThreshold(min_var))
        selector = var_pipe.fit(X)
        variables = selector.get_feature_names_out()
        pipelado = var_pipe.transform(X)
        columnas = pipelado.shape[1]

        if min_var == 1.0:
            break

    X_new = pd.DataFrame(pipelado, columns=list(variables))
    return X_new


def Impute_Tree_Regressor(df: pd.core.frame.DataFrame, n_max_depth: int, random_state: int) -> pd.core.frame.DataFrame:
    """
    Método de imputación de variables contínuas, a través de un árbol de decisión.

    EXCLUSIVAMENTE ÚTIL PARA MATRICES NUMÉRICAS, ONE HOT ENCODER/ LABEL ENCODER HA DE ESTAR YA REALIZADO

    cuando se dispone exclusivamente de un NaN por fila, en caso de que haya más de un NaN por fila se eliminará la fila del df.
    """

    # Quitamos los warnings para un output más limpio del código
    import sys

    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    # eliminamos las filas con Nan>1 como se explica arriba
    df = df.dropna(thresh=df.shape[1] - 1)
    df2 = df.dropna()

    # Comienza el bucle
    while (sum(df.isnull().any(1)) > 0):
        # identificar fila y columna del NAN
        nan_rows = df[df.isnull().any(1)]
        nan_columns = df.columns[df.isnull().any()]
        for i in nan_columns:
            for j in nan_rows.index:
                # En caso de que sea Nan
                if (np.isnan(df.loc[j, i])):
                    # separo el target de entrenamiento
                    target = df2[i]
                    # separo mi X_train
                    X_train = df2.drop(i, axis=1)
                    # defino y entreno el modelo
                    tree_reg = DecisionTreeRegressor(max_depth=2, random_state=42)
                    tree_reg.fit(X_train, target)
                    # obtengo la fila a la que se imputa el Nan
                    X_test = df.loc[[j]]
                    X_test = pd.DataFrame(X_test)
                    X_test.drop(i, axis=1, inplace=True)
                    # realizo su predicción
                    pred = tree_reg.predict(X_test)
                    # sustituyo en df
                    df.loc[j, i] = pred
                    # actualizo las condiciones
                    nan_rows = df[df.isnull().any(1)]
                    nan_columns = df.columns[df.isnull().any()]
                else:
                    continue
    return df


def Impute_Tree_classifier(df: pd.core.frame.DataFrame, categorical_variable: str, n_max_depth: int,
                           random_state: int) -> pd.core.frame.DataFrame:
    """
    Método de imputación de variables categóricas, a través de un árbol de decisión.

    EXCLUSIVAMENTE ÚTIL PARA MATRICES NUMÉRICAS, ONE HOT ENCODER/ LABEL ENCODER HA DE ESTAR YA REALIZADO

    Aplicable cuando se dispone exclusivamente de un NaN por fila, en caso de que haya más de un NaN por fila se eliminará la fila del df
    """

    # Quitamos los warnings para un output más limpio del código
    import sys

    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    # eliminamos las filas con Nan>1 como se explica arriba
    df = df.dropna(thresh=df.shape[1] - 1)

    new_df = df[[categorical_variable]]
    df2 = df.dropna()

    # Comienza el bucle
    while (sum(new_df.isnull().any(1)) > 0):
        # identificar fila y columna del NAN
        nan_rows = new_df[new_df.isnull().any(1)]
        for j in nan_rows.index:
            # En caso de que sea Nan
            if (np.isnan(new_df.loc[j])[0]):
                # separo el target de entrenamiento
                target = df2[categorical_variable]
                # separo mi X_train
                X_train = df2.drop(categorical_variable, axis=1)
                # defino y entreno el modelo
                tree_clf = DecisionTreeClassifier(max_depth=n_max_depth, random_state=random_state)
                tree_clf.fit(X_train, target)
                # obtengo la fila a la que se imputa el Nan
                X_test = df.loc[[j]]
                X_test = pd.DataFrame(X_test)
                X_test.drop(categorical_variable, axis=1, inplace=True)
                # realizo su predicción
                pred = tree_clf.predict(X_test)
                # sustituyo en df
                df.loc[j, categorical_variable] = pred
                # actualizo las condiciones
                new_df.loc[j, categorical_variable] = pred
                nan_rows = df[df.isnull().any(1)]
            else:
                continue
    return df


def relative_absolute_error(y_train: pd.core.series.Series, y_test: pd.core.series.Series,
                            y_predicted: pd.core.series.Series, type_metric='error') -> float:
    """
    Función que calcula la métrica de error Relative Absolute error o bien su score
    si así se desea ha de cambiarse type_metric por score.

    El numerador se compone por la suma de los errores absolutos,
    el denominador se compone por el error de un modelo trivial, que en este caso consiste en la media del target train.

    Esta función calcula una metrica que por lo general estará acotada entre abs(0,1) siempre y cuando nuestro modelo prediga mejor que el modelo trivial.
    """
    # En caso que las longitudes de los vectores no sean iguales dar un error
    if ((len(y_test) == len(y_predicted)) == False):
        raise TypeError("y_test and y_predicted han de ser de la misma longitud")
    else:
        # En caso que en type_metric se introduzca otro string diferente a los permitidos dar un error
        if (type_metric) not in (['error', 'score']):
            raise TypeError("type_metric ha de ser error (default) o score")
        # calculo de la métrica
        else:
            if (type_metric == 'score'):
                numerator = np.sum(np.abs(y_predicted - y_test))
                denominator = np.sum(np.mean(y_train) - y_test)
                return (-(numerator / denominator))
            else:
                numerator = np.sum(np.abs(y_predicted - y_test))
                denominator = np.sum(np.mean(y_train) - y_test)
                return (numerator / denominator)


def specificity(y_true, y_pred):
    '''esta función determina la especificidad utilizando una matriz de confusión.
    Args:
        y_true: el verdadero target
        y_pred: el target previsto

    return:
        valor de especificidad

    '''

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    specificity = tn / (tn + fp)
    return specificity


def classifier_cat(dataf):
    '''
        Descripcion: Funcion para clasificar las varibles categoricas

        Args: dataframe

        Returns: dos listas. Una lista con las variables binarias y otra con las NO binarias
    '''
    categorias = dataf.columns[dataf.dtypes == 'object']
    # Si nuestras columnas categoricas tienen sólo dos valores, utilizar Label Encoder sino One Hot Encoder

    categorias_bin = []
    categorias_NO_bin = []

    for i in categorias:
        if dataf[i].nunique() <= 2:
            categorias_bin.append(i)
        else:
            categorias_NO_bin.append(i)

    return categorias_bin, categorias_NO_bin


def cat_to_num(dataf):
    '''
        Descripcion: Funcion para transformar valores categoricos a numericos,
                    teniendo en cuenta la cantidad de valores en cada columna,
                    usando Label Encoder y One Hot Encoder

        Args: dataframe

        Returns: dataframe con los valores categoricos transformados en numericos
    '''

    # Si nuestras columnas categoricas tienen sólo dos valores, utilizar Label Encoder sino One Hot Encoder
    le = LabelEncoder()
    ohe = OneHotEncoder(handle_unknown='ignore')

    bin, NO_bin = classifier_cat(dataf)

    for i in bin:
        # print(i)
        le.fit(dataf[i])
        dataf[i] = le.transform(dataf[i])

    # verbose_feature_names_out=False es para mantener los nombres sin prefijos
    transformer = make_column_transformer((ohe, NO_bin), remainder='passthrough', verbose_feature_names_out=False)

    transformer.fit(dataf)
    transformed = transformer.transform(dataf)

    # transformed = transformer.fit_transform(df)

    dataf = pd.DataFrame(transformed, columns=transformer.get_feature_names_out())

    return dataf


# Ver balance de datos del target
def ver_balance(target):
    '''
        Descripcion: Funcion para ver el balance de los datos del target.

        Args: dataframe['target']

        Returns: dataframe balanceado
    '''
    # Vemos si mis datos estan balanceados
    print(target.value_counts())
    ax = target.value_counts().plot(kind='bar')
    ax.set_title('0 = no tiene, 1 = sí tiene')
    ax.set_ylabel('Cantidad')
    plt.show()
    return ax


def under(X, y):
    '''
        Descripcion: Funcion que balancea los dataframes con un undersampling.

        Args: X_dataframe, y_dataframe

        Returns: X_dataframe e y_dataframe balanceados
    '''
    subsample = RandomUnderSampler(random_state=42)

    X_train_new, y_train_new = subsample.fit_resample(X, y)

    return X_train_new, y_train_new


def over(X, y):
    '''
        Descripcion: Funcion que balancea los dataframes con un oversampling.

        Args: X_dataframe, y_dataframe

        Returns: X_dataframe e y_dataframe balanceados
    '''
    oversample = SMOTE(random_state=42)
    X_train_new, y_train_new = oversample.fit_resample(X, y)

    return X_train_new, y_train_new


def sampling(X, y):
    '''
        Descripcion: Funcion que dependiendo de la diferencia entre 0s y 1s en y_dataframe,
                     balancea los dataframes(X_dataframe e y_dataframe) con un undersampling,
                     oversampling, oversampling-undersampling o los deja igual.

        Args: X_dataframe, y_dataframe

        Returns: X_dataframe  e y_dataframe balanceados
    '''

    # Contar cuantos valores de cada tipo en el target tenemos
    target_0 = y.value_counts()[0]
    print('Cantidad de 0s inicial: ', target_0)
    target_1 = y.value_counts()[1]
    print('Cantidad de 1s inicial: ', target_1)

    # Comprobamos la diferencia entre el numero de 0s y 1s
    if (abs(target_0 - target_1) > 150) and (abs(target_0 - target_1) <= 2000):
        # Hacemos oversampling para ajustar el dataset
        X_new, y_new = over(X, y)

        target_0 = y_new.value_counts()[0]
        print('Cantidad de 0s final: ', target_0)
        target_1 = y_new.value_counts()[1]
        print('Cantidad de 1s final: ', target_1)
        return X_new, y_new
    # Comprobamos la diferencia entre el numero de 0s y 1s
    elif (abs(target_0 - target_1) > 2000) and (abs(target_0 - target_1) <= 5000):
        # Hacemos oversampling-undersampling para ajustar el dataset
        X_n, y_n = over(X, y)
        X_new, y_new = under(X_n, y_n)

        target_0 = y_new.value_counts()[0]
        print('Cantidad de 0s final: ', target_0)
        target_1 = y_new.value_counts()[1]
        print('Cantidad de 1s final: ', target_1)
        return X_new, y_new
    # Comprobamos la diferencia entre el numero de 0s y 1s
    elif (abs(target_0 - target_1) > 10000):
        # Hacemos undersampling para ajustar el dataset
        X_new, y_new = under(X, y)

        target_0 = y_new.value_counts()[0]
        print('Cantidad de 0s final: ', target_0)
        target_1 = y_new.value_counts()[1]
        print('Cantidad de 1s final: ', target_1)
        return X_new, y_new
    else:
        # Dejamos los dataframes tal cual
        X_new, y_new = X, y
        target_0 = y_new.value_counts()[0]
        print('Cantidad de 0s final: ', target_0)
        target_1 = y_new.value_counts()[1]
        print('Cantidad de 1s final: ', target_1)
        return X_new, y_new


def gradBoosting(X_train, X_test, y_train, y_test):
    '''
        Descripcion: Funcion que encuentra el mejor score y su estimador usando el modelo Gradient Boosting
                     Calcula uno a uno los scores.

        Args: X_train, X_test, y_train, y_test

        Returns: best_estimator, max_score
    '''
    score_max = 0
    cont = 0
    estimator_param = np.arange(50, 2000, 15)
    best_estimator = 0

    print(estimator_param)

    for i in estimator_param:
        gbrt_clf = GradientBoostingClassifier(criterion='friedman_mse', random_state=42, n_estimators=i,
                                              learning_rate=0.1)
        gbrt_clf.fit(X_train, y_train)

        goal = gbrt_clf.score(X_test, y_test)

        if score_max < goal:
            score_max = goal
            best_estimator = i
        else:
            # Si el score no mejore en 5 estimadores, salgo del bucle
            if cont < 5:
                score_max = score_max
                cont += 1
                continue
            else:
                break

        print(best_estimator, score_max)

    return best_estimator, score_max


# here I check the unique varible
def cal_cols(df, column, n=0):
    '''df: Dataframe,
    columns: columnas a realizar encode
    revisa el numero de columnas necesarias para el encode
    basado en el numero de categorias de las columnas'''
    num_val = 2 ** n
    if num_val >= df[column].nunique():
        return n
    else:
        n += 1
        return cal_cols(df, column, n)


# here I do an array with all posible binary combination
def bi_ray(n, bi=[[1], [0]], num_loop=1):
    ''' n: numero de columnas necesarias
    Crea un array con todas las columnas binarias posibles en n columnas'''

    if n == 1:
        return np.array(bi)
    else:
        list_bi = list(map(lambda x: x + [0] if x[-1] == [1] else x + [1], bi))
        list_bi1 = list(map(lambda x: x + [1] if x[-1] == [1] else x + [0], bi))
        bi = list_bi + list_bi1
    if num_loop + 1 == n:
        return np.array(bi)
    else:
        num_loop += 1
        return bi_ray(n, bi, num_loop)


# here I transform that array to a frame
def frame_maker(df, columns, up_array, num_loops=0, num_col=0, dict_decod={}, full_frame=pd.DataFrame([])):
    '''df: Dataframe
    columns: lista de columnas con todas las columnas a codificar
    up_array: array utilizado para el encode
    Crea un data frame con todas las columnas que se ha decidido codificar'''

    frame = pd.DataFrame(df[columns[num_loops]].unique())

    frame[columns[num_loops] + "_" + str(num_col)] = up_array[num_loops][:, num_col]

    frame = frame.rename(columns={0: columns[num_loops]})

    df = pd.merge(df, frame, on=[columns[num_loops]])

    if len(up_array[num_loops][0]) != num_col + 1:
        num_col += 1

        if num_col == 1:

            full_frame = pd.DataFrame(df[columns[num_loops]].unique()).rename(columns={0: columns[num_loops]})

            full_frame = pd.merge(full_frame, frame, on=columns[num_loops])
        else:

            full_frame = pd.merge(full_frame, frame, on=columns[num_loops])
        return frame_maker(df, columns, up_array, num_loops, num_col, dict_decod, full_frame)
    else:
        if num_col == 0:
            full_frame = frame
            dict_decod[columns[num_loops]] = full_frame
            full_frame = pd.DataFrame([])
            df = df.drop(columns[num_loops], axis=1)

        else:
            num_col = 0

            full_frame = pd.merge(full_frame, frame, on=columns[num_loops])
            dict_decod[columns[num_loops]] = full_frame
            full_frame = pd.DataFrame([])
            df = df.drop(columns[num_loops], axis=1)

    if len(columns) != num_loops + 1:
        num_loops += 1

        return frame_maker(df, columns, up_array, num_loops, num_col, dict_decod, full_frame)
    return df, dict_decod


def bi_hot_encoding(df, columns=None):
    '''df: DataFrame
    columns: lista de columnas con todas las columnas a codificar, default None todas las columnas serán codificadas
    Crea un dataframe codificado añadiendo al nombre de las columnas codificadas + "_number",
    y un diccionario como claves el nombre de la columna codificada y valores un dataframe con los valores codificados'''

    if columns == None:
        columns = list(df.select_dtypes("object").columns)

    n = list(map(lambda x: cal_cols(df, x, n=0), columns))

    list_array = list(map(lambda x: bi_ray(n=x), n))

    num_feat = list(map(lambda x: df[x].nunique(), columns))

    up_array = list(map(lambda x: list_array[num_feat.index(x)][:x], num_feat))

    df = frame_maker(df, columns, up_array)

    return df


def get_clusters(X_train, cluster_fd=KNeighborsClassifier(), cluster_mk=DBSCAN()):
    """esta función recoge los datos de entrenamiento y define clusters no supervisados mediante DBSCAN,
     a continuación entrena un modelo KNeighborsClassifier para predecir los clusters en los datos de prueba.
    Args:
        X_train: los datos de entrenamiento.

    Returns:
        los datos de entrenamiento con el cluster colum y un modelo KNeighborsClassifier entrenado.
    """

    predictions = cluster_mk.fit_predict(X_train)

    cluster_fd.fit(X_train, predictions)

    if str(type(X_train)) == "<class 'pandas.core.frame.DataFrame'>":

        X_train = pd.concat([X_train, pd.DataFrame(predictions).rename(columns={0: "cluster"})], axis=1)

    else:

        X_train = pd.concat([pd.DataFrame(X_train), pd.DataFrame(predictions).rename(columns={0: "cluster"})], axis=1)

    return X_train, cluster_fd


def model_dic(df_model, n=0, dic={}):
    """esta función toma una lista de modelos entrenados, los datos de entrenamiento y su numero de cluster,
    y hace un diccionario con el número de cluster como clave y la lista como valor.
    Args:
        df_model: lista de modelos entrenados, los datos de entrenamiento y su numero de cluster.

    Returns:
        diccionario con el número de cluster como clave y la lista como valor.
    """
    dic.update({df_model[n][3]: df_model[n]})

    n += 1

    if len(df_model) == n:
        return dic

    return model_dic(df_model, n, dic)


class cluster_ensemble:
    """
    este es el objeto cluster_ensemble,
    hace predicciones de datos basadas en los clusters que identifica usando DBSCAN

    Atributos:

        model: el modelo que se utilizará para realizar las predicciones.
        por defecto: RandomForestClassifier

        cluster_fd: el modelo que predice los clusters utilizando las evaluaciones de DBSCAN.
        por defecto: KNeighborsClassifier

        cluster_mk: el modelo DBSCAN básico que calificará los clusters en el proceso de entrenamiento
        por defecto: DBSCAN, con los parámetros por defecto, no puede ser otro modelo

        dic_model: diccionario de modelos vacío por defecto

    Metodos:

        fit:
            este método entrena el modelo en los diferentes clusters en los datos de entrenamiento,
            al final de este proceso tenemos un diccionario de modelos entrenados y
            un modelo para clasificar los clusters en los datos de test.

            Args:
                X_train: datos de entrenamiento
                y_train: target de entrenamiento
                self: todos los atributos

            Returns:
                    entrena todos os atributos


        predict:
            este método predice el target

            Args:
                X_test: datos de test
                self: self.cluster_fd, self.dic_model

            Returns:
                    predice el target


    """

    def __init__(self, model=RandomForestClassifier(), cluster_fd=KNeighborsClassifier(), cluster_mk=DBSCAN(),
                 dic_model={}):
        self.model = model
        self.cluster_fd = cluster_fd
        self.cluster_mk = cluster_mk
        self.dic_model = dic_model

    def fit(self, X_train, y_train):

        X_train, self.cluster_fd = get_clusters(X_train, self.cluster_fd, self.cluster_mk)

        if str(type(y_train)) == "<class 'pandas.core.frame.DataFrame'>":

            X_train = pd.concat([X_train, y_train], axis=1)

        else:

            X_train = pd.concat([X_train, pd.DataFrame(y_train)], axis=1)

        with cf.ThreadPoolExecutor() as excutor:

            df_list = list(excutor.map(lambda x: [np.array(X_train[X_train["cluster"] == x].iloc[:, :-2]),
                                                  np.array(X_train[X_train["cluster"] == x].iloc[:, -1]), x],
                                       X_train["cluster"].unique()))

        df_model = list(map(lambda x: [self.model.fit(x[0], x[1])] + x, df_list))

        self.dic_model = model_dic(df_model)

    def predict(self, X_test):

        if str(type(X_test)) == "<class 'pandas.core.frame.DataFrame'>":

            X_test["cluster"] = self.cluster_fd.predict(X_test)

        else:

            X_test = pd.DataFrame(X_test)

            X_test["cluster"] = self.cluster_fd.predict(X_test)

        preds = list(
            map(lambda x: self.dic_model[x][0].predict(X_test[X_test["cluster"] == x].iloc[:, :-1]).tolist()[0],
                self.dic_model.keys()))

        preds = list(functools.reduce(lambda x, y: x + y, preds))

        preds_val = preds[::2]
        preds_index = preds[1::2]

        preds_val = list(functools.reduce(lambda x, y: x + y, preds_val))
        preds_index = list(functools.reduce(lambda x, y: x + y, preds_index))

        preds = list(map(lambda x: preds_val[x], preds_index))

        return preds


def Dec_tree_clf(X, y):
    '''
    Función para obtener, con bases de datos numéricas y limpias, 10 valores de score,
    en un Árbol Clasificador, con parámetros random (que también se obtendrán).

    X -> Dataframe sin nuestro target
    y -> Target

    return -> dataframe con parámetros ordenados por score
    '''
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.25,
                                                        random_state=42)

    max = X.shape[1] + 1

    # En cada lista irán los valores de un parámetro
    params1 = []
    params2 = []
    params3 = []

    # En estas listas irán los valores de accuracy de train y test
    Pred_train_accuracy = []
    Pred_test_accuracy = []

    # El objetivo del bucle while es probar 100 combinaciones distintas de parámetros.
    # La función mostrará los 10 mejores accuracy obtenidos en test, así como los parámetros necesarios.
    i = 0
    while i < 100:
        param1 = np.arange(1, 6).tolist()
        param2 = np.arange(2, 12).tolist()
        param3 = np.arange(3, max).tolist()

        tree_clf = DecisionTreeClassifier(random_state=42,
                                          min_samples_leaf=np.random.choice(param1),
                                          max_depth=np.random.choice(param2),
                                          max_features=np.random.choice(param3)
                                          )

        tree_clf.fit(X_train, y_train)

        y_pred_train = tree_clf.predict(X_train)
        y_pred_test = tree_clf.predict(X_test)

        # Añadimos a cada lista los valores que le corresponden

        params1.append(str(tree_clf.get_params)[65:77])
        params2.append(str(tree_clf.get_params)[78:94])
        params3.append(str(tree_clf.get_params)[94:114])

        Pred_train_accuracy.append(accuracy_score(y_train, y_pred_train))

        Pred_test_accuracy.append(accuracy_score(y_test, y_pred_test))

        i += 1

    # Creamos un dataframe con las 5 listas
    df_1 = pd.DataFrame()

    df_1['Parámetro 1'] = params1
    df_1['Parámetro 2'] = params2
    df_1['Parámetro 3'] = params3
    df_1['Parámetro 4'] = 'random state = 42'
    df_1['accuracy en train'] = Pred_train_accuracy
    df_1['accuracy en test'] = Pred_test_accuracy

    return df_1.sort_values(by='accuracy en test', ascending=False).head(10)


def LogisticReg(X, y):
    '''
    Función para obtener, con bases de datos numéricas y limpias, 10 valores de score,
    en una Logistic Regression, con parámetros random (que también se obtendrán).

    X -> Dataframe sin nuestro target
    y -> Target

    return -> dataframe con parámetros ordenados por accuracy
    '''

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.25,
                                                        random_state=42)

    # En cada lista irán los valores de un parámetro
    params1 = []

    # En estas listas irán los valores de accuracy de train y test
    Pred_train_accuracy = []
    Pred_test_accuracy = []

    # El objetivo del bucle while es probar 100 combinaciones distintas de parámetros.
    # La función mostrará los 10 mejores accuracy obtenidos en test, así como los parámetros necesarios.
    param1 = np.arange(0, 1000, 1).tolist()
    try:
        param2 = ['l1', 'l2', 'elasticnet', 'none']
        i = 0

        while i < 100:
            lr = LogisticRegression(penalty=np.random.choice(param2),
                                    C=np.random.choice(param1))

            lr.fit(X_train, y_train)

            y_pred_train = lr.predict(X_train)
            y_pred_test = lr.predict(X_test)

            # Añadimos a cada lista los valores que le corresponden

            params1.append(str(lr.get_params)[60:])

            Pred_train_accuracy.append(accuracy_score(y_train, y_pred_train))

            Pred_test_accuracy.append(accuracy_score(y_test, y_pred_test))

            i += 1

    # PROBLEMA
    # En algunas ocasiones solo te acepta, como calor de penalty, l2 o none
    except ValueError:
        param2 = ['l2', 'none']

        i = 0

        while i < 100:
            lr = LogisticRegression(penalty=np.random.choice(param2),
                                    C=np.random.choice(param1))

            lr.fit(X_train, y_train)

            y_pred_train = lr.predict(X_train)
            y_pred_test = lr.predict(X_test)

            # Añadimos a cada lista los valores que le corresponden

            params1.append(str(lr.get_params)[60:])

            Pred_train_accuracy.append(accuracy_score(y_train, y_pred_train))

            Pred_test_accuracy.append(accuracy_score(y_test, y_pred_test))

            i += 1

    # Creamos un dataframe con las 5 listas
    df_1 = pd.DataFrame()

    df_1['Parámetros'] = params1
    df_1['accuracy en train'] = Pred_train_accuracy
    df_1['accuracy en test'] = Pred_test_accuracy

    return df_1.sort_values(by='accuracy en test', ascending=False).head(10)


def RandomForest(X, y):
    '''
    Función para obtener, con bases de datos numéricas y limpias, 10 valores de score,
    en un Random Forest, con parámetros random (que también se obtendrán)

    X -> Dataframe sin nuestro target
    y -> Target

    return -> dataframe con parámetros ordenados por accuracy
    '''
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.25,
                                                        random_state=42)

    # En cada lista irán los valores de un parámetro
    params1 = []
    params2 = []
    params3 = []
    max = X.shape[1] + 1

    # En estas listas irán los valores de accuracy de train y test
    Pred_train_accuracy = []
    Pred_test_accuracy = []

    # El objetivo del bucle while es probar 100 combinaciones distintas de parámetros.
    # La función mostrará los 5 mejores accuracy obtenidos en test, así como los parámetros necesarios.
    i = 0
    while i < 100:
        param1 = np.arange(1, 200).tolist()
        param2 = np.arange(2, 12).tolist()
        param3 = np.arange(3, max).tolist()

        rnd_clf = RandomForestClassifier(random_state=42,
                                         n_estimators=np.random.choice(param1),
                                         max_depth=np.random.choice(param2),
                                         max_features=np.random.choice(param3))

        rnd_clf.fit(X_train, y_train)

        y_pred_train = rnd_clf.predict(X_train)
        y_pred_test = rnd_clf.predict(X_test)

        # Añadimos a cada lista los valores que le corresponden

        params1.append(str(rnd_clf.get_params)[65:77])
        params2.append(str(rnd_clf.get_params)[78:93])
        params3.append(str(rnd_clf.get_params)[94:110])

        Pred_train_accuracy.append(accuracy_score(y_train, y_pred_train))

        Pred_test_accuracy.append(accuracy_score(y_test, y_pred_test))

        i += 1

    # Creamos un dataframe con las 5 listas
    df_1 = pd.DataFrame()

    df_1['Parámetro 1'] = params1
    df_1['Parámetro 2'] = params2
    df_1['Parámetro 3'] = params3
    df_1['Parámetro 4'] = 'random state = 42'
    df_1['accuracy en train'] = Pred_train_accuracy
    df_1['accuracy en test'] = Pred_test_accuracy

    return df_1.sort_values(by='accuracy en test', ascending=False).head(10)


def pickleizer(nombre, modelo=None):
    ''' pickleizer tiene la capacidad de guardar modelos ya entrenados o abrir modelos entrenados desde una carpeta.
        Tiene la ventaja de que la propia ejecución de la funcion importa la libreria pickle.

        Args:
            nombre: Nombre del archivo donde se quiere importar o guardar el modelo.
            modelo: En caso de que se seleccione un modelo (ya entrenado) lo guardará. Cuando no se especifíca un modelo lo abre. Default = None'''
    import pickle
    if modelo == None:
        with open(nombre, 'rb') as archivo_entrada:
            trained_model = pickle.load(archivo_entrada)
        return (trained_model)
    else:
        with open(nombre, 'wb') as archivo_salida:
            pickle.dump(modelo, archivo_salida)


def DPRegressor(X: pd.DataFrame, y: pd.Series):
    '''
    Regresor con capas ocultas de neuronas
    Esta función solo se puede usar si todas las colunmnas son numericas

    Args:
    X -> DataFrame
        Matriz con los datos
    y -> Series
        Vector con el target

    Return:
    model -> Pipeline
        Modelo ya entrenado
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    mlp_reg = MLPRegressor(hidden_layer_sizes=[50, 50, 50], random_state=42)

    # Debemos escalar los datos ya que utiliza descenso de gradiente
    pipeline = make_pipeline(StandardScaler(), mlp_reg)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)

    print('El error medio es de:', rmse)

    return pipeline


def read_it(url):
    """Mediante la función read_it() buscamos cargar un dataset
    sin tener que preocuparnos por el tipo de archivo que sea (con
    diferentes separadores) ni la codificación que tenga,

    Args:
      url (URL): Link o ubicación del dataset que vamos a trabajar

    Returns:
      Devuelve un dataset ya transformado para poder trabajar con pandas
      """

    sep = ["\t", ",", ";", "|", ":"]
    encoding = ["utf_32", "utf_16", "utf_8"]

    for i in sep:
        for j in encoding:

            try:
                pd.read_csv(url, sep=i, encoding=j)

            except:
                continue

            if pd.read_csv(url, sep=i, encoding=j).shape[1] == 1:
                continue

            else:
                return pd.read_csv(url, sep=i, encoding=j)


def google_img(path_api, urls, directory_names, directory_path):
    """Mediante google_img() buscamos automatizar la descarga de imagenes relacionadas
        con una busqueda determinada en nuestro navegador de internet, nos
        apoyaremos en la API de Selenium y simularemos una serie de busquedas
        para posteriormente descargar dichas imagenes en las carpetas que previamente
        hemos nombrado

        Args:
            path_api ("string"): Ubicación de la API del navegador web de Selenium
            urls ("lista"): Lista de strings que componen las URLs de las imagenes que queremos obtener
            directory_names("lista"): Lista de strings con los nombres que queremos llamar a las carpetas donde estarán las imagenes (y las imagenes)
            directory_path("string"): Ubicación donde crear dichas carpetas

        Returns:
            Devuelve "n" carpetas con la mayor cantidad de imagenes posibles descargadas de la URLs que les hemos pasado
        """

    wd = webdriver.Chrome(executable_path=path_api)

    def get_images_from_google(wd, delay, max_images, url):
        def scroll_down(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)

        url = url
        wd.get(url)

        image_urls = set()
        skips = 0
        while len(image_urls) + skips < max_images:
            scroll_down(wd)
            thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

            for img in thumbnails[len(image_urls) + skips:max_images]:
                try:
                    img.click()
                    time.sleep(delay)
                except:
                    continue

                images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                for image in images:
                    if image.get_attribute('src') in image_urls:
                        max_images += 1
                        skips += 1
                        break

                    if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                        image_urls.add(image.get_attribute('src'))

        return image_urls

    def download_image(down_path, url, file_name, image_type='JPEG',
                       verbose=True):
        try:
            time = dt.now()
            curr_time = time.strftime('%H:%M:%S')
            img_content = requests.get(url).content
            img_file = io.BytesIO(img_content)
            image = Image.open(img_file)
            file_pth = down_path + file_name

            with open(file_pth, 'wb') as file:
                image.save(file, image_type)

            if verbose == True:
                print(f'The image: {file_pth} downloaded successfully at {curr_time}.')
        except Exception as e:
            print(f'Unable to download image from Google Photos due to\n: {str(e)}')

    if __name__ == '__main__':
        google_urls = urls
        nombre_carpeta = directory_names

        coin_path = directory_path

        for lbl in nombre_carpeta:
            if not os.path.exists(coin_path + lbl):
                print(f'Making directory: {str(lbl)}')
                os.makedirs(coin_path + lbl)

        for url_current, lbl in zip(google_urls, nombre_carpeta):
            urls = get_images_from_google(wd, 0, 100, url_current)

            for i, url in enumerate(urls):
                download_image(down_path=coin_path + lbl + "/",
                               url=url,
                               file_name=str(i + 1) + '.jpg',
                               verbose=True)
        wd.quit()


def dif_encoder(x, y):
    '''dif_encoder devuelve una nueva columna en el Dataframe codificando en 0 y 1
        en base a la resta entre dos columnas seleccionadas por el usuario

            0 -> La diferencia es negativa
            1 -> La diferencia es positiva
        Args:
            x: Columna 1 del dataframe
            y: Columna 2 del dataframe
        Returns:
            Una nueva columna dentro del Dataframe con la codificación en 0 y 1

    '''

    return np.where(x > y, 1, 0)


def splityear(x):
    '''splityear devuelve el año de una fecha completa dd/mm/aaaa

        Args:
            x: Columna de dataframe que se quiere modificar

        Returns:
            Año que aparece en la fecha completa'''

    for i in x:
        año = [int(i.split('/')[2]) for i in x]
        return año


def simbolcleaner(x):
    '''simbolcleaner limpia aquellos elementos numéricos que contienen caracteres especiales
        Args:
            x: Columna de dataframe que se quiera limpiar de caracteres especiales
        Returns:
            Números sin caracteres especiales

    '''

    lista = []
    for i in x:
        lista.append(''.join(filter(str.isalnum, i)))
    return lista


def too_many_nans(df, threshold=0, clean=True):
    '''too_many_nans permite eliminar las columnas seleccionadas en funcion del porcentaje de valores nulos que haya en ellas.
        Args:
            df: El dataframe
            threshold: El porcentaje de valores nulos a partir del cual se quieren eliminar columnas. Default=0
            clean: Cuando es True se eliminan las columnas. Cuando es False se genera un nuevo df en el que se muestra el porcentaje de valores
                   nulos de cada columna. Default=True

    '''
    na = df.isna().sum()
    n = len(df)
    percent = np.round(na * 100 / n, 2)
    df_perc = pd.DataFrame(percent, columns=['Nans Percentage']).sort_values('Nans Percentage', ascending=False)
    if clean == False:
        return df_perc

    elif clean == True:
        cols_to_drop = (df_perc[df_perc['Nans Percentage'] > threshold].index.values)
        df_clean = df.drop(cols_to_drop, axis=1)
        return df_clean


def num_processor(df, chars1=',\'', chars2='@\'€%"$'):
    '''num_processor permite introducir un Dataframe y procesa los valores para devolver todos los números en formato float y sin valores
        erróneos como comas o símbolos de dinero.

        Args:
            df: un Dataframe
            chars1: caracteres que pueden encontrarse como separadores decimales. Default: (, ')
            chars2: caracteres especiales que pueeden aparecer en un dataframe. Default: (@\'€%"$)

        Returns:
            Un nuevo Dataframe con los valores procesados.

    '''
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
    df_return = pd.DataFrame()

    for columns in df.columns:
        if df[columns].dtypes == object:

            columns_list = df[columns].tolist()

            final_list = []
            for values in columns_list:
                values = str(values)

                for c in chars1:
                    values = values.replace(c, '.')
                for c in chars2:
                    values = values.replace(c, '')

                characters = [*values]
                num_list = []
                for i in characters:
                    if i in nums:
                        num_list.append(i)
                if len(num_list) == 0:
                    num_list.append('No Num')
                final_num = ''.join(num_list)

                try:
                    final_num = float(final_num)
                except ValueError:
                    True

                final_list.append(final_num)

            n = 0
            for categorical in final_list:
                if categorical == 'No Num':
                    n += 1
                if n == len(final_list):
                    final_list = (df[columns]).tolist()

        else:
            final_list = (df[columns]).tolist()

        df_return[columns] = final_list

    for columns in df_return.columns:
        for errors in df_return[columns]:
            if errors == 'No Num':
                print('Posible incongruencia en:')
                print('Columna: ', columns)
                print('Indice: ', df_return[df_return[columns] == 'No Num'].index.values[0])
                print()

    return df_return


def mueve_imagenes(carpeta_fuente, carpeta_train, carpeta_test, n_max=500, split=0.2):
    '''Mueve_imagenes cambia la dirección de las imágenes desde una carpeta original hasta una carpeta de train y otra de test.

       Args:
            carpeta_fuente(str): path de la carpeta original en la que se encuentran las imagenes.
            carpeta_train(str): path de la carpeta de train.
            carpeta_test(str): path de la carpeta de test.
            n_max(int): número máximo de imágenes con las que se quiere trabajar, depende de la disponibilidad. Default= 500.
            split(float): porcentaje de imágenes que se quieren reservar para test. Default=0.2

       Returns: None
    '''

    import shutil
    import os

    # Primera parte de la funcion
    imagenes = os.listdir(carpeta_fuente)

    if not os.path.exists(carpeta_train):  # esto es para que no se sobreescriba la carpeta
        os.makedirs(carpeta_train)
        print('Carpeta creada: ', carpeta_train)

    count = 0
    for i, nombreimg in enumerate(imagenes):
        if i < n_max:
            # Copia de la carpeta fuente a la destino
            shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_train + '/' + str(count) + '.jpg')
            count += 1

    # Segunda parte
    imagenes = os.listdir(carpeta_train)
    if not os.path.exists(carpeta_test):  # esto es para que no se sobreescriba la carpeta
        os.makedirs(carpeta_test)
        print('Carpeta creada: ', carpeta_test)

    count = 0
    count = 0
    for i, nombreimg in enumerate(imagenes):
        if i > (np.round(n_max - n_max * split,
                         0)):  # En lugar de un numero fijo para dividir en train/test se deja en un porcentaje que por defecto es 0.2
            # Copia de la carpeta fuente a la destino
            shutil.move(carpeta_train + '/' + nombreimg, carpeta_test + '/' + str(count) + '.jpg')
            count += 1


def read_data(path, im_size, class_names):
    ''' read_data lee las imagenes de la carpeta "train" y "test", crea el target a partir de una lista y las convierte en un arreglo de
        numpy para las X y otro para los targests. Por ultimo, mezcla los datos y las etiquetas de forma aleatoria.

        ARGS:
            path(str): carpeta en la que se encuentran las imagenes.
            im_size(tuple): tamaño de las imagenes.
            class_names(list): nombres de las categorías.

        Returns:
            Dos np.arrays, el primero son las X y el segundo las categorías.
    '''

    class_names_label = {class_name: i for i, class_name in enumerate(class_names)}

    X = []
    y = []

    for folder in os.listdir(path):
        label = class_names_label[folder]
        folder_path = os.path.join(path, folder)
        # Iterar sobre todo lo que haya en path
        for file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, file)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, im_size)
            X.append(image)
            y.append(label)

    X_train = np.array(X)
    y_train = np.array(y)

    X_train, y_train = shuffle(X_train, y_train, random_state=42)

    return X_train, y_train


def edad(df, columna):
    '''
    Sustituye los valores de fecha de nacimiento por la edad.

    Args:
        df --> Dataframe
        columna --> Columna a la que aplicar la función. Ejemplo: Dataframe['columna']

    Returns:
        Un nuevo Dataframe con la función aplicada.

    '''

    hoy = date.today()
    columna = pd.to_datetime(columna)

    edad = []
    for i in columna:
        age = hoy.year - i.year - ((hoy.month, hoy.day) < (i.month, i.day))
        edad.append(age)

    df[columna.name] = edad

    df[columna.name] = df[columna.name].astype('Int64')
    df.rename(columns={columna.name: 'edad'}, inplace=True)

    return df


def igualar_strings(df, columna, string_deseado):
    '''
    Cuando en una columna existen strings iguales pero escritos de diferente manera (con acentuación o sin, en mayúsculas o en minúsculas),
    los sustituye por el string que ingresemos manualmente.

    Args:
        df --> Dataframe
        columna --> Columna a la que aplicar la función. Ejemplo: Dataframe['columna'].
        string_deseado --> String por el que queremos sustituir los valores. Ejemplo: "Japón"

    Returns:
        Un dataframe con la función aplicada

    '''

    def comparacion(string_original):

        if unidecode(string_original.lower()) == unidecode(string_deseado.lower()):
            return string_deseado
        else:
            return string_original

    string_cambiado = columna.apply(comparacion)

    df[columna.name] = string_cambiado

    return df


def outliers(df, columna):
    '''
    Encuentra valores outliers de una columna y elimina las filas en las que se encuentran dichos valores.

    Args:
        df --> Dataframe
        columna --> Columna a la que aplicar la función. Ejemplo: Dataframe['columna']

    Returns:
        Un nuevo Dataframe sin outliers.

    '''

    # delimitar los quantiles
    quantile1 = np.percentile(columna, 25, interpolation='midpoint')
    quantile3 = np.percentile(columna, 75, interpolation='midpoint')

    inter_quartile_range = quantile3 - quantile1

    print('Old Shape: ', df.shape)

    # Límite superior
    upper = np.where(columna >= (quantile3 + 1.5 * inter_quartile_range))
    # Límite inferior
    lower = np.where(columna <= (quantile1 - 1.5 * inter_quartile_range))

    # Eliminar los outliers
    df.drop(upper[0], inplace=True)
    df.drop(lower[0], inplace=True)

    print('New Shape: ', df.shape)

    return df


def porcentaje(columna):
    '''
    Obtiene el porcentaje de aparición de un valor en una columna concreta.

    Args:
        columna --> Columna a la que aplicar la función. Ejemplo: Dataframe['columna'].

    Returns:
        Un dataframe con la columna objetivo y la columna porcentaje.

    '''

    porcentaje = round(columna.value_counts(normalize=True) * 100, 2)
    return pd.DataFrame(porcentaje).reset_index().rename(columns={'index': columna.name, columna.name: 'porcentaje'})


def trimestre(df, string_columna):
    '''
    Agrupa las fechas de una columna datetime por trimestres, sumando los valores del resto de columnas agrupadas.

    Args:
        df --> Dataframe
        string_columna --> Columna a la que aplicar la función. Ejemplo: "columna"'.

    Returns:
        Un dataframe con la agrupación aplicada

    '''

    df_trimestre = df.groupby(pd.Grouper(key=string_columna, freq='3M')).aggregate(np.sum)
    return df_trimestre


def deteccion_outliers(data, features):
    '''
    Ésta función realiza un bucle para pasar por todas las columnas que indiquemos
    y calcula los valores que se encuentran fuera de los limites de los cuantiles 1 y 3,
    mete en una lista los indices de los valores y cuenta cuantas veces se repiten entre todas las columnas.
    Si el indice lo detecta como outlier en mas de dos columnas mete el indice
    en la lista de outlier del dataframe.

    Precisa de tener numpy instalado

    Args:
        -data(DataFrame): Base de datos que tiene todas las columnas que queremos revisar

        -features(columnas): Nombre de todas las columnas que contiene el dataframe a revisar,
        se puede introducir data.columns.

    Return:
        devuelve una lista con los indices que estan fuera de los cuantiles 1 y 3 en
        mas de dos columnas del DataFrame.

    Agradecimientos a:
     Enes Besinci. Enlace a kaggle-->https://www.kaggle.com/enesbeinci
    '''

    outlier_indices = []

    for c in features:
        # 1st quartile
        Q1 = np.percentile(data[c], 25)
        # 3rd quartile
        Q3 = np.percentile(data[c], 75)
        # IQR
        IQR = Q3 - Q1
        # Outlier limite
        outlier_limite = IQR * 1.5
        # detect outlier and their indeces
        outlier_list_col = data[(data[c] < Q1 - outlier_limite) | (data[c] > Q3 + outlier_limite)].index
        # store indeces
        outlier_indices.extend(outlier_list_col)

    outlier_indices = Counter(outlier_indices)
    multiples_outliers = list(i for i, v in outlier_indices.items() if v > 2)

    return multiples_outliers


def lista_de_listas(lista):
    '''
    La función lista_de_listas crea una lista individual por cada elemento de la lista argumento,
    pasando asi a una lisa cuyos elementos son listas con un solo elemento

    esto es especialmente util para poder trabajar con strings de varias palabras
    dentro de una lista.

    ejemplo:
        lista = ['estoy programando en python','hola mundo',1234]
        lista_de_listas(lista)
        return [['estoy programando en python'],['hola mundo'],[1234]]

    Args:
        lista: introducir una lista independientemente de los elementos existentes dentro

    Return:
        lista_vacia: una lista de sublistas, cada sublista es un elemento de la lista original.

    '''
    lista_vacia = []
    for i in range((len(lista))):
        lista_vacia.append([])  # introduce una lista vacia en lista_vacia por cada vuelta del bucle

    for n, i in enumerate(lista_vacia):
        i.append(lista[
                     n])  # en cada valor de lista vacia(i) realiza un append del elemento correspondiente de lista, indicando su indice mediante n

    return lista_vacia


def ratio_nulos(data, features):
    '''
    Función que calcula el porcentaje de valores nulos
    para cada columna de un dataframe.

    Args:
        data(DataFrame): introduce un dataframe completo
        features(columnas): las columnas del dataframe, podemos usar dataframe.columns.

    return:
        devuelve un dataframe en el cual los indices son los nombres de las columnas
        y una unica columna con los ratios de valores nulos asignados cada uno a su
        columna correspondiente.
    '''

    diccionario = {}
    for c in features:
        ratio = (len(data[c][data[c].isnull() == True]) / len(data[c])) * 100

        diccionario[c] = round(ratio, 2)

    return pd.DataFrame(diccionario.values(), columns=['null_ratio'], index=diccionario.keys())
