#  The MIT License (MIT)
#
#  Copyright (c) 2022. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import os
import os.path
import shutil
from datetime import datetime

import pandas as pd
from config42 import ConfigManager
from sc_inclusive_balance_detail_analysis.main import main as detain_main
from sc_utilities import calculate_column_index

from sc_inclusive import PROJECT_NAME, __version__
from .base_analyzer import BaseAnalyzer


class InclusiveAvgDailySummaryAnalyzer(BaseAnalyzer):
    """
    普惠日均分析
    """

    def __init__(self, *, config: ConfigManager, excel_writer: pd.ExcelWriter):
        super().__init__(config=config, excel_writer=excel_writer)
        self._key_enabled = "inclusive.avg_daily_summary.enabled"
        self._key_business_type = "inclusive.avg_daily_summary.business_type"
        # self._key_export_column_list = "inclusive.avg_daily_summary.sheet_config.export_column_list"

    def _read_config(self, *, config: ConfigManager):
        # 报表文件路径
        self._src_filepath = config.get("inclusive.avg_daily_summary.source_file_path")
        # 是否重新分析原明细数据
        config_str = config.get("inclusive.avg_daily_summary.reanalyze_detail_data")
        self._reanalyze_detail_data = False if config_str is None else config_str
        # 日期格式
        self._date_format = config.get("inclusive.avg_daily_summary.date_format")
        # 分析开始日期
        self._start_date_str = config.get("inclusive.avg_daily_summary.start_date")
        self._start_date = datetime.strptime(self._start_date_str, self._date_format)
        # 分析结束日期
        self._end_date_str = config.get("inclusive.avg_daily_summary.end_date")
        self._end_date = datetime.strptime(self._end_date_str, self._date_format)

        # Sheet名称
        self._manager_sheet_name = config.get("inclusive.avg_daily_summary.manager_summary.sheet_name")
        # 表头行索引
        self._manager_header_row = config.get("inclusive.avg_daily_summary.manager_summary.header_row")

        self._manager_base_columns = list()
        self._manager_base_columns_names = list()
        base_columns_config = config.get("inclusive.avg_daily_summary.manager_summary.base_columns")
        if base_columns_config is not None and type(base_columns_config) == list:
            self._manager_base_columns.extend(base_columns_config)

        self._manager_avg_columns = list()
        self._manager_avg_columns_names = list()
        avg_columns_config = config.get("inclusive.avg_daily_summary.manager_summary.avg_columns")
        if avg_columns_config is not None and type(avg_columns_config) == list:
            self._manager_avg_columns.extend(avg_columns_config)

        # Sheet名称
        self._branch_sheet_name = config.get("inclusive.avg_daily_summary.branch_summary.sheet_name")
        # 表头行索引
        self._branch_header_row = config.get("inclusive.avg_daily_summary.branch_summary.header_row")

        self._branch_base_columns = list()
        self._branch_base_columns_names = list()
        base_columns_config = config.get("inclusive.avg_daily_summary.branch_summary.base_columns")
        if base_columns_config is not None and type(base_columns_config) == list:
            self._branch_base_columns.extend(base_columns_config)

        self._branch_avg_columns = list()
        self._branch_avg_columns_names = list()
        avg_columns_config = config.get("inclusive.avg_daily_summary.branch_summary.avg_columns")
        if avg_columns_config is not None and type(avg_columns_config) == list:
            self._branch_avg_columns.extend(avg_columns_config)

    def _date_within_range(self, date: datetime):
        return self._start_date <= date <= self._end_date

    def _scan_analyze_directory(self):
        path = os.getcwd()
        logging.getLogger(__name__).info("扫描 {path} 文件夹下待分析日期...")
        config_src_file = os.path.join(path, "detail-production.yml")
        manifest_file_path = self._config.get("manifest.source_file_path")
        manifest_src_file = os.path.join(path, manifest_file_path)
        date_dirs = dict()
        # 扫描日期文件夹
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.startswith('.') or entry.is_file():
                    continue
                try:
                    dir_date = datetime.strptime(entry.name, self._date_format)
                    if not self._date_within_range(dir_date):
                        # 不在此次需要重跑的日期列表中，则忽略
                        continue
                    date_dirs[entry.name] = entry.path
                    config_dest_file = os.path.join(entry.path, "production.yml")
                    manifest_dest_file = os.path.join(entry.path, manifest_file_path)
                    # 复制配置文件
                    shutil.copyfile(config_src_file, config_dest_file)
                    shutil.copyfile(manifest_src_file, manifest_dest_file)
                except ValueError:
                    # 不是日期文件夹，则忽略
                    continue
                except Exception as e:
                    logging.getLogger(__name__).error("{} 分析失败：{}".format(self._business_type, e))
                    continue
        # 将文件夹按日期前后顺序排序
        date_dirs = dict(sorted(date_dirs.items()))
        return date_dirs

    def analysis_new(self) -> int:
        """
        主分析流程分析

        """
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        self._business_type = self._config.get(self._key_business_type)
        # 如果未启用，则直接返回上一次的分析数据
        if not self._enabled():
            # 处理缺少配置的情况下日志记录不到具体分析类型的问题
            business_type = self._business_type
            if business_type is None:
                business_type = self._key_business_type
            logging.getLogger(__name__).info("{} 分析未启用".format(business_type))
            return 1
        # 读取业务类型
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))
        # 扫描待分析的文件夹
        date_dirs = self._scan_analyze_directory()
        logging.getLogger(__name__).info(f"待处理日期列表：{date_dirs.keys()}")
        if self._reanalyze_detail_data:
            path = os.getcwd()
            error_occurred = False
            for date_str, full_path in date_dirs.items():
                os.chdir(full_path)
                logging.getLogger(__name__).info(f"处理文件夹：{date_str}")
                # 跑普惠相关数据余额明细分析
                detail_result = detain_main()
                if detail_result != 0:
                    logging.error(f"分析文件夹出错，分析结果：{detail_result}")
                    error_occurred = True
                    break
            if error_occurred:
                logging.getLogger(__name__).error("分析 {} 数据时出错".format(self._business_type))
                return 1
            logging.getLogger(__name__).info(f"完成所有日期的分析：{date_dirs.keys()}")
            os.chdir(path)

        # 日均分析
        manager_sum = pd.DataFrame()
        branch_sum = pd.DataFrame()
        first = True
        for date_str, full_path in date_dirs.items():
            real_src_filepath = os.path.join(full_path, self._src_filepath)
            logging.getLogger(__name__).info("读取源文件：{}".format(real_src_filepath))
            data_manager = pd.read_excel(
                real_src_filepath,
                sheet_name=self._manager_sheet_name,
                header=self._manager_header_row
            )
            data_branch = pd.read_excel(
                real_src_filepath,
                sheet_name=self._branch_sheet_name,
                header=self._branch_header_row
            )
            if first:
                first = False
                for column_key in self._manager_base_columns:
                    column_index = calculate_column_index(column_key)
                    self._manager_base_columns_names.append(data_manager.columns[column_index])
                for column_key in self._manager_avg_columns:
                    column_index = calculate_column_index(column_key)
                    self._manager_avg_columns_names.append(data_manager.columns[column_index])
                for column_key in self._branch_base_columns:
                    column_index = calculate_column_index(column_key)
                    self._branch_base_columns_names.append(data_branch.columns[column_index])
                for column_key in self._branch_avg_columns:
                    column_index = calculate_column_index(column_key)
                    self._branch_avg_columns_names.append(data_branch.columns[column_index])

            # 将各天的数据统计到一个 dataframe
            manager_sum = pd.concat([manager_sum, data_manager])
            branch_sum = pd.concat([branch_sum, data_branch])

        # 求均值
        manager_result = manager_sum.groupby(self._manager_base_columns_names)[self._manager_avg_columns_names].mean()
        manager_result = manager_result.reset_index()
        branch_result = branch_sum.groupby(self._branch_base_columns_names)[self._branch_avg_columns_names].mean()
        branch_result = branch_result.reset_index()

        manager_result.to_excel(
            excel_writer=self._excel_writer,
            index=False,
            sheet_name=self._manager_sheet_name,
        )
        branch_result.to_excel(
            excel_writer=self._excel_writer,
            index=False,
            sheet_name=self._branch_sheet_name,
        )

        logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
        return 0
