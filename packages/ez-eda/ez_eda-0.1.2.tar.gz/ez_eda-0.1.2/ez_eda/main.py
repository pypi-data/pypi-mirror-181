import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def ez_corr_heatmap(df: pd.DataFrame, vmin: float = None,
                    vmax: float = None, center: float = None):
    """
    Custom Heatmap Plot
    References: https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
    Inputs:pandas Dataframe
    Optional Inputs: vmin, vmax, center
    Output: Seaborn Heatmap Plot
    """
    corr = df.corr(numeric_only=True)
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 10))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 11, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=vmin, vmax=vmax,
                center=center, square=True, linewidths=.5,
                cbar_kws={"shrink": .5})


def ez_2d_pca_plot(df: pd.DataFrame, hue: str = None):
    pca_2 = PCA(n_components=2)
    scaler = StandardScaler()
    numeric_fields = df.select_dtypes(include=np.number).columns.tolist()
    df[numeric_fields] = scaler.fit_transform(df[numeric_fields])
    df = pd.get_dummies(df)
    df[['pca_1', 'pca_2']] = pca_2.fit_transform(df)
    sns.scatterplot(data=df, x='pca_1', y='pca_2', hue=hue)