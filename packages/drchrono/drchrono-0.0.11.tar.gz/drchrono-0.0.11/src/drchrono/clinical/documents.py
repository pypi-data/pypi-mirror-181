import requests 

class DOCUMENTS():

    def __init__(self, api_key, date=None, description=None, doctor=None, document=None, patient=None, archieved=None, metatags=None):
        self.date = date
        self.description = description
        self.doctor = doctor
        self.document = document
        self.patient = patient
        self.archieved = archieved
        self.metatags = metatags
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    def create_document(self, date, description, doctor, document, patient, metatags):
        """
            Create a document
        """
        path = 'https://drchrono.com/api/documents'
        data = {
            'date':date,
            'description': description,
            'doctor': doctor,
            'patient': patient,
            'metatags': metatags,
        }
        file=document
        try:
            data = requests.post(path, data, files=file, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json

        except Exception as e:
            print(e)