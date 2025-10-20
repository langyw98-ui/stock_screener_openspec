import logging
import logging.config
import os
import yaml

def setup_logging(default_path='config/logging_config.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    :param default_path: Path to the logging configuration file
    :param default_level: Default logging level
    :param env_key: Environment variable name to get the logging config path
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                return True
            except Exception as e:
                print(f'Error in Logging Configuration: {e}')
                logging.basicConfig(level=default_level)
                return False
    else:
        logging.basicConfig(level=default_level)
        return False

def get_logger(name):
    """
    Get a logger instance
    :param name: Logger name
    :return: Logger instance
    """
    return logging.getLogger(name)