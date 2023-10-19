#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Retrieving Data
df= 'NSW_fire.csv'
df= pd.read_csv("C:\\Users\\kaurr\\NSW_fire.csv", sep=",", decimal=".")

# Define your target variable
target_variable = 'Label'

# Define the sensitive attributes
sensitive_attributes = ['FID', 'FireName', 'StartDate', 'EndDate', 'Season']

# Check the distribution of your target variable
target_distribution = df[target_variable].value_counts(normalize=True)
print(f"Distribution of {target_variable}:\n{target_distribution}\n")

# Check the distribution of the sensitive attributes
for attribute in sensitive_attributes:
    attribute_distribution = df[attribute].value_counts(normalize=True)
    print(f"Distribution of {attribute}:\n{attribute_distribution}\n")

# Visualize the distribution of sensitive attributes with respect to the target variable
for attribute in sensitive_attributes:
    plt.figure(figsize=(8, 6))
    sns.countplot(df=df, x=attribute, hue=target_variable)
    plt.title(f"Distribution of {attribute} by {target_variable}")
    plt.show()

# Perform statistical tests (e.g., chi-squared) to assess relationships between sensitive attributes and the target variable
from scipy.stats import chi2_contingency

for attribute in sensitive_attributes:
    contingency_table = pd.crosstab(df[attribute], df[target_variable])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Chi-squared test for independence between {attribute} and {target_variable}:\n")
    print(f"Chi2: {chi2}\n")
    print(f"P-value: {p}\n")
    if p < 0.05:
        print(f"Significant relationship between {attribute} and {target_variable}\n")
    else:
        print(f"No significant relationship between {attribute} and {target_variable}\n")

