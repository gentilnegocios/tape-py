# -*- coding: utf-8 -*-
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Resource(object):
    """Represents a Tape Resource"""
    def __init__(self, transport):
        self.transport = transport

    @staticmethod
    def sanitize_id(record_id: int):
        if isinstance(record_id, int):
            return str(record_id)
        return record_id

    @staticmethod
    def get_options(silent=False, hook=True, workflow=True, **kwargs):
        """
        Generate a query string with the appropriate options.

        :param silent: If set to true, the object will not be bumped up in the stream and
                       notifications will not be generated.
        :type silent: bool
        :param hook: True if hooks should be executed for the change, false otherwise.
        :type hook: bool
        :return: The generated query string
        :rtype: str
        """
        options_ = {}
        if silent:
            options_['silent'] = silent
        if not hook:
            options_['hook'] = hook
        if not workflow:
            options_['workflow'] = workflow
        if kwargs:
            options_.update(kwargs)
        if options_:
            return '?' + urlencode(options_)
        return ''


class Record(Resource):
    def find(self, record_id: int, **kwargs):
        """
        Get record

        :param record_id: Record ID
        :param basic: ?
        :type record_id: int
        :return: Record info
        :rtype: dict
        """
        return self.transport.GET(url='/v1/record/%d' % record_id, **kwargs)

    def filter(self, app_id: int, attributes: dict, **kwargs):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url="/v1/record/filter/app/%d%s" %
                                   (app_id, self.get_options(**kwargs)),
                                   body=attributes,
                                   type="application/json")

    def filter_by_view(self, view_id: int, **kwargs):
        return self.transport.GET(url="/v1/record/view/%d%s" %
                                   (view_id, self.get_options(**kwargs)))

    def create(self, app_id: int, attributes: dict, silent=False, hook=True, workflow=True):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(body=attributes,
                                   type='application/json',
                                   url='/v1/record/app/%d%s' % (app_id,
                                                            self.get_options(silent=silent,
                                                                             hook=hook,
                                                                             workflow=workflow)))

    def update(self, record_id: int, attributes: dict, silent=False, hook=True, workflow=True):
        """
        Updates the item using the supplied attributes. If 'silent' is true, Tape will send
        no notifications to subscribed users and not post updates to the stream.

        Important: webhooks will still be called.
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.PUT(body=attributes,
                                  type='application/json',
                                  url='/v1/record/%d%s' % (record_id, self.get_options(silent=silent,
                                                                                hook=hook,
                                                                                workflow=workflow)))

    def delete(self, record_id: int, silent=False, hook=True, skip_trash=False):
        return self.transport.DELETE(url='/v1/record/%d%s' % (record_id,
                                                         self.get_options(silent=silent,
                                                                          hook=hook,
                                                                          skip_trash=skip_trash)),
                                     handler=lambda x, y: None)

    def restore(self, record_id: int, silent=False, hook=True):
        return self.transport.POST(url='/v1/record/%d/restore%s' % (record_id,
                                                                     self.get_options(silent=silent,
                                                                                      hook=hook)))


class App(Resource):

    def get_records(self, app_id: int, **kwargs):
        return self.transport.GET(url='/v1/record/app/%d%s' % (app_id, self.get_options(**kwargs)))

    def find(self, app_id: int):
        return self.transport.GET(url='/v1/app/%d' % app_id)


class Workspace(Resource):

    def get_all_for_org(self):
        return self.transport.GET(url='/v1/workspace/org')


class File(Resource):

    def upload(self, filename: str, filedata):
        """Create a file from raw data"""
        attributes = {'filename': filename,
                      'file': filedata}
        return self.transport.POST(url='/v1/file/upload', body=attributes, type='multipart/form-data')
