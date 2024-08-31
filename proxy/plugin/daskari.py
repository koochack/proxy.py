# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.

    .. spelling::

       shortlink
"""
import os
from typing import Optional

from ..http.proxy import HttpProxyBasePlugin
from ..http.parser import HttpParser
from ..http.responses import NOT_FOUND_RESPONSE_PKT, seeOthersResponse
from ..common.constants import DOT, SLASH


class Daskari(HttpProxyBasePlugin):
    """Add support for short links in your favorite browsers / applications.

    Enable ShortLinkPlugin and speed up your daily browsing experience.

    Example::
    * ``f/`` for ``facebook.com``
    * ``g/`` for ``google.com`
    * ``t/`` for ``twitter.com``
    * ``y/`` for ``youtube.com``
    * ``proxy/`` for ``py`` internal web servers.
    Customize map below for your taste and need.

    Paths are also preserved. E.g. ``t/imoracle`` will
    resolve to my Twitter profile for username ``imoracle``.
    """

    def handle_client_request(
            self, request: HttpParser,
    ) -> Optional[HttpParser]:
        # if request.host and request.host != b'localhost' and DOT not in request.host:
        #     if request.host in self.SHORT_LINKS:
        #         path = SLASH if not request.path else request.path
        #         self.client.queue(
        #             seeOthersResponse(
        #                 b'http://' + self.SHORT_LINKS[request.host] + path,
        #             ),
        #         )
        #     else:
        #         self.client.queue(NOT_FOUND_RESPONSE_PKT)
        #     return None
        #request.headers[b'proxy-connection'] = (b'Proxy-Connection', b'keep-alive')

        return request

        if "_REMOTE" in os.environ.keys(): return request
        headerHost = request.headers[b'host'][1]
        headerHost = self.scrambleHost(headerHost, "left")
        # bArray = bytearray(headerHost)
        # #bArray = [(~x)+256 for x in bArray]
        # bArray.append(bArray.pop(0))
        # toBytes = bytes(bArray)

        request.del_header(b'Host')
        request.add_header(b'Host', headerHost)
        colonIdx = headerHost.find(b':')
        host = headerHost[:colonIdx]
        request.host = host
        #request.del_header(b'proxy-connection')
        #if request.body is None: request.body = b""
        #request.total_size += 100
        #request.body += b"<:alkjhnmdgfyte$%^19ujdhfgyrtegshdgcbsqieystcgeb^@#$UFJQHR5n2#VN3%W#mn34j5tn34#^&7m3jg34mn5#^#&N#$3j"


        if (request.chunk is not None) or (request.body is not None) or (request.buffer is not None):
            print("chunk: " + str(request.chunk) + "\n")
            print("body: " + str(request.body) + "\n")
            print("buffer: " + str(request.buffer) + "\n")
        print("HCR \n"+str(request.headers[b'host'][1]))
        return request

    def before_upstream_connection(
            self, request: HttpParser,
    ) -> Optional[HttpParser]:
        """Handler called just before Proxy upstream connection is established.

        Return optionally modified request object.
        If None is returned, upstream connection won't be established.

        Raise HttpRequestRejected or HttpProtocolException directly to drop the connection."""

        return request

        #request.headers[b'proxy-connection'] = (b'Proxy-Connection', b'keep-alive')
        if "_LOCAL" in os.environ.keys(): return request
        headerHost = request.headers[b'host'][1]
        headerHost = self.scrambleHost(headerHost, "right")
        # bArray = bytearray(headerHost)
        # #bArray = [(~x)+256 for x in bArray]
        # bArray.insert(0, bArray.pop(-1))
        # toBytes = bytes(bArray)

        request.del_header(b'Host')
        request.add_header(b'Host', headerHost)
        colonIdx = headerHost.find(b':')
        host = headerHost[:colonIdx]
        request.host = host
        #request.del_header(b'proxy-connection')
        #request.total_size -= 100
        #request.body = request.body[:-100]


        print("BUC \n" + str(request.headers[b'host'][1]))
        return request # pragma: no cover

    # def handle_client_data(
    #         self, raw: memoryview,
    # ) -> Optional[memoryview]:
    #     """Handler called in special scenarios when an upstream server connection
    #     is never established.
    #
    #     Essentially, if you return None from within before_upstream_connection,
    #     be prepared to handle_client_data and not handle_client_request.
    #
    #     Only called after initial request from client has been received.
    #
    #     Raise HttpRequestRejected to tear down the connection
    #     Return None to drop the connection
    #     """
    #     return raw
    #     temp = raw.tobytes()
    #     temp = bytearray([ord(self.map[chr(temp[i])]) if 97 <= temp[i] <= 122 else temp[i] for i in range(len(temp))])
    #     return memoryview(temp)
    #     # pragma: no cover
    # def handle_upstream_chunk(self, chunk: memoryview) -> Optional[memoryview]:
    #     """Handler called right after receiving raw response from upstream server.
    #
    #     For HTTPS connections, chunk will be encrypted unless
    #     TLS interception is also enabled.
    #
    #     Return None if you don't want to sent this chunk to the client.
    #     """
    #     return chunk
    #     temp = chunk.tobytes()
    #     temp = bytearray([ord(self.map[chr(temp[i])]) if 97 <= temp[i] <= 122 else temp[i] for i in range(len(temp))])
    #     return memoryview(temp)
    #     # pragma: no cover

    def scrambleHost(self, headerHost, shift, reverse=True):
        bArray = bytearray(headerHost)
        colonIdx = bArray.find(b':')
        host = bArray[:colonIdx]
        if shift == "left":
            # host.append(host.pop(0))
            # if reverse: host = bytearray([host[-i - 1] for i in range(len(host))])
            #host = bytearray([host[i] - 1 if 98<=host[i]<=122 else host[i] for i in range(len(host))]) #a-z are reduced by 1
            host = bytearray([ord(self.map[chr(host[i])]) if 97<=host[i]<=122 else host[i] for i in range(len(host))])
        if shift == "right":
            # if reverse: host = bytearray([host[-i - 1] for i in range(len(host))])
            # host.insert(0, host.pop(-1))
            #host = bytearray([host[i] + 1 if 97 <= host[i] <= 121 else host[i] for i in range(len(host))]) #a-z are increased by 1
            host = bytearray([ord(self.map[chr(host[i])]) if 97<=host[i]<=122 else host[i] for i in range(len(host))])
        both = host + bArray[colonIdx:]
        return bytes(both)

    map = \
        {
            'a':'y',
            'b':'g',
            'c':'u',
            'd':'m',
            'e':'l',
            'f':'s',
            'g':'b',
            'h':'v',
            'i':'p',
            'j':'n',
            'k':'q',
            'l':'e',
            'm':'d',
            'n':'j',
            'o':'x',
            'p':'i',
            'q':'k',
            'r':'z',
            's':'f',
            't':'w',
            'u':'c',
            'v':'h',
            'w':'t',
            'x':'o',
            'y':'a',
            'z':'r'
        }
