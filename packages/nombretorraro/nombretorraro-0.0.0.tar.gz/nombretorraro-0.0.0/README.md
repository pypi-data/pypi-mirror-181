# LIBRERÍA DE LA CLASE DE LA CLASE DE DATA SCIENCE DE THE BRIDGE, GRUPO DE SEPTIEMBRE 2022 MODALIDAD FULL TIME

## Esta librería incluye funciones de limpieza, visualización y machine learning


### Limpieza

read_it(url)
google_img(path_api, urls, directory_names, directory_path)
dif_encoder(x, y)
splityear(x)
simbolcleaner(x)
too_many_nans(df, threshold=0, clean=True)
num_processor(df, chars1=',\'', chars2='@\'€%"$')
mueve_imagenes(carpeta_fuente, carpeta_train, carpeta_test, n_max=500, split=0.2)
read_data(path, im_size, class_names)
edad(df, columna)
igualar_strings(df, columna, string_deseado)
outliers(df, columna)
porcentaje(columna)
trimestre(df, string_columna)
deteccion_outliers(data, features)
lista_de_listas(lista)
ratio_nulos(data, features)



### Visualización

visualize_data(x, y)
s_temporal(df, a, y)
comparacion_stemporal(train, test, prediction, lower_series, upper_series)
candle_plot(df)
grafica_creator(df)
grid_creator(data, x, y, hue)
Line_Line_bar_party(x, y, y1, label_x="x", label_y="y", label_y1="y1", plotsize=(20, 12), barcolor="grey", linecolor_y="green" linecolor_y1="b")
balanced_target(X_train, y_train)
feature_importances_visualization(best_estimator, X_train, plotsize=(20, 10))
matrices_comparadas(y, x_test_scaled, y_test, nombre_modelo, y_2, x_test_scaled_2, y_test_2, nombre_modelo_2, size)
plot_matriz_confusion(y, x_test_scaled, y_test, nombre_modelo, size)
piechart_etiquetado(data, size)
test_transformers(df, cols)
report_plot(tree_entrenado, X_test, y_test, columnas_X)
bar_plot(df, columna)
mapa_folium(df, geojson, key, coord, legend="Mapa")
vis_line(df, ejex, ejey, group="", type=0)
matrix_sca (df, dimensiones, agrupar, titulo="Scatter Matrix")
pca_visualization(df)


### Machine Learning

my_pca(n_components, df)
my_kmeans(n_clusters, df)
anomalias_var(feature)
FeatureImportance_rf(X, y, n)
FeatureSelection_var(X, min_var)
Impute_Tree_Regressor(df: pd.core.frame.DataFrame, n_max_depth: int, random_state: int)
Impute_Tree_classifier(df: pd.core.frame.DataFrame, categorical_variable: str, n_max_depth: int, random_state: int)
relative_absolute_error(y_train: pd.core.series.Series, y_test: pd.core.series.Series, y_predicted: pd.core.series.Series, type_metric='error')
specificity(y_true, y_pred)
classifier_cat(dataf)
cat_to_num(dataf)
ver_balance(target)
under(X, y)
over(X, y)
sampling(X, y)
gradBoosting(X_train, X_test, y_train, y_test)
cal_cols(df, column, n=0)
bi_ray(n, bi=[[1], [0]], num_loop=1)
frame_maker(df, columns, up_array, num_loops=0, num_col=0, dict_decod={}, full_frame=pd.DataFrame([]))
bi_hot_encoding(df, columns=None)
get_clusters(X_train, cluster_fd=KNeighborsClassifier(), cluster_mk=DBSCAN())
model_dic(df_model, n=0, dic={})
class cluster_ensemble
Dec_tree_clf(X, y)
LogisticReg(X, y)
RandomForest(X, y)
pickleizer(nombre, modelo=None)
DPRegressor(X: pd.DataFrame, y: pd.Series)
