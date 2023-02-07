import logging

from kin_reports_generation.settings import Settings


logging.basicConfig(
     level=Settings().log_level,
     format='[%(asctime)s] %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
