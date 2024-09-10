#remote
import proxy
if __name__ == '__main__':
    with proxy.Proxy(['--port', '9000', '--log-level', 'd']) as p:
        proxy.sleep_loop()
