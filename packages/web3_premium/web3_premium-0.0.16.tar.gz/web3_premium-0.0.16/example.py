import datetime
import time

# import pandas as pd
# from tqdm import trange

from src.web3_premium.explorer import snowtrace
from src.web3_premium.contract import Contract
from src.web3_premium.chains import avalanche


snowtrace.set_api_key("EW1TBC2J8P6TNGARYFE4U1895DBW6MQ354")
c = Contract("0x486Af39519B4Dc9a7fCcd318217352830E8AD9b4", avalanche, snowtrace)
print(c.admin())

import src.web3_premium.utils as utils

print(utils.get_block_by_datetime(snowtrace, datetime.datetime.now()))
