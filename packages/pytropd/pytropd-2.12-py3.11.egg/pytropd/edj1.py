# diff.py - implementation of ForwardDifferenceVar, and the 'diff' method.

from pygeode.var import Var
from functools import reduce
import numpy as np
import functions as f

class EDJVar (Var):
  '''Forward difference variable.'''

  def __init__ (self, var, axis, n):
  
    '''__init__()'''

    from pygeode.var import Var
    from pygeode.axis import NamedAxis

    df = 'right'  # Hard-coded to match numpy behaviour.
                  # May be extended in the future?

    self.daxis = daxis = var.whichaxis(axis)
    assert var.shape[daxis] > n, "need at least %d value(s) along difference axis"%n

    self.n = n
    self.df = df
    self.var = var

    # Construct new variable

    if var.name != '':
      name = 'd' + var.name
    else:
      name = 'd(UnknownVar)'

    axes = list(var.axes)
    if df == 'left':
      axes[daxis] = axes[daxis].slice[n:]
    else:
      axes[daxis] = axes[daxis].slice[:-n]
    oaxes = [NamedAxis(values=np.arange(2),name='Metrics')]
    Var.__init__(self, oaxes, var.dtype, name=name, atts=var.atts, plotatts=var.plotatts)
  

  def getview (self, view, pbar):
  
    from functools import reduce
    
    daxis = self.daxis
    n = self.n

    # Get integer indices along the difference axis
    left = view.integer_indices[daxis]

    # All the points we need to request (unique occurrences only)
    allpoints = left

    # Set a view on the original variable, to request these points
    allview = view.replace_axis(daxis, self.var.axes[daxis])

    # Get the data values for these points
    allvalues = allview.get(self.var, pbar=pbar)

    # Compute the difference
    diff = np.diff(allvalues, axis=daxis, n=n)
    # Compute the difference
    edj_lats = TropD_Metric_EDJ(allvalues, lat=self.var.axes[daxis][:])

    # Define a map back to our points
    getleft = np.searchsorted(allpoints,left)
    # Make this 1D map into the right shape for the view (if multi-dimensional)
    getleft = tuple([slice(None)]*daxis + [getleft] + [slice(None)]*(self.naxes-daxis-1))
    print(allpoints)
    

    # Finally, map the data to our points, and return.
    return edj_lats[getleft]
  
def TropD_Metric_EDJ(U, lat, lev=np.array([1]), method='peak', n=0, n_fit=1):
  '''TropD Eddy Driven Jet (EDJ) metric
       
     Latitude of maximum of the zonal wind at the level closest to the 850 hPa level
     
     Args:
       U (lat,lev) or U (lat,): Zonal mean zonal wind. Also takes surface wind 
       lat : latitude vector
       lev: vertical level vector in hPa units

       method (str, optional): 'peak' (default) |  'max' | 'fit'
       
        peak (Default): Latitude of the maximum of the zonal wind at the level closest to the 850 hPa level (smoothing parameter n=30)
        
        max: Latitude of the maximum of the zonal wind at the level closest to the 850 hPa level (smoothing parameter n=6)
        fit: Latitude of the maximum of the zonal wind at the level closest to the 850 hPa level using a quadratic polynomial fit of data from gridpoints surrounding the gridpoint of the maximum
        
       n (int, optional): If n is not set (0), n=6 (default) is used in TropD_Calculate_MaxLat. Rank of moment used to calculate the position of max value. n = 1,2,4,6,8,...  
     
     Returns:
       tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of EDJ in SH and NH

  '''

  try:
    assert (not hasattr(n, "__len__") and n >= 0)  
  except AssertionError:
   print('TropD_Metric_EDJ: ERROR : the smoothing parameter n must be >= 0')
   
  try:
    assert(method in ['max','peak'])
  except AssertionError:
    print('TropD_Metric_EDJ: ERROR : unrecognized method ', method)

  eq_boundary = 15
  polar_boundary = 70
  
  if len(lev) > 1:
    u = U[:,f.find_nearest(lev, 850)]
  else:
    u = np.copy(U)
    
  if method == 'max':
    if n:
      PhiNH = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < polar_boundary)],\
              lat[(lat > eq_boundary) & (lat < polar_boundary)], n=n)
      PhiSH = f.TropD_Calculate_MaxLat(u[(lat > -polar_boundary) & (lat < -eq_boundary)],\
              lat[(lat > -polar_boundary) & (lat < -eq_boundary)], n=n)

    else:
      #Default value of n=6 is used
      PhiNH = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < polar_boundary)],\
              lat[(lat > eq_boundary) & (lat < polar_boundary)])
      PhiSH = f.TropD_Calculate_MaxLat(u[(lat > -polar_boundary) & (lat < -eq_boundary)],\
              lat[(lat > -polar_boundary) & (lat < -eq_boundary)])
  
  elif method == 'peak':
    if n:
      PhiNH = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < polar_boundary)],\
              lat[(lat > eq_boundary) & (lat < polar_boundary)], n=n)
      PhiSH = f.TropD_Calculate_MaxLat(u[(lat > -polar_boundary) & (lat < -eq_boundary)],\
              lat[(lat > -polar_boundary) & (lat < -eq_boundary)], n=n)
    else:
      PhiNH = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < polar_boundary)],\
              lat[(lat > eq_boundary) & (lat < polar_boundary)],n=30)
      PhiSH = f.TropD_Calculate_MaxLat(u[(lat > -polar_boundary) & (lat < -eq_boundary)],\
              lat[(lat > -polar_boundary) & (lat < -eq_boundary)],n=30)
  
  elif method == 'fit':
    Uh = u[(lat > eq_boundary) & (lat < polar_boundary)]
    Lat = lat[(lat > eq_boundary) & (lat < polar_boundary)]
    m = np.nanmax(Uh)
    Im = np.nanargmax(Uh)
     
    if (Im == 0 or Im == len(Uh)-1):
      PhiNH = Lat[Im]
    
    elif (n_fit > Im or n_fit > len(Uh)-Im+1):
      N = np.min(Im, len(Uh)-Im+1)
      p = np.polyfit(Lat[Im-N:Im+N+1], Uh[Im-N:Im+N+1],2) 
      PhiNH = -p[1]/(2*p[0])
    else:
      p = np.polyfit(Lat[Im-n_fit:Im+n_fit+1], Uh[Im-n_fit:Im+n_fit+1],2) 
      PhiNH = -p[1]/(2*p[0])
    
    Uh = u[(lat > -polar_boundary) & (lat < -eq_boundary)]
    Lat = lat[(lat > -polar_boundary) & (lat < -eq_boundary)]
    
    m = np.nanmax(Uh)
    Im = np.nanargmax(Uh)
    
    if (Im == 0 or Im == len(Uh)-1):
      PhiSH = Lat[Im]
    
    elif (n_fit > Im or n_fit > len(Uh)-Im+1):
      N = np.min(Im, len(Uh)-Im+1)
      p = np.polyfit(Lat[Im-N:Im+N+1], Uh[Im-N:Im+N+1],2) 
      PhiSH = -p[1]/(2*p[0])
    else:
      p = np.polyfit(Lat[Im-n_fit:Im+n_fit+1], Uh[Im-n_fit:Im+n_fit+1],2) 
      PhiSH = -p[1]/(2*p[0])
  
  else:
    print('TropD_Metric_EDJ: ERROR: unrecognized method ', method)

  return np.array([PhiSH, PhiNH])

def edj(var, axis=0, n=1):

  '''Computes the forward difference along the given axis.
  Mimics the same behaviour of the :func:`np.diff` function.

  Parameters
  ----------
  axis : string, :class:`Axis` class, or int
    Axis along which to compute differences.
  n : int (optional)
    Number of times values are differenced.

  Returns
  -------
  dvar : :class:`Var`
    New variable containing n-th differenced values.

  Examples
  --------
  >>> import pygeode as pyg
  >>> v = pyg.yearlessn(5)
  >>> v[:]
  array([0., 1., 2., 3., 4.])
  >>> v.diff('time')[:]
  array([1., 1., 1., 1.])
  >>> v.diff('time', 2)[:]
  array([0., 0., 0.])
  '''
  return EDJVar(var, axis, n)

