import numpy
import xarray
import pandas

fname = "data.npy"
arr = numpy.load(fname)
df = pandas.DataFrame({"lon":arr[:,0], "lat":arr[:,1], "data":arr[:,3]})
df = df[~df.index.duplicated(keep='first')]
ds = df.set_index(["lat","lon"]).to_xarray()
ds.to_netcdf("data.nc")
