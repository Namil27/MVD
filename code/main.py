import re
import numpy as np
import pandas as pd
import missingno as msno
from matplotlib import pyplot as plt
import seaborn as sns

"""pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
csv_file = pd.read_csv("monster_com_job_sample.csv")
for _ in csv_file:
    uniq = len(csv_file[_].unique())
    if uniq == 22000:
        print(print(f"{_}: все значения уникальны.\n\n"))
    else:
        print(print(f"{_}: не все значения уникальны.\n\n"))"""
"""
print([_ for _ in csv_file])

save = set()
for _ in csv_file["country"]:
    save.add(_)
print(save)


save1 = set()
for _ in csv_file["country_code"]:
    save1.add(_)
print(save1)


save11 = set()
for _ in csv_file["has_expired"]:
    save11.add(_)
print(save11)

save111 = set()
for _ in csv_file["job_board"]:
    save111.add(_)
print(save111)
"""
"""import pandas as pd

patterns = {
    'city_state_zip': r'^[A-Za-z .\-]+,\s*[A-Z]{2}\s*\d{5}$',
    'city_state': r'^[A-Za-z .\-]+,\s*[A-Z]{2}$',
    'state_zip': r'^[A-Z]{2}\s*\d{5}$',
    'state_only': r'^[A-Z]{2}$',
    'zip_only': r'^\d{5}$',
    'city_only': r'^[A-Za-z .\-]+$',
}


def detect_location_format(location):
    if pd.isna(location):
        return 'unknown'
    for name, pattern in patterns.items():
        if re.match(pattern, location.strip()):
            return name
    return 'unknown'


df = pd.read_csv('monster_com_job_sample.csv')

df['location_format'] = df['location'].astype(str).map(detect_location_format)

format_counts = df['location_format'].value_counts()

format_counts.plot(kind='bar', figsize=(10, 6))
plt.title('Форматы значений в столбце location')
plt.xlabel('Формат')
plt.ylabel('Количество')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plot1.png")
"""
df = pd.read_csv('monster_com_job_sample.csv')
df_unknown_location = df[df['location_format'] == 'unknown'].copy()
df_valid_location = df[df['location_format'] != 'unknown'].copy()

def extract_location_parts(location):
    city = state = zip_code = None
    location = location.strip()

    zip_match = re.search(r'\b\d{5}\b', location)
    if zip_match:
        zip_code = int(zip_match.group())

    state_match = re.search(r'\b[A-Z]{2}\b', location)
    if state_match:
        state = state_match.group()

    if ',' in location:
        city_part = location.split(',')[0]
        city = city_part.strip()
    else:
        parts = location.split()
        for part in parts:
            if not re.fullmatch(r'[A-Z]{2}|\d{5}', part):
                city = part.strip()
                break

    return pd.Series([city, state, zip_code])

df_valid_location[['city', 'state', 'zip']] = df_valid_location['location'].apply(extract_location_parts)

print(df_valid_location[['location', 'city', 'state', 'zip']].head())