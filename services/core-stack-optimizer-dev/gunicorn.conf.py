from src.util.config_loader import Config

bind = Config.value("port")
workers = Config.value("workers")
