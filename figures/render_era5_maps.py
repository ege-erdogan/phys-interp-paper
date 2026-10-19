"""Render cached ERA5 examples for the probing diagram; no downloads or inference."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xarray as xr
from cartopy.util import add_cyclic_point

PROJECT = Path('/Users/egeerdogan/Desktop/phys-interp')
sys.path.insert(0, str(PROJECT))
from map_style import global_map_subplots, DATA_CRS

OUT = Path(__file__).resolve().parent
for hour in ('12', '18'):
    source = PROJECT / 'era5_cache_aurora/1440x721' / f'2020-08-06T{hour}:00:00.nc'
    with xr.open_dataset(source) as ds:
        field = ds['2t'].isel(time=0).load() - 273.15
        values, lon = add_cyclic_point(field.values, coord=ds.longitude.values)
        fig, ax = global_map_subplots(figsize=(4, 2.1))
        ax.pcolormesh(lon, ds.latitude.values, values, transform=DATA_CRS,
                      cmap='coolwarm', vmin=-50, vmax=40, rasterized=True)
        ax.spines['geo'].set_linewidth(.5)
        fig.subplots_adjust(left=.005, right=.995, bottom=.005, top=.995)
        fig.savefig(OUT / f'era5_2t_{hour}.png', dpi=250, transparent=True)
        plt.close(fig)
fig, ax = plt.subplots(figsize=(3.2, .38))
fig.subplots_adjust(left=.05, right=.95, bottom=.60, top=.90)
cb = matplotlib.colorbar.ColorbarBase(ax, cmap='coolwarm',
    norm=matplotlib.colors.Normalize(-50,40), orientation='horizontal', ticks=[-50,0,40])
cb.ax.tick_params(labelsize=8, length=2, pad=2)
cb.outline.set_linewidth(.4)
fig.savefig(OUT / 'era5_temperature_scale.png', dpi=250, transparent=True, bbox_inches='tight', pad_inches=.02)
plt.close(fig)
