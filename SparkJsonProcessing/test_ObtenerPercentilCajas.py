from funciones import *
import math
from pyspark.sql import functions as F
import  pyspark.sql.column
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
from pyspark.sql.functions import col, udf
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col

def test_ObtenerPercentilCajas_ListaVacia():
    # validar que valores nulos no afecte el canculo
    
    caja_list = []

    valor = ObtenerPercentilCajas(caja_list,25)

    #percintil si la lista es vacia =0
    assert valor == 0
    
    print ("test_ObtenerPercentilCajas_ListaVacia OK")
    
    
def test_ObtenerPercentilCajas_ValidPerc25(spark_session):
    # validar el primer percentil sea valido
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 50.0),
            ("caja3",75.0),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()


    valor = ObtenerPercentilCajas(caja_list,25)
    
    assert valor == 25.0
    
    print ("test_ObtenerPercentilCajas_ValidPerc25 OK")
    
    
def test_ObtenerPercentilCajas_ValidPerc50(spark_session):
        # validar el segundo percentil sea valido
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 50.0),
            ("caja3",75.0),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()


    valor = ObtenerPercentilCajas(caja_list,50)
    
    assert valor == 50.0
    
    print ("test_ObtenerPercentilCajas_ValidPerc50 OK")
    
    
def test_ObtenerPercentilCajas_ValidPerc75(spark_session):
        # validar el tercer percentil sea valido
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 50.0),
            ("caja3",75.0),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()


    valor = ObtenerPercentilCajas(caja_list,75)

    assert valor == 75.0
    
    print ("test_ObtenerPercentilCajas_ValidPerc75 OK")
    
def test_ObtenerPercentilCajas_NullValues(spark_session):
        # validar la funcion con valores nulos
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", None),
            ("caja2", None),
            ("caja3",None),
            ("caja4",None)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,75)
    
    assert valor == 0
    
    print ("test_ObtenerPercentilCajas_NullValues OK")
    

def test_ObtenerPercentilCajas_Perc25NullValues(spark_session):
        # validar si el primer lugar es nulo lo elimine y sea 50 el primer percentil
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", None),
            ("caja2", 50.0),
            ("caja3",75.0),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,25)
    assert valor == 50
    
    print ("test_ObtenerPercentilCajas_Perc25NullValues OK")

def test_ObtenerPercentilCajas_Perc50NullValues(spark_session):
        # validar si el primer lugar es nulo lo elimine y sea 50 el primer percentil
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", None),
            ("caja3",75.0),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,50)
    assert valor == 75
    
    print ("test_ObtenerPercentilCajas_Perc50NullValues OK")

def test_ObtenerPercentilCajas_Perc75NullValues(spark_session):
        # validar si el primer lugar es nulo lo elimine y sea 50 el primer percentil
    
    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 50.0),
            ("caja3",None),
            ("caja4",100.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,75)
    assert valor == 100
    
    print ("test_ObtenerPercentilCajas_Perc75NullValues OK")


def test_ObtenerPercentilCajas_Perc75UnSoloValor(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,75)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_Perc75UnSoloValor OK")


def test_ObtenerPercentilCajas_Perc50TodoIguales(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 25.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,75)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_Perc50TodoIguales OK")


def test_ObtenerPercentilCajas_Perc25TodoIguales(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 25.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,25)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_Perc25TodoIguales OK")


def test_ObtenerPercentilCajas_Perc50TodoIguales(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 25.0),
            ("caja2", 25.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,50)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_Perc50TodoIguales OK")


def test_ObtenerPercentilCajas_Perc25OrdenInverso(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 100.0),
            ("caja2", 75.0),
            ("caja3", 50.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,25)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_Perc25OrdenInverso OK")


def test_ObtenerPercentilCajas_NombresCajaNulo(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            (None, 100.0),
            (None, 75.0),
            (None, 50.0),
            (None, 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,25)
    
    assert valor == 25
    
    print ("test_ObtenerPercentilCajas_NombresCajaNulo OK")


def test_ObtenerPercentilCajas_TodoDatasetNulo(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            (None, None),
            (None, None),
            (None, None),
            (None, None)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,25)
    
    assert valor == 0
    
    print ("test_ObtenerPercentilCajas_TodoDatasetNulo OK")

def test_ObtenerPercentilCajas_PercentilMayor100(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 100.0),
            ("caja2", 75.0),
            ("caja3", 50.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,101)

    assert valor == 0
    
    print ("test_ObtenerPercentilCajas_TodoDatasetNulo OK")


def test_ObtenerPercentilCajas_PercentilNoValido(spark_session):

    schema = StructType([StructField('caja', StringType()),
                         StructField('total', FloatType())])
    
    expected_ds = spark_session.createDataFrame(
        [
            ("caja1", 100.0),
            ("caja2", 75.0),
            ("caja3", 50.0),
            ("caja3", 25.0)
        ],schema)

    
    caja_list = expected_ds.collect()

    valor = ObtenerPercentilCajas(caja_list,"test")

    assert valor == 0
    
    print ("test_ObtenerPercentilCajas_PercentilNoValido OK")
