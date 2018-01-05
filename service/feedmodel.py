# -*- coding: utf-8 -*-
from cloudant import cloudant


USERNAME = ''
PASSWORD = ''
URL = ''

class FacebookFeed():

    @classmethod
    def add_document(cls, dbname, document):
        """
        Create a new document where

        :param str dbname: The database name to insert the new document
        :param json document: Document with feed info
        """
        with cloudant(USERNAME, PASSWORD, url=URL) as client:
            my_database = client[dbname]
            my_document = my_database.create_document(document)
            document["_id"] = my_document["_id"]
        return document
