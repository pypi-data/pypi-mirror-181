import logging
import sys
from deepdriver.sdk import util
logger = logging.getLogger("deepdriver")

console_handler = logging.StreamHandler(sys.stdout)
if not util.is_notebook():
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    console_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


from deepdriver.sdk.artifact import *
from deepdriver.sdk.config import *
from deepdriver.sdk.experiment import *
from deepdriver.sdk.login import *
from deepdriver.sdk.setting import *
from deepdriver.sdk.run import *
from deepdriver.sdk.visualization import visualize
from deepdriver.sdk.chart.histogram import histogram
from deepdriver.sdk.chart.line import line
from deepdriver.sdk.chart.scatter import scatter
from deepdriver.sdk.data_types.dataFrame import DataFrame
from deepdriver.sdk.data_types.image import Image
from deepdriver.sdk.data_types.table import Table

config = Config()


