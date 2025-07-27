import pandas as pd
from datetime import datetime, timedelta
import re  # Import the regular expression module

# Load the CSV file
file_path = 'data/newest_gm_reviews.csv'
df = pd.read_csv(file_path)

# 1. Remove unnecessary columns if needed (e.g., 'url_user' if mostly empty)
df.drop(columns=['url_user'], inplace=True)

# 2. Fill missing values in 'caption' with 'No Caption'
df['caption'].fillna('No Caption', inplace=True)

# 3. Reformat the 'place_name' column
df['place_name'] = df['place_name'].str.replace('+', ' ')

# 4. Convert 'relative_date' to a standard date format (if it's in a relative time format)
def convert_relative_date(relative_date, retrieval_date):
    retrieval_datetime = datetime.strptime(retrieval_date, '%Y-%m-%d %H:%M:%S.%f')
    time_values = re.findall(r'(\d+)\s(\w+)', relative_date)
    
    if time_values:
        quantity, unit = int(time_values[0][0]), time_values[0][1]
        if 'minute' in unit:
            final_date = retrieval_datetime - timedelta(minutes=quantity)
        elif 'hour' in unit:
            final_date = retrieval_datetime - timedelta(hours=quantity)
        elif 'day' in unit:
            final_date = retrieval_datetime - timedelta(days=quantity)
        elif 'week' in unit:
            final_date = retrieval_datetime - timedelta(weeks=quantity)
        elif 'month' in unit:
            final_date = retrieval_datetime - timedelta(days=quantity * 30)
        elif 'year' in unit:
            final_date = retrieval_datetime - timedelta(days=quantity * 365)
        return final_date.strftime('%Y-%m-%d %H:%M:%S')
    return relative_date

df['relative_date'] = df.apply(lambda row: convert_relative_date(row['relative_date'], row['retrieval_date']), axis=1)

# 5. Save the cleaned data to a new CSV file
cleaned_file_path = 'data/cleaned_gm_reviews.csv'
df.to_csv(cleaned_file_path, index=False, encoding='utf-8')

print(f"Cleaned data saved to {cleaned_file_path}")
