from django.http import QueryDict

class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        print "Entrando al metodoooooo"
        #print request.META
        if request.META.has_key('HTTP_X_METHODOVERRIDE'):
            print "Request:"
            #print request
            http_method = request.META['HTTP_X_METHODOVERRIDE']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
                request.PUT = QueryDict(request.body)
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
                request.DELETE = QueryDict(request.body)
        return None
