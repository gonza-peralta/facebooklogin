# -*- coding: utf-8 -*-
from flask import Response
from werkzeug.http import HTTP_STATUS_CODES


class BaseAPIExceptionError(Exception):
    status_code = None
    message = None

    def __init__(self, message=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if self.status_code is None:
            raise NotImplementedError()
        try:
            _ = self.payload
        except AttributeError:
            self.payload = None
        if payload is not None:
            self.payload = payload

    def to_dict(self):
        pay_load_dict = dict(self.payload or ())
        if self.message:
            pay_load_dict["message"] = self.message
        return pay_load_dict

    def get_body(self):
        return (
            u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
            u'<title>%(code)s %(name)s</title>\n'
            u'<h1>%(name)s</h1>\n'
        ) % {
            'code':         self.status_code,
            'name':         HTTP_STATUS_CODES.get(self.status_code,
                                                  'Unknown Error')
        }

    def get_headers(self):
        """Get a list of headers."""
        return [('Content-Type', 'text/html')]

    def get_response(self):
        return Response(self.get_body(), self.status_code, self.get_headers())


class BadRequestError(BaseAPIExceptionError):
    status_code = 400
    message = "Unprocessable"


class NotFoundError(BaseAPIExceptionError):
    """
    NotFound Error
    """
    status_code = 404


class InternalServerError(BaseAPIExceptionError):
    """
    InternalServer Error
    """
    status_code = 500

class BadGateWayError(BaseAPIExceptionError):
    """
    Bad Gateway Error
    """
    status_code = 522
