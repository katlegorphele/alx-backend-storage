#!/usr/bin/env python3

'''
script that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient

def main() -> None:
    '''
    Main function
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx

    print(f'{log_collection.count_documents({})} logs')
    print('Methods:')
    status_count: int = logs_collection.count_documents({"method": "GET",
                                                         "path": "/status"})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        method_count: int = logs_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {method_count}')
    print(f'{status_count} status check')

if __name__ == '__main__':
    main()
