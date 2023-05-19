from scripts.constants.app_constants import CONFIGURATION_FILE
from scripts.utilities.yaml_reader import file_reader

app_config = file_reader(CONFIGURATION_FILE)
