from . import session
class APPOINTMENTS(object):

    def __init__(self, appointment_startdate=None, appointment_enddate=None, appointment_id=None, fake_count=1):
        self.appointment_startdate = appointment_startdate
        self.appointment_enddate = appointment_enddate
        self.appointment_id = appointment_id
        self.fake_count = fake_count

    @classmethod
    def appointment_list(cls, appointment_startdate=None, appointment_enddate=None):
        """
            Appointment startdate format: YYYY-MM-DD
            Appointment endate format: YYYY-MM-DD
        """
        path = 'https://drchrono.com/api/appointments?since={}'.format(appointment_startdate)
        list_response = []
        while path:
            data = session.get(path).json()
            list_response.extend(data['results'])
            path = data['next'] # A JSON null on the last page
        return list_response

    @classmethod
    def appointment_single(cls, appointment_id):
        path = 'https://drchrono.com/api/appointments/{}'.format(appointment_id)
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)