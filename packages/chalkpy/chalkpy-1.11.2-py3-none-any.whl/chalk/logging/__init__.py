import logging
from typing import Optional

import chalk.utils.log_with_context


class _UserLoggerFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.is_user_logger = True
        return True


def get_logger(name: Optional[str]):
    logger = chalk.utils.log_with_context.get_logger(name)
    logger.addFilter(_UserLoggerFilter())
    return logger
