#!/usr/bin/env python3

'''
List all docs in python
'''

from typing import List

def list_all(mongo_collection) -> List:
    ''' list all docs in collection '''
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
