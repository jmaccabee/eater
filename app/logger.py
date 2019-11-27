import logging
import os


logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a+',
    filename=os.path.join(os.path.dirname(__file__), '../eater_app.log'),
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO,
)

eater_logger = logging.getLogger()
