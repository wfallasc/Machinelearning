from funciones import *

from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col



def test_ObtenerProdMayorMontoVentas_ValidMayor(spark_session):
    # validar que obtenga el prod de mayor venta
    
    
    schema = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod3", 3,18.0),
            ("Prod2", 2,8.0),
            ("Prod1",1,2.0)
        ],schema)

    
    prod_list = expected_ds.collect()
    
    prod = ObtenerProdMayorMontoVentas(prod_list)
    
    #valida que el de mayor cantidad de venta sea Prod3
    assert prod[0] == "Prod3"
    
    print ("test_ObtenerProdMayorMontoVentas_ValidMayor OK")


def test_ObtenerProdMayorMontoVentas_Todos0(spark_session):
    # todas las cantidades iguales en 0, debe retornar 0
    
    
    schema = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod3", 0,18.0),
            ("Prod2", 0,8.0),
            ("Prod1",0,2.0)
        ],schema)

    
    prod_list = expected_ds.collect()

    
    prod = ObtenerProdMayorMontoVentas(prod_list)

    #valida que el de mayor cantidad de venta sea Prod3
    assert prod[1] == 0
    
    print ("test_ObtenerProdMayorMontoVentas_Todos0 OK")


def test_ObtenerProdMayorMontoVentas_Nulos(spark_session):
    # validar que valores nulos no afecte el canculo
    
    
    schema = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod3", 3,18.0),
            ("Prod2", 2,8.0),
            ("Prod1",None,2.0)
        ],schema)

    
    prod_list = expected_ds.collect()


    prod = ObtenerProdMayorMontoVentas(prod_list)
    
    #valida que el de mayor cantidad de venta sea Prod3
    assert prod[0] == "Prod3"
    
    print ("test_ObtenerProdMayorMontoVentas_Nulos OK")

def test_ObtenerProdMayorMontoVentas_NombreNulos(spark_session):
    # validar que valores nulos no afecte el canculo
    
    
    schema = StructType([StructField('producto', StringType()),
                         StructField('sum(cantidad)', IntegerType()),
                         StructField('sum(Subtotal)', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("Prod3", 3,18.0),
            ("Prod2", 2,8.0),
            (None,1,2.0)
        ],schema)

    
    prod_list = expected_ds.collect()


    prod = ObtenerProdMayorMontoVentas(prod_list)
    
    #valida que el de mayor cantidad de venta sea Prod3
    assert prod[0] == "Prod3"
    
    print ("test_ObtenerProdMayorMontoVentas_NombreNulos OK")


def test_ObtenerProdMayorMontoVentas_ListaVacia(spark_session):
    # validar que valores nulos no afecte el canculo
    

    prod_list = []


    prod = ObtenerProdMayorMontoVentas(prod_list)

    #valida que el de mayor cantidad de venta sea Prod3
    assert prod[0] == ""
    
    print ("test_ObtenerProdMayorMontoVentas_ListaVacia OK")
    
