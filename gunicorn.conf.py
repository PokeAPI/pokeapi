import os
from multiprocessing import cpu_count

bind = "0.0.0.0:{}".format(os.environ.get("SERVER_PORT", "80"))
workers = threads = cpu_count() * 2
