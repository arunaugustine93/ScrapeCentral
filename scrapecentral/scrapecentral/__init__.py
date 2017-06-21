# import csv
# import os.path
#
#
# detail_field_set = ['drug_arrest', 'DOB', 'treat_last_visit', 'city', 'prequalifies', 'qualify_condition', 'phy_fax_work', 'patient_name', 'location', 'patient_note', 'zip', 'rec_date', 'address1', 'phone', 'prior_rec', 'recent_medicine', 'valid_identification', 'appointment_type', 'onset_month', 'address_data', 'rec_state', 'uploaded_files', 'sex', 'phy_lname', 'ins_name', 'first_choice', 'lname', 'state', 'fname', 'ins_coverage', 'email', 'phy_fname', 'titration_history', 'adult_18', 'general_availability', 'phone2', 'current_parole_probation', 'prescription_meds', 'current_treat', 'onset_yr', 'current_NYresident', 'state_residence', 'prescribed', 'phy_phone_work', 'med_records', 'second_choice']
#
# filepath = '/home/sayone/projects/Scrapy/scrapecentral/scrapecentral/md_data.csv'
# print '++++++++++++++++++\n\n\n\n', os.path.exists(filepath)
# if os.path.exists(filepath) is False:
#     with open('md_data.csv', 'a') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=detail_field_set)
#         writer.writeheader()
