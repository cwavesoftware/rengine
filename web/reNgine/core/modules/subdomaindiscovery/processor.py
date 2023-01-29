#!/usr/bin/env python3
import os
import subprocess
import sys


def process(resultsDir, outfile):
    resultsDir = os.path.join(resultsDir, 'subdomaindiscovery')
    files = []
    for file in os.listdir(resultsDir):
        # print(file)
        if os.path.isfile(f'{os.path.join(resultsDir,file)}'):
            print(f'{os.path.basename(__file__)}: found {file}')
            files.append(f'{os.path.join(resultsDir,file)}')
    finalFile = os.path.join(resultsDir, outfile)
    if len(files):
        cmd = f'cat {" ".join(files)} | sort -u > {finalFile}'
        print(f'{os.path.basename(__file__)}: {cmd}')
        proc = subprocess.run(cmd, shell=True)
        return proc.returncode


if __name__ == '__main__':
    process(sys.argv[1])
    print(f'{os.path.basename(__file__)} done')
