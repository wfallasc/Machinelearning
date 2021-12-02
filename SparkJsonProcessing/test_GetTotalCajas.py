from funciones import *

from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col

def test_GetTotalCajas_NotValidParameter(spark_session):
    #validar que no falle si se envian parametros no validos
    my_emptyResult = GetTotalCajas('',spark_session)
    
    assert my_emptyResult.count() == 0
    print ("test_GetTotalCajas_NotValidParameter OK")


def test_GetTotalCajas_SumaMismaCaja(spark_session):
    # validar que sume correctamente la misma caja
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,100.0), 
                          ("Caja1",'producto1', 2,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    
    #el monto sumado para el producto debe ser igual a 200
    assert actual_ds.collect()[0][1] == 200.0
    
    print ("test_GetTotalCajas_SumaMismaCaja OK")

def test_GetTotalCajas_SumaDistintasCajas(spark_session):
    # validar que sume correctamente las distintas cajas
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,100.0), 
            ("Caja2",'producto1', 2,50.0),
            ("Caja3",'producto1', 2,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    
    #3 cajas distintas , debe dar 3 sumas
    assert  actual_ds.count() == 3
    
    print ("test_GetTotalCajas_SumaDistintasCajas OK")

def test_GetTotalCajas_ValoresNulos(spark_session):
    # validar que retorne las 3 cajas aunque no temga valores    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",None,None,None), 
            ("Caja2",None, None,None),
            ("Caja3",None, None,None)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    schemaResult = StructType([StructField('num_caja', StringType()),
                         StructField('Total', FloatType())])
        
    
    #debe retornar 3 filas
    assert actual_ds.count() == 3
    
    print ("test_GetTotalCajas_ValoresNulos OK")


def test_GetTotalCajas_NombresNulos(spark_session):
    # validar que los nombres nulos no afecten el resultado final
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,100.0), 
            ("Caja1",'producto1', 2,50.0),
            (None,'producto1', 2,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    schemaResult = StructType([StructField('num_caja', StringType()),
                         StructField('Total', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("Caja1",200.0),(None,100.0)
        ],schemaResult)

    assert actual_ds.collect() == expected_ds.collect()
    
    
    print ("test_GetTotalCajas_NombresNulos OK")


def test_GetTotalCajas_ProductosDistintos(spark_session):
    # validar suma de productos distintos, los sume a la misma caja
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,100.0), 
            ("Caja1",'producto1', 2,50.0),
            ("Caja1",'producto1', 2,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    schemaResult = StructType([StructField('num_caja', StringType()),
                         StructField('Total', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("Caja1",300.0)
        ],schemaResult)

    assert actual_ds.collect() == expected_ds.collect()
    
    
    print ("test_GetTotalCajas_ProductosDistintos: OK")

def test_GetTotalCaja_EmptyDataset(spark_session):
    # Valida que la funcion funciona cuando llega un dataset vacio
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = []
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    

    assert actual_ds.count() == 0 
    
    print ("test_GetTotalCaja_EmptyDataset OK")


def test_GetTotalCajas_Order(spark_session):
    # validar el orden, debe devolver de mayor venta a menor, se usa p futuros calculos
    
    
    schema = StructType([StructField('num_caja', StringType()),
                         StructField('producto', StringType()),
                         StructField('cantidad', IntegerType()),
                          StructField('precio_unitario', FloatType())
                    ])
    
    data = [("Caja1",'producto1',1,20.0), 
            ("Caja2",'producto1', 3,50.0),
            ("Caja3",'producto1', 4,50.0)]
    
    df = spark_session.createDataFrame(data,schema)
    actual_ds = GetTotalCajas(df,spark_session)
    
    
    schemaResult = StructType([StructField('num_caja', StringType()),
                         StructField('Total', FloatType())])
        
    expected_ds = spark_session.createDataFrame(
        [
            ("Caja3",200.0),("Caja2",150.0),("Caja1",20.0)
        ],schemaResult)

    assert actual_ds.collect() == expected_ds.collect()
    
    
    print ("test_GetTotalCajas_Order OK")
