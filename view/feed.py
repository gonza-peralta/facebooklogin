# -*- coding: utf-8 -*-
from flask import request
from flask import Response
from flask import Blueprint
from core.exceptions import BadRequestError
from core.exceptions import NotFoundError
from service.feedmodel import FacebookFeed
from service.companymodel import CompanyLink


fbfeed = Blueprint('fbfeed', __name__)
VERIFY_TOKEN = '0JOZ0mKh5nCV'


@fbfeed.route('/fbhook')
def register():
    """
    Get facebook request to validate webhook
    """
    args = request.values
    try:
        challenge = args.get('hub.challenge', '0')
    except ValueError:
        raise BadRequestError()

    try:
        token = args.get('hub.verify_token', None)
    except ValueError:
        raise BadRequestError()
    if token == VERIFY_TOKEN:
        return Response(challenge, status=200, mimetype='application/json')
    raise BadRequestError()    

@fbfeed.route('/fbhook', methods=['POST'])
def notifications():
    """
    Get facebook notification
    """
    # senderid = request.json["entry"][0]["messaging"][0]["sender"]["id"]
    
    payload = request.json
    print("======= Entrante Feed =========")
    print(payload)
    print("================================")
    try:
        page_id = payload["entry"][0]["id"]
    except ValueError:
        pass
    cmplink = CompanyLink()
    cmpnode = cmplink.getcompanytoken(page_id)
    if cmpnode is not None:
        fbfeed = FacebookFeed()
        for change in payload["entry"][0]["changes"]:
            if change["value"]["item"] != "like":
                fbfeed.add_document(cmpnode["dbname"], change["value"])
    else:
        raise NotFoundError("Page's company not found")
