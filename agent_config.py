import argparse
import os
from typing import List, Optional, Dict, Any


class AgentConfig:
    """Agent配置类，支持命令行参数和交互模式"""

    # 运行模式常量
    MODE_INTERACTIVE = 1
    MODE_ARGS = 2

    # 报告类型常量
    REPORT_MONTHLY = 1
    REPORT_CHANGELOG = 2
    EXIT = 3

    def __init__(self):
        # 基础配置
        self.mode = self.MODE_INTERACTIVE

        # 报告类型选择
        self.choice = None

        # 月报参数
        self.month = None
        self.year = None

        # Changelog参数
        self.pr_num_list = []

        # 通用参数
        self.important_pr_list = []
        self.translate = True

    @classmethod
    def from_args(cls) -> 'AgentConfig':
        """从命令行参数构建配置"""
        parser = argparse.ArgumentParser(description='Higress报告生成工具')

        # 基本参数
        parser.add_argument('--mode', type=int, choices=[cls.MODE_INTERACTIVE, cls.MODE_ARGS],
                            default=cls.MODE_INTERACTIVE,
                            help='运行模式: 1=交互模式, 2=命令行参数模式')

        # 报告类型
        parser.add_argument('--choice', type=int, choices=[cls.REPORT_MONTHLY, cls.REPORT_CHANGELOG],
                            help='报告类型: 1=月报, 2=Changelog')

        # 月报相关参数
        parser.add_argument('--month', type=int, help='月份 (仅月报有效)')
        parser.add_argument('--year', type=int, help='年份 (仅月报有效)')

        # Changelog相关参数
        parser.add_argument('--pr_nums', type=str,
                            help='PR编号列表，逗号分隔 (仅Changelog有效)')

        # 通用参数
        parser.add_argument('--important_prs', type=str,
                            help='重要PR编号列表，逗号分隔')
        parser.add_argument('--no_translate', action='store_true',
                            help='设置此标志将不生成英文翻译')

        args = parser.parse_args()
        config = cls()

        if args.mode:
            config.mode = args.mode
        config.choice = args.choice

        # 设置月报参数
        if args.month:
            config.month = args.month
        if args.year:
            config.year = args.year

        # 设置Changelog参数
        if args.pr_nums:
            try:
                config.pr_num_list = [int(x.strip())
                                      for x in args.pr_nums.split(',')]
            except ValueError:
                raise ValueError("PR编号格式不正确，请输入数字")

        # 设置通用参数
        if args.important_prs:
            try:
                config.important_pr_list = [
                    int(x.strip()) for x in args.important_prs.split(',')]
            except ValueError:
                print("重要PR编号格式不正确，将忽略重要PR设置")
                config.important_pr_list = []

        config.translate = not args.no_translate

        config.validate()
        return config

    def validate(self) -> bool:
        """验证配置是否合法"""
        # 如果是命令行参数模式，需要检查必要的参数
        if self.mode == self.MODE_ARGS:
            if not self.choice:
                raise ValueError("必须指定报告类型 (--choice)")

            if self.choice == self.REPORT_CHANGELOG:
                if not self.pr_num_list:
                    raise ValueError("生成Changelog时必须提供PR编号列表 (--pr_nums)")

        return True

    # def get_report_params(self) -> Dict[str, Any]:
    #     """根据报告类型获取对应的参数字典"""
    #     params = {
    #         'translate': self.translate
    #     }

    #     # 添加重要PR
    #     if self.important_pr_list:
    #         params['important_pr_list'] = self.important_pr_list

    #     # 根据报告类型添加特定参数
    #     if self.choice == self.REPORT_MONTHLY:
    #         if self.month:
    #             params['month'] = self.month
    #         if self.year:
    #             params['year'] = self.year
    #     elif self.choice == self.REPORT_CHANGELOG:
    #         params['pr_num_list'] = self.pr_num_list

    #     return params
