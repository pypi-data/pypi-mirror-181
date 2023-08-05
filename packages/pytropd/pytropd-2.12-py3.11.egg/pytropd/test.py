
''' Tools for computing some basic statistical quantities. '''


import numpy as np
from scipy.stats import norm, t as tdist

def correlate(X, Y, axes=None, output = 'r,p', pbar=None):
# {{{
  r'''Computes Pearson correlation coefficient between variables X and Y.

  Parameters
  ==========
  X, Y : :class:`Var`
    Variables to correlate. Must have at least one axis in common.

  axes : list, optional
    Axes over which to compute correlation; if nothing is specified, the correlation
    is computed over all axes common to  shared by X and Y.

  output : string, optional
    A string determining which parameters are returned; see list of possible outputs
    in the Returns section. The specifications must be separated by a comma. Defaults
    to 'r,p'.

  pbar : progress bar, optional
    A progress bar object. If nothing is provided, a progress bar will be displayed
    if the calculation takes sufficiently long.

  Returns
  =======
  results : :class:`Dataset` 
    The names of the variables match the output request string (i.e. if ``ds``
    is the returned dataset, the correlation coefficient can be obtained
    through ``ds.r2``).

    * 'r': The Pearson correlation coefficient :math:`\rho_{XY}`
    * 'r2': The coefficient of determination :math:`\rho^2_{XY}`
    * 'p':  The p-value; see notes.

  Notes
  =====
  The coefficient :math:`\rho_{XY}` is computed following von Storch and Zwiers
  1999, section 8.2.2. The p-value is the probability of finding a correlation
  coeefficient of equal or greater magnitude (two-sided) to the given result
  under the hypothesis that the true correlation coefficient between X and Y is
  zero. It is computed from the t-statistic given in eq (8.7), in section
  8.2.3, and assumes normally distributed quantities.'''

  from pygeode.tools import loopover, whichaxis, combine_axes, shared_axes, npnansum
  from pygeode.view import View

  # Split output request now
  # Default output is 'r,p' so as not to break existing scripts
  ovars = ['r', 'r2', 'p']
  output = [o for o in output.split(',') if o in ovars]
  if len(output) < 1: raise ValueError('No valid outputs are requested from correlation. Possible outputs are %s.' % str(ovars))

  xn = X.name if X.name != '' else 'X' # Note: could write:  xn = X.name or 'X'
  yn = Y.name if Y.name != '' else 'Y'

  # Put all the axes being reduced over at the end 
  # so that we can reshape 
  srcaxes = combine_axes([X, Y])
  oiaxes, riaxes = shared_axes(srcaxes, [X.axes, Y.axes])
  if axes is not None:
    ri_new = []
    for a in axes:
      i = whichaxis(srcaxes, a)
      if i not in riaxes: 
        raise KeyError('%s axis not shared by X ("%s") and Y ("%s")' % (a, xn, yn))
      ri_new.append(i)
    oiaxes.extend([r for r in riaxes if r not in ri_new])
    riaxes = ri_new
    
  oaxes = [srcaxes[i] for i in oiaxes]
  inaxes = oaxes + [srcaxes[i] for i in riaxes]
  oview = View(oaxes) 
  iview = View(inaxes) 
  siaxes = list(range(len(oaxes), len(srcaxes)))

  # Construct work arrays
  x  = np.full(oview.shape, np.nan, 'd')
  y  = np.full(oview.shape, np.nan, 'd')
  xx = np.full(oview.shape, np.nan, 'd')
  yy = np.full(oview.shape, np.nan, 'd')
  xy = np.full(oview.shape, np.nan, 'd')
  Na = np.full(oview.shape, np.nan, 'd')

  if pbar is None:
    from pygeode.progress import PBar
    pbar = PBar(message = "Computing correlation '%s' vs '%s'" % (xn, yn))
  dddd
  for outsl, (xdata, ydata) in loopover([X, Y], oview, inaxes, pbar=pbar):
    xdata = xdata.astype('d')
    ydata = ydata.astype('d')
    xydata = xdata*ydata

    xbc = [s1 // s2 for s1, s2 in zip(xydata.shape, xdata.shape)]
    ybc = [s1 // s2 for s1, s2 in zip(xydata.shape, ydata.shape)]
    xdata = np.tile(xdata, xbc)
    ydata = np.tile(ydata, ybc)
    xdata[np.isnan(xydata)] = np.nan
    ydata[np.isnan(xydata)] = np.nan

    # It seems np.nansum does not broadcast its arguments automatically
    # so there must be a better way of doing this...
    x[outsl]  = np.nansum([x[outsl],  npnansum(xdata, siaxes)], 0)
    y[outsl]  = np.nansum([y[outsl],  npnansum(ydata, siaxes)], 0)
    xx[outsl] = np.nansum([xx[outsl], npnansum(xdata**2, siaxes)], 0)
    yy[outsl] = np.nansum([yy[outsl], npnansum(ydata**2, siaxes)], 0)
    xy[outsl] = np.nansum([xy[outsl], npnansum(xydata, siaxes)], 0)

    # Count of non-NaN data points
    Na[outsl] = np.nansum([Na[outsl], npnansum(~np.isnan(xydata), siaxes)], 0)

  imsk = (Na > 0)

  xx[imsk] -= (x*x)[imsk]/Na[imsk]
  yy[imsk] -= (y*y)[imsk]/Na[imsk]
  xy[imsk] -= (x*y)[imsk]/Na[imsk]

  # Ensure variances are non-negative
  xx[xx <= 0.] = 0.
  yy[yy <= 0.] = 0.

  # Compute correlation coefficient, t-statistic, p-value
  den = np.zeros(oview.shape, 'd')
  rho = np.zeros(oview.shape, 'd')

  den[imsk] = np.sqrt((xx*yy)[imsk])
  dmsk = (den > 0.)

  rho[dmsk] = xy[dmsk] / np.sqrt(xx*yy)[dmsk]

  den = 1 - rho**2
  # Saturate the denominator (when correlation is perfect) to avoid div by zero warnings
  eps = 1e-8
  den[den < eps] = eps

  t = np.zeros(oview.shape, 'd')
  p = np.zeros(oview.shape, 'd')

  t[imsk] = np.abs(rho)[imsk] * np.sqrt((Na[imsk] - 2.)/den[imsk])
  p[imsk] = 2. * (1. - tdist.cdf(t[imsk], Na[imsk] - 2))

  p[~imsk] = np.nan
  rho[~imsk] = np.nan

  p[~dmsk] = np.nan
  rho[~dmsk] = np.nan

  pbar.update(100)

  # Construct and return variables
  from pygeode.var import Var
  from pygeode.dataset import asdataset

  rvs = []

  if 'r' in output:
    r = Var(oaxes, values=rho, name='r')
    r.atts['longname'] = 'Correlation coefficient r between %s and %s' % (xn, yn)
    rvs.append(r)

  if 'r2' in output:
    from warnings import warn
    warn ("r2 now returns the correct value as opposed to r")
    r2 = Var(oaxes, values=rho**2, name='r2')
    r2.atts['longname'] = 'Coefficient of determination r^2 between %s and %s' % (xn, yn)
    rvs.append(r2)

  if 'p' in output:
    p = Var(oaxes, values=p, name='p')
    p.atts['longname'] = 'p-value for correlation coefficient between %s and %s' % (xn, yn)
    rvs.append(p)

  ds = asdataset(rvs)
  ds.atts['description'] = 'correlation analysis %s against %s' % (yn, xn)

  return ds
# }}}
