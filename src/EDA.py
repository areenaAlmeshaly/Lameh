import matplotlib.pyplot as plt
import pandas as pd
import math
import seaborn as sns
def descr(df,ID):
    descriptions = {}
    for i in df.columns:
        column=df[i]
        if i not in ID:
            descriptions[i] = column.describe()
    return descriptions

def num_vizual(df,numric_col):
            n = len(numric_col)
            cols = 3
            rows = math.ceil(n / cols)
            fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
            fig.patch.set_facecolor("#101A2C")

            axes = axes.flatten()
            for i, col in enumerate(numric_col):
                df[col].hist(bins=30,color="#14B87E",
            edgecolor="#0A101E",ax=axes[i])
                axes[i].set_title(col, color="white")
                axes[i].tick_params(axis="both", colors="white")
            for i in range(n, len(axes)):
                 axes[i].set_visible(False)
            plt.tight_layout()
            return fig

def num_rela(df,numric_col):
    corr = df[numric_col].corr()
    fig,ax= plt.subplots(
        figsize=(
            max(10, len(numric_col) * 0.5),
            max(8, len(numric_col) * 0.5)))
    fig.patch.set_facecolor("#101A2C")
    ax.set_facecolor("#101A2C")

    cmap = sns.color_palette(
        ["#0A101E", "#0A6B49", "#14B87E", "#C9A84C"],
        as_cmap=True
    )
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        ax=ax,
        cmap=cmap,
        vmin=-1,
        vmax=1,
        center=0,
        linewidths=0.4
    )
    ax.set_title("Correlation Heatmap", color="white")
    ax.tick_params(axis="both", colors="white")
    for text in ax.texts:
        text.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("white")

    plt.tight_layout()
    return fig


def cat_vizual(df, cat_col):

    n = len(cat_col)
    cols = 3
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(15, 4 * rows))

    axes = axes.flatten()
    for i, col in enumerate(cat_col):

        df[col].value_counts().plot.bar(
            ax=axes[i],
            color="#14B87E",
            edgecolor="#0A6B49")

        axes[i].set_title(col,
            color="#EDF2F9",
            fontsize=11,
            fontweight="bold")

        axes[i].set_xlabel("",
            color="#B8C2D4")

        axes[i].set_ylabel("Count",
            color="#B8C2D4")

        axes[i].tick_params(axis="x", colors="#B8C2D4",rotation=35)

        axes[i].tick_params(axis="y",colors="#B8C2D4")

        axes[i].set_facecolor("#101A2C")

        axes[i].grid(axis="y",alpha=0.15)

        for spine in axes[i].spines.values():
            spine.set_color("#26344D")

    for i in range(n, len(axes)):
        axes[i].set_visible(False)

    fig.patch.set_facecolor("#101A2C")
    plt.tight_layout()
    return fig


def generate_insights(df,numric_col,cat_col,id_col):
    insights=[]
    valid_num=[]

    for i in numric_col:
        if i not in id_col:
            valid_num.append(i)

    if len(valid_num) >= 2:
        corr=df[valid_num].corr()
        strongest_corr=0
        strongest_pair=None

        for i in range(len(corr.columns)):
            for j in range(i+1,len(corr.columns)):
                value=corr.iloc[i,j]

                if pd.notna(value) and abs(value)>abs(strongest_corr):
                    strongest_corr=value
                    strongest_pair=(corr.columns[i],corr.columns[j])

        if strongest_pair and abs(strongest_corr)>=0.7:
            insights.append(
                f"{strongest_pair[0]} and {strongest_pair[1]} "
                f"have a strong relationship (r={strongest_corr:.2f}).")
            
    for i in valid_num:
        skewness=df[i].skew()

        if abs(skewness)>=1:
            if skewness>0:
                direction="right"
            else:
                direction="left"

            insights.append(
                f"{i} is strongly {direction}-skewed.")
    for i in cat_col:
        if i in id_col:
            continue

        values=df[i].value_counts(normalize=True,dropna=True)
        if len(values)==0:
            continue

        percentage=values.iloc[0]*100

        if percentage>=60:
            category=values.index[0]

            insights.append(
                f"{i} is highly concentrated in "
                f"'{category}' ({percentage:.0f}%).")

    return insights