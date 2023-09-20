import xmlrpc.client
import time

class xmlrpc_odoo():
    def __init__(self, db, username, password, host, port, http_type):
        self.db = db
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.http_type = http_type

        self.common = None
        self.sock = None
        self.max_retry = 3
        self.is_connect = False
        self.uid = None
    
    def connect(self):
        for i in range(1, self.max_retry+1):
            try:
                url_common = '%s://%s:%s/xmlrpc/2/common' % (self.http_type, self.host, self.port)
                url_object = '%s://%s:%s/xmlrpc/2/object' % (self.http_type, self.host, self.port)
                if not self.port:
                    url_common = '%s://%s/xmlrpc/2/common' % (self.http_type, self.host)
                    url_object = '%s://%s/xmlrpc/2/object' % (self.http_type, self.host)
                self.common = xmlrpc.client.ServerProxy(url_common)
                self.uid = self.common.authenticate(self.db, self.username, self.password, {})
                self.sock = xmlrpc.client.ServerProxy(url_object)
                self.is_connect = True
                break
            except ConnectionRefusedError:
                time.sleep(1)

    def version_odoo(self):
        if self.common:
            return self.common.version()
        else:
            return None
    
    def disconnect(self):
        self.is_connect = False
        self.sock = None
        self.common = None

    def call_method(self, model, method, param1=[], param2={}): ##Calling methods
        return self.sock.execute_kw(self.db, self.uid, self.password, model, method, param1, param2)

    def call_list(self, model, param1=[], param2={}, offset=None, limit=None): ### ไม่ใช่
        if offset:
            param2["offset"] = offset
        if limit:
            param2["limit"] = limit
        return self.sock.execute_kw(self.db, self.uid, self.password, model, "search", param1, param2)

    def call_count(self, model, param1=[]):
        return self.sock.execute_kw(self.db, self.uid, self.password, model, "search_count", param1)
    
    def call_read(self, model, ids, fields=[], offset=None, limit=None): ### ไม่ใช่
        param2 = {}
        if offset:
            param2["offset"] = offset
        if limit:
            param2["limit"] = limit
        if fields:
            param2["fields"] = fields
        return self.sock.execute_kw(self.db, self.uid, self.password, model, 'read', ids, param2)

    def call_search_read(self, model, param1=[], param2={}):
        ### param1 Ex. [[['is_company', '=', True]]]
        ### param2 Ex. {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        return self.sock.execute_kw(self.db, self.uid, self.password, model, 'search_read', param1, param2)

    def call_create(self, model, param1=[]):
        ### param1 Ex. [{'name': "New Partner"}]
        return self.sock.execute_kw(self.db, self.uid, self.password, model, 'create', param1)
    
    def call_write(self, model, id, param1=[]):
        ### param1 Ex. [[id], {'name': "Newer partner"}]
        self.sock.execute_kw(self.db, self.uid, self.password, model, 'write', param1)
        return self.sock.execute_kw(self.db, self.uid, self.password, model, 'name_get', [[id]])

    def call_delete(self, model, id):
        if id:
            self.sock.execute_kw(self.db, self.uid, self.password, model, 'unlink', [[id]])
            return self.sock.execute_kw(self.db, self.uid, self.password, model, 'search', [[['id', '=', id]]])