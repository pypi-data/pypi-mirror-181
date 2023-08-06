# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

import pandas as pd

from sc_config import ConfigUtils
from sc_inclusive import PROJECT_NAME, __version__
from sc_inclusive.manifest_utils import ManifestUtils
from sc_analyzer_base import BranchUtils
import argparse
from .analyzer.inclusive_avg_daily_summary_analyzer import InclusiveAvgDailySummaryAnalyzer


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)
        # 生成的目标Excel文件存放路径
        self._target_directory = self._config.get("inclusive.target_directory")
        # 目标文件名称
        self._target_filename = self._config.get("inclusive.target_filename")
        # 生成的Excel中按客户经理汇总的Sheet的名称
        self._target_manager_summary_sheet_name = self._config.get("inclusive.target_manager_summary_sheet_name")
        # 生成的Excel中按客户经理汇总的Sheet的名称
        self._target_branch_summary_sheet_name = self._config.get("inclusive.target_branch_summary_sheet_name")

    def _load_branch_stuff(self):
        try:
            BranchUtils.set_config(self._config)
            # 加载机构名称对应表
            BranchUtils.load_branch_name_mapping()
            # 加载公共户关键字列表
            BranchUtils.load_common_account_keyword_list()
            # 加载业绩归属机构配置
            BranchUtils.load_sales_performance_attribution_mapping()
            # 加载所有发生业务的机构清单
            BranchUtils.load_all_business_branch_list()
            return 0
        except Exception as error:
            logging.getLogger(__name__).error("加载机构名称对应表失败：{}".format(error))
            return 1

    def _load_manifest_stuff(self):
        try:
            ManifestUtils.set_config(self._config)
            # 加载花名册
            ManifestUtils.load_manifest()
            return 0
        except Exception as error:
            logging.getLogger(__name__).error("加载花名册相关信息失败：{}".format(error))
            return 1

    def run(self, *, args):
        logging.getLogger(__name__).info("开始进行普惠旺季营销数据分析...")
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config.as_dict()))

        # 加载机构相关配置
        result = self._load_branch_stuff()
        if result != 0:
            return result

        # 加载花名册相关配置
        result = self._load_manifest_stuff()
        if result != 0:
            return result

        target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename_full_path):
            logging.getLogger(__name__).info("删除输出文件：{} ".format(target_filename_full_path))
            try:
                os.remove(target_filename_full_path)
            except Exception as e:
                logging.getLogger(__name__).error("删除文件 {} 失败：{} ".format(target_filename_full_path, e))
                return 1
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename_full_path))
        try:
            with pd.ExcelWriter(target_filename_full_path) as excel_writer:
                # 按客户经理汇总结果
                manifest_data = ManifestUtils.get_manifest_df().copy()
                previous_data = pd.DataFrame()
                # 分析客户经理汇总
                analyzer = InclusiveAvgDailySummaryAnalyzer(config=self._config, excel_writer=excel_writer)
                analysis_result = analyzer.analysis_new()
                if analysis_result != 0:
                    logging.getLogger(__name__).error("分析 {} 时出错：结果集为空。".format(analyzer.get_business_type()))
                    return analysis_result
        except Exception as e:
            logging.getLogger(__name__).exception("分析 {} 时出错".format(analyzer.get_business_type()), exc_info=e)
            return 1

        logging.getLogger(__name__).info("结束普惠旺季营销数据分析...")
        return 0


def main():
    try:
        parser = argparse.ArgumentParser(description='Inclusive Analysis Tools')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
