#!/usr/bin/env python3
'''
Function that insers a new doc in collection
'''
from typing import List

def insert_school(mongo_collection, **kwargs) -> str:
    ''' inserts new doc in collection '''
    new_school: Dict[Any, Any] = mongo_collection.insert_one(kwargs)
    return new_school.inserted_id
