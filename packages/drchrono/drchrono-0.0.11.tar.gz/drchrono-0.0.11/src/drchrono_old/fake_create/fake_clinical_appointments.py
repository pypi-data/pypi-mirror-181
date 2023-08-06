from faker import Faker
import datetime
import random

def appointment_list_fake(fake_count, pt_ids, doc_ids):
    localeList = ['en-US']
    fake = Faker(localeList)
    list_response = []
    start_date = datetime.datetime.now() - datetime.timedelta(days=1095)
    end_date = datetime.datetime.now() + datetime.timedelta(days=30)
    for i in range(fake_count):
        dictionaryResponse = {
                "allow_overlapping": fake.boolean(),
                "appt_is_break": fake.boolean(),
                "base_recurring_appointment": fake.boolean(),
                "billing_notes": [
                    {
                    "appointment": fake.numerify(text='######'),
                    "created_at": fake.date_between(start_date, end_date).isoformat(),
                    "created_by": fake.numerify(text='######'),
                    "id": fake.numerify(text='######'),
                    "text": fake.paragraph(nb_sentences=5)
                    }
                ],
                "billing_provider": fake.numerify(text='######'),
                "billing_status": fake.random_element(elements=('No Show', 'Pain In Full', 'Cancelled', 'Balance Due')),
                "clinical_note": {
                    "locked": fake.boolean(),
                    "pdf": fake.boolean(),
                    "updated_at": fake.date_between(start_date, end_date).isoformat()
                },
                "cloned_from": fake.numerify(text='######'),
                "color": fake.random_element(elements=('#BFBFFF', '#FF7F05', '#9932CC', '#228B22')),
                "created_at": fake.date_between(start_date, end_date).isoformat(),
                "custom_fields": [
                    {
                    "created_at": fake.date_between(start_date, end_date).isoformat(),
                    "field_type": fake.random_element(elements=('category', 'date', 'dropdown', 'number', 'text')),
                    "field_value": fake.text(max_nb_chars=20),
                    "updated_at": fake.date_between(start_date, end_date).isoformat()
                    }
                ],
                "custom_vitals": [
                    {
                    "value": fake.numerify(text='##'),
                    "vital_type": fake.text(max_nb_chars=20)
                    }
                ],
                "deleted_flag": fake.boolean(),
                "doctor": random.choice(doc_ids),
                "duration": fake.random_element(elements=('15', '30', '45', '60', '90')),
                "exam_room": fake.numerify(text='######'),
                "extended_updated_at": fake.date_between(start_date, end_date).isoformat(),
                "first_billed_date": fake.date_between(start_date, end_date).isoformat(),
                "icd10_codes": 
                    [fake.random_element(elements=('A00', 'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A48', 'A49', 'A50', 'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57', 'A58', 'A59', 'A60', 'A61', 'A62', 'A63', 'A64', 'A65', 'A66', 'A67', 'A68', 'A69', 'A70', 'A71', 'A72', 'A73', 'A74', 'A75', 'A76', 'A77', 'A78', 'A79', 'A80', 'A81', 'A82', 'A83', 'A84', 'A85', 'A86', 'A87', 'A88', 'A89', 'A90', 'A91', 'A92', 'A93', 'A94', 'A95', 'A96', 'A97', 'A98', 'A99', 'B00', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 
                    'B17', 'B18', 'B19', 'B20', 'B21', 'B22')) for i in range(random.randint(0,10))],
                "icd9_codes":
                    [fake.random_element(elements=('A00', 'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A48', 'A49', 'A50', 'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57', 'A58', 'A59', 'A60', 'A61', 'A62', 'A63', 'A64', 'A65', 'A66', 'A67', 'A68', 'A69', 'A70', 'A71', 'A72', 'A73', 'A74', 'A75', 'A76', 'A77', 'A78', 'A79', 'A80', 'A81', 'A82', 'A83', 'A84', 'A85', 'A86', 'A87', 'A88', 'A89', 'A90', 'A91', 'A92', 'A93', 'A94', 'A95', 'A96', 'A97', 'A98', 'A99', 'B00', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 
                    'B17', 'B18', 'B19', 'B20', 'B21', 'B22')) for i in range(random.randint(0,10))],
                "id": fake.numerify(text='######'),
                "ins1_status": fake.random_element(elements=('Arrived', 'Checked In', 'Checked Out', 'No Show', 'Scheduled', 'Waiting')),
                "ins2_status": fake.random_element(elements=('Arrived', 'Checked In', 'Checked Out', 'No Show', 'Scheduled', 'Waiting')),
                "is_virtual_base": fake.boolean(),
                "is_walk_in": fake.boolean(),
                "last_billed_date": fake.date_between(start_date, end_date).isoformat(),
                "notes": fake.sentences(nb=10),
                "office": fake.numerify(text='######'),
                "patient": random.choice(pt_ids),
                "primary_insurance_id_number": fake.numerify(text='###########'),
                "primary_insurer_name": fake.company(),
                "primary_insurer_payer_id": fake.numerify(text='########'),
                "profile": fake.numerify(text='######'),
                "reason": fake.random_element(elements=('Pain', 'Sick', 'Other')),
                "recurring_appointment": fake.boolean(),
                "reminder_profile": fake.numerify(text='######'),
                "reminders": [
                    {
                    "id": fake.numerify(text='######'),
                    "scheduled_time": fake.date_between(start_date, end_date).isoformat(),
                    "type": fake.random_element(elements=('SMS', 'Email', 'Phone Call'))
                    }
                ],
                "scheduled_time": fake.date_between(start_date, end_date).isoformat(),
                "secondary_insurance_id_number": fake.pystr(),
                "secondary_insurer_name": fake.company(),
                "secondary_insurer_payer_id": fake.pystr(),
                "status": fake.random_element(elements=('Arrived', 'Checked In', 'Cancelled', 'Checked Out', 'No Show', 'Scheduled', 'Waiting')),
                "status_transitions": [
                    {
                    "appointment": fake.numerify(text='######'),
                    "datetime": fake.date_between(start_date, end_date).isoformat(),
                    "from_status": fake.random_element(elements=('Arrived', 'Checked In', 'Cancelled', 'Checked Out', 'No Show', 'Scheduled', 'Waiting')),
                    "to_status": fake.random_element(elements=('Arrived', 'Checked In', 'Cancelled', 'Checked Out', 'No Show', 'Scheduled', 'Waiting'))
                    }
                ],
                "supervising_provider": fake.numerify(text='######'),
                "vitals": {
                    "blood_pressure_1": fake.numerify(text='###'),
                    "blood_pressure_2": fake.numerify(text='##'),
                    "bmi": fake.numerify(text='##'),
                    "head_circumference": fake.numerify(text='##'),
                    "head_circumference_units": fake.random_element(elements=('cm', 'in')),
                    "height": fake.numerify(text='##'),
                    "height_units": fake.random_element(elements=('cm', 'in')),
                    "oxygen_saturation": fake.numerify(text='##'),
                    "pain": fake.random_element(elements=('None', 'Mild', 'Moderate', 'Severe')),
                    "pulse": fake.numerify(text='##'),
                    "respiratory_rate": fake.numerify(text='##'),
                    "smoking_status": fake.random_element(elements=('Current', 'Former', 'Never', 'Unknown')),
                    "temperature": fake.numerify(text='##'),
                    "temperature_units": fake.random_element(elements=('C', 'F')),
                    "weight": fake.numerify(text='##'),
                    "weight_units": fake.random_element(elements=('kg', 'lb'))
                },
                "updated_at": fake.date_between(start_date, end_date).isoformat()
        }
        
        list_response.append(dictionaryResponse)

    return list_response