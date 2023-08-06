import logging
import os
from pathlib import Path

import pytest
from _pytest.logging import get_log_level_for_setting

from pytest_xlsx.file import XlsxFile
from pytest_xlsx.runner import PrintRunner, Runner
from pytest_xlsx.settings import settings

logger = logging.getLogger(__name__)


@pytest.fixture
def xlsx_runner() -> Runner:
    _runner = PrintRunner()
    return _runner


@pytest.fixture()
def xlsx_log_result(request):
    logger.debug(f"case is staring: {request.node.nodeid}")
    failed_a = request.session.testsfailed
    yield
    failed_b = request.session.testsfailed
    if bool(failed_b - failed_a):
        logger.warning(f"case is failed : {request.node.nodeid}")
    else:
        logger.debug(f"case is pass   : {request.node.nodeid}")


def pytest_addoption(parser):
    parser.addini(
        "xlsx_meta_column_name",
        default="标记",
        help="设置标记的列名",
    )


def pytest_configure(config):
    log_file = config.getini("log_file")
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    use_xdist = bool(config.getoption("tx", False))

    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(exist_ok=True)

    if use_xdist:
        config.option.dist = "loadscope"
        try:
            from xdist.dsession import DSession

            delattr(DSession, "pytest_collection")
        except (ImportError, AssertionError):
            pass

    if worker_id and log_file:  # Compatible with multiple processes
        new_filename = f"{log_file.stem}_{worker_id}{log_file.suffix}"
        log_file = log_file.parent / new_filename

        logging.basicConfig(
            format=config.getini("log_file_format"),
            filename=log_file,
            encoding="utf-8",
            level=get_log_level_for_setting(config.getini("log_file_level")),
        )

    xlsx_settings_dict = {
        "meta_column_name": config.getini("xlsx_meta_column_name"),
    }

    settings.reload_settings(xlsx_settings_dict)


def pytest_html_results_table_row(report, cells):
    """fix： pytest-html文件名乱码问题"""
    if report.fspath.endswith(".xlsx"):
        from py.xml import html

        cells[1] = html.td(report.nodeid, class_="col-name")


def pytest_collect_file(parent, file_path: Path):

    if file_path.suffix == ".xlsx" and file_path.name.startswith("test"):
        logger.debug(f"XlsxFile: {file_path.absolute()}")
        return XlsxFile.from_parent(parent, path=file_path)
