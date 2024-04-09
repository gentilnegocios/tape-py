# -*- coding: utf-8 -*-
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Resource(object):
    """
    Represents a Tape resource
    """
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
        :param hook: True if hooks should be executed for the change, False otherwise.
        :type hook: bool
        :param workflow: True if trigger Workflows for the change, False otherwise.
        :type workflow: bool
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
    """
    Represents a Record resource
    """
    def find(self, record_id: int, **kwargs):
        """
        Get a record

        Docs: https://developers.tapeapp.com/docs/api/resource/record#retrieve-a-record
        """
        return self.transport.GET(url='/v1/record/%d' % record_id, **kwargs)

    def filter(self, app_id: int, attributes: dict, **kwargs):
        """
        Filter records

        Docs: https://developers.tapeapp.com/docs/api/resource/record#retrieve-filtered-records-for-an-app
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url="/v1/record/filter/app/%d%s" %
                                   (app_id, self.get_options(**kwargs)),
                                   body=attributes,
                                   type="application/json")

    def filter_by_view(self, view_id: int, **kwargs):
        """
        Filter records by view

        Docs: https://developers.tapeapp.com/docs/api/resource/record#retrieve-records-for-a-view
        """
        return self.transport.GET(url="/v1/record/view/%d%s" %
                                   (view_id, self.get_options(**kwargs)))

    def create(self, app_id: int, attributes: dict, silent=False, hook=True, workflow=True):
        """
        Create a record

        Docs: https://developers.tapeapp.com/docs/api/resource/record#create-a-record
        """
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
        Update a record

        Docs: https://developers.tapeapp.com/docs/api/resource/record#update-a-record
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
        """
        Delete a record

        Docs: https://developers.tapeapp.com/docs/api/resource/record#delete-a-record
        """
        return self.transport.DELETE(url='/v1/record/%d%s' % (record_id,
                                                         self.get_options(silent=silent,
                                                                          hook=hook,
                                                                          skip_trash=skip_trash)),
                                     handler=lambda x, y: None)

    def restore(self, record_id: int, silent=False, hook=True):
        """
        Restore a record

        Docs: https://developers.tapeapp.com/docs/api/resource/record#restore-a-record
        """
        return self.transport.POST(url='/v1/record/%d/restore%s' % (record_id,
                                                                     self.get_options(silent=silent,
                                                                                      hook=hook)))


class App(Resource):
    """
    Represents an App resource
    """
    def get_records(self, app_id: int, **kwargs):
        """
        Get records for an app

        Docs: https://developers.tapeapp.com/docs/api/resource/record#retrieve-records-for-an-app
        """
        return self.transport.GET(url='/v1/record/app/%d%s' % (app_id, self.get_options(**kwargs)))

    def find(self, app_id: int):
        """
        Get an app

        Docs: https://developers.tapeapp.com/docs/api/resource/app#retrieve-a-single-app
        """
        return self.transport.GET(url='/v1/app/%d' % app_id)


class Workspace(Resource):
    """
    Represents a Workspace resource
    """
    def get_all_for_org(self):
        """
        Get all workspaces for the organization

        Docs: https://developers.tapeapp.com/docs/api/resource/workspace#retrieve-workspaces
        """
        return self.transport.GET(url='/v1/workspace/org')


class File(Resource):
    """
    Represents a File resource
    """
    def upload(self, filename: str, filedata):
        """
        Upload a file

        Docs: https://developers.tapeapp.com/docs/api/resource/file#upload-a-file
        """
        attributes = {'filename': filename,
                      'file': filedata}
        return self.transport.POST(url='/v1/file/upload', body=attributes, type='multipart/form-data')
