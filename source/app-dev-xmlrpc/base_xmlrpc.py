import xmlrpc.client

class xmlrpc_odoo():
    def __init__(self, db, username, password, common_url, object_url):
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.common = xmlrpc.client.ServerProxy(common_url)
        self.models = xmlrpc.client.ServerProxy(object_url)
        self.common_url = common_url
        self.object_url = object_url
    
    def version_odoo(self):
        if self.common:
            return self.common.version()
        else:
            return None
    
    def login(self):
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        return self.uid

    def call_method(self, model, method, param1=[], param2={}): ##Calling methods
        return self.models.execute_kw(self.db, self.uid, self.password, model, method, param1, param2)

    def call_list(self, model, param1=[], param2={}, offset=None, limit=None): ### ไม่ใช่
        if offset:
            param2["offset"] = offset
        if limit:
            param2["limit"] = limit
        return self.models.execute_kw(self.db, self.uid, self.password, model, "search", param1, param2)

    def call_count(self, model, param1=[]):
        return self.models.execute_kw(self.db, self.uid, self.password, model, "search_count", param1)
    
    def call_read(self, model, ids, fields=[], offset=None, limit=None): ### ไม่ใช่
        param2 = {}
        if offset:
            param2["offset"] = offset
        if limit:
            param2["limit"] = limit
        if fields:
            param2["fields"] = fields
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'read', ids, param2)

    def call_search_read(self, model, param1=[], param2={}):
        ### param1 Ex. [[['is_company', '=', True]]]
        ### param2 Ex. {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_read', param1, param2)

    def call_create(self, model, param1=[]):
        ### param1 Ex. [{'name': "New Partner"}]
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'create', param1)
    
    def call_write(self, model, id, param1=[]):
        ### param1 Ex. [[id], {'name': "Newer partner"}]
        self.models.execute_kw(self.db, self.uid, self.password, model, 'write', param1)
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'name_get', [[id]])

    def call_delete(self, model, id):
        if id:
            self.models.execute_kw(self.db, self.uid, self.password, model, 'unlink', [[id]])
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'search', [[['id', '=', id]]])