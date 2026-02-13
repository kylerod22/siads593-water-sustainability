import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon

def spatial_plot(df, var1='pet',var2='',
                     title='Potential Evapotranspiration at Sampling Locations', legend_title='PET (mm/day)'):
    '''
    Plots Chloropleth
    input
    -----
    - df: geopandas dataframe
    - var1: str
    - var2: str
    - title: str
    - legend_kwds: dict
    
    return
    ------
    Cloropleth
    '''
    # Plot
    fig, ax = plt.subplots(figsize=(11, 7))

    # Generate GDF
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326"
    )
    
    # Province Map
    provinces = gpd.read_file("data/za_shp", layer='za').to_crs("EPSG:4326")
    provinces = provinces.rename(columns={'name':'province'}).sort_values(by='province')
    new_polygon = provinces['geometry'].explode()[7][:1]
    multipolygon = MultiPolygon(new_polygon)
    provinces.loc[7, 'geometry'] = multipolygon


    provinces.plot(ax=ax, color='#B6B6B6')
    provinces['coords'] = provinces['geometry'].apply(lambda x: x.representative_point().coords[:])
    provinces['coords'] = [coords[0] for coords in provinces['coords']]
    for idx, row in provinces.iterrows():
        plt.annotate(text=row['province'], xy=row['coords'], horizontalalignment='center', color='white')
    #https://medium.com/nerd-for-tech/labelling-areas-of-coordinates-with-geopandas-74d25c8aada6
    
    # Overlay Data
    legend_kwds = {'label':legend_title}
    if var2:
        gdf.plot(column=var1, ax=ax, marker='o', markersize=gdf[var2] / 4, cmap='Blues', vmin=0, legend=True, legend_kwds=legend_kwds)
    else:
        gdf.plot(column=var1, ax=ax, marker='o', cmap='Blues', vmin=0, legend=True, legend_kwds=legend_kwds)
    
    ax.set_axis_off() # leave the axis to see correlation between position and PET value
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.show();