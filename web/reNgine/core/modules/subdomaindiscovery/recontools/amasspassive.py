#!/usr/bin/env python3
import subprocess
import os
import shlex
from reNgine.definitions import *

def run(domainName, resultsDir, yaml_configuration):
    outDir = os.path.join(resultsDir, 'subdomaindiscovery')
    try:
        os.makedirs(outDir)
    except FileExistsError:
        pass
    
    outFile = f'{os.path.join(outDir, os.path.basename(os.path.splitext(__file__)[0]))}.out'
    command = f'amass enum -passive -d {domainName} -o {outFile}'
    if USE_AMASS_CONFIG in yaml_configuration and yaml_configuration[USE_AMASS_CONFIG]:
                command += ' -config /root/.config/amass.ini'
    print(f'running {command} ...\n')
    proc = subprocess.run(shlex.split(command), capture_output=True)
    
    return proc.returncode


if __name__ == '__main__':
    rcode = run('cwavesoftware.com', 'out')
    print (f'{os.path.basename(__file__)} completed with status code {rcode}')
    print('Done')