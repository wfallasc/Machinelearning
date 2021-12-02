import  pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType,DecimalType,BooleanType
from pyspark.sql.functions import isnan, when, count, col






def ProcessWeatherData(spark,DT_Weather):
    #cambiar columna type a numerico
    DT_Weather = EncodeTypeColumn(spark,DT_Weather)

    #cambiar severity serverity a numerico
    DT_Weather = EncodeSeverity(spark,DT_Weather)

    #combine type and serverity in single column
    DT_Weather= CalculateEventSeverity(spark,DT_Weather)

    return DT_Weather

def ReadWeatherCsv(spark):
    WeatherSchema = StructType([
                StructField("EventId", StringType()),
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("EndTime", StringType()),
                StructField("TimeZone", StringType()),
                StructField("AirportCode", StringType()),
                StructField("LocationLat", StringType()),
                StructField("LocationLng", StringType()),
                StructField("City", StringType()),
                StructField("County", StringType()),
                StructField("State", StringType()),
                StructField("ZipCode", StringType())])

    Weather_Path= "US_WeatherEvents_2016-2019.csv"

    weather_df = spark.read.format("csv").option("path", Weather_Path).option("header", True).schema(WeatherSchema).load()

    #remover columnas no necesarias
    weather_df = weather_df.select(col("Type"),col("Severity"),col("StartTime"),col("State"))

    return weather_df

def EncodeTypeColumn(spark,weather_df):
    weather_df = weather_df.withColumn('Type', translate('Type', 'Cold', '0'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Fog', '2'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Precipitation', '3'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Rain', '3'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Hail', '4'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Storm', '5'))
    weather_df = weather_df.withColumn('Type', translate('Type', 'Snow', '6'))

    return weather_df

def EncodeSeverity(spark,weather_df):
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'Other', '0'))
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'UNK', '0'))
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'Light', '1'))
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'Moderate', '1'))
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'Heavy', '3'))
    weather_df = weather_df.withColumn('Severity', translate('Severity', 'Severe', '5'))

    return weather_df

def CalculateEventSeverity(spark,weather_df):
    weather_df = weather_df.withColumn("EventSeverity",
                                        col("Severity") *  col("Type"))

    weather_df= weather_df.withColumn('FormatDate', col("StartTime").substr(1, 10))
    weather_df = weather_df.withColumn("State", trim(weather_df.State))
    weather_df = weather_df.select(col("EventSeverity"),col("State"),col("FormatDate"))

    return weather_df




def ReadSAASCsv(spark):

    SAAS_Schema = StructType([
                StructField("OrgState", StringType()),
                StructField("DestState", StringType()),
                StructField("ShipmentDirection", StringType()),
                StructField("ServiceLevel", StringType()),
                StructField("Priorityid", IntegerType()),
                StructField("TotalFreightCost", DecimalType()),
                StructField("MaxFreightClass", StringType()),
                StructField("Total_Pieces", DecimalType()),
                StructField("Total_Pallets", DecimalType()),
                StructField("Total_Weight", StringType()),
    
                StructField("CarrierCode", StringType()),
                StructField("Has_Hazmat", IntegerType()),
                StructField("Has_LiftGate", IntegerType()),
                StructField("is_Holiday", IntegerType()),
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
  
                StructField("ConRetraso", IntegerType())
                ])  

    SAAS_Path= "saas.csv"

    SAAS_df = spark.read.format("csv").option("path", SAAS_Path).option("header", False).schema(SAAS_Schema).load()

    #trim columns
    SAAS_df = SAAS_df.withColumn("OrgState", trim(SAAS_df.OrgState))
    SAAS_df = SAAS_df.withColumn("DestState", trim(SAAS_df.DestState))

    return SAAS_df


def GetStatesDF(spark,SAAS_df):
    
    SAAS_States =SAAS_df.select("OrgState").distinct()

    return SAAS_States


def Join_Frames(Df_Left,Df_Rigth,where,spark,joinType,Final_Schema):
    #"""Return the spark dataframe wit the join.""
  
    if not(isinstance(where, pyspark.sql.column.Column)) :
        print("No valid where parameter")
        return spark.createDataFrame([], Final_Schema)
    
    if not(isinstance(Df_Left, pyspark.sql.dataframe.DataFrame)) :
        print("No valid Df_Left parameter")
        return spark.createDataFrame([], Final_Schema)
    
    if not(isinstance(Df_Rigth, pyspark.sql.dataframe.DataFrame)) :
        print("No valid Df_Rigth parameter")
        return spark.createDataFrame([], Final_Schema)
    
    df = Df_Left.join(Df_Rigth, where, joinType)
    
    return df


def GetSummarizeWeatherInfo(spark,joint_df):
    #Summariza por dia y devuelve solo las columnas necesarias
    Df_SumEventos = joint_df.groupBy("State","FormatDate").sum("EventSeverity")

    Df_SumEventos = Df_SumEventos.select(col("State"), col("FormatDate"),col("sum(EventSeverity)").alias("EventSeverity"))

    return Df_SumEventos



    
def UnionSAASWeather(spark,DF_SAAS,DF_Weather,Final_Schema):

    #get the distinct states from SAAS
    Df_states= GetStatesDF(spark,DF_SAAS)

    #hacer inner join con los estados que viene en SAAS, tiene el efecto de reducir el DF gigante de eventos del tiempo
    #trayendose solo los estados que estan SAAS
    where =  (Df_states.OrgState == DF_Weather.State) 
    joint_df=Join_Frames(DF_Weather,Df_states,where,spark,"inner",Final_Schema)

    #sumarizar eventos por dia y estado
    Df_SumEventos=GetSummarizeWeatherInfo(spark,joint_df)

    #finalmente hacer left join del dataset saas con el dataset del tiempo
    where =  ((DF_SAAS.OrgState == Df_SumEventos.State) & (DF_SAAS.PickupDate == Df_SumEventos.FormatDate))

    DT_Final=Join_Frames(DF_SAAS,Df_SumEventos,where,spark,"left_outer",Final_Schema)

    return DT_Final


def SaveDFPosgress(spark,DF,TableName):

    Properties = {
        "user": "postgres",
        "password": "testPassword",
        "driver": "org.postgresql.Driver"
    }

    print("Begin write on table")

    db_url="jdbc:postgresql://host.docker.internal:5433/postgres"
    DF.write.jdbc(url=db_url,table=TableName,mode='overwrite',properties=Properties)

    print(" write on table OK!!!")

    return True

