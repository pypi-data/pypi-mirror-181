import os
import tempfile

TEMP_FOLDER = tempfile.gettempdir()
FONT_CACHE_DIR = f'/{TEMP_FOLDER}/'

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

API_ROUND_DECIMAL_FIELDS = 2
