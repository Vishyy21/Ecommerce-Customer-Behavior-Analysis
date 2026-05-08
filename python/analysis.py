# ============================================================
# E-Commerce Customer Behavior & Retention Analysis - EDA
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# ---- STEP 1: Load Dataset ----
df = pd.read_csv('../data/ecommerce_raw.csv')

print('Shape:', df.shape)
print(df.head())

# ---- STEP 2: Clean Dataset ----
print('\nNull Values Before Cleaning:')
print(df.isnull().sum())

df.dropna(subset=['Satisfaction Level'], inplace=True)
df.drop_duplicates(inplace=True)

df.columns = df.columns.str.strip().str.replace(' ', '_')

print('Shape After Cleaning:', df.shape)

# ---- STEP 3: Key Metrics ----
total_revenue = df['Total_Spend'].sum()
avg_spend = df['Total_Spend'].mean()
avg_rating = df['Average_Rating'].mean()

print(f'Total Revenue   : ${total_revenue:,.2f}')
print(f'Average Spend   : ${avg_spend:,.2f}')
print(f'Average Rating  : {avg_rating:.2f}')
print(f'Total Customers : {len(df)}')

# ---- STEP 4: Membership Analysis ----
mem_rev = df.groupby('Membership_Type')['Total_Spend'].agg(['sum','mean','count'])

print('\nMembership Analysis:')
print(mem_rev)

# ---- STEP 5: Satisfaction Analysis ----
sat_dist = df['Satisfaction_Level'].value_counts(normalize=True) * 100

print('\nSatisfaction Distribution (%):')
print(sat_dist.round(1))

# ---- STEP 6: City Revenue ----
city_rev = df.groupby('City')['Total_Spend'].sum().sort_values(ascending=False)

print('\nCity Revenue:')
print(city_rev)

# ---- STEP 7: Discount Impact ----
disc_impact = df.groupby('Discount_Applied')['Total_Spend'].mean()

print('\nAvg Spend - Discount Impact:')
print(disc_impact)

# ---- STEP 8: Retention Segments ----
bins = [0, 15, 30, 45, 100]
labels = ['Active (0-15d)', 'Warm (15-30d)', 'At Risk (30-45d)', 'Churned (45d+)']

df['Retention_Segment'] = pd.cut(
    df['Days_Since_Last_Purchase'],
    bins=bins,
    labels=labels
)

ret_dist = df['Retention_Segment'].value_counts().reindex(labels)

print('\nRetention Segments:')
print(ret_dist)

# ---- STEP 9: Charts ----
sns.set_theme(style='whitegrid')

fig, axes = plt.subplots(2, 3, figsize=(18, 11))

fig.suptitle(
    'E-Commerce Customer Behavior & Retention Analysis',
    fontsize=16,
    fontweight='bold'
)

# Revenue by Membership
rev_data = df.groupby('Membership_Type')['Total_Spend'].sum().reindex(
    ['Gold','Silver','Bronze']
)

axes[0,0].bar(
    rev_data.index,
    rev_data.values,
    color=['#FFD700','#A8A9AD','#CD7F32']
)

axes[0,0].set_title('Total Revenue by Membership Type')

# Satisfaction Pie
sat_counts = df['Satisfaction_Level'].value_counts()

axes[0,1].pie(
    sat_counts.values,
    labels=sat_counts.index,
    autopct='%1.1f%%',
    colors=['#4CAF50','#FF9800','#F44336']
)

axes[0,1].set_title('Customer Satisfaction Distribution')

# City Revenue
city_data = df.groupby('City')['Total_Spend'].sum().sort_values()

axes[0,2].barh(
    city_data.index,
    city_data.values,
    color='steelblue'
)

axes[0,2].set_title('Revenue by City')

# Discount Impact
disc_data = df.groupby('Discount_Applied')['Total_Spend'].mean()

axes[1,0].bar(
    ['No Discount','Discount Applied'],
    disc_data.values,
    color=['#5C85D6','#F4A261']
)

axes[1,0].set_title('Avg Spend: Discount vs No Discount')

# Retention Segments
axes[1,1].bar(
    ret_dist.index,
    ret_dist.values,
    color=['#27AE60','#F39C12','#E67E22','#E74C3C']
)

axes[1,1].set_title('Customer Retention Segments')

# Avg Rating by Membership
rat_data = df.groupby('Membership_Type')['Average_Rating'].mean().reindex(
    ['Gold','Silver','Bronze']
)

axes[1,2].bar(
    rat_data.index,
    rat_data.values,
    color=['#FFD700','#A8A9AD','#CD7F32']
)

axes[1,2].set_title('Avg Rating by Membership Type')

plt.tight_layout()

plt.savefig(
    '../screenshots/eda_charts.png',
    dpi=150,
    bbox_inches='tight'
)

plt.show()

# ---- STEP 10: Export Cleaned Dataset ----
df.to_csv('../data/ecommerce_cleaned.csv', index=False)

print('Cleaned dataset exported successfully.')