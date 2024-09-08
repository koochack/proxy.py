#proxy.py can be started by running this script instead of running it as a module.
#This is useful for pyinstaller to create a standalone .exe file out of proxy.py

import sys, multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.argv.append('--plugins')
    sys.argv.append('proxy.plugin.ProxyPoolPlugin')
    sys.argv.append('--proxy-pool')
    sys.argv.append('77.37.63.119:9000')
    sys.argv.append('--log-level')
    sys.argv.append('c')
    from proxy import entry_point
    entry_point()
