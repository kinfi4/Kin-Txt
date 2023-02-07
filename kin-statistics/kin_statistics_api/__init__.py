import logging

from kin_statistics_api.settings import Settings


logging.basicConfig(
     level=Settings().log_level,
     format='[%(asctime)s] %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
