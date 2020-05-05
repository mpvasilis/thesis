from sys import exit
from textwrap import dedent
from OID.modules.parser import *
from OID.modules.utils import *
from OID.modules.downloader import *
from OID.modules.show import *
from OID.modules.csv_downloader import *
from OID.modules.bounding_boxes import *
from OID.modules.image_level import *


ROOT_DIR = ''
DEFAULT_OID_DIR = os.path.join(ROOT_DIR, 'OID')

if __name__ == '__main__':

    args = parser_arguments()

    if args.command == 'downloader_ill':
        image_level(args, DEFAULT_OID_DIR)
    else:
        bounding_boxes_images(args, DEFAULT_OID_DIR)