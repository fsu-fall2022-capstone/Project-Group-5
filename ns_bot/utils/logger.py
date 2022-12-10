import logging
import logging.handlers


class Logger:
    __slots__ = ("logger",)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)

    def __init__(self, name) -> None:
        self.logger = logging.getLogger(f"nations.{name}")
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(self.handler)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)


def setup_discord_loggers():
    discord_http_logger = logging.getLogger("discord.http")
    discord_http_logger.setLevel(logging.INFO)
    discord_http_logger.addHandler(Logger.handler)

    dpy_logger = logging.getLogger("discord")
    dpy_logger.setLevel(logging.INFO)
    dpy_logger.addHandler(Logger.handler)
