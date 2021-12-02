import  pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, StructField, StructType,FloatType,DecimalType,BooleanType
from pyspark.sql.functions import isnan, when, count, col
from LoadFunciones import *



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


spark = SparkSession \
    .builder \
    .appName("Proyecto_WilliamFallas") \
    .config("spark.driver.extraClassPath", "postgresql-42.2.14.jar") \
    .config("spark.executor.extraClassPath", "postgresql-42.2.14.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

print("Process weather data---------------------------")
    #leer csv de eventos del tiempo
DF_Weather = ReadWeatherCsv(spark)
SaveDFPosgress(spark,DF_Weather,"Raw_WeatherDF")
DF_Weather = ProcessWeatherData(spark,DF_Weather)
print("Weather data processed OK!---------------------")

print("Process SAAS data---------------------------")
DF_SAAS = ReadSAASCsv(spark)
SaveDFPosgress(spark,DF_SAAS,"Raw_SAASDF")
print("SAAS data processed OK!---------------------")

print("join SAAS and weather --------------------------------------")
FinalDF = UnionSAASWeather(spark,DF_SAAS,DF_Weather,Final_Schema)

FinalDF= FinalDF.select(col("OrgState") ,col("DestState"),col("ShipmentDirection"),col("ServiceLevel"),
                        col("Priorityid"),col("TotalFreightCost"),col("MaxFreightClass"),col("Total_Pieces"),
                        col("Total_Pallets"),col("Total_Weight"),col("CarrierCode"),col("Has_Hazmat"),
                       col("Has_LiftGate"),col("is_Holiday"),col("PickUpDay"),col("PickUpMonth"),col("PickupDate"),
                       col("EventSeverity"),col("ConRetraso"))

print("join SAAS and weather processed OK!!! ---------------------")

#salvar resultado final en posgress
print("send to posgress: Final DF -------------------------------")
SaveDFPosgress(spark,FinalDF,"FinalDF")
print("Saved in posgress:FinalDF.. OK!---------------------------")



print("Ejemplo Dataframe final: Final DF -------------------------------")
#mostrar ejemplo de loq se guardo
examples_ds = FinalDF.select(col("CarrierCode") ,col("PickUpMonth"),col("EventSeverity"),col("OrgState"),col("DestState"),col("ConRetraso"))
examples_ds.show()



