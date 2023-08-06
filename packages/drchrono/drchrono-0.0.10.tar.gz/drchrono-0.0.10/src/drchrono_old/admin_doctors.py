from . import session

class DOCTORS(object):

    """
    https://app.drchrono.com/api-docs/#tag/Administrative/operation/doctors_list

    """

    def __init__(self, doctor_id=None, fake_count=1):
        self.doctor_id = doctor_id
        self.fake_count = fake_count

    @staticmethod
    def doctorlist():
        path = 'https://app.drchrono.com/api/doctors'
        list_response = []

        while path:
            data = session.get(path)
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next'] 
        
        return list_response
            
    @classmethod
    def doctor_single(cls, doctor_id):
        path = 'https://app.drchrono.com/api/doctors/{}'.format(doctor_id)
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)





