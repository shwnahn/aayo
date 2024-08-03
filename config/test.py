import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / './.env')
print(env('DB_HOST'))