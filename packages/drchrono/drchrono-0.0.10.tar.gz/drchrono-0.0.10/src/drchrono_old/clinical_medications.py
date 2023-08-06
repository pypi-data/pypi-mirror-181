from . import session

class MEDICATIONS(object):

    def __init__(self, medication_id=None, patient_id=None):
        self.medication_id = medication_id
        self.patient_id = patient_id

    @staticmethod
    def medicationlist_types():
        dictionaryResponse = {
            "data": [
                {
                "appointment": 0,
                "date_prescribed": "string",
                "date_started_taking": "string",
                "date_stopped_taking": "string",
                "daw": "true",
                "dispense_quantity": 0,
                "doctor": 0,
                "dosage_quantity": "string",
                "dosage_units": "string",
                "frequency": "string",
                "id": 0,
                "indication": "string",
                "name": "string",
                "ndc": "string",
                "notes": "string",
                "number_refills": 0,
                "order_status": "",
                "patient": 0,
                "pharmacy_note": "string",
                "prn": "true",
                "route": "string",
                "rxnorm": "string",
                "signature_note": "string",
                "status": "active"
                }
            ],
            "next": "string",
            "previous": "string"
        }

        return dictionaryResponse

    @staticmethod
    def medicationlist():
        path = 'https://app.drchrono.com/api/medications'
        list_response = []
        while path:
            data = session.get(path)
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @classmethod
    def medication_patient(cls, patient_id):
        path = "https://app.drchrono.com/api/medications?patient=" + patient_id 
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

    @classmethod
    def medication_single(cls, medication_id):
        path = 'https://app.drchrono.com/api/medications/{}'.format(medication_id)
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

