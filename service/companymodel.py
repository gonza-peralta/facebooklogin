# -*- coding: utf-8 -*-
from cloudant import cloudant
from cloudant.query import Query
from cloudant.database import CloudantDatabase
import requests
import json

DBNAME = 'companies'
USERNAME = 'd01f3799-f0f2-47fe-a6ee-cfc970f42a63-bluemix'
PASSWORD = 'eefcb0f5a3b7775e96c59d0bd3bec69ff32ee13a83e957538859c79fa1127eb0'
URL = 'https://d01f3799-f0f2-47fe-a6ee-cfc970f42a63-bluemix:eefcb0f5a3b7775e'\
    '96c59d0bd3bec69ff32ee13a83e957538859c79fa1127eb0@d01f3799-f0f2-47fe-a6ee'\
    '-cfc970f42a63-bluemix.cloudant.com'
SUSCRURL = "https://graph.facebook.com/v2.11/{0}/"\
    "subscribed_apps?access_token={1}"

class CompanyLink():

    @classmethod
    def add_node(cls, user_id, cmp_token, page_id, page_token):
        """
        Create a new document where

        :param str user_id: User's facebook id
        :param str cmp_token: Token that represent the installation 
        :param str page_id: page id to link feeds
        :param str page_token: page valid token
        """
        document = cls.getcompanytoken(page_id)
        if document is None:
            node = {"user_id": user_id,
                    "dbname": cmp_token,
                    "page_id": page_id,
                    "page_token": page_token}
            with cloudant(USERNAME, PASSWORD, url=URL) as client:
                my_database = client[DBNAME]
                my_document = my_database.create_document(node)
                node["_id"] = my_document["_id"]
        else:
            with cloudant(USERNAME, PASSWORD, url=URL) as client:
                my_database = client[DBNAME]
                node = my_database[document["_id"]]
                node["user_id"] = user_id
                node["dbname"] = cmp_token
                node["page_token"] = page_token
                node.save()

        return node
    
    @classmethod
    def del_node(cls, page_id):
        """
        Delete a node with page_id
        """
        document = cls.getcompanytoken(page_id)
        if document is not None:
            with cloudant(USERNAME, PASSWORD, url=URL) as client:
                database = client[DBNAME]
                todelete = database[document["_id"]]
                todelete.delete()
        
    @classmethod
    def getcompanytoken(cls, page_id):
        """
        Get the document that represent the facebook page.
        If not exists return None
        """
        with cloudant(USERNAME, PASSWORD, url=URL) as client:
            database = client[DBNAME]
            query = Query(database,
                          selector={"page_id": {"$eq": page_id}})
            for node in query(limit=1)['docs']:
                return node
        return None

    @classmethod
    def create_index(cls):
        """
        Create an Indexs for the "page_id" attribute
        """
        with cloudant(USERNAME, PASSWORD, url=URL) as client:
            clouddb = CloudantDatabase(client, DBNAME)
            clouddb.create_query_index(index_name='pageid-index',
                                       index_type='text',
                                       fields=[{"name": "page_id",
                                                "type": "string"}])

    @classmethod
    def suscribe_expandfeed(cls, page_id, page_token):
        """
        Suscribe the users page to Expand Feed
        """
        suscrurl = SUSCRURL.format(page_id, page_token)
        
        result = requests.post(suscrurl, verify=False)
        print("suscribe_expandfeed")
        print("page_id -> " + page_id)
        print(result.status_code)
        print(result.content)
        if result.status_code == 200:
            response = json.loads(result.content)
            return response["success"]
        return False
    
        
    @classmethod
    def unsuscribe_expandfeed(cls, page_id, page_token):
        """
        Unsuscribe the users page to Expand Feed
        """
        suscrurl = SUSCRURL.format(page_id, page_token)
        
        result = requests.delete(suscrurl, verify=False)
        print("unsuscribe_expandfeed")
        print("page_id -> " + page_id)
        print(result.status_code)
        print(result.content)
        if result.status_code == 200:
            response = json.loads(result.content)
            return response["success"]
        return False


