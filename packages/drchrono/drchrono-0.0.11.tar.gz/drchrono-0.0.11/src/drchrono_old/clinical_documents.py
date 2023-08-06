from . import session
class DOCUMENTS(object):

    def __init__(self, date=None, description=None, doctor=None, document=None, patient=None, archieved=None, metatags=None):
        self.date = date
        self.description = description
        self.doctor = doctor
        self.document = document
        self.patient = patient
        self.archieved = archieved
        self.metatags = metatags

    @classmethod
    def create_document(cls, date, description, doctor, document, patient, metatags):
        """
            Create a document
        """
        path = 'https://drchrono.com/api/documents'
        data = {
            'date': date,
            'description': description,
            'doctor': doctor,
            'patient': patient,
            'metatags': metatags,
        }
        file=document
        try:
            data = session.post(path, data, files=file)
            data_json = data.json()
            return data_json

        except Exception as e:
            print(e)