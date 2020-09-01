import datetime
import os
import time

__author__ = 'cagey'

import subprocess
import pathlib
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

job_path = settings["OUYEEL_JOB_PATH"]
datax_path = settings["DATAX_PATH"]

def push_data(datax_path, job_path):
    """
    调用datax插件,推送同步数据
    :param datax_path:
    :param job_path:
    :return:
    """
    # now = datetime.datetime.now()
    # zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    # job_file = str(pathlib.Path.cwd().parent) + "/job/oy_tmp.json"
    job_file = str(pathlib.Path.cwd()) + "/job/oy_tmp.json"
    # print(job_file)
    # print("*"*100)
    today = time.strftime("%Y-%m-%d", time.localtime())
    table_name = settings['MONGODB_COLLECTION_OY'] + "_" + today
    subprocess.getstatusoutput(f"sed 's/ouyeel_tmp/{table_name}/g' {job_path} >> {job_file}")
    cmd = f"python {datax_path} {job_file}"
    # cmd = f"python {datax_path} {job_path}"
    # print(cmd)
    status, res = subprocess.getstatusoutput(cmd)
    os.remove(job_file)
    if status == 0:
        return True, res
    else:
        return False, res


if __name__ == "__main__":
    status, res = push_data(datax_path, job_path)
    print(status, res)



