#!/usr/bin/env python3
import subprocess
import os
import shlex


def run(domainName, resultsDir):
    outDir = os.path.join(resultsDir, 'subdomaindiscovery')
    try:
        os.makedirs(outDir)
    except FileExistsError:
        pass
    outFile = f'{os.path.join(outDir, os.path.basename(os.path.splitext(__file__)[0]))}.out'
    command = f'python3 /usr/src/github/Sublist3r/sublist3r.py -d {domainName} -t 10 -o {outFile}'
    print(f'running {command} ...\n')
    proc = subprocess.run(command, shell=True, capture_output=True)
    return proc.returncode



if __name__ == '__main__':
    rcode = run('cwavesoftware.com', './out')
    print (f'{os.path.basename(__file__)} completed with status code {rcode}')
    print('Done')