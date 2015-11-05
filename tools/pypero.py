#! /usr/bin/env python
"""
pypero
======

*a robot communication framework*

PYPERO_LIST is an environment variable containing ';' separated list of URL:
protocol://[user[:pass]@]host[:port][/folder]

ATLAAS_PATH is the local absolute path to atlaas tiles.
"""
import os
import sys
import json
import shutil
import socket
import logging
try: # python3
    from urllib.request import urlopen, urlretrieve
except ImportError: # python2
    from urllib import urlopen, urlretrieve

from lxml import etree
import gdal

atlaas_path = os.environ.get('ATLAAS_PATH', '.')
pypero_list = os.environ.get('PYPERO_LIST', '')

pypero_list = pypero_list.split(';')
while '' in pypero_list: pypero_list.remove('')

# initialize the logger
logger = logging.getLogger(__name__) # or __file__
handler = logging.StreamHandler()
handler.setFormatter( logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s') )
logger.addHandler( handler )
logger.setLevel(logging.DEBUG)

def tile(XxY, base=atlaas_path):
    return "%s/region.%s.png" % (base, XxY)

def check(filepath):
    geotiff = gdal.Open(filepath)
    npoints = geotiff.GetRasterBand(1).ReadAsArray()
    return npoints[npoints>2].size / float(npoints.size)

def get(url):
    xml = etree.parse(url)
    typ = xml.xpath('/PAMDataset/Metadata/MDI[@key="COVERAGE"]')
    return float(typ[0].text)

def process(tiles):
    logger.debug("process %s"%str(tiles))
    if not pypero_list:
        logger.error("no host list available. export PYPERO_LIST")
        return
    data = {}
    for host in pypero_list:
        for XxY in tiles:
            try:
                coverage = get(tile(XxY, host)+".aux.xml")
            except IOError as e:
                if 'failed to load HTTP resource' in e.message:
                    logger.warning("file does not exist on host [%s,%s]"%(XxY,
                                                                          host))
                    continue # try next tile
                elif 'failed to load external entity' in e.message:
                    logger.warning("host down [%s]"%host)
                    break # dont try to get other tile from it for now
            if XxY not in data or data[XxY][1] > coverage:
                data[XxY] = [host, coverage]

    for XxY, [host, coverage] in data.items():
        try:
            filepath, _ = urlretrieve(tile(XxY, host[0]))
            filemeta, _ = urlretrieve(tile(XxY, host[0])+".aux.xml",
                                      filepath+".aux.xml")
            logger.info("got %s from %s"%(filepath, host[0]))
            # make sure the file is OK
            if abs(check(filepath) - host[1]) < 1e-6:
                # mv filepath -> tile(XxY)
                logger.info("tile %s success moving it"%XxY)
                # os.rename dont work across filesystem
                #   [Errno 18] Invalid cross-device link
                shutil.copy(filepath, tile(XxY))
                shutil.copy(filemeta, tile(XxY)+".aux.xml")
                os.remove(filepath)
                os.remove(filemeta)
        except Exception as e:
            logger.error(str(e))

process(['1x1', '-1x0'])
