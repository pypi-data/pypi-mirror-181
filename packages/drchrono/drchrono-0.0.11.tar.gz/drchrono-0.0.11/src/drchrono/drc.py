from . import constants

from .clinical import appointments, documents, medications, patients
from .admin import doctors, users
from .fake import faker

"""
documentation section: https://app.drchrono.com/api-docs/#section/Introduction 
"""

class drc:

    """
    Entry point class providing ad-hoc API clients for each drChrono API.
    """

    def __init__(self, api_key=None):
        ## if api_key is None, display warning message
        assert api_key is not None, 'API Key must be set for real data retrieval'
        self.api_key = api_key

    @property
    def version(self):
        """
        Returns the current version of the Drchrono API wrapper library
        :returns: `tuple`
        """
        return constants.DRC_VERSION

    @property
    def version_patients(self):
        """
        Returns the current version of the Drchrono API wrapper library
        :returns: `tuple`
        """
        return constants.PATIENTS_API_VERSION

    ##### clinical section #####
    ##### clinical section #####
    ##### clinical section #####
    ##### clinical section #####

    def appointments(self):
        """
        Gives a `drc.patient_manager.appointments` instance that can be used to read/write data from the
        patient API.
        """
        return appointments.APPOINTMENTS(self.api_key)

    def documents(self):
        """
        Gives a `drc.patient_manager.documents` instance that can be used to read/write data from the
        patient API.
        """
        return documents.DOCUMENTS(self.api_key)

    def medications(self):
        """
        Gives a `drc.patient_manager.medications` instance that can be used to read/write data from the
        patient API.
        """
        return medications.MEDICATIONS(self.api_key)

    def patients(self):
        """
        Gives a `drc.patient_manager.patients` instance that can be used to read/write data from the
        patient API.
        """
        return patients.PATIENTS(self.api_key)

    ##### admin section ######
    ##### admin section ######
    ##### admin section ######
    ##### admin section ######

    def doctors(self):
        """
        Gives a `drc.admin.doctors` instance that can be used to read/write data from the
        patient API.
        """
        return doctors.DOCTORS(self.api_key)

    def users(self):
        """
        Gives a `drc.admin.users` instance that can be used to read/write data from the
        patient API.
        """
        return users.USERS(self.api_key)

    ##### fake section ######
    ##### fake section ######
    ##### fake section ######
    ##### fake section ######

    def faker():
        """
        Gives a `drc.fake.faker` instance that can be used to read/write data from the
        patient API.
        """
        return faker.faker()








