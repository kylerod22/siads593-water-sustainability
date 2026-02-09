import pandas as pd
import numpy as np
from branca.colormap import linear
import folium

def gen_map(in_df, col, log_plot=False):
    # Read in maps
    df = in_df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Subset of samples where pop_density is in top 25%
    quant_75 = df["pop_density_nn"].quantile(0.75)
    high_pop_df = df[df["pop_density_nn"] > quant_75]

    # Isolate lat+lon, target col columns
    df = df[["latitude","longitude",col]].dropna()
    df[["latitude","longitude",col]] = df[["latitude","longitude",col]].apply(pd.to_numeric, errors="coerce")
    df = df.dropna()

    if (log_plot):
        # Log scale, generate color mapping
        log_name = f"{col}_log"
        df[log_name] = np.log(df[col])
        vmin = df[log_name].quantile(0.01)
        vmax = df[log_name].quantile(0.99)
        cmap = linear.viridis.scale(vmin, vmax)
        cmap.caption = f"{col} (log)"
        
        
        m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=5, tiles="CartoDB positron")

        # Add each color-mapped data point
        for _, r in df.iterrows():
            val = float(np.clip(r[log_name], vmin, vmax))
            folium.CircleMarker(
                location=[r["latitude"], r["longitude"]],
                radius=4,
                color=cmap(val),
                fill=True,
                fill_color=cmap(val),
                fill_opacity=0.8,
                weight=0.5,
                tooltip=f"{col}: {r[col]:.1f} | log: {r[log_name]:.2f}"
            ).add_to(m)
    
    else:
        vmin = df[col].quantile(0.01)
        vmax = df[col].quantile(0.99)

        cmap = linear.viridis.scale(vmin, vmax)
        cmap.caption = col

        m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=5, tiles="CartoDB positron")

        for _, r in df.iterrows():
            val = float(np.clip(r[col], vmin, vmax))
            folium.CircleMarker(
                location=[r["latitude"], r["longitude"]],
                radius=4,
                color=cmap(val),
                fill=True,
                fill_color=cmap(val),
                fill_opacity=0.8,
                weight=0.5,
                tooltip=f"{col} {r[col]:.2f}"
            ).add_to(m)

        cmap.add_to(m)

    

    # Circle higher density areas in red
    for _, r in high_pop_df.iterrows():
        folium.CircleMarker(
            location=[r["latitude"], r["longitude"]],
            radius=10,
            color="red",
            fill=False,
            weight=0.5,
        ).add_to(m)

    cmap.add_to(m)
    return m