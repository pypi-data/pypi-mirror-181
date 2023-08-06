import logging
import random
from abc import ABCMeta, abstractmethod

from pytest_xlsx.file import XlsxItem

logger = logging.getLogger(__name__)


class Runner(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, item: XlsxItem):
        """
        :param item: pytest用例对象
        :return:
        """


class PrintRunner(Runner):
    def execute(self, item: XlsxItem):
        print("-" * 10)
        print(f"当前用例id：{item.nodeid}")
        print(f"当前用例名称：{item.name}")
        print(f"当前用例步骤：{item.current_step}")
        print(f"当前用例步骤序号：{item.current_step_no}")
        print(f"最大用例步骤序号：{item.max_step_no}")
        print(f"当前是否第一个步骤：{item.is_first_step}")
        print(f"当前是否最后一个步骤：{item.is_last_step}")

        if item.is_last_step:
            print("=" * 20)
        elif item.current_step_no == random.randint(1, 9):
            ...
            # 1 / 0  # 随机报错，展示报错效果
