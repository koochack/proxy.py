#proxy.py can be started by running this script instead of running it as a module.
#This is useful for pyinstaller to create a standalone .exe file out of proxy.py

#local
import proxy, multiprocessing
if __name__ == '__main__':
    multiprocessing.freeze_support()
    with proxy.Proxy(['--plugins', 'proxy.plugin.ProxyPoolPlugin', '--proxy-pool', '77.37.63.119:9000', '--log-level', 'c', '--timeout', '200', '--local-executor', '0']) as p:
        proxy.sleep_loop(p)
