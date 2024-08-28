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

    # def before_upstream_connection(
    #         self, request: HttpParser,
    # ) -> Optional[HttpParser]:
    #     if request.host and request.host != b'localhost' and DOT not in request.host:
    #         # Avoid connecting to upstream
    #         return None
    #     return request

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

        if (request.chunk is not None) or (request.body is not None) or (request.buffer is not None):
            print("####################################################################\n###############################################")
        print("HCR \n"+str(request.headers[b'host'][1]))
        return request

    def before_upstream_connection(
            self, request: HttpParser,
    ) -> Optional[HttpParser]:
        """Handler called just before Proxy upstream connection is established.

        Return optionally modified request object.
        If None is returned, upstream connection won't be established.

        Raise HttpRequestRejected or HttpProtocolException directly to drop the connection."""

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

        print("BUC \n" + str(request.headers[b'host'][1]))
        return request # pragma: no cover

    def scrambleHost(self, headerHost, shift, reverse=True):
        bArray = bytearray(headerHost)
        colonIdx = bArray.find(b':')
        host = bArray[:colonIdx]
        if shift == "left":
            host.append(host.pop(0))
            if reverse: host = bytearray([host[-i - 1] for i in range(len(host))])
        if shift == "right":
            if reverse: host = bytearray([host[-i - 1] for i in range(len(host))])
            host.insert(0, host.pop(-1))
        both = host + bArray[colonIdx:]
        return bytes(both)
