#!/usr/bin/env python3
''' Function that returns all students sorted by average score
'''

def top_student(mongo_collection):
    ''' gets top student '''

    pipeline = [
        # project stage
        {"$project": {"name": "$name",
                      "averageScore": {"$avg": "$topics.score"}}},
        # sort stage
        {"$sort": {"averageScore": -1}}


    ]
    result = list(mongo_collection.aggregate(pipeline))

    return result
