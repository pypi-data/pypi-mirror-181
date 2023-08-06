# drchrono-wrapper

## Requirements 
- checkout the requirements.txt file 
- min. python version: 3.10 because of switch statement utilization that is only available starting with python 3.10

## API token requirement
- please visit for more information on how to generate: https://app.drchrono.com/api-docs/#section/Authorization 
- first load in the package and set the API token: 
    - `from drchrono.drc import drc` 
    - load in API token from .env: 
        - `drc_client = drc(api_key=os.getenv('DRCHRONO_API_TOKEN'))`
    - type in API token manually (not recommended):
        - `drc_client = drc(api_key=123321asddsa321123)`

## Endpoints currently covered: 
- *Fake data generation*:
    - Admin: 
        - Users 
        - Doctors 
    - Clinical: 
        - Patients 
        - Appointments 

- *Real data pulls*: 
    - Admin: 
        - Users 
        - Doctors 
    - Clinical: 
        - Patients 
        - Appointments 
        - Medications 
        - Documents

## Basic examples: 

### Getting real data: 
- Get all patients: 
    - `patient_all = drc_client.patients().patientlist`
    - If you want additional metadata, like custom demographics, add on verbose_true=True
        - `patient_all = drc_client.patients().patientlist(verbose_true=True)`
- Get a single patient: 
    - `patient_single = drc_client.patients().patient_single(patient_id='200110461')`
- Get a list of all doctors: 
    - `doctor_list = drc_client.doctors().doctorlist`
- Get a list of all appointments (requires a specific start date):
    - `appointments = drc_client.appointments().appointment_list(appointment_startdate='2019-01-01')`
- Pushing a existing pdf into a patient record as a document: 
    - Load the file: `files = {'document': open('src/new_test_myfile.pdf', 'rb')}`
    - Send the data over: `drc_client.documents().create_document(date='2017-01-01', description='testdocumentnov21_ANOTHER ONE' doctor=os.getenv('DRCHRONO_DOCTOR_ID'), patient=os.getenv('DRCHRONO_PATIENT_ID'), metatags='["fake-pdf", "document"]', document=files)`

### Generating fake dataset: 
- Fake dataset with linked patients and appointments; fake users and doctors; 
    - `f_users, f_doctors, f_patients, f_appointments = drc.faker().generate(20, 40, 150, 500)`

## Package admin: 
- Note to self, to create new version: 
    - update setup.py version number 
    - re-run `python setup.py sdist` to create new distribution 
    - upload to pypi with `twine upload dist/*` 