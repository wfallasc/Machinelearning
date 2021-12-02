from funciones import *
import os
import json
import inspect, os.path

def test_ProcessJsonFileEmptyDirectory():
    
    my_emptyResult = ProcessJsonFile('')
    
    assert len(my_emptyResult) == 0
    print ("test_ProcessJsonFileEmptyDirectory OK")


def test_ProcessJsonNotValidDirectory():
    
    my_emptyResult = ProcessJsonFile('test')
    
    assert len(my_emptyResult) == 0
    print ("test_ProcessJsonNotValidDirectory OK")