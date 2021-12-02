import sys
import os
import json
import math
import csv
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col


def getArgsPath():
    
    Data_Folder= "Datos"

    try:
        if len(sys.argv)>0:
            Data_Folder= str(sys.argv[1])
            if (len(Data_Folder)>0):
                return Data_Folder
    except:
        print("Rutas no validas espeficadas en args")
                
    return Data_Folder


def ProcessJsonFile(directory):
    
    
    tmp_List=[]
    
    if len(directory)==0:
        return tmp_List
    
    if not os.path.isdir(directory):
        return tmp_List
    
    
    for file in os.listdir(directory):
        
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            FilePath = directory + filename
            with open(FilePath, "r") as read_file:
            
                data = json.load(read_file)

                numcaja = data["numero_caja"]

                for compra in data["compras"]:   
                    for prod in compra:
                        tmp_List.append(AgregarTupla(numcaja,prod))
                continue
        else:
                continue
        
    return tmp_List


def AgregarTupla(numcaja,prod):
    
    try:
        
        cant = int(prod["cantidad"])
        precio = float(prod["precio_unitario"])
                       
    except:
        cant=0
        precio=0
        print("not valid values")
        
    Data = ( numcaja , prod["nombre"] , cant , precio )

    return Data


def GetTotalProducts(dfData,spark):
    #group by porducto, cons los sumarizados de cantidad y subtotal
    schema = StructType([ StructField('Producto', StringType()),
                        StructField('sum(cantidad)', IntegerType()),
			StructField('sum(Subtotal)', FloatType())])
    
    
    if not(isinstance(dfData, pyspark.sql.dataframe.DataFrame)) :
        print("No valid dataframe")
        return spark.createDataFrame([], schema)
    
    Df_TotalProducts = dfData.withColumn("Subtotal",
                                    col("cantidad") *  col("precio_unitario"))
    
    Df_TotalProducts = Df_TotalProducts.groupBy("producto").sum("cantidad","Subtotal").orderBy('sum(cantidad)',ascending=False)
    

    
    return Df_TotalProducts


def GetTotalCajas(dfData,spark):
    #agrupa por cajas
    schema = StructType([ StructField('num_caja', StringType()),
                        StructField('Total', FloatType())])
    
    
    if not(isinstance(dfData, pyspark.sql.dataframe.DataFrame)) :
        print("No valid dataframe")
        return spark.createDataFrame([], schema)
    
    Df_TotalCajas = dfData.withColumn("Subtotal",
                                    col("cantidad") *  col("precio_unitario"))
    

    Df_TotalCajas = Df_TotalCajas.groupBy("num_caja").sum("Subtotal").orderBy('sum(Subtotal)', ascending=False)
    
    Df_TotalCajas = Df_TotalCajas.withColumn("Total", func.round(Df_TotalCajas["sum(Subtotal)"], 2))
    
    columns_to_drop = ['sum(Subtotal)']
    Df_TotalCajas = Df_TotalCajas.drop(*columns_to_drop)
    
    return Df_TotalCajas


def ObtenerProdMayorCantidadVentas(prod_list):
    
    if len(prod_list)==0:
        empty=('',0,0.00)
        return empty
    
    prod_list = [t for t in prod_list if   isinstance(t[1], int) ]
    prod_list.sort(key = lambda x: x[1])
    return prod_list[-1]


def ObtenerProdMayorMontoVentas(prod_list):
    if len(prod_list)==0:
        empty=('',0,0.00)
        return empty
    prod_list = [t for t in prod_list if   isinstance(t[2], float) ]
    prod_list.sort(key = lambda x: x[2])
    return prod_list[-1]

def ObtenerCajasMayorMontoVentas(cajas_list):
    if len(cajas_list)==0:
        empty=('',0.00)
        return empty
    
    return cajas_list[0]


def ObtenerCajasMenosMontoVentas(cajas_list):
    if len(cajas_list)==0:
        empty=('',0.00)
        return empty
    
    return  cajas_list[-1]

def ObtenerPercentilCajas(cajas_list, perc):
    
    if not isinstance(perc, int):
        return 0

    if (perc>100):
        return 0

    if len(cajas_list)==0:
        return 0
    
    cajas_list = [t for t in cajas_list if   isinstance(t[1], float) ]
    
    if len(cajas_list)==0:
        return 0
    ListaMontosVentas = [item[1] for item in cajas_list]
    size = len(ListaMontosVentas)
    return sorted(ListaMontosVentas)[int(math.ceil((size * perc) / 100)) - 1]


def SalvarArchivoMetricas(ListaMetricas):
    with open('metricas.csv', 'w') as f:
        writer = csv.writer(f , lineterminator='\n')
        for tup in ListaMetricas:
            writer.writerow(tup)


def SalvarArchivoVentasCajas(ListaCajas):
    with open('total_cajas.csv', 'w') as f:
        writer = csv.writer(f , lineterminator='\n')
        for tup in ListaCajas:
            writer.writerow(tup)

def SalvarArchivoVentasProductos(prod_list):
    with open('total_productos.csv', 'w') as f:
        writer = csv.writer(f , lineterminator='\n')
        for tup in prod_list:
            new_tup= (tup[0],tup[1])
            writer.writerow(new_tup)
