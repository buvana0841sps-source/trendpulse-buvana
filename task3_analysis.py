import pandas as pd
import numpy as np

# Load the cleaned CSV from Task 2
csv_file = "data/trends_clean.csv"
df = pd.read_csv(csv_file)

# Print the first 5 rows
print("First 5 rows:")
print(df.head())

# Print the number of rows and columns
print("Shape:", df.shape)

# Calculate average score and comments
print("Average score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())
# Calculate statistics using NumPy
scores = df["score"].to_numpy()

print("--- NumPy Stats ---")
print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Standard deviation:", np.std(scores))
print("Highest score:", np.max(scores))
print("Lowest score:", np.min(scores))
# Find the category with the most stories
category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()

print("Most stories in:", most_common_category, 
      "(", category_counts.max(), "stories)")

# Find the story with the most comments
most_commented = df.loc[df["num_comments"].idxmax()]

print("Most commented story:", most_commented["title"],
      "-", most_commented["num_comments"], "comments")
# Calculate engagement for each story
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Mark stories whose score is above the average score
average_score = df["score"].mean()
df["is_popular"] = df["score"] > average_score
# Save the analysed data for Task 4
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print("Saved to", output_file)