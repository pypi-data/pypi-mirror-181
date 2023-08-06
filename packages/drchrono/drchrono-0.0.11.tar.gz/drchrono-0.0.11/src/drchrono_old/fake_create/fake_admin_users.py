from faker import Faker

def userlist_fake(fake_count):
    localeList = ['en-US']
    fake = Faker(localeList)
    list_response = []
    for i in range(fake_count):
        dictionaryResponse = {
            "doctor": fake.numerify(text='######'),
            "id": fake.numerify(text='######'),
            "is_doctor": fake.boolean(),
            "is_staff": fake.boolean(),
            "permissions": {
                'share_patients': fake.boolean(),
                'access_all_messages_for_practice_group': fake.boolean(),
                'show_patient_balance': fake.boolean(),
                'access_to_erx': fake.boolean(),
                'access_patient_payments': fake.boolean(),
                'emergency_access': fake.boolean(),
                'access_patient_analytics': fake.boolean(),
                'provider_dropdown': fake.boolean(),
                'create_and_update_patients': fake.boolean(),
                'appointment_provider_selection': fake.boolean(),
                'manage_templates': fake.boolean(),
                'access_to_message_center': fake.boolean(),
                'show_billing_summary': fake.boolean(),
                'access_patient_statements': fake.boolean(),
                'access_reports': fake.boolean(),
                'manage_accounts': fake.boolean(),
                'manage_permissions': fake.boolean(),
                'drug_interactions_check': fake.boolean(),
                'sign/lock_clinical_notes': fake.boolean(),
                'access_billing': fake.boolean(),
                'access_clinical_notes': fake.boolean(),
                'billing_administrator': fake.boolean(),
                'access_institutional_billing': fake.boolean(),
                'add_new_referring_sources': fake.boolean(),
                'export_patients': fake.boolean(),
                'use_ipad_ehr': fake.boolean(),
                'settings': fake.boolean(),
                'access_balance/ledger': fake.boolean(),
                'access_scheduling': fake.boolean(),
                'show_billing_tab': fake.boolean(),
                'create_and_update_contacts': fake.boolean(),
                'view_practice_group': fake.boolean()
            },
            "practice_group": fake.numerify(text='######'),
            "username": (fake.name()).replace(" ", "")
        }
        list_response.append(dictionaryResponse)
    return list_response