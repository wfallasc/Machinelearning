from funciones import *

from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col



def test_ObtenerCajasMayorMontoVentas_ValidMayor(spark_session):
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
    
    caja = ObtenerCajasMayorMontoVentas(cajas_list)
    
    #valida que el de mayor cantidad de venta sea Caja1
    assert caja[0] == "Caja1"
    
    print ("test_ObtenerCajasMayorMontoVentas_ValidMayor OK")


def test_ObtenerCajasMayorMontoVentas_Todos0(spark_session):
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

    
    caja = ObtenerCajasMayorMontoVentas(caja_list)

    #valida que el de mayor cantidad sea 0
    assert caja[1] == 0
    
    print ("test_ObtenerCajasMayorMontoVentas_Todos0 OK")


def test_ObtenerCajasMayorMontoVentas_Nulos(spark_session):
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


    caja = ObtenerCajasMayorMontoVentas(cajas_list)
    
    #valida que el de mayor cantidad de venta sea caja1
    assert caja[0] == "caja1"
    
    print ("test_ObtenerCajasMayorMontoVentas_Nulos OK")

def test_ObtenerCajasMayorMontoVentas_NombreNulos(spark_session):
    # validar que valores nulos no afecte el canculo
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 18.0),
            ("caja2", 8.0),
            (None,2.0)
        ],schema)

    
    caja_list = expected_ds.collect()


    caja = ObtenerCajasMayorMontoVentas(caja_list)
    
    #valida que el de mayor cantidad de venta sea caja1
    assert caja[0] == "caja1"
    
    print ("test_ObtenerCajasMayorMontoVentas_NombreNulos OK")


def test_ObtenerCajasMayorMontoVentas_ListaVacia(spark_session):
    # validar que valores nulos no afecte el canculo
    
    caja_list = []

    caja = ObtenerCajasMayorMontoVentas(caja_list)

    #valida que el de mayor cantidad de venta sea Prod3
    assert caja[0] == ""
    
    print ("test_ObtenerCajasMayorMontoVentas_ListaVacia OK")



