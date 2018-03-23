
from    json        import dumps
from    os          import stat
from    binascii    import b2a_base64
import  socket, gc, _thread, time


class MicroWebSrv :

    _indexPages = [
        "index.html",
    ]

    _mimeTypes = {
        ".htm"   : "text/html",
        ".json"  : "application/json",
    }

    _html_escape_chars = {
        "&" : "&amp;",
        '"' : "&quot;",
        "'" : "&apos;",
        ">" : "&gt;",
        "<" : "&lt;"
    }

    def _tryAllocByteArray(size) :
        for x in range(10) :
            try :
                gc.collect()
                return bytearray(size)
            except :
                pass
        return None

    def _tryStartThread(func, args=()) :
        old_size = _thread.stack_size()
        _ = _thread.stack_size(6*1024)
        for x in range(4) :
            try :
                gc.collect()
                th = _thread.start_new_thread("MicroWebServer", func, args)
                _thread.stack_size(old_size)
                return th
            except :
                time.sleep_ms(100)
        _thread.stack_size(old_size)
        return False


    def _unquote(s) :
        r = s.split('%')
        for i in range(1, len(r)) :
            s = r[i]
            try :
                r[i] = chr(int(s[:2], 16)) + s[2:]
            except :
                r[i] = '%' + s
        return ''.join(r)


    def _unquote_plus(s) :
        return MicroWebSrv._unquote(s.replace('+', ' '))

    def _fileExists(path) :
        try :
            stat(path)
            return True
        except :
            return False

    def __init__(self, routeHandlers=None, port=80, webPath="/flash/www") :
        self._routeHandlers = routeHandlers
        self._srvAddr       = ('0.0.0.0', port)
        self._webPath       = webPath
        self._notFoundUrl   = None
        self._started       = False
        self.thID           = None
        self.isThreaded     = False

    def _serverProcess(self) :
        self._started = True
        self._state = "Running"
        while True :
            try :
                client, cliAddr = self._server.accepted()
                if client == None:
                    if self.isThreaded:
                        notify = _thread.getnotification()
                        if notify == _thread.EXIT:
                            break
                        elif notify == _thread.SUSPEND:
                            self._state = "Suspended"
                            while _thread.wait() != _thread.RESUME:
                                pass
                            self._state = "Running"
                    # gc.collect()
                    time.sleep_ms(2)
                    continue
            except :
                break
            self._client(self, client, cliAddr)
        self._started = False


    def Start(self, threaded=True) :
        if not self._started :
            gc.collect()
            self._server = socket.socket( socket.AF_INET,
                                          socket.SOCK_STREAM,
                                          socket.IPPROTO_TCP )
            self._server.setsockopt( socket.SOL_SOCKET,
                                     socket.SO_REUSEADDR,
                                     1 )
            self._server.bind(self._srvAddr)
            self._server.listen(1)
            self.isThreaded = threaded
            # using non-blocking socket
            self._server.settimeout(0.5)
            if threaded :
                th = MicroWebSrv._tryStartThread(self._serverProcess)
                if th:
                    self.thID = th
            else :
                self._serverProcess()

    def Stop(self) :
        if self._started :
            self._server.close()

    def GetRouteHandler(self, resUrl, method) :
        if self._routeHandlers :
            resUrl = resUrl.upper()
            method = method.upper()
            for route in self._routeHandlers :
                if len(route) == 3 and            \
                   route[0].upper() == resUrl and \
                   route[1].upper() == method :
                   return route[2]
        return None

    class _client :


        def __init__(self, microWebSrv, socket, addr) :
            socket.settimeout(2)
            self._microWebSrv   = microWebSrv
            self._socket        = socket
            self._addr          = addr
            self._method        = None
            self._path          = None
            self._httpVer       = None
            self._resPath       = "/"
            self._queryString   = ""
            self._queryParams   = { }
            self._headers       = { }
            self._contentType   = None
            self._contentLength = 0
            self._processRequest()


        def _processRequest(self) :
            try :
                response = MicroWebSrv._response(self)
                if self._parseFirstLine(response) :
                    if self._parseHeader(response) :
                        upg = self._getConnUpgrade()
                        if not upg :
                            routeHandler = self._microWebSrv.GetRouteHandler(self._resPath, self._method)
                            if routeHandler :
                                routeHandler(self, response)
                            else :
                                response.WriteResponseMethodNotAllowed()
                        else :
                            response.WriteResponseNotImplemented()
                    else :
                        response.WriteResponseBadRequest()
            except :
                response.WriteResponseInternalServerError()
            try :
                self._socket.close()
            except :
                pass


        def _parseFirstLine(self, response) :
            try :
                elements = self._socket.readline().decode().split()
                if len(elements) == 3 :
                    self._method  = elements[0].upper()
                    self._path    = elements[1]
                    self._httpVer = elements[2].upper()
                    elements      = self._path.split('?', 1)
                    if len(elements) > 0 :
                        self._resPath = MicroWebSrv._unquote(elements[0])
                        if len(elements) > 1 :
                            self._queryString = elements[1]
                            elements = self._queryString.split('&')
                            for s in elements :
                                param = s.split('=', 1)
                                if len(param) > 0 :
                                    value = MicroWebSrv._unquote_plus(param[1]) if len(param) > 1 else ''
                                    self._queryParams[MicroWebSrv._unquote(param[0])] = value
                    return True
            except :
                pass
            return False
    

        def _parseHeader(self, response) :
            while True :
                elements = self._socket.readline().decode().strip().split(':', 1)
                if len(elements) == 2 :
                    self._headers[elements[0].strip()] = elements[1].strip()
                elif len(elements) == 1 and len(elements[0]) == 0 :
                    if self._method == 'POST' :
                        self._contentType   = self._headers.get("Content-Type", None)
                        self._contentLength = int(self._headers.get("Content-Length", 0))
                    return True
                else :
                    return False


        def _getConnUpgrade(self) :
            if 'upgrade' in self._headers.get('Connection', '').lower() :
                return self._headers.get('Upgrade', '').lower()
            return None

        def GetRequestQueryParams(self) :
            return self._queryParams


        def GetRequestHeaders(self) :
            return self._headers


        def GetRequestContentType(self) :
            return self._contentType


        def GetRequestContentLength(self) :
            return self._contentLength


        def ReadRequestContent(self, size=None) :
            self._socket.setblocking(False)
            b = None
            try :
                if not size :
                    b = self._socket.read(self._contentLength)
                elif size > 0 :
                    b = self._socket.read(size)
            except :
                pass
            self._socket.setblocking(True)
            return b if b else b''


        def ReadRequestPostedFormData(self) :
            res  = { }
            data = self.ReadRequestContent()
            if len(data) > 0 :
                elements = data.decode().split('&')
                for s in elements :
                    param = s.split('=', 1)
                    if len(param) > 0 :
                        value = MicroWebSrv._unquote_plus(param[1]) if len(param) > 1 else ''
                        res[MicroWebSrv._unquote(param[0])] = value
            return res

    class _response :


        def __init__(self, client) :
            self._client = client


        def _write(self, data) :
            return self._client._socket.write(data)


        def _writeFirstLine(self, code) :
            reason = self._responseCodes.get(code, ('Unknown reason', ))[0]
            self._write("HTTP/1.0 %s %s\r\n" % (code, reason))


        def _writeHeader(self, name, value) :
            self._write("%s: %s\r\n" % (name, value))


        def _writeContentTypeHeader(self, contentType, charset=None) :
            if contentType :
                ct = contentType \
                   + (("; charset=%s" % charset) if charset else "")
            else :
                ct = "application/octet-stream"
            self._writeHeader("Content-Type", ct)


        def _writeEndHeader(self) :
            self._write("\r\n")


        def _writeBeforeContent(self, code, headers, contentType, contentCharset, contentLength) :
            self._writeFirstLine(code)
            if isinstance(headers, dict) :
                for header in headers :
                    self._writeHeader(header, headers[header])
            if contentLength > 0 :
                self._writeContentTypeHeader(contentType, contentCharset)
                self._writeHeader("Content-Length", contentLength)
            self._writeHeader("Server", "PolyExpressive")
            self._writeHeader("Connection", "close")
            self._writeEndHeader()

        def WriteResponse(self, code, headers, contentType, contentCharset, content) :
            try :
                contentLength = len(content) if content else 0
                self._writeBeforeContent(code, headers, contentType, contentCharset, contentLength)
                if contentLength > 0 :
                    self._write(content)
                return True
            except :
                return False

        def WriteResponseOk(self, headers=None, contentType=None, contentCharset=None, content=None) :
            return self.WriteResponse(200, headers, contentType, contentCharset, content)


        def WriteResponseJSONOk(self, obj=None, headers=None) :
            return self.WriteResponseOk(headers, "application/json", "UTF-8", dumps(obj))

        def WriteResponseError(self, code) :
            responseCode = self._responseCodes.get(code, ('Unknown reason', ''))
            return self.WriteResponse( code,
                                       None,
                                       "text/html",
                                       "UTF-8",
                                       self._errCtnTmpl % {
                                            'code'    : code,
                                            'reason'  : responseCode[0],
                                            'message' : responseCode[1]
                                       } )


        def WriteResponseJSONError(self, code, obj=None) :
            return self.WriteResponse( code,
                                       None,
                                       "application/json",
                                       "UTF-8",
                                       dumps(obj if obj else { }) )


        def WriteResponseBadRequest(self) :
            return self.WriteResponseError(400)


        def WriteResponseForbidden(self) :
            return self.WriteResponseError(403)


        def WriteResponseNotFound(self) :
            return self.WriteResponseError(404)


        def WriteResponseMethodNotAllowed(self) :
            return self.WriteResponseError(405)


        def WriteResponseInternalServerError(self) :
            return self.WriteResponseError(500)


        def WriteResponseNotImplemented(self) :
            return self.WriteResponseError(501)


        _errCtnTmpl = """\
        <html>
            <head>
                <title>Error</title>
            </head>
            <body>
                <h1>%(code)d %(reason)s</h1>
                %(message)s
            </body>
        </html>
        """

        _responseCodes = {
            404: ('Not Found', 'Nothing matches the given URI'),
        }

