#remote
import proxy
if __name__ == '__main__':
    #for VPS use the upper one. For local testing use the lower one
    with proxy.Proxy(['--hostname', '0.0.0.0', '--port', '9000', '--log-level', 'c', '--num-acceptors', '16', '--num-workers', '16', '--timeout', '200', '--local-executor', '0']) as p:
    #with proxy.Proxy(['--port', '9000', '--log-level', 'i']) as p:
        proxy.sleep_loop(p)
