from funciones import *

from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col

def test_ObtenerCajasMenosMontoVentas_ValidMenor(spark_session):
    # validar que obtenga el prod de mayor venta
    
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Caja1",18.0),
            ("Caja2",8.0),
            ("Caja3",2.0)
        ],schema)

    
    cajas_list = expected_ds.collect()
    
    caja = ObtenerCajasMenosMontoVentas(cajas_list)
    
    #valida que el de mayor cantidad de venta sea Caja1
    assert caja[0] == "Caja3"
    
    print ("test_ObtenerCajasMenosMontoVentas_ValidMenor OK")


def test_ObtenerCajasMenosMontoVentas_Todos0(spark_session):
    # todas las cantidades iguales en 0, debe retornar 0
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Caja1",0.0),
            ("Caja2",0.0),
            ("Caja3",0.0)
        ],schema)


    
    caja_list = expected_ds.collect()

    
    caja = ObtenerCajasMenosMontoVentas(caja_list)

    #valida que la menor cantidad sea 0
    assert caja[1] == 0
    
    print ("test_ObtenerCajasMenosMontoVentas_Todos0 OK")


def test_ObtenerCajasMenosMontoVentas_Nulos(spark_session):
    # validar que valores nulos no afecte el canculo
    
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1",18.0),
            ("caja2",8.0),
            ("caja3",None)
        ],schema)

    
    cajas_list = expected_ds.collect()


    caja = ObtenerCajasMenosMontoVentas(cajas_list)
    

    #valida que el de menor cantidad, deberia ser el q tiene el valor en null
    assert caja[0] == "caja3"
    
    print ("test_ObtenerCajasMenosMontoVentas_Nulos OK")

def test_ObtenerCajasMenosMontoVentas_NombreNulos(spark_session):
    # validar que valores nulos no afecte el canculo
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 18.0),
            ("caja2", 6.0),
            (None,4.0)
        ],schema)

    
    caja_list = expected_ds.collect()


    caja = ObtenerCajasMenosMontoVentas(caja_list)
    
    
    #valida que el de menor cantidad de venta sea la nula
    assert caja[0] == None
    
    print ("test_ObtenerCajasMenosMontoVentas_NombreNulos OK")


def test_ObtenerCajasMenosMontoVentass_ListaVacia(spark_session):
    # validar que valores nulos no afecte el canculo
    
    caja_list = []

    caja = ObtenerCajasMenosMontoVentas(caja_list)

    #valida que el de mayor cantidad de venta sea Prod3
    assert caja[0] == ""
    
    print ("test_ObtenerCajasMenosMontoVentass_ListaVacia OK")
    