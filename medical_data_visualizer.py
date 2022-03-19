import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

# Import data
df = pd.read_csv(r"C:\Users\shawn\Desktop\Python Learning\medical_examination.csv", delimiter=",")

# Add 'overweight' column
df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)  # calculate BMI
df.loc[df["bmi"] > 25, "overweight"] = 1  # normalize data
df.loc[df["bmi"] <= 25, "overweight"] = 0
df = df.astype({"overweight": int}).drop(columns="bmi")

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value
# 0. If the value is more than 1, make the value 1.
df.loc[df["gluc"] == 1, "gluc"] = 0
df.loc[df["gluc"] > 1, "gluc"] = 1
df.loc[df["cholesterol"] == 1, "cholesterol"] = 0
df.loc[df["cholesterol"] > 1, "cholesterol"] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco',
    # 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars="cardio", value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one
    # of the columns for the catplot to work correctly.

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, x="variable", hue="value", kind="count", col="cardio")\
        .set_axis_labels("variable", "total").fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &  # keeping valid data and leaving out outliers
              (df['height'] >= df['height'].quantile(0.025)) &
              (df['height'] <= df['height'].quantile(0.975)) &
              (df['weight'] >= df['weight'].quantile(0.025)) &
              (df['weight'] <= df['weight'].quantile(0.975))
              ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))  # used to leave out top right triangle of chart

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, center=0, robust=True, vmin=-0.1, vmax=0.3, fmt=".1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
