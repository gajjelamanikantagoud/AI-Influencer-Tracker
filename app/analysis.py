import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
DATA_FILE = os.path.join("data", "influencers.csv")
OUTPUT_CHART = os.path.join("data", "platform_distribution_chart.png")

# --- Data Cleaning Function ---
def convert_followers(val):
    """Converts string followers (e.g., '1.2M', '500K') to numeric floats."""
    val = str(val).upper().replace(' ', '') # Remove spaces
    
    if 'K' in val:
        val = val.replace('K', '')
        return float(val) * 1_000
    elif 'M' in val:
        val = val.replace('M', '')
        return float(val) * 1_000_000
    elif 'B' in val:
        val = val.replace('B', '')
        return float(val) * 1_000_000_000
    else:
        try:
            return float(val)
        except ValueError:
            return None # Return None for unparseable values

# --- Main Analysis ---
print(f"Loading data from {DATA_FILE}...")
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ERROR: Data file not found.")
    print(f"Please make sure '{DATA_FILE}' exists.")
    exit()

print("Cleaning 'Followers' column...")
df['Followers'] = df['Followers'].apply(convert_followers)

# --- Analysis 1: Platform Distribution ---
print("Analyzing platform distribution...")
platform_counts = df['Platform'].value_counts()

plt.figure(figsize=(10, 6))
platform_counts.plot(kind='bar', color='#1f77b4')
plt.title("AI Influencers by Platform", fontsize=16)
plt.xlabel("Platform", fontsize=12)
plt.ylabel("Number of Influencers", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the chart
plt.savefig(OUTPUT_CHART)
print(f"Chart saved to {OUTPUT_CHART}")

# --- Analysis 2: Total Followers by Platform ---
print("Analyzing total followers by platform...")
platform_followers_sum = df.groupby('Platform')['Followers'].sum().sort_values(ascending=False)

print("\n--- Top Platforms by Count ---")
print(platform_counts)

print("\n--- Top Platforms by Total Followers ---")
print(platform_followers_sum)

print("\nAnalysis complete.")