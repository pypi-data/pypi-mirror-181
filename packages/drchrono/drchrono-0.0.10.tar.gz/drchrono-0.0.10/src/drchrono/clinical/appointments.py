import requests

class APPOINTMENTS():

    def __init__(self, api_key, appointment_startdate=None, appointment_enddate=None, appointment_id=None, **kwargs):
        self.appointment_startdate = appointment_startdate
        self.appointment_enddate = appointment_enddate
        self.appointment_id = appointment_id
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    def appointment_list(self, appointment_startdate):
        """
            Appointment startdate format: YYYY-MM-DD
            Appointment endate format: YYYY-MM-DD
        """
        print('appointment_startdate:', appointment_startdate)
        path = 'https://drchrono.com/api/appointments?since={}'.format(appointment_startdate)
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key}).json()
            list_response.extend(data['results'])
            path = data['next'] # A JSON null on the last page
        
        return list_response

    def appointment_single(self, appointment_id):
        path = 'https://drchrono.com/api/appointments/{}'.format(appointment_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)