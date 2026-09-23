import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# Load the analysed CSV from Task 3
csv_file = "data/trends_analysed.csv"
df = pd.read_csv(csv_file)

# Create the outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)

print("Data loaded:", df.shape)


# -----------------------------
# Chart 1: Top 10 Stories
# -----------------------------

# Select the top 10 stories by score
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

print("Chart 1 saved")


# -----------------------------
# Chart 2: Stories by Category
# -----------------------------

# Count the number of stories in each category
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=["blue", "green", "orange", "red", "purple"]
)

plt.title("Number of Stories by Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

print("Chart 2 saved")

print("All charts completed successfully.")
# -----------------------------
# Chart 3: Score vs Comments
# -----------------------------

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(9, 6))

# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    color="green",
    label="Popular"
)

# Plot non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="red",
    label="Not Popular"
)

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

print("Chart 3 saved")
# -----------------------------
# Bonus: TrendPulse Dashboard
# -----------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Dashboard Chart 1: Top 10 stories
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")

# Dashboard Chart 2: Stories by category
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=["blue", "green", "orange", "red", "purple"]
)
axes[1].set_title("Stories by Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

# Dashboard Chart 3: Score vs comments
axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    color="green",
    label="Popular"
)

axes[2].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="red",
    label="Not Popular"
)

axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Overall dashboard title
fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Dashboard saved")
print("All charts completed successfully.")