#proxy.py can be started by running this script instead of running it as a module.
#This is useful for pyinstaller to create a standalone .exe file out of proxy.py

#local
import proxy
if __name__ == '__main__':
    with proxy.Proxy(['--plugins', 'proxy.plugin.ProxyPoolPlugin', '--proxy-pool', '127.0.0.1:9000', '--log-level', 'i']) as p:
        proxy.sleep_loop()
