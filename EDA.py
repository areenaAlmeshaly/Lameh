import pandas as pd 
import matplotlib.pyplot as plt
import math
import seaborn as sns
def descr(df,ID):
    for i in df.columns:
        column=df[i]
        if i not in ID :
            print(column.describe())

def num_vizual(df,numric_col):
            n = len(numric_col)
            cols = 3
            rows = math.ceil(n / cols)
            fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
            axes = axes.flatten()
            for i, col in enumerate(numric_col):
                df[col].hist(bins=30,edgecolor="black",ax=axes[i])
                axes[i].set_title(col)
            for i in range(n, len(axes)):
                 axes[i].set_visible(False)
            plt.tight_layout()
            plt.show()


def num_rela(df,numric_col):
    corr = df[numric_col].corr()
    fig, ax = plt.subplots(
        figsize=(
            max(10, len(numric_col) * 0.5),
            max(8, len(numric_col) * 0.5)
        )
    )

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    plt.tight_layout()
    plt.show()

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
            ax=axes[i])
        axes[i].set_title(col)
    for i in range(n, len(axes)):
        axes[i].set_visible(False)
    plt.tight_layout()
    plt.show()