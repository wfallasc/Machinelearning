import os
from funciones import *
import json
from pyspark.sql.functions import col, split
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType,DecimalType
from pyspark.sql import SparkSession
import pyspark.sql.functions as func
import inspect, os.path


print("Init program-----------------------------")

spark = SparkSession.builder.appName("LoadData").getOrCreate()

filename = inspect.getframeinfo(inspect.currentframe()).filename
my_path     = os.path.dirname(os.path.abspath(filename))

data_path = getArgsPath()

my_path= my_path + "/" + data_path + "/"


directory = os.fsencode(my_path)

ListaCompras=[]
ListaMetricas=[]

ListaCompras=ProcessJsonFile(my_path)


schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])


df = spark.createDataFrame(ListaCompras,schema)

DfTotalProducts = GetTotalProducts(df,spark)
DfTotalCajas =GetTotalCajas(df,spark)

#materializar los dataframe en colecciones de tuplas para trabajar en memoria
prod_list = DfTotalProducts.collect()
cajas_list = DfTotalCajas.collect()


ProdMasCantidadVentas = ObtenerProdMayorCantidadVentas(prod_list)
ProdMasMontoVentas = ObtenerProdMayorMontoVentas(prod_list)
CajaMasVentas = ObtenerCajasMayorMontoVentas(cajas_list)
CajaMenosVentas = ObtenerCajasMenosMontoVentas(cajas_list)
CajasPerc25 = ObtenerPercentilCajas(cajas_list, 25)
CajasPerc50 = ObtenerPercentilCajas(cajas_list, 50)
CajasPerc75 = ObtenerPercentilCajas(cajas_list, 75)

tp = ( "caja_con_mas_ventas",CajaMasVentas[0])
ListaMetricas.append(tp)

tp = ( "caja_con_menos_ventas",CajaMenosVentas[0])
ListaMetricas.append(tp)

tp = ( "percentil_25_por_caja",CajasPerc25)
ListaMetricas.append(tp)

tp = ( "percentil_50_por_caja",CajasPerc50)
ListaMetricas.append(tp)

tp = ( "percentil_75_por_caja",CajasPerc75)
ListaMetricas.append(tp)

tp = ( "producto_mas_vendido_por_unidad",ProdMasCantidadVentas[0])
ListaMetricas.append(tp)

tp = ( "producto_de_mayor_ingreso",ProdMasMontoVentas[0])
ListaMetricas.append(tp)

#producir los archivos----------------
SalvarArchivoMetricas(ListaMetricas)
SalvarArchivoVentasCajas(cajas_list)
SalvarArchivoVentasProductos(prod_list)

print("End program------------------------------")
