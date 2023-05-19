"""
Purpose: Read the configurations from yaml file
"""
import yaml


# this method is to read the configuration from backup.conf
def file_reader(file_name):
    """
    :param file_name:
    :return: all the configuration constants
    """
    with open(file_name, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
