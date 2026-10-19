"""Additional actual ERA5 fields for the input stacks; uses only local data."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xarray as xr
from cartopy.util import add_cyclic_point
PROJECT=Path('/Users/egeerdogan/Desktop/phys-interp')
sys.path.insert(0,str(PROJECT))
from map_style import global_map_subplots, DATA_CRS
OUT=Path(__file__).resolve().parent
for hour in ('12','18'):
    with xr.open_dataset(PROJECT/'era5_cache_aurora/1440x721'/f'2020-08-06T{hour}:00:00.nc') as ds:
        fields=[('10u',ds['10u'].isel(time=0).load(),'PuOr_r',-20,20),
                ('q850',ds['q'].isel(time=0).sel(level=850).load()*1000,'YlGnBu',0,16)]
        for name,field,cmap,vmin,vmax in fields:
            values,lon=add_cyclic_point(field.values,coord=ds.longitude.values)
            fig,ax=global_map_subplots(figsize=(4,2.1))
            ax.pcolormesh(lon,ds.latitude.values,values,transform=DATA_CRS,cmap=cmap,
                          vmin=vmin,vmax=vmax,rasterized=True)
            ax.spines['geo'].set_linewidth(.5)
            fig.subplots_adjust(left=.005,right=.995,bottom=.005,top=.995)
            fig.savefig(OUT/f'era5_{name}_{hour}.png',dpi=250,transparent=True)
            plt.close(fig)
