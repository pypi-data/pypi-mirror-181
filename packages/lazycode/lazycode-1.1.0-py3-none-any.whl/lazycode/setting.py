from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

RESOURCE_DIR = Path(BASE_DIR).joinpath('resource')
CODE_DATA_DIR = Path(RESOURCE_DIR).joinpath('code_data')
TEMP_DIR = Path(RESOURCE_DIR).joinpath('temp')


random_data_file = Path(CODE_DATA_DIR).joinpath('random_data.json')




