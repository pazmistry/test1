import os
import logging
import sys
''' Searches a list of directories and truncates trace files larger than specified size to new specified size
set up test data on the mac
mkdir /tmp/delme ; mkdir /tmp/delme2 ; cp Downloads/delmelarge.txt /tmp/delme ; cp Downloads/IMG_0113.jpeg /tmp/delme ; cp /tmp/delme/delmelarge.txt /tmp/delme/delmelarge.trc ; cp /tmp/delme/IMG_0113.jpeg /tmp/delme/small.trc ; cp /tmp/delme/* /tmp/delme2/ ;
find /tmp/delme*

'''

myDir = ('/tmp/delme','/tmp/delme2')
cn_largeFileSize = 1024*1024*1024
cn_smallFileSize = 1024*1024*10
mydir = "/tmp/delme"


def truncateFile(ps_filelocation):
    # Open a file
    fo = open(ps_filelocation, "w")
    # Now truncate remaining file.
    fo.truncate(cn_smallFileSize)
    fo.close
    pass

def checkForLargeFiles(mydir):
    for myfilename in os.listdir(mydir):
        if myfilename.endswith('.trc') or myfilename.endswith('.trm'):
            filelocation = mydir+"/"+myfilename
            ln_filesize = os.path.getsize(filelocation)
            logger.debug('Truncated: %s %s', filelocation,ln_filesize)
            if os.path.getsize(filelocation) > cn_largeFileSize:
                logger.info('Truncated: %s %s', filelocation,ln_filesize)
#                print(filelocation,ln_filesize,"LARGE")
                truncateFile(filelocation)
            #else:
            #    print(filelocation, ln_filesize,"small")

def checkInDirectories(myDir):
    for name in myDir:
        logger.info('Directory: %s', name)
        checkForLargeFiles(name)

'''
FORMAT = '%(asctime)-15s'
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('__main__')

'''
logger = logging.getLogger('snap_logs')
logger.setLevel(20)

# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(20)

# create formatter
formatter = logging.Formatter('%(asctime)s %(levelname)8s > %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)




logger.info('Execution Started')
logger.debug('myDir: %s',myDir)

checkInDirectories(myDir)
logger.info('Execution Completed')
