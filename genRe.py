import os 
import pandas as pd 

policy_data = pd.read_csv('genre/policy_data.csv')
claims_data = pd.read_csv('genre/claims_data.csv')
policy_data = pd.DataFrame(policy_data)
claims_data = pd.DataFrame(claims_data)

### Q1 Inspect data
# policy_data.info()
# policy_data.describe()
# claims_data.info()
# claims_data.describe()

# Data cleaning
#Check that the data is between 2000/1/1 to 2015/12/31
policy_data['Effective Date'] = pd.to_datetime(policy_data['Effective Date'])
claims_data['Effective Date'] = pd.to_datetime(claims_data['Effective Date'])
claims_data['Event Date'] = pd.to_datetime(claims_data['Event Date'])
filtered_dates = policy_data[(policy_data['Effective Date'] < pd.Timestamp('2015-12-31')) | (policy_data['Effective Date'] > pd.Timestamp('2000-01-01'))]
bad_dates =  policy_data[(policy_data['Effective Date'] > pd.Timestamp('2015-12-31')) | (policy_data['Effective Date'] <= pd.Timestamp('2000-01-01'))]

#missing, duplicated, outliers
missing_policy = policy_data.isnull().sum() 
missing_claims = claims_data.isnull().sum()
#print('missing_policy is', missing_policy) 
#print('missing_claims is', missing_claims)

duplicates_policy = policy_data.duplicated().sum()
duplicates_claims = claims_data.duplicated().sum()
policy_data = policy_data.drop_duplicates()
duplicates_policy = policy_data.duplicated().sum()
#print('new duplicates_policy without duplicates is', duplicates_policy)
#print('duplicates_claims is', duplicates_claims)

policy_data = policy_data.dropna(subset=['Policy Number'])
claims_data = claims_data.dropna(subset=['Policy Number'])

mean_amount = policy_data['Face Amount (Dread Disease Benefit)'].mean() #234359.3843693784
std_amount = policy_data['Face Amount (Dread Disease Benefit)'].std() #317515.98039509484
policy_data['Amount Z-score'] = (policy_data['Face Amount (Dread Disease Benefit)'] - mean_amount) / std_amount 

# Define a threshold for outliers (e.g., z-score greater than 3 or less than -3)
outlier_threshold = 3
outliers = policy_data[(policy_data['Amount Z-score'] > outlier_threshold) | (policy_data['Amount Z-score'] < -outlier_threshold)]
# print('mean_amount is', mean_amount) 
# print('std_amount is', std_amount)
# print("policy_data['Amount Z-score'] is", policy_data[['Policy Number', 'Amount Z-score']])
# print('outliers is', outliers[['Policy Number', 'Face Amount (Dread Disease Benefit)', 'Amount Z-score']])

# Ensure all Policy IDs in claims are also in policy data
valid_claims_plan = claims_data[claims_data['Policy Number'].isin(policy_data['Policy Number'])]
#print('valid claim plans is')
#valid_claims_plan.info()

# Check all terminated due to claims data in policy_data are in claims_data
terminated_due_to_claim = policy_data[policy_data['End of Survey Period Coverage Status'] == 'Terminated due to Claim']['Policy Number']
terminated_due_to_claim.describe()

#Check that policy number and insuredID are the same. 
merged_data = pd.merge(policy_data, claims_data, on='Policy Number', suffixes=('_policy', '_claim'))
date_mismatch1 = merged_data[merged_data['Insured ID_policy'] != merged_data['Insured ID_claim']]
#print('data_mismatch is', date_mismatch1[['Policy Number', 'Insured ID_policy', 'Insured ID_claim']])

#Check that effective dates are the same 
date_mismatch2 = merged_data[merged_data['Effective Date_policy'] != merged_data['Effective Date_claim']]
#print('data_mismatch of effective start date is', date_mismatch2[['Policy Number', 'Effective Date_policy', 'Effective Date_claim']])

# Check that Plan Codes are the same 
date_mismatch3 = merged_data[merged_data['Plan Code (Dread Disease)_policy'] != merged_data['Plan Code (Dread Disease)_claim']]
date_mismatch4 = merged_data[merged_data['Plan Code (Basic Plan)_policy'] != merged_data['Plan Code (Basic Plan)_claim']]
#print('mismatch of plan code(dread disease)', date_mismatch3[['Policy Number', 'Plan Code (Dread Disease)_policy', 'Plan Code (Dread Disease)_claim']])
#print('mismatch of plan code (basic plan)', date_mismatch4[['Policy Number', 'Plan Code (Basic Plan)_policy', 'Plan Code (Basic Plan)_claim']])

#Check that Face Amount of Dread Disease Benefit and claimed amount is the same
date_mismatch5 = merged_data[merged_data['Face Amount (Dread Disease Benefit)_policy'] != merged_data['Face Amount (Dread Disease Benefit)_claim']]
#print('mismatch of face amount is', date_mismatch5[['Policy Number', 'Face Amount (Dread Disease Benefit)_policy', 'Face Amount (Dread Disease Benefit)_claim']])

#Check that each policy is only claimed once 
unique_policy_numbers = claims_data['Policy Number'].nunique()
unique_id = claims_data['Insured ID'].nunique()
#print('unique_id', unique_id)
#print('number of polices claimted is', unique_policy_numbers)

#Check that event date occus after effective date 
filter = claims_data['Event Date'] < claims_data['Effective Date']
filtered_data = claims_data[filter]
#print(filtered_data[['Policy Number','Effective Date','Event Date']])


### Q2 To determine the probability of illnesses 
# Filter data for Plan Code Z
policy_plan_z = policy_data[policy_data['Plan Code (Dread Disease)'] == 'Z']
claims_plan_z = claims_data[claims_data['Plan Code (Dread Disease)'] == 'Z']

# Filter by gender, age, etc.
claims_plan_z

# Calculate the number of policies and claims
num_policies = policy_plan_z['Insured ID'].nunique()
num_claims = claims_plan_z['Insured ID'].nunique()
incidence_rate = (num_claims / num_policies) * 100

# Output the results
print(f"Incidence Rate for Plan Code Z: {incidence_rate}%")