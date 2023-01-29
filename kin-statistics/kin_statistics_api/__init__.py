import os
import logging

from kin_statistics_api.settings import Settings
from kin_statistics_api.settings import CelerySettings


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

logging.basicConfig(
     level=Settings().log_level,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
