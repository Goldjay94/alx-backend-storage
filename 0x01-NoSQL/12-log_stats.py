#!/usr/bin/env python3
""" A Python module tha provides stats about nginx """
from pymongo import MongoClient


def main():
    """Python script that provides some stats about
    Nginx logs stored in MongoDB
    Database: logs
    Collection: nginx

    Display (same as the example):
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
    (see example below - warning: it’s a tabulation before each line)

    one line with the number of documents with:
        method=GET
        path=/status"""

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    print(f"{nginx.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"""\tmethod {method}: {nginx.count_documents(
                {"method": method})}"""
              )
    print(f"""{nginx.count_documents({
            "method": "GET", "path": "/status"})} status check"""
          )


if __name__ == "__main__":
    main()
