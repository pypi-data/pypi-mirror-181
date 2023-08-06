import os
import requests
import json
from dotenv import load_dotenv

# import keys 
load_dotenv()

"""
documentation section: https://app.drchrono.com/api-docs/#section/Introduction 
"""

API_TOKEN = os.environ.get('DRCHRONO_API_TOKEN')
BASE_URL = "https://drchrono.com/api/"

### Initial a initial session 
session = requests.Session()
session.headers = {}
session.headers['Authorization'] = 'Bearer %s' % API_TOKEN

class APIKeyMissingError(Warning):
    pass

if not API_TOKEN:
    print("""All production methods require an API access token that is valid for 48 hours. 
        If you are planning on using the fake endpoints, 
        you can still use the package without an API key.
        """)

from .admin_doctors import DOCTORS
from .admin_users import USERS 
from .clinical_appointments import APPOINTMENTS
from .clinical_documents import DOCUMENTS
from .clinical_medications import MEDICATIONS
from .clinical_patients import PATIENTS
from .fake_data import FAKER
