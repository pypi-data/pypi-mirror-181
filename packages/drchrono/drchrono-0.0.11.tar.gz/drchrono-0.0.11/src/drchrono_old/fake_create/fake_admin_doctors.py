
from faker import Faker

def doctorlist_fake(fake_count):
    localeList = ['en-US']
    fake = Faker(localeList)
    list_response = []
    for i in range(fake_count):
        dictionaryResponse = {
            "cell_phone": fake.phone_number(),  
            "country": fake.random_element(elements=('US', 'MX', 'CA', 'BD', 'IN')), 
            "email": fake.email(), 
            "first_name": fake.first_name(), 
            "group_npi_number": fake.numerify(text='##########'),
            "home_phone": fake.phone_number(),
            "id": fake.numerify(text='######'),
            "is_account_suspended": fake.boolean(),
            "job_title": fake.random_element(elements=('Provider/Staff', 'Provider/Admin')),
            "last_name": fake.last_name(),
            "npi_number": fake.numerify(text='##########'),
            "office_phone": fake.phone_number(),
            "practice_group": fake.numerify(text='######'),
            "practice_group_name": fake.company(),
            "profile_picture": fake.image_url(),
            "specialty": fake.random_element(elements=('Psychiatrist', 'Psychologist', 'Caremanager', 'Nurse', 'Social Worker', 'Gastroenterologist', 'Dermatologist', 'Cardiologist', 'Neurologist', 'Oncologist', 'Ophthalmologist', 'Orthopedic Surgeon', 'Pediatrician', 'Family Physician', 'General Practitioner', 'Internist', 'Obstetrician/Gynecologist', 'Surgeon', 'Urologist', 'Endocrinologist', 'Infectious Disease Specialist', 'Nephrologist', 'Pulmonologist', 'Rheumatologist', 'Allergist/Immunologist', 'Anesthesiologist', 'Emergency Medicine Specialist', 'Hematologist/Oncologist', 'Neonatologist', 'Neurosurgeon', 'Radiologist', 'Sports Medicine Specialist', 'Vascular Surgeon', 'Other')),
            "suffix": fake.suffix(),
            "timezone": fake.random_element(elements=('US/Central', 'US/Western', 'US/Eastern', 'US/Mountain', 'US/Pacific', 'US/Alaska', 'US/Hawaii', 'US/Arizona', 'US/Indiana-Starke', 'US/Michigan', 'US/Pacific-New', 'US/Samoa')),
            "website": fake.url()
            }
        list_response.append(dictionaryResponse)
    return list_response