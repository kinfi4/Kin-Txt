import logging

from kin_news_core.reports_building.settings import Settings


logging.basicConfig(
     level=Settings().log_level,
     format='[%(asctime)s] %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
