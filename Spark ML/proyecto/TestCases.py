
    
def test_CalculateEventSeverity_NullValues(spark_session):
    wt_data = [(None,2, 'CO'), 
                          (3,4, 'CA')]
    wt_ds = spark_session.createDataFrame(wt_data,
                                              ['Type', 'Severity','State'])

    actual_ds = CalculateEventSeverity(wt_ds,spark_session)
    total = actual_ds.groupBy().agg(F.sum("EventSeverity")).collect()
    cred = total[0][0]
    assert  cred == 12
    print ("test_CalculateEventSeverity_NormalValues OK")

def test_CalculateEventSeverity_EmpyDF(spark_session):
    wt_data = []
    wt_ds = spark_session.createDataFrame(wt_data,
                                              ['Type', 'Severity','State'])

    actual_ds = CalculateEventSeverity(wt_ds,spark_session)
    qty = actual_ds.groupBy().agg(F.sum("EventSeverity")).count()
    assert  qty == 0
    print ("test_CalculateEventSeverity_EmpyDF OK")

def test_CalculateEventSeverity_NotValidValues(spark_session):
    wt_data = [("test",2, 'CO'), 
                          (3,"test", 'CA')]
    wt_ds = spark_session.createDataFrame(wt_data,
                                              ['Type', 'Severity','State'])

    actual_ds = CalculateEventSeverity(wt_ds,spark_session)
    total = actual_ds.groupBy().agg(F.sum("EventSeverity")).collect()
    cred = total[0][0]
    assert  cred == 0
    print ("test_CalculateEventSeverity_NormalValues OK")


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

 
    actual_ds = GetStatesDF(saas_ds,spark_session)

    expected_ds = spark_session.createDataFrame(
        [ ("CA"),("NJ")],"OrgState")
    
    assert actual_ds.collect() == expected_ds.collect()

    print ("test_GetStatesDF_DistinctStates OK")


def test_GetStatesDF_EmptyDF(spark_session):
    
    saas_data = []

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

 
    actual_ds = GetStatesDF(saas_ds,spark_session)

    expected_ds = spark_session.createDataFrame([],"OrgState")
    
    assert actual_ds.collect() == expected_ds.collect()

    print ("test_GetStatesDF_EmptyDF OK")


def test_GetStatesDF_NullStates(spark_session):
    
    saas_data = [(None, 'WI','O','I',1,0,0,0,0,0,'TEST',0,1,10,'2020-01-01',0), 
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

 
    actual_ds = GetStatesDF(saas_ds,spark_session)

    assert actual_ds.count() == 2

    print ("test_GetStatesDF_NullStates OK")

