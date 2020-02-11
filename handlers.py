import tornado
import tornado.web
import tornado.websocket
import tornado.httpclient
import tornado.gen

tornado.httpclient.AsyncHTTPClient.configure(None, defaults={'decompress_response': False})


class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self, proxy_url='/', **kwargs):
        super(ProxyHandler, self).initialize(**kwargs)
        self.proxy_url = proxy_url

    async def get(self, url=None):
        '''Get the login page'''
        print("INCOMING URL: "+url)
        #url = url or self.proxy_url
        if url is None:
            if self.request.uri.startswith('/'):
                url = self.request.uri[1:]
            else:
                url = self.request.uri

        debug = True
        if url[:6] == 'static' or url[:7] == 'favicon':
            debug = False

        url = self.proxy_url+url

        if debug:
            print("GET : "+url)

        incoming_headers = {}

        for k,v in self.request.headers.items():
            if not k.lower() in ['host', 'pragma', 'upgrade-insecure-requests',
                                 'sec-fetch-user', 'sec-fetch-site', 'sec-fetch-mode', 'accept-encoding']:
                # 'accept-encoding', 'accept-language', 'accept', 'cache-control',
                incoming_headers[k] = v

        req = tornado.httpclient.HTTPRequest(url, headers=incoming_headers)
        client = tornado.httpclient.AsyncHTTPClient()

        response = None
        retries = 0

        while not response and retries < 100:
            response = await client.fetch(req, raise_error=False)
            if response.error:
                print(" **** response.error")
                print(response.error)
                if response.code == 599: # Maybe server wasn't yet ready
                    print(" **** response.error 599 ***")
                    response = None
                    retries += 1
                    await tornado.gen.sleep(0.1)

        if not response:
            self.set_status(404)
            self.finish()
            return

        if debug:
            print(incoming_headers)

            print(response)

            print(response.headers)

            print(response.code)

        self.set_status(response.code)
        if response.code != 200:
            self.finish()
        else:
            if response.body:
                if debug:
                    print("response body")
                for header, v in response.headers.get_all():
                    if header.lower() == 'content-length':
                        self.set_header(header, str(max(len(response.body), int(v))))
                    else:
                        self.set_header(header, v)

            self.write(response.body)

            self.finish()


class ProxyWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, proxy_url='/', **kwargs):
        super(ProxyWSHandler, self).initialize(**kwargs)
        self.proxy_url = proxy_url
        self.ws = None
        self.closed = True

    async def open(self, url=None):
        self.closed = False
        #url = url or self.proxy_url
        if url is None:
            if self.request.uri.startswith('/'):
                url = self.request.uri[1:]
            else:
                url = self.request.uri
        url = self.proxy_url+url

        def write(msg):
            if self.closed or msg is None:
                if self.ws:
                    self.ws.close()
                    self.ws = None
            else:
                if self.ws:
                    self.write_message(msg, binary=isinstance(msg, bytes))

        if url[:4] == 'http':
            url = 'ws' + url[4:]

        print("WEBSOCKET OPENING ON "+url)
        self.ws = await tornado.websocket.websocket_connect(url,
                                                            on_message_callback=write)

    async def on_message(self, message):
        if self.ws:
            await self.ws.write_message(message, binary=isinstance(message, bytes))

    def on_close(self):
        if self.ws:
            self.ws.close()
            self.ws = None
            self.closed = True
