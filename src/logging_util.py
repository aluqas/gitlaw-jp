"""Logging utility for Gitlaw-Jp pipeline."""

import logging
import os
import sys


def configure_logging(level_env: str = "LOG_LEVEL") -> None:
    """
    Configure logging for the Gitlaw-Jp pipeline.

    Reads the log level from the specified environment variable.
    Defaults to INFO if the variable is not set.

    Args:
        level_env: Environment variable name to read log level from.
    """
    level_str = os.environ.get(level_env, "INFO").upper()

    # Validate log level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level_str not in valid_levels:
        level_str = "INFO"

    level = getattr(logging, level_str)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create and configure StreamHandler (stdout)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Set formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(handler)

    root_logger.debug(f"Logging configured with level: {level_str}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Module name (typically __name__).

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
