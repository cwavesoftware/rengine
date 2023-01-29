#!/usr/bin/env python3

import threading
import importlib
import sys
import os
import time


class ToolRunner(threading.Thread):
    def __init__(self, module, domainName, resultsDir, config=None):
        threading.Thread.__init__(self)
        self.module = module
        self.domainName = domainName
        self.resultsDir = resultsDir
        self.name = module
        self.exception = None
        self.config = config

    def run(self):
        print(f'loading module {self.module}...\n')
        try:
            tool = importlib.import_module(self.module)
            tool.run(self.domainName, self.resultsDir, self.config)
        except Exception as ex:
            self.exception = ex


if __name__ == '__main__':
    toolsdir = '/usr/src/app/core/modules/subdomaindiscovery/recontools'
    threads = []
    for file in os.listdir(toolsdir):
        # print(file)
        if os.path.isfile(f'{os.path.join(toolsdir, file)}'):
            module = f'{toolsdir.replace("/usr/src/app/core/modules/subdomaindiscovery/","").replace("/", ".")}.{os.path.basename(os.path.splitext(file)[0])}'
            t = ToolRunner( module, 
                            sys.argv[2], 
                            sys.argv[1])
            t.start()
            threads.append(t)

    for t in threads:
        print(f'joining {t.name}')
        t.join()
        print(f'{t.name} finished')
    import processor
        
    print(f'{os.path.basename(__file__)} done')