import pandas as pd
import os

# Load the JSON file created in Task 1
json_file = "data/trends_20260923.json"
df = pd.read_json(json_file)

# Print the number of rows loaded
print("Loaded", len(df), "stories from", json_file)

# Remove duplicate stories using post_id
df = df.drop_duplicates(subset="post_id")

print("After removing duplicates:", len(df))

# Remove rows with missing important values
df = df.dropna(subset=["post_id", "title", "score"])

print("After removing nulls:", len(df))
# Remove stories with a score below 5
df = df[df["score"] >= 5]

print("After removing low scores:", len(df))
# Remove extra spaces from story titles
df["title"] = df["title"].str.strip()
# Make score and comments whole numbers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
# Save the cleaned data as a CSV file
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print("Saved", len(df), "rows to", output_file)

# Print the number of stories in each category
print("Stories per category:")
print(df["category"].value_counts())