import  pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType
import pyspark.sql.functions as func
from LoadFunciones import *


def test_CalculateEventSeverity_NormalValues(spark_session):
    wt_data = [(2,2, 'CO','2016-01-06 23:14:00'), (3,4, 'CA','2016-02-05 23:14:00')]
    wt_ds = spark_session.createDataFrame(wt_data,
                                              ['Type', 'Severity','State','StartTime'])

    actual_ds = CalculateEventSeverity(spark_session,wt_ds)
    total = actual_ds.groupBy().agg(F.sum("EventSeverity")).collect()
    cred = total[0][0]
    assert  cred == 16
    print ("test_CalculateEventSeverity_NormalValues OK")


    
def test_CalculateEventSeverity_NullValues(spark_session):
    wt_data = [(None,2, 'CO','2016-01-06 23:14:00'), 
                          (3,4, 'CA','2016-01-06 23:14:00')]
    wt_ds = spark_session.createDataFrame(wt_data,
                                              ['Type', 'Severity','State','StartTime'])

    actual_ds = CalculateEventSeverity(spark_session,wt_ds)
    total = actual_ds.groupBy().agg(F.sum("EventSeverity")).collect()
    cred = total[0][0]
    assert  cred == 12
    print ("test_CalculateEventSeverity_NormalValues OK")

def test_CalculateEventSeverity_EmpyDF(spark_session):


    schemaResult = StructType([StructField('Type', IntegerType()),
                         StructField('Severity', IntegerType()),
                         StructField('State', StringType()),
                         StructField('StartTime', StringType())])
        

    wt_data = []
    wt_ds = spark_session.createDataFrame(wt_data,schemaResult)

    actual_ds = CalculateEventSeverity(spark_session,wt_ds)
    total = actual_ds.groupBy().agg(F.sum("EventSeverity")).collect()
    event = total[0][0]
    assert  event == None
    print ("test_CalculateEventSeverity_EmpyDF OK")

def test_GetStatesDF_DistinctStates(spark_session):
    
    saas_data = [('CA', 'WI','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-01',0), 
                ('NJ', 'TX','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-02',0)]

    saas_ds = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"]) 

 
    actual_ds = GetStatesDF(spark_session,saas_ds)

    assert actual_ds.count() == 2

    print ("test_GetStatesDF_DistinctStates OK")

def test_GetStatesDF_EmptyDF(spark_session):
    
    saas_data = []

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


    saas_ds = spark_session.createDataFrame(saas_data,SAAS_Schema) 

 
    actual_ds = GetStatesDF(spark_session,saas_ds)

    result_Schema = StructType([StructField("OrgState", StringType())])
    expected_ds = spark_session.createDataFrame([],result_Schema)
    
    assert actual_ds.collect() == expected_ds.collect()

    print ("test_GetStatesDF_EmptyDF OK")


def test_GetStatesDF_SameStates(spark_session):
    
    saas_data = [('CA', 'WI','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-01',0), 
                ('CA', 'TX','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-02',0)]

    saas_ds = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"]) 

 
    actual_ds = GetStatesDF(spark_session,saas_ds)

    assert actual_ds.count() == 1

    print ("test_GetStatesDF_SameStates OK")


def test_Join_Frames_NormalInnerJoin(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = [(1,"Name1"), (2,"name2")]
    Df_Left = spark_session.createDataFrame(left_data,
                                              ['id', 'name'])
    
    right_data = [(1, 'job1'), (2, 'job2')]
    Df_Rigth = spark_session.createDataFrame(right_data,
                                               ['idPersona', 'job'])
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"inner",result_Schema)
    
    assert actual_ds.count() == 2
    print ("test_Join_Frames_NormalInnerJoin OK")


def test_Join_Frames_LeftJoin(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = [(1,"Name1"), (2,"name2")]
    Df_Left = spark_session.createDataFrame(left_data,
                                              ['id', 'name'])
    
    right_data = [(4, 'job1'), (5, 'job2')]
    Df_Rigth = spark_session.createDataFrame(right_data,
                                               ['idPersona', 'job'])
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"left_outer",result_Schema)
    
    
    assert actual_ds.count() == 2
    print ("test_Join_Frames_LeftJoin OK")


def test_Join_Frames_LeftEmpyJoin(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = []
    left_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType())
                ])
    Df_Left = spark_session.createDataFrame(left_data,left_Schema)
    
    right_data = [(4, 'job1'), (5, 'job2')]
    Df_Rigth = spark_session.createDataFrame(right_data,
                                               ['idPersona', 'job'])
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"left_outer",result_Schema)
    
    actual_ds.show()
    assert actual_ds.count() == 0
    print ("test_Join_Frames_LeftEmpyJoin OK")

def test_Join_Frames_RightEmpyJoin(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = [(1,"Name1"), (2,"name2")]
    left_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType())
                ])
    Df_Left = spark_session.createDataFrame(left_data,left_Schema)
    
    right_data = []
    right_Schema = StructType([
                StructField("idPersona", IntegerType()),
                StructField("job", StringType())
                ])
    Df_Rigth = spark_session.createDataFrame(right_data,right_Schema)
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"left_outer",result_Schema)
    
    assert actual_ds.count() == 2
    print ("test_Join_Frames_RightEmpyJoin OK")

def test_Join_Frames_TwoEmpyJoin(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = []
    left_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType())
                ])
    Df_Left = spark_session.createDataFrame(left_data,left_Schema)
    
    right_data = []
    right_Schema = StructType([
                StructField("idPersona", IntegerType()),
                StructField("job", StringType())
                ])
    Df_Rigth = spark_session.createDataFrame(right_data,right_Schema)
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"left_outer",result_Schema)
    
    assert actual_ds.count() == 0
    print ("test_Join_Frames_TwoEmpyJoin OK")

def test_Join_Frames_InnerJoinEmptyFrame(spark_session):
    
    
    result_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType()),
                StructField("idPersona", IntegerType()),
                StructField("job", StringType()),
                ])


    left_data = [(1,"Name1"), (2,"name2")]
    left_Schema = StructType([
                StructField("id", IntegerType()),
                StructField("name", StringType())
                ])
    Df_Left = spark_session.createDataFrame(left_data,left_Schema)
    
    right_data = []
    right_Schema = StructType([
                StructField("idPersona", IntegerType()),
                StructField("job", StringType())
                ])
    Df_Rigth = spark_session.createDataFrame(right_data,right_Schema)
    
    where =  Df_Left.id==Df_Rigth.idPersona
    
    actual_ds = Join_Frames(Df_Left,Df_Rigth,where,spark_session,"inner",result_Schema)
    
    assert actual_ds.count() == 0
    print ("test_Join_Frames_InnerJoinEmptyFrame OK")


def test_CalculateEventSeverity_normal(spark_session):
    
    Data = [(1,2,"2016-01-06 23:14:00","CA"), (1,4,"2016-01-06 23:14:00","CA")]
    schema = StructType([
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("State", StringType())])
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = CalculateEventSeverity(spark_session,Df_weather)
    
    
    result_Schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    ResultData = [(2.0,"CA","2016-01-06"), (4.0,"CA","2016-01-06")]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_CalculateEventSeverity_normal OK")



def test_CalculateEventSeverity_Nullvalue(spark_session):
    
    Data = [(None,2,"2016-01-06 23:14:00","CA"), (1,None,"2016-01-06 23:14:00","CA")]
    schema = StructType([
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("State", StringType())])
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = CalculateEventSeverity(spark_session,Df_weather)
    
    
    result_Schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    ResultData = [(None,"CA","2016-01-06"), (None,"CA","2016-01-06")]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_CalculateEventSeverity_Nullvalue OK")
    

def test_CalculateEventSeverity_RemoveBlankSpacesState(spark_session):
    
    Data = [(1,2,"2016-01-06 23:14:00","CA  "), (1,2,"2016-01-06 23:14:00","CA  ")]
    schema = StructType([
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("State", StringType())])
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = CalculateEventSeverity(spark_session,Df_weather)
    
    
    result_Schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    ResultData = [(2.0,"CA","2016-01-06"), (2.0,"CA","2016-01-06")]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_CalculateEventSeverity_RemoveBlankSpacesState OK")

def test_GetSummarizeWeatherInfo_NormalData(spark_session):
    
    Data = [(2.0,"CA","2016-01-06"), (2.0,"CA","2016-01-06")]
    schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = GetSummarizeWeatherInfo(spark_session,Df_weather)
    
    result_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    ResultData = [("CA","2016-01-06",4.0)]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_GetSummarizeWeatherInfo_NormalData OK")
    
def test_GetSummarizeWeatherInfo_NullData(spark_session):
    
    Data = [(2.0,"CA","2016-01-06"), (None,"CA","2016-01-06")]
    schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = GetSummarizeWeatherInfo(spark_session,Df_weather)
    
    
    result_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    ResultData = [("CA","2016-01-06",2.0)]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_GetSummarizeWeatherInfo_NullData OK")


def test_GetSummarizeWeatherInfo_EmptyFrame(spark_session):
    
    Data = []
    schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = GetSummarizeWeatherInfo(spark_session,Df_weather)
    
    
    result_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    ResultData = []

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.collect() == Df_expected.collect()
    print ("test_GetSummarizeWeatherInfo_EmptyFrame OK")


def test_GetSummarizeWeatherInfo_DistinctStates(spark_session):
    
    Data = [(2.0,"CA","2016-01-06"), (2.0,"NJ","2016-01-06")]
    schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = GetSummarizeWeatherInfo(spark_session,Df_weather)
    

    result_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    ResultData = [("NJ","2016-01-06",2.0),("CA","2016-01-06",2.0)]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.count() == 2
    print ("test_GetSummarizeWeatherInfo_DistinctStates OK")


def test_GetSummarizeWeatherInfo_DistinctDates(spark_session):
    
    Data = [(2.0,"CA","2016-01-06"), (2.0,"NJ","2016-01-06")]
    schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = GetSummarizeWeatherInfo(spark_session,Df_weather)
    

    result_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    ResultData = [("CA","2016-01-06",2.0),("CA","2016-01-07",2.0)]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)

    assert actual_ds.count() == 2
    print ("test_GetSummarizeWeatherInfo_DistinctDates OK")
    

def test_UnionSAASWeather_Normal(spark_session):
    
    
    Final_Schema = StructType([
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
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
                StructField("EventSeverity", IntegerType()),
                StructField("ConRetraso", IntegerType())
                ])

    weather_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    WeatherData = [("CA","2016-01-06",2.0),("CA","2016-01-07",2.0)]
    
    Df_weather = spark_session.createDataFrame(WeatherData,weather_Schema)
    
    
    
    saas_data = [('CA', 'WI ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-01',0), 
                ('CA', 'TX ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-02',0)]
    Df_SAAS = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"])
    
    
    
    final_ds = UnionSAASWeather(spark_session,Df_SAAS,Df_weather,Final_Schema)
    

    assert final_ds.count() == 2
    print ("test_UnionSAASWeather_Normal OK")

def test_UnionSAASWeather_EmptyWeatherData(spark_session):
    
    
    Final_Schema = StructType([
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
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
                StructField("EventSeverity", IntegerType()),
                StructField("ConRetraso", IntegerType())
                ])

    weather_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    WeatherData = []
    
    Df_weather = spark_session.createDataFrame(WeatherData,weather_Schema)
    
    
    
    saas_data = [('CA', 'WI ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-01',0), 
                ('CA', 'TX ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-02',0)]
    Df_SAAS = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"])
    
    
    
    final_ds = UnionSAASWeather(spark_session,Df_SAAS,Df_weather,Final_Schema)
    

    assert final_ds.count() == 2
    print ("test_UnionSAASWeather_EmptyWeatherData OK")


def test_UnionSAASWeather_ValidateEventSum(spark_session):
    
    
    Final_Schema = StructType([
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
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
                StructField("EventSeverity", IntegerType()),
                StructField("ConRetraso", IntegerType())
                ])

    weather_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    WeatherData = [("CA","2016-01-06",2.0),("CA","2016-01-07",3.0)]
    
    Df_weather = spark_session.createDataFrame(WeatherData,weather_Schema)
    
    
    
    saas_data = [('CA', 'WI ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-06',0), 
                ('CA', 'TX ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-07',0)]
    Df_SAAS = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"])

    
    final_ds = UnionSAASWeather(spark_session,Df_SAAS,Df_weather,Final_Schema)
    
    final_ds = final_ds.select(col("EventSeverity"), col("FormatDate"))
    
    result_Schema = StructType([
               
                 StructField("EventSeverity", FloatType()),
                StructField("FormatDate", StringType())])
    ResultData = [(2.0,"2016-01-06"),(3.0,"2016-01-07")]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)
    
    assert final_ds.collect() == Df_expected.collect()
    print ("test_UnionSAASWeather_ValidateEventSum OK")

def test_UnionSAASWeather_NotEventinDate(spark_session):
    
    
    Final_Schema = StructType([
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
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
                StructField("EventSeverity", IntegerType()),
                StructField("ConRetraso", IntegerType())
                ])

    weather_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    WeatherData = [("CA","2016-01-06",2.0),("CA","2016-01-07",3.0)]
    
    Df_weather = spark_session.createDataFrame(WeatherData,weather_Schema)
    
    
    
    saas_data = [('CA', 'WI ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-12',0), 
                ('CA', 'TX ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-14',0)]
    Df_SAAS = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"])

    
    final_ds = UnionSAASWeather(spark_session,Df_SAAS,Df_weather,Final_Schema)
    
    final_ds = final_ds.select(col("OrgState"),col("EventSeverity"), col("FormatDate"))
    
    result_Schema = StructType([
                    StructField("OrgState", StringType()),
                 StructField("EventSeverity", FloatType()),
                StructField("FormatDate", StringType())])
    ResultData = [('CA',None,None),('CA',None,None)]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)
    
    assert final_ds.collect() == Df_expected.collect()
    print ("test_UnionSAASWeather_NotEventinDate OK")


def test_UnionSAASWeather_ValidSumSameDateState(spark_session):
    
    
    Final_Schema = StructType([
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
                StructField("PickUpDay", IntegerType()),
                StructField("PickUpMonth", IntegerType()),
                StructField("PickupDate", StringType()),
                StructField("EventSeverity", IntegerType()),
                StructField("ConRetraso", IntegerType())
                ])

    weather_Schema = StructType([
               
                StructField("State", StringType()),
                StructField("FormatDate", StringType()),
                 StructField("EventSeverity", FloatType()),])
    WeatherData = [("CA","2016-01-06",2.0),("CA","2016-01-06",3.0)]
    
    Df_weather = spark_session.createDataFrame(WeatherData,weather_Schema)
    
    
    
    saas_data = [('CA', 'WI ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-06',0), 
                ('CA', 'TX ','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2016-01-06',0)]
    Df_SAAS = spark_session.createDataFrame(saas_data,["OrgState",
                "DestState",
                "ShipmentDirection",
                "ServiceLevel",
                "Priorityid", 
                "TotalFreightCost",
                "MaxFreightClass", 
                "Total_Pieces", 
                "Total_Pallets", 
                "Total_Weight", 
                "CarrierCode", 
                "Has_Hazmat",
                "PickUpDay", 
                "PickUpMonth", 
                "PickupDate",  
                "ConRetraso"])

    
    final_ds = UnionSAASWeather(spark_session,Df_SAAS,Df_weather,Final_Schema)
    
    final_ds = final_ds.select(col("OrgState"),col("EventSeverity"), col("FormatDate"))
    result_Schema = StructType([
                    StructField("OrgState", StringType()),
                 StructField("EventSeverity", FloatType()),
                StructField("FormatDate", StringType())])
    ResultData = [('CA',5.0,'2016-01-06'),('CA',5.0,'2016-01-06')]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)
    
    assert final_ds.collect() == Df_expected.collect()
    print ("test_UnionSAASWeather_ValidSumSameDateState OK")



def test_ProcessWeatherData_ValidateEventSeverity(spark_session):
    
    Data = [("1","Snow","Light","2016-01-06 10:14:00","2016-01-06 23:14:00","CA"), 
            ("2","Fog","Severe","2016-01-07 10:14:00","2016-01-07 23:14:00","NJ")]
    schema = StructType([
                StructField("EventId", StringType()),
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("EndTime", StringType()),
                StructField("State", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = ProcessWeatherData(spark_session,Df_weather)
    
    result_Schema = StructType([
                StructField("EventSeverity", FloatType()),
                StructField("State", StringType()),
                StructField("FormatDate", StringType())])
    
    ResultData = [(5.0,"2016-01-06","CA"),(8.0,"2016-01-07","NJ")]

    Df_expected = spark_session.createDataFrame(ResultData,result_Schema)
    
    total = actual_ds.select(F.sum("EventSeverity")).collect()[0][0]
    
    assert total == 15.0
    print ("test_ProcessWeatherData_ValidateEventSeverity OK")


def test_ProcessWeatherData_EmptyDataframe(spark_session):
    
    Data = []
    schema = StructType([
                StructField("EventId", StringType()),
                StructField("Type", StringType()),
                StructField("Severity", StringType()),
                StructField("StartTime", StringType()),
                StructField("EndTime", StringType()),
                StructField("State", StringType())])
    
    Df_weather = spark_session.createDataFrame(Data,schema)
    
    
    actual_ds = ProcessWeatherData(spark_session,Df_weather)
    

    assert actual_ds.count() == 0
    print ("test_ProcessWeatherData_EmptyDataframe OK")





