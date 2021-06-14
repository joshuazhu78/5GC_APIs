import argparse
import os
import numpy as np
import glob
import htmllistparse
from urllib.parse import urljoin
from pathlib import Path
import requests
import zipfile
import shutil
import yaml

parser = argparse.ArgumentParser(description='Find 5GAPI yaml files')
parser.add_argument('--apiVersion', type=str, default="1.0.0", help='3GPP 5GC API version, e.g. 1.0.0')
parser.add_argument('--outputDir', type=str, default="v1.0.0", help='output folder')

args = parser.parse_args()

def main():
    yamlFileList = glob.glob("*.yaml")
    specList = [f[2:7] for f in yamlFileList]
    specList = list(set(specList))
    urlList = ["https://www.3gpp.org/ftp/Specs/archive/"+s[0:2]+"_series/"+s[0:2]+"."+s[2:5]+"/" for s in specList]
    tmpFolder = "tmp"
    if not os.path.isdir(tmpFolder):
        os.makedirs(tmpFolder)
    if not os.path.isdir(args.outputDir):
        os.makedirs(args.outputDir)
    for url in urlList:
        cwd, listing = htmllistparse.fetch_listing(url, timeout=30)
        found = False
        for f in listing:
            if found:
                break
            if Path(f.name).suffix != ".zip":
                continue
            majorVersion = f.name[6]
            if majorVersion < 'f':
                continue
            filenameWithoutSuffix = os.path.splitext(f.name)[0]
            downloadZipFile = os.path.join(tmpFolder, f.name)
            if not os.path.exists(downloadZipFile):
                urlFile = urljoin(url, f.name)
                print("downloading "+urlFile)
                r = requests.get(urlFile, allow_redirects=True)
                open(downloadZipFile, 'wb').write(r.content)
            unzipFolder = os.path.join(tmpFolder, filenameWithoutSuffix)
            if not os.path.isdir(unzipFolder):
                os.makedirs(unzipFolder)
                with zipfile.ZipFile(downloadZipFile, 'r') as zip_ref:
                    print("unzipping "+downloadZipFile)
                    zip_ref.extractall(unzipFolder)
            else:
                print("reuse unzipped "+downloadZipFile)
            unzippedYamlFileList = glob.glob(os.path.join(unzipFolder, "*.yaml"))
            if len(unzippedYamlFileList) == 0:
                continue
            for unzippedYamlFile in unzippedYamlFileList:
                stream = open(unzippedYamlFile, 'r')
                doc = yaml.load(stream,Loader=yaml.Loader)
                if doc['info']['version'] == args.apiVersion:
                    apiYamlFile = os.path.join(args.outputDir,os.path.basename(unzippedYamlFile))
                    print(apiYamlFile)
                    shutil.copyfile(unzippedYamlFile, apiYamlFile)
                    found = True

if __name__ == "__main__":
    main()

