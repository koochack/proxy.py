#remote
import proxy
if __name__ == '__main__':
    #for VPS use the upper one. For local testing use the lower one
    with proxy.Proxy(['--hostname', '0.0.0.0', '--port', '9000', '--log-level', 'i', '--client-recvbuf-size', '512000', '--server-recvbuf-size', '512000', '--max-sendbuf-size', '1024000']) as p:
    #with proxy.Proxy(['--port', '9000', '--log-level', 'i']) as p:
        proxy.sleep_loop()
