# -*- coding: utf-8 -*-
from flask import request
from flask import Blueprint
from flask import Response
import json
from core.exceptions import BadRequestError
from core.exceptions import BadGateWayError
from service.companymodel import CompanyLink

page = Blueprint('page', __name__)


@page.route('/link', methods=['POST'])
def link():
    """
    Add a new user's page as link between the page
    and our system 
    """
    payload = request.json
    print("======= Entrante Link =========")
    print(payload)
    print("================================")
    try:
        userid = payload["user_id"]
        cmptoken = payload["company_token"]
        pageid = payload["page_id"]
        pagetoken = payload["page_token"]
    except ValueError:
        raise BadRequestError()
    cmplink = CompanyLink()
    try:
        link = cmplink.add_node(userid, cmptoken, pageid, pagetoken)
    except Exception as exc:
        print("Error de add")
        print(exc)
    if link:
        try:
            suscr = cmplink.suscribe_expandfeed(pageid, pagetoken)
        except Exception as exc:
            print("error en agregar feed")
            print(exc)
        print("Suscr")
        print(suscr)
        if suscr:
            return Response(json.dumps(link), status=201,
                            mimetype='application/json')
        else:
            # Something wrong happened
            print("BadGateWayError")
            raise BadGateWayError()


@page.route('/unlink', methods=['DELETE'])
def unlink():
    """
    Delete a user's page as link between the page
    and our system 
    """
    payload = request.json
    print("======= Entrante UnLink =========")
    print(payload)
    print("================================")
    try:
        pageid = payload["page_id"]
        pagetoken = payload["page_token"]
    except ValueError:
        raise BadRequestError()
    cmplink = CompanyLink()
    unsuscr = cmplink.unsuscribe_expandfeed(pageid, pagetoken)
    print("Unsuscr")
    print(unsuscr)
    if unsuscr:
        cmplink.del_node(pageid)
        return Response(json.dumps({"success": True}), status=200,
                        mimetype='application/json')
    else:
        # Something wrong happened
        print("BadGateWayError")
        raise BadGateWayError()

@page.route('/index', methods=['POST'])
def index():
    """
    Create the index
    """
    cmplink = CompanyLink()
    cmplink.create_index()
    return Response(json.dumps({"success": True}), status=201,
                    mimetype='application/json')
