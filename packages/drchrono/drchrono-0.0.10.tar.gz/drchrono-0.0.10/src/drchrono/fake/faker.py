from .admin_doctors import *
from .admin_users import *
from .clinical_appointments import *
from .clinical_patients import *

class faker(object):

    def __init__(self, fakecount_adminuser=None, fakecount_admindocs=None, fakecount_clin_patients=None, fakecount_clin_appt=None, **kwargs):
        self.fakecount_adminuser = fakecount_adminuser
        self.fakecount_admindocs = fakecount_admindocs
        self.fakecount_clin_patients = fakecount_clin_patients
        self.fakecount_clin_appt = fakecount_clin_appt

    @classmethod
    def generate(cls, fakecount_adminuser=None, fakecount_admindocs=None, fakecount_clin_patients=None, fakecount_clin_appt=None):
        
        adm_users = userlist_fake(fakecount_adminuser)
        adm_docs = doctorlist_fake(fakecount_admindocs)

        # get a unique list of id's from docs dictionary
        doc_ids = []
        for i in adm_docs:
            doc_ids.append(i['id'])
        
        clin_pts = patientlist_fake(fakecount_clin_patients, doc_ids)

        pt_ids = []
        for i in clin_pts:
            pt_ids.append(i['id'])        
            
        clin_appts = appointment_list_fake(fakecount_clin_appt, pt_ids, doc_ids)

        return adm_users, adm_docs, clin_pts, clin_appts
