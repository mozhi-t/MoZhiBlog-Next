"""
Logger - 日志配置模块
提供同时输出到控制台和按天分割的日志文件功能
"""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


def setup_logger(
    log_level: str = "INFO",
    log_dir: str = None,
    log_filename_prefix: str = "mblog_log",
    backup_count: int = 30
) -> logging.Logger:
    # 获取项目根目录
    project_root = Path(__file__).resolve().parent.parent

    # 设置日志目录
    if log_dir is None:
        log_dir = project_root / "logs"
    else:
        log_dir = Path(log_dir)

    # 确保日志目录存在
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"警告: 无法创建日志目录 {log_dir}，请检查目录权限")
        log_dir = Path(".")
    except Exception as e:
        print(f"警告: 创建日志目录失败: {e}，日志将仅输出到控制台")
        log_dir = None

    # 创建 logger
    logger = logging.getLogger("mblog")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 定义日志格式
    file_formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台日志格式
    console_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 添加文件处理器
    if log_dir and log_dir.exists():
        try:
            log_file = log_dir / f"{log_filename_prefix}_{datetime.now().strftime('%Y-%m-%d')}.log"

            # 使用 TimedRotatingFileHandler 按天分割
            file_handler = TimedRotatingFileHandler(
                filename=str(log_file),
                when="midnight",  # 午夜分割
                interval=1,
                backupCount=backup_count,
                encoding="utf-8"
            )

            # 设置日志文件名格式
            file_handler.suffix = "%Y-%m-%d.log"

            # 设置文件日志级别
            file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        except PermissionError:
            logger.warning(f"警告: 无法写入日志文件 {log_file}，请检查文件权限")
        except Exception as e:
            logger.warning(f"警告: 创建日志文件处理器失败: {e}")

    return logger


# 创建默认日志实例
logger = setup_logger()
