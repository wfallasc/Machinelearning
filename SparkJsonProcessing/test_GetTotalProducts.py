from funciones import *

from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col



def test_NoValidParameterGetTotalProducts(spark_session):
    #validar que no falle si se envian parametros no validos
    my_emptyResult = GetTotalProducts('',spark_session)
    
    assert my_emptyResult.count() == 0
    print ("test_NoValidParameterGetTotalProducts OK")


def test_GetTotalProducts_SameProductTwice(spark_session):
    # validar la suma correcta de dos productos iguales
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,100.0), 
                          ("Caja2",'producto1', 2,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    
    
    #el monto sumado para el producto debe ser igual a 200
    assert actual_ds.collect()[0][2] == 200.0
    
    print ("test_GetTotalProducts_SameProductTwice OK")


def test_GetTotalProducts_MontoWithNullValues(spark_session):
    # validar la suma correcta de dos productos iguales
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',None,None), 
                          ("Caja2",'producto2', 2,None)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    
    
    schemaResult = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("producto2",2,None),
            ("producto1", None, None)
        ],schemaResult)
    
    #subtotales en nulo, pero una cantidad valida
    assert actual_ds.collect() == expected_ds.collect()
    
    print ("test_GetTotalProducts_MontoWithNullValues OK")

def test_GetTotalProducts_DistinctProducts(spark_session):
    # nombres de prodcuto distinto no debe agruparlos
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',2,23.0), 
            ("Caja1",'producto2', 2,24.3),
            ("Caja2",'producto3', 2,24.3)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    

    #debe generar 3 filas de resultados
    assert actual_ds.count() == 3
    
    print ("test_GetTotalProducts_DistinctProducts OK")


def test_GetTotalProducts_EmptyProductName(spark_session):
    # sumar los nombre de productos no validas en un solo
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",None,1,2.0), 
            ("Caja1",None, 2,4.0),
            ("Caja2",None, 3,6.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    
    schemaResult = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            (None,6,28.0)
        ],schemaResult)

    #debe sumar los nombres vacios en uno solo
    assert actual_ds.collect() == expected_ds.collect()
    
    print ("test_GetTotalProducts_EmptyProductName OK")


def test_GetTotalProducts_ValidOrder(spark_session):
    # se retorna ordernado de mayor a menor p facilidad de futuros calculos
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1","Prod1",1,2.0), 
            ("Caja1","Prod2", 2,4.0),
            ("Caja2","Prod3", 3,6.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    
    schemaResult = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod3", 3,18.0),
            ("Prod2", 2,8.0),
            ("Prod1",1,2.0)
        ],schemaResult)

    #valida que el orden sea correcto
    assert actual_ds.collect() == expected_ds.collect()
    
    print ("test_GetTotalProducts_ValidOrder OK")


def test_GetTotalProducts_SumaDifCajas(spark_session):
    # Valida la correcta suma del mismo producto en distintas cajas
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1","Prod1",1,10.0), 
            ("Caja3","Prod1", 2,10.0),
            ("Caja3","Prod1", 3,10.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    
    schemaResult = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod1",6,60.0)
        ],schemaResult)

    #valida que de un solo registro del producto  para distintas cajas
    assert actual_ds.collect() == expected_ds.collect()
    
    print ("test_GetTotalProducts_SumaDifCajas OK")


def test_GetTotalProducts_EmptyDataset(spark_session):
    # Valida que la funcion funciona cuando llega un dataset vacio
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = []
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalProducts(df,spark_session)
    

    assert actual_ds.count() == 0 
    
    print ("test_GetTotalProducts_EmptyDataset OK")



