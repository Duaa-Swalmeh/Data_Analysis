# -*- coding: utf-8 -*-
"""Analysis_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WhzOK04QwWucBsrQ8WNU7vngE3biufP3

#
Undertand top50 Data
"""

import pandas as pd
df=pd.read_csv("/content/insurance.csv")

df.head()

df.info()
"""
data size:(1337, 7)
There are no null values.
we have :
7 features:
    3 categorical features :sex,smoker,region
    4 numarical features:
         2 features:float64
         2 features:int64
"""

df.describe()
"""
mean(age)=39.222139
sd(age)=14.044333
max(age)=64.000000
min(age)=18.000000
mean(bmi)=30.663452
sd(bmi)=6.100468
max(bmi)=53.130000
min(bmi)=15.960000
mean(children	)=1.095737
sd(children	)=1.205571
max(children	)=5.000000
min(children	)=0.000000
mean(charges)=13279.121487
sd(charges)=12110.359656
max(charges)=63770.428010
min(charges)=1121.873900
"""

df.columns
#we have 7 columns 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges'

"""#Data Cleaning"""

df.duplicated().sum()
#we dont have any duplicated values

df.shape
#data size=(1337, 7)

df.isna().sum()
##we dont have any null values

df["sex"].value_counts()
#male=675
#female=662

df["smoker"].value_counts()
"""
no smoker=1063
smoker=274
"""

df["region"].value_counts()
"""
we have 4 regions:
southeast:364
southwest:	325
northwest:	324
northeast:	324


"""

df.to_csv("/content/silver_insurance.csv",index=False)

"""#EDA"""

df=pd.read_csv("/content/silver_insurance.csv")

df.head()

df.isna().sum()

df_num=df.select_dtypes(include=["float64","int64"])

df_num.head()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


# Set the visual style
sns.set_style("whitegrid")
sns.set_palette("deep")

# Define the number of columns and calculate rows dynamically
n_cols = 2  # Number of plots per row
n_rows = (len(df_num.columns) + n_cols - 1) // n_cols  # Calculate required rows

# Create the main figure
fig, axes = plt.subplots(n_rows, n_cols, figsize=(8, 4))  # Adjust overall size

# Flatten the axes array for easier indexing
axes = axes.flatten()

# Plotting
for i, col in enumerate(df_num.columns):
    # Extract column data
    data = df_num[col]

    # Fit the normal distribution
    mean, std = norm.fit(data)

    # Generate x values for the curve
    x = np.linspace(data.min(), data.max(), 1000)
    y = norm.pdf(x, mean, std)

    # Plot histogram and the fitted curve
    sns.histplot(data, kde=False, stat="density", bins=30, color="darkblue", ax=axes[i], label="Data Histogram")
    axes[i].plot(x, y, color="pink", label=f"Normal Fit ($\mu={mean:.2f}, \sigma={std:.2f}$)")

    # Add titles and labels
    axes[i].set_title(f"Normal Fit for {col}")
    axes[i].set_xlabel(f"{col} Values")
    axes[i].set_ylabel("Density")
    axes[i].legend()

# Remove empty axes if any
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Improve layout
plt.tight_layout()
plt.show()

"""
1. Normal Fit for Age
The mean age (μ) is about 39.22 years with a standard deviation (σ) = 14.04.
The distribution appears close to normal, but there is a slight increase in individuals in the 20-25 age group.
This may mean that the data contains a good number of young people, with a reasonable balance of the rest of the age groups.

2. Normal Fit for BMI
The mean BMI is 30.66 with a standard deviation of 6.10.
The graph shows a bell-shaped figure (normal distribution), but with a long tail to the right, indicating that there are high BMI cases that may fall into the obese category.
Most people are in the 20-40 BMI range, which covers the normal weight to moderate obesity category.

3. Normal Fit for Children
The mean number of children is 1.10 with a standard deviation of 1.21.
The data show that the majority have one or no children at all.
The cases with 4 or 5 children are considered very few (long tail to the right).

4. Normal Fit for Charges
The average cost is $13,279.12 with a large standard deviation = $12,105.83.
The graph shows a clear concentration of costs in the less than $20,000 category, while the long tail indicates cases with very high costs.
High costs may be related to factors such as smoking or high BMI.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Prepare scatter plots for all column pairs
columns = df_num.columns
n_cols = 2  # Number of plots per row
n_rows = (len(columns) * (len(columns) - 1)) // (2 * n_cols) + 1  # Calculate rows needed

# Create the main figure
fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 6), constrained_layout=True)
axes = axes.flatten()

# Plotting scatter plots for each pair
index = 0
for i, col1 in enumerate(columns):
    for j, col2 in enumerate(columns):
        if i < j:  # Ensure unique pairs
            # Scatter plot
            axes[index].scatter(df_num[col1], df_num[col2], color="red", alpha=0.7)

            # Add titles and labels
            axes[index].set_title(f"{col1} vs {col2}", color="black")
            axes[index].set_xlabel(col1, color="black")
            axes[index].set_ylabel(col2, color="black")

            index += 1

# Remove any unused axes
for k in range(index, len(axes)):
    fig.delaxes(axes[k])

# Display the plot
plt.show()

"""
1. **Age vs BMI**

- BMI is distributed roughly evenly across all ages, and there is no clear trend (such as BMI increasing with age).

- The disparity in BMI is large between young and old ages, suggesting that obesity is not age-specific.

2. **Age vs Children**

- The number of children increases slightly with age, but is roughly constant after age 30.

- Younger people tend to have fewer children (makes sense).

3. **Age vs Charges**

- Charges increase significantly with age, especially between the ages of **40-60**.

- Some young people have very high charges, perhaps due to certain health problems or high BMI.

4. **BMI vs Children**
- BMI does not seem to be significantly affected by the number of children.

- People with 4 or 5 children have a similar BMI range to people without children.

5. **BMI vs Charges**

- There is a significant relationship: costs increase significantly with increasing BMI, especially after BMI = 30.
- People with BMI above 40 pay higher costs, reflecting the impact of obesity on health costs.

6. **Children vs Charges**

- The number of children does not show a significant effect on costs, but costs increase slightly with more children (perhaps due to increased family health needs).
- The differences are not very large, which means that other factors (such as smoking and BMI) have a greater impact.
**************************
- The strongest relationship is evident between BMI and costs, followed by the relationship between age and costs.
- The remaining relationships (such as children and BMI) have a less pronounced or less significant effect compared to BMI and age.
"""

df_cat = df.select_dtypes(include=["object"])

df_cat.head()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Define the number of columns for the layout
n_cols = 2  # Number of plots per row
n_rows = (len(df_cat.columns) + n_cols - 1) // n_cols  # Calculate rows dynamically

# Create the figure and axes
fig, axes = plt.subplots(n_rows, n_cols, figsize=(8,4))
axes = axes.flatten()

# Plot bar charts for each categorical column
for i, col in enumerate(df_cat.columns):
    counts = df_cat[col].value_counts()  # Count the frequency of each category

    # Create the bar chart
    axes[i].bar(counts.index, counts.values, color=["#FF6F61", "#6B5B95", "#88B04B"])  # Attractive colors

    # Add titles and labels
    axes[i].set_title(f"Bar Chart for {col}", fontsize=12)
    axes[i].set_xlabel("Category", fontsize=10)
    axes[i].set_ylabel("Count", fontsize=10)

# Remove unused axes
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust layout for clarity
plt.tight_layout()
plt.show()

"""

1. (Bar Chart for sex):
- This chart shows the distribution of individuals by gender.
- Red represents males, and purple represents females.
- The number of males and females appears to be roughly equal.

2. (Bar Chart for smoker):
- This chart shows the distribution of individuals by smoking status.
- Red represents "non-smokers" (no), and purple represents "smokers" (yes).
- It is clear that the majority are non-smokers, while the number of smokers is much smaller.

3. (Bar Chart for region):
- Shows the distribution of individuals by geographic region.
- The different colors represent the regions: southeast, southwest, northwest, and northeast.
- The distribution appears to be roughly equal among the four regions, with a slight difference in numbers.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Define the number of columns for the layout
n_cols = 2  # Number of plots per row
n_rows = (len(df_cat.columns) + n_cols - 1) // n_cols  # Calculate rows dynamically

# Create the figure and axes
fig, axes = plt.subplots(n_rows, n_cols, figsize=(8, 4))
axes = axes.flatten()

# Plot pie charts for each categorical column
for i, col in enumerate(df_cat.columns):
    counts = df_cat[col].value_counts()  # Get category counts

    # Create the pie chart
    axes[i].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90,
                colors=plt.cm.Paired.colors)
    axes[i].set_title(f"Pie Chart for {col}")

# Remove unused axes
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust layout for clarity
plt.tight_layout()
plt.show()

"""
1. Pie Chart for sex:

- Shows the distribution of individuals by gender.
- Male percentage: **50.5%**.
- Female percentage: **49.5%**.
- This distribution shows a nearly equal balance between the sexes.

2. Pie Chart for smoker:
- Shows the distribution of individuals by smoking status.
- Non-smoker percentage: **79.5%**.
- Smoker percentage: **20.5%**.
- The vast majority of the sample are non-smokers, highlighting a significant difference between smokers and non-smokers.

3. Pie Chart for region:
- Shows the distribution of individuals by geographic region.
- South-east: **27.2%**.
- South-west: **24.3%**.
- North-east: **24.2%**.
- North-west: **24.2%**.
There is a relative balance in the distribution of individuals between the different regions, with a slight advantage for the southeast.


"""