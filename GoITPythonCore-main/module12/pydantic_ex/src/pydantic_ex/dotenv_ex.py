from dotenv import load_dotenv
import os


#python-dotenv
# Load environment variables from .env file

# env_path = Path("/path/to/your/.env")
# load_dotenv(dotenv_path=env_path)

load_dotenv()

# Access variables
debug = os.getenv("DEBUG")
secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

print(f"DEBUG = {debug}")
print(f"SECRET_KEY = {secret_key}")
print(f"DATABASE_URL = {database_url}")
