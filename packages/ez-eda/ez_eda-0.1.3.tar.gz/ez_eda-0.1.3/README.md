# ez-eda overview
- This library is a collection of simplified functions for visualizing dataframes quickly and easily
- I started this project after needing more refined heatmaps to understanding correlation

## ez correlation plot 
```
from ez_eda import ez_corr_heatmap
```
This function creates a cleaner seaborn-based heatmap to show correlations between numeric features

**Parameters**

ez_corr_heatmap(df: pd.DataFrame, color_min: float = None, color_max: float = None, color_center: float = 0)
- df: input pandas dataframe
- color_min: minimum value for heatmap scale - defaults to corr() minimum
- color_max: maximum value for heatmap scale - defaults to corr() maximum
- color_center: center for heatmap color scale - defaults to midpoint between vmin and vmax

Example Correlation Heatmap Image
![heatmap](static/example_heatmap.png)

## ez 2D PCA Plot
```
from ez_eda import ez_2d_pca_plot
```
This function creates a simplified 2D plot of the data in seaborn to show the overall structure

**Parameters**

ez_2d_pca_plot(df: pd.DataFrame, hue: str = None)
- df: input pandas dataframe
- hue: color for scatter plot (Optional)