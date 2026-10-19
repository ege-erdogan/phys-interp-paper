"""Actual aligned ERA5 token footprints on a shared geographic crop."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import xarray as xr
import numpy as np
PROJECT=Path('/Users/egeerdogan/Desktop/phys-interp')
sys.path.insert(0,str(PROJECT))
from map_style import global_map_subplots, DATA_CRS
OUT=Path(__file__).resolve().parent
with xr.open_dataset(PROJECT/'era5_cache_aurora/1440x721/2020-08-06T18:00:00.nc') as ds:
    # Row 160, column 0 align with all three patch widths on the 720-row grid.
    north=float(ds.latitude[160])+.125
    west=float(ds.longitude[0])-.125
    for width in (4,8,16):
        fig,ax=global_map_subplots(figsize=(2,2))
        ax.set_extent([-2.125,6.125,43.875,52.125], crs=DATA_CRS)
        ax.stock_img()
        east=west+.25*width; south=north-.25*width
        ax.plot([west,east,east,west,west],[north,north,south,south,north],
                transform=DATA_CRS,color='#df2020',linewidth=2.4,
                path_effects=[pe.Stroke(linewidth=4.2,foreground='white'),pe.Normal()],zorder=20)
        ax.spines['geo'].set_linewidth(.4)
        fig.subplots_adjust(left=.015,right=.985,bottom=.015,top=.985)
        fig.savefig(OUT/f'era5_patch_{width}.png',dpi=300,transparent=True)
        plt.close(fig)
