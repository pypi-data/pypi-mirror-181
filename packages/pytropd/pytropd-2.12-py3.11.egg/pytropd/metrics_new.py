# Written by Ori Adam Mar.21.2017
# Edited by Alison Ming Jul.4.2017
import numpy as np
from . import functions as f

def TropD_Metric_EDJ(U, lat, hem=1, lev=np.array([1]), method='peak', n=0, n_fit=1):
  '''TropD Eddy Driven Jet (EDJ) metric
       
     Latitude of maximum of the zonal wind at the level closest to the 850 hPa level
     
     Args:
       U (lat,lev) or U (lat,): Zonal mean zonal wind. Also takes surface wind 
       lat : latitude vector
       lev: vertical level vector in hPa units
       hem: +1 for northern hemisphere (default), -1 for southern hemisphere 
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
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)], n=n)

    else:
      #Default value of n=6 is used
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)])
  
  elif method == 'peak':

    if n:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)], n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)],n=30)
  
  elif method == 'fit':
    Uh = u[(lat > eq_boundary) & (lat <polar_boundary)]
    Lat = lat[(lat > eq_boundary) & (lat <polar_boundary)]
    m = np.nanmax(Uh)
    Im = np.nanargmax(Uh)
     
    if (Im == 0 or Im == len(Uh)-1):
      Phi = Lat[Im]
    
    elif (n_fit > Im or n_fit > len(Uh)-Im+1):
      N = np.min(Im, len(Uh)-Im+1)
      p = np.polyfit(Lat[Im-N:Im+N+1], Uh[Im-N:Im+N+1],2) 
      Phi = -p[1]/(2*p[0])
    else:
      p = np.polyfit(Lat[Im-n_fit:Im+n_fit+1], Uh[Im-n_fit:Im+n_fit+1],2) 
      Phi = -p[1]/(2*p[0])
    
  
  else:
    print('TropD_Metric_EDJ: ERROR: unrecognized method ', method)

  return Phi




def TropD_Metric_OLR(olr, lat, method='250W', Cutoff=50, n=int(6)):
  """TropD Outgoing Longwave Radiation (OLR) metric
     
     Args:
     
       olr(lat,): zonal mean TOA olr (positive)
       
       lat: equally spaced latitude column vector
        
       method (str, optional):

         '250W'(Default): the first latitude poleward of the tropical OLR maximum in each hemisphere where OLR crosses 250W/m^2
         
         '20W': the first latitude poleward of the tropical OLR maximum in each hemisphere where OLR crosses the tropical OLR max minus 20W/m^2
         
         'cutoff': the first latitude poleward of the tropical OLR maximum in each hemisphere where OLR crosses a specified cutoff value
         
         '10Perc': the first latitude poleward of the tropical OLR maximum in each hemisphere where OLR is 10# smaller than the tropical OLR maximum
         
         'max': the latitude of maximum of tropical olr in each hemisphere with the smoothing paramerer n=6 in TropD_Calculate_MaxLat
         
         'peak': the latitude of maximum of tropical olr in each hemisphere with the smoothing parameter n=30 in TropD_Calculate_MaxLat
       
       
       Cutoff (float, optional): Scalar. For the method 'cutoff', Cutoff specifies the OLR cutoff value. 
       
       n (int, optional): For the 'max' method, n is the smoothing parameter in TropD_Calculate_MaxLat
     
     Returns:
     
       tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of near equator OLR threshold crossing in SH and NH
     
  """

  try:
    assert(isinstance(n, int)) 
  except AssertionError:
    print('TropD_Metric_OLR: ERROR: the smoothing parameter n must be an integer')
  
  try:
    assert(n>=1) 
  except AssertionError:
    print('TropD_Metric_OLR: ERROR: the smoothing parameter n must be >= 1')

  
  # make latitude vector monotonically increasing
  if lat[-1] < lat[0]:
    olr = np.flip(olr,0)
    lat = np.flip(lat,0)
    
  eq_boundary = 5
  subpolar_boundary = 40
  polar_boundary = 60
  
  olr_max_lat = f.TropD_Calculate_MaxLat(olr[(lat > eq_boundary) & (lat < subpolar_boundary)],\
                    lat[(lat > eq_boundary) & (lat < subpolar_boundary)])
  olr_max = max(olr[(lat > eq_boundary) & (lat < subpolar_boundary)])


  if method == '20W':
    Phi = f.TropD_Calculate_ZeroCrossing(olr[(lat > olr_max_lat_NH) & (lat <polar_boundary)] - olr_max_NH + 20,\
                    lat[(lat > olr_max_lat_NH) & (lat <polar_boundary)])

  elif method == '250W':
    Phi = f.TropD_Calculate_ZeroCrossing(olr[(lat > olr_max_lat_NH) & (lat <polar_boundary)] - 250,\
                    lat[(lat > olr_max_lat_NH) & (lat <polar_boundary)])

  elif method == 'cutoff':
    Phi = f.TropD_Calculate_ZeroCrossing(olr[(lat > olr_max_lat_NH) & (lat <polar_boundary)] - Cutoff,\
                    lat[(lat > olr_max_lat_NH) & (lat <polar_boundary)])
  
  elif method == '10Perc':
    Phi = f.TropD_Calculate_ZeroCrossing(olr[(lat > olr_max_lat_NH) & (lat <polar_boundary)] / olr_max_NH - 0.9,\
                    lat[(lat > olr_max_lat_NH) & (lat <polar_boundary)])

  elif method == 'max':
    if Cutoff_is_set:
      Phi = f.TropD_Calculate_MaxLat(olr[(lat > eq_boundary) & (lat < subpolar_boundary)],\
                    lat[(lat > eq_boundary) & (lat < subpolar_boundary)], n=n)
    else:
      Phi = np.copy(olr_max_lat_NH)
 
  elif method == 'peak':
    Phi = f.TropD_Calculate_MaxLat(olr[(lat > eq_boundary) & (lat < subpolar_boundary)],\
                    lat[(lat > eq_boundary) & (lat < subpolar_boundary)],n=30)

  else:
    print('TropD_Metric_OLR: unrecognized method ', method)

    Phi = np.empty(0)
  
  return Phi
    
    
def TropD_Metric_PE(pe,lat,method='zero_crossing',lat_uncertainty=0.0):

  ''' TropD Precipitation minus Evaporation (PE) metric
     
      Args:

        pe(lat,): zonal-mean precipitation minus evaporation
   
        lat: equally spaced latitude column vector

        method (str): 
       
          'zero_crossing': the first latitude poleward of the subtropical minimum where P-E changes from negative to positive values. Only one method so far.
  
        lat_uncertainty (float, optional): The minimal distance allowed between the first and second zero crossings along lat

      Returns:
        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of first subtropical P-E zero crossing in SH and NH

  '''    
  try:
    assert(method in ['zero_crossing'])
  except AssertionError:
    print('TropD_Metric_PE: ERROR : unrecognized method ', method)
    
  # make latitude vector monotonically increasing
  if lat[-1] < lat[0]:
      pe = np.flip(pe,0)
      lat = np.flip(lat,0)
    
  # The gradient of PE is used to determine whether PE becomes positive at the zero crossing
  ped = np.interp(lat, (lat[:-1] + lat[1:])/2.0, np.diff(pe))
    
  # define latitudes of boundaries certain regions 
  eq_boundary = 5
  subpolar_boundary = 50
  polar_boundary = 60

    
  # NH
  M1 = f.TropD_Calculate_MaxLat(-pe[(lat > eq_boundary) & (lat < subpolar_boundary)],\
                 lat[(lat > eq_boundary) & (lat < subpolar_boundary)], n=30)
  ZC1 = f.TropD_Calculate_ZeroCrossing(pe[(lat > M1) & (lat <polar_boundary)], \
                 lat[(lat > M1) & (lat <polar_boundary)], lat_uncertainty=lat_uncertainty)
  if np.interp(ZC1, lat, ped) > 0:
    Phi = ZC1
  else:
    Phi = f.TropD_Calculate_ZeroCrossing(pe[(lat > ZC1) & (lat <polar_boundary)], \
                  lat[(lat > ZC1) & (lat <polar_boundary)], lat_uncertainty=lat_uncertainty)
  
  return Phi

def TropD_Metric_PSI(V, lat, lev, method='Psi_500', lat_uncertainty=0):
  ''' TropD Mass streamfunction (PSI) metric

      Latitude of the meridional mass streamfunction subtropical zero crossing
     
      Args:
  
        V(lat,lev): zonal-mean meridional wind
      
        lat: latitude vector

        lev: vertical level vector in hPa units
  
        method (str, optional):
  
          'Psi_500'(default): Zero crossing of the stream function (Psi) at the 500hPa level

          'Psi_500_10Perc': Crossing of 10# of the extremum value of Psi in each hemisphre at the 500hPa level

          'Psi_300_700': Zero crossing of Psi vertically averaged between the 300hPa and 700 hPa levels

          'Psi_500_Int': Zero crossing of the vertically-integrated Psi at the 500 hPa level

          'Psi_Int'    : Zero crossing of the column-averaged Psi
    
        lat_uncertainty (float, optional): The minimal distance allowed between the first and second zero crossings. For example, for lat_uncertainty = 10, the function will return a NaN value if a second zero crossings is found within 10 degrees of the most equatorward zero crossing.   
  
      Returns:

        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of Psi zero crossing in SH and NH
  
  '''


  try:
    assert (lat_uncertainty >= 0)  
  except AssertionError:
    print('TropD_Metric_PSI: ERROR : lat_uncertainty must be >= 0')
  
  try:
    assert(method in ['Psi_500','Psi_500_10Perc','Psi_300_700','Psi_500_Int','Psi_Int'])
  except AssertionError:
    print('TropD_Metric_PSI: ERROR : unrecognized method ', method)
    
  subpolar_boundary = 30
  polar_boundary = 60
    
  Psi = f.TropD_Calculate_StreamFunction(V, lat, lev)
  Psi[np.isnan(Psi)]=0
  # make latitude vector monotonically increasing
  if lat[-1] < lat[0]:
      Psi = np.flip(Psi, 0)
      lat = np.flip(lat, 0)
    
  COS = np.repeat(np.cos(lat*np.pi/180), len(lev), axis=0).reshape(len(lat),len(lev))
    
  if ( method == 'Psi_500' or method == 'Psi_500_10Perc'):
    # Use Psi at the level nearest to 500 hPa
    P = Psi[:,f.find_nearest(lev, 500)]

  elif method == 'Psi_300_700':
    # Use Psi averaged between the 300 and 700 hPa level
    P = np.trapz(Psi[:,(lev <= 700) & (lev >= 300)] * COS[:,(lev <= 700) & (lev >= 300)],\
                  lev[(lev <= 700) & (lev >= 300)]*100, axis=1)

  elif method == 'Psi_500_Int':
    # Use integrated Psi from p=0 to level mearest to 500 hPa
    PPsi_temp = sp.integrate.cumtrapz(Psi*COS, lev, axis=1)
    PPsi = np.zeros(np.shape(Psi))
    PPsi[:,1:] = PPsi_temp
    P = PPsi[:,f.find_nearest(lev, 500)]
     
  elif method == 'Psi_Int':
    # Use vertical mean of Psi 
    P = np.trapz(Psi*COS, lev, axis=1)
  
  else:
    print('TropD_Metric_PSI: ERROR : Unrecognized method ', method)
  
    
  # 1. Find latitude of maximal (minimal) tropical Psi in the NH (SH)
  # 2. Find latitude of minimal (maximal) subtropical Psi in the NH (SH)
  # 3. Find the zero crossing between the above latitudes

  # NH
  Lmax = f.TropD_Calculate_MaxLat(P[(lat > 0) & (lat < subpolar_boundary)],\
                                lat[(lat > 0) & (lat < subpolar_boundary)])

  Lmin = f.TropD_Calculate_MaxLat(-P[(lat > Lmax) & (lat <polar_boundary)],\
                                lat[(lat > Lmax) & (lat <polar_boundary)])
  if method == 'Psi_500_10Perc':
    Pmax = max(P[(lat > 0) & (lat < subpolar_boundary)])
    Phi = f.TropD_Calculate_ZeroCrossing(P[(lat > Lmax) & (lat < Lmin)] - 0.1*Pmax,\
            lat[(lat > Lmax) & (lat < Lmin)])

  else:
    Phi = f.TropD_Calculate_ZeroCrossing(P[(lat > Lmax) & (lat < Lmin)],\
            lat[(lat > Lmax) & (lat < Lmin)], lat_uncertainty=lat_uncertainty)
  
  return Phi

    
def TropD_Metric_PSL(ps, lat, method='peak', n=0):

  ''' TropD Sea-level pressure (PSL) metric

      Latitude of maximum of the subtropical sea-level pressure
  
      Args:
  
        ps(lat,): sea-level pressure
      
        lat: equally spaced latitude column vector

        method (str, optional): 'peak' (default) | 'max'
  
      Returns:

        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of subtropical sea-level pressure maximum SH and NH

  '''
  try:
    assert(method in ['max','peak'])
  except AssertionError:
    print('TropD_Metric_PSL: ERROR : unrecognized method ', method)

  try:
    assert (not hasattr(n, "__len__") and n >= 0)  
  except AssertionError:
    print('TropD_Metric_PSL: ERROR : the smoothing parameter n must be >= 0')

  eq_boundary = 15
  polar_boundary = 60
    
  if method == 'max':
    if n:
      Phi = f.TropD_Calculate_MaxLat(ps[(lat > eq_boundary) & (lat <polar_boundary)],\
             lat[(lat > eq_boundary) & (lat <polar_boundary)],n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(ps[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)])

  elif method == 'peak':
    if n:
      Phi = f.TropD_Calculate_MaxLat(ps[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)], n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(ps[(lat > eq_boundary) & (lat <polar_boundary)],\
              lat[(lat > eq_boundary) & (lat <polar_boundary)], n=30)
  else:
    print('TropD_Metric_PSL: ERROR: unrecognized method ', method)
  
  return Phi
    

def TropD_Metric_STJ(U, lat, lev, method='adjusted_peak', n=0):

  ''' TropD Subtropical Jet (STJ) metric
  
      Args:
  
        U(lat,lev): zonal mean zonal wind

        lat: latitude vector
      
        lev: vertical level vector in hPa units
  
        method (str, optional): 

          'adjusted_peak': Latitude of maximum (smoothing parameter n=30) of the zonal wind averaged between the 100 and 400 hPa levels minus the zonal mean zonal wind at the level closes to the 850 hPa level, poleward of 10 degrees and equatorward of the Eddy Driven Jet latitude
          
	  'adjusted_max' : Latitude of maximum (smoothing parameter n=6) of the zonal wind averaged between the 100 and 400 hPa levels minus the zonal mean zonal wind at the level closes to the 850 hPa level, poleward of 10 degrees and equatorward of the Eddy Driven Jet latitude

          'core_peak': Latitude of maximum of the zonal wind (smoothing parameter n=30) averaged between the 100 and 400 hPa levels, poleward of 10 degrees and equatorward of 70 degrees
          
	  'core_max': Latitude of maximum of the zonal wind (smoothing parameter n=6) averaged between the 100 and 400 hPa levels, poleward of 10 degrees and equatorward of 70 degrees
    
      Returns:

        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of STJ SH and NH

  '''

  try:
    assert (not hasattr(n, "__len__") and n >= 0)  
  except AssertionError:
    print('TropD_Metric_STJ: ERROR : the smoothing parameter n must be >= 0')
  
  try:
    assert(method in ['adjusted_peak','core_peak','adjusted_max','core_max'])
  except AssertionError:
    print('TropD_Metric_STJ: ERROR : unrecognized method ', method)

  eq_boundary = 10
  polar_boundary = 60

  lev_int = lev[(lev >= 100) & (lev <= 400)]

  if (method == 'adjusted_peak' or method == 'adjusted_max'): 
    idx_850 = f.find_nearest(lev, 850)

    # Pressure weighted vertical mean of U minus near surface U
    if len(lev_int) > 1:
      u = np.trapz(U[:, (lev >= 100) & (lev <= 400)], lev_int, axis=1) \
          / (lev_int[-1] - lev_int[0]) - U[:,idx_850]

    else:
      u = np.mean(U[:,(lev >= 100) & (lev <= 400)], axis=1) - U[:,idx_850]

  elif (method == 'core_peak' or method == 'core_max'):
    # Pressure weighted vertical mean of U
    if len(lev_int) > 1:
      u = np.trapz(U[:, (lev >= 100) & (lev <= 400)], lev_int, axis=1) \
          / (lev_int[-1] - lev_int[0])

    else:
      u = np.mean(U[:, (lev >= 100) & (lev <= 400)], axis=1)

  else:
    print('TropD_Metric_STJ: unrecognized method ', method)
    print('TropD_Metric_STJ: optional methods are: adjusted_peak (default), adjusted_max, core_peak, core_max')

  if method == 'core_peak':
    if n:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
          lat[(lat > eq_boundary) & (lat <polar_boundary)], n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
          lat[(lat > eq_boundary) & (lat <polar_boundary)],n=30)

  elif method == 'core_max':
    if n:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
          lat[(lat > eq_boundary) & (lat <polar_boundary)], n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat <polar_boundary)],\
          lat[(lat > eq_boundary) & (lat <polar_boundary)], n=6)

  elif method == 'adjusted_peak':
    Phi_EDJ = TropD_Metric_EDJ(U,lat,lev)
    if n:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < Phi_EDJ)],\
          lat[(lat > eq_boundary) & (lat < Phi_EDJ)], n=n)

    else:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < Phi_EDJ)],\
          lat[(lat > eq_boundary) & (lat < Phi_EDJ)], n=30)

  elif method == 'adjusted_max':
    Phi_EDJ = TropD_Metric_EDJ(U,lat,lev)
    if n:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < Phi_EDJ)],\
          lat[(lat > eq_boundary) & (lat < Phi_EDJ)], n=n)
    else:
      Phi = f.TropD_Calculate_MaxLat(u[(lat > eq_boundary) & (lat < Phi_EDJ)],\
          lat[(lat > eq_boundary) & (lat < Phi_EDJ)], n=6)

  return Phi   

def TropD_Metric_STJ_strength(U, lat, lev):

  ''' TropD Subtropical Jet (STJ) metric
  
      Args:
  
        U(lat,lev): zonal mean zonal wind

        lat: latitude vector
      
        lev: vertical level vector in hPa units
  
      Returns:

        tuple: PhiSH (ndarray), PhiNH (ndarray) STJ strength SH and NH

  '''

  try:
    assert (not hasattr(n, "__len__") and n >= 0)  
  except AssertionError:
    print('TropD_Metric_STJ: ERROR : the smoothing parameter n must be >= 0')
  
  try:
    assert(method in ['adjusted_peak','core_peak','adjusted_max','core_max'])
  except AssertionError:
    print('TropD_Metric_STJ: ERROR : unrecognized method ', method)

  eq_boundary = 10
  polar_boundary = 60

  lev_int = lev[(lev >= 100) & (lev <= 400)]

  idx_850 = f.find_nearest(lev, 850)

  # Pressure weighted vertical mean of U minus near surface U
  if len(lev_int) > 1:
    u = np.trapz(U[:, (lev >= 100) & (lev <= 400)], lev_int, axis=1) \
        / (lev_int[-1] - lev_int[0]) - U[:,idx_850]

  else:
    u = np.mean(U[:,(lev >= 100) & (lev <= 400)], axis=1) - U[:,idx_850]

  Phi_EDJ = TropD_Metric_EDJ(U,lat,lev)

  PhiNH, Phi_strength = f.TropD_Calculate_EqPeaks(u[(lat > eq_boundary) & (lat < Phi_EDJ)],\
      lat[(lat > eq_boundary) & (lat < Phi_EDJ)])


  return Phi, Phi_strength  

def TropD_Metric_TPB(T, lat, lev, method='max_gradient', n=0, Z=None, Cutoff=15*1000):

  ''' TropD Tropopause break (TPB) metric
  
      Args:

        T(lat,lev): temperature (K)

        lat: latitude vector

        lev: pressure levels column vector in hPa

        method (str, optional): 
  
          'max_gradient' (default): The latitude of maximal poleward gradient of the tropopause height
  
          'cutoff': The most equatorward latitude where the tropopause crosses a prescribed cutoff value
  
          'max_potemp': The latitude of maximal difference between the potential temperature at the tropopause and at the surface
  
        Z(lat,lev) (optional): geopotential height (m)

        Cutoff (float, optional): geopotential height (m) cutoff that marks the location of the tropopause break

      Returns:
        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of tropopause break SH and NH

  '''


  Rd = 287.04
  Cpd = 1005.7
  k = Rd / Cpd
  try:
    assert (not hasattr(n, "__len__") and n >= 0)  
  except AssertionError:
    print('TropD_Metric_TPB: ERROR : the smoothing parameter n must be >= 0')

  try:
    assert(method in ['max_gradient','max_potemp','cutoff'])
  except AssertionError:
    print('TropD_Metric_TPB: ERROR : unrecognized method ', method)
  
  polar_boundary = 60

  if method == 'max_gradient':
    Pt = f.TropD_Calculate_TropopauseHeight(T,lev)
    Ptd = np.diff(Pt) / (lat[1] - lat[0])
    lat2 = (lat[1:] + lat[:-1]) / 2
    
    if (n >= 1):
      Phi = f.TropD_Calculate_MaxLat(Ptd[:,(lat2 > 0) & (lat2 <polar_boundary)],\
              lat2[(lat2 > 0) & (lat2 <polar_boundary)], n=n)
    
    else:
      Phi = f.TropD_Calculate_MaxLat(Ptd[:,(lat2 > 0) & (lat2 <polar_boundary)],\
              lat2[(lat2 > 0) & (lat2 <polar_boundary)])
     
  elif method == 'max_potemp':
    XF = np.tile((lev / 1000) ** k, (len(lat), 1))
    PT = T / XF
    Pt, PTt = f.TropD_Calculate_TropopauseHeight(T, lev, Z=PT)
    PTdif = PTt - np.nanmin(PT, axis = 1)
    if (n >= 1):
      Phi = f.TropD_Calculate_MaxLat(PTdif[:,(lat > 0) & (lat <polar_boundary)],\
              lat[(lat > 0) & (lat <polar_boundary)], n=n)
    
    else:
      Phi = f.TropD_Calculate_MaxLat(PTdif[:,(lat > 0) & (lat <polar_boundary)],\
              lat[(lat > 0) & (lat <polar_boundary)], n=30)
   
  elif method == 'cutoff':
    Pt, Ht = f.TropD_Calculate_TropopauseHeight(T, lev, Z)
    
    # make latitude vector monotonically increasing
    if lat[-1] < lat[0]:
      Ht = np.flip(np.squeeze(Ht),0)
      lat = np.flip(lat,0)
    
    polar_boundary = 60
      
    Phi = f.TropD_Calculate_ZeroCrossing(Ht[(lat > 0) & (lat <polar_boundary)] - Cutoff,
              lat[(lat > 0) & (lat <polar_boundary)])
  
  else:
    print('TropD_Metric_TPB: ERROR : Unrecognized method ', method)

  return Phi
  

def TropD_Metric_UAS(U, lat, lev=np.array([1]), method='zero_crossing', lat_uncertainty = 0):
  
  ''' TropD near-surface zonal wind (UAS) metric
  
      Args:

        U(lat,lev) or U (lat,)-- Zonal mean zonal wind. Also takes surface wind 
        
        lat: latitude vector
        
        lev: vertical level vector in hPa units. lev=np.array([1]) for single-level input zonal wind U(lat,)

        method (str): 
          'zero_crossing': the first subtropical latitude where near-surface zonal wind changes from negative to positive

        lat_uncertainty (float, optional): the minimal distance allowed between the first and second zero crossings
  
      Returns:
        tuple: PhiSH (ndarray), PhiNH (ndarray) Latitude of first subtropical zero crossing of the near surface zonal wind in SH and NH
        
  '''

  try:
    assert (lat_uncertainty >= 0)  
  except AssertionError:
    print('TropD_Metric_UAS: ERROR : lat_uncertainty must be >= 0')
    
  try:
    assert(method in ['zero_crossing'])
  except AssertionError:
    print('TropD_Metric_UAS: ERROR : unrecognized method ', method)
    
  if len(lev) > 1:
    uas = U[:,f.find_nearest(lev, 850)]
  else:
    uas = np.copy(U)
    
  # make latitude vector monotonically increasing
  if lat[-1] < lat[0]:
      uas = np.flip(uas,0)
      lat = np.flip(lat,0)

  # define latitudes of boundaries certain regions 
  eq_boundary = 5
  subpolar_boundary = 30
  polar_boundary = 60

  uas_min_lat = f.TropD_Calculate_MaxLat(-uas[(lat > eq_boundary) & (lat < subpolar_boundary)],\
                   lat[(lat > eq_boundary) & (lat < subpolar_boundary)])
  try:
    assert(method == 'zero_crossing')
    Phi = f.TropD_Calculate_ZeroCrossing(uas[(lat > uas_min_lat) & (lat <polar_boundary)],\
            lat[(lat > uas_min_lat) & (lat <polar_boundary)], lat_uncertainty=lat_uncertainty)

    return Phi
  except AssertionError:
    print('TropD_Metric_UAS: ERROR : unrecognized method ', method)

# ========================================  
#Stratospheric metrics
#

## Written by Kasturi Shah
# Last updated: August 3 2020
# converted to python by Alison Ming 8 April 2021
    
def Shah_et_al_2020_GWL_3D(tracer_3d_strat=None,lon=None,lat=None,pressure_strat=None,timepoints=None,*args,**kwargs):
    '''Computes the gradient-weighted latitude (GWL) from 3-D tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_3d_strat: numpy array (dimensions: lon x lat x pressure x time)
    longitude: numpy array in degrees (1-D)
    latitude: numpy array in degrees (1-D)
    pressure: numpy array (1-D)
    time: numpy array (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH (dimensions: pressure x time)
    * GWL width SH (dimensions: pressure x time)

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lon, lat, pressure, time
    nlon=len(lon)
    nlat=len(lat)
    npressure=len(pressure_strat)
    ntimepoints=len(timepoints)

    nlat=np.where(lat > 0)[0]
    tracer_3d_strat=tracer_3d_strat[:,nlat,:,:]

    lat90n = np.where(abs(lat[nlat]-90)==np.min(abs(lat[nlat]-90)))[0][0]

    # arrays for storing area-equivalent GWL widths
    tracer_steep_equiv = np.empty((npressure,ntimepoints))
    tracer_steep_equiv[:] = np.nan

    lat_in_rad = np.deg2rad(lat)

    for dt in np.arange(ntimepoints):
        for p in np.arange(npressure):

            # arrays for storing the GWL widths
            gradient_weighted_lat = np.empty((nlon,))
            gradient_weighted_lat[:] = np.nan

            for k in np.arange(nlon):

                # calculating gradients
                gradient=np.diff(tracer_3d_strat[k,:lat90n+1,p,dt].T) / np.diff(lat_in_rad[nlat[:lat90n+1]])
                gradient_weighted_lat[k] = np.sum(lat_in_rad[nlat[:lat90n]] * gradient \
                                                * np.cos(lat_in_rad[nlat[:lat90n]]))  \
                                               / np.sum(gradient * np.cos(lat_in_rad[nlat[:lat90n]]))
            # area equivalent latitude at this pressure and longitude 
            #(in degrees)
            tracer_steep_equiv[p,dt]=np.rad2deg(np.arcsin(np.nansum(np.sin(gradient_weighted_lat))/nlon))


    
    return tracer_steep_equiv

    
def Shah_et_al_2020_GWL_zonalmean(tracer_2d_strat=None,lat=None,pressure_strat=None,timepoints=None,*args,**kwargs):
    '''Computes the gradient-weighted latitude (GWL) from zonal mean tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_2d_strat: numpy array (dimensions: lat x pressure x time)
    latitude: numpy array in degrees (1-D)
    pressure: numpy array (1-D)
    time: numpy array (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH (dimensions: pressure x time)
    * GWL width SH (dimensions: pressure x time)

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lat, pressure, time
    nlat=len(lat)
    npressure=len(pressure_strat)
    ntimepoints=len(timepoints)

    nlat=np.where(lat > 0)[0]
    tracer_2d_strat=tracer_2d_strat[nlat,:,:]

    lat90n = np.where(abs(lat[nlat]-90)==np.min(abs(lat[nlat]-90)))[0][0]

    # arrays for storing area-equivalent GWL widths
    tracer_steep_equiv=np.empty((npressure,ntimepoints))
    tracer_steep_equiv[:] = np.nan

    lat_in_rad = np.deg2rad(lat)

    for dt in np.arange(ntimepoints):
        for p in np.arange(npressure):
            # calculating gradients
            gradient=np.diff(tracer_2d_strat[:lat90n+1,p,dt]) / np.diff(lat_in_rad[nlat[:lat90n+1]])

            tracer_steep_equiv[p,dt] = np.rad2deg(np.sum(lat_in_rad[nlat[:lat90n]] * gradient \
                                            * np.cos(lat_in_rad[nlat[:lat90n]])) \
                                            / np.sum(gradient * np.cos(lat_in_rad[nlat[:lat90n]])) )


    return tracer_steep_equiv

def TropD_Metric_GWL(tracer_2d_strat=None,lat=None,*args,**kwargs):
    '''Computes the gradient-weighted latitude (GWL) from zonal mean tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_2d_strat: numpy array (dimensions: lat)
    latitude: numpy array in degrees (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH 
    * GWL width SH 

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lat, pressure, time
    nlat=len(lat)

    nlat=np.where(lat > 0)[0]
    tracer_2d_strat=tracer_2d_strat[nlat]

    lat90n = np.where(abs(lat[nlat]-90)==np.min(abs(lat[nlat]-90)))[0][0]

    # arrays for storing area-equivalent GWL widths

    lat_in_rad = np.deg2rad(lat)

    # calculating gradients
    gradient=np.diff(tracer_2d_strat[:lat90n+1]) / np.diff(lat_in_rad[nlat[:lat90n+1]])

    tracer_steep_equiv = np.rad2deg(np.sum(lat_in_rad[nlat[:lat90n]] * gradient \
                                    * np.cos(lat_in_rad[nlat[:lat90n]])) \
                                    / np.sum(gradient * np.cos(lat_in_rad[nlat[:lat90n]])) )


    return tracer_steep_equiv

    
def Shah_et_al_2020_one_sigma_3D(tracer_3d_strat=None,lon=None,lat=None,pressure_strat=None,timepoints=None,*args,**kwargs):
    '''Computes the one-sigma width from 3-D tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_3d_strat: numpy array (dimensions: lon x lat x pressure x time)
    longitude: numpy array in degrees (1-D)
    latitude: numpy array in degrees (1-D)
    pressure: numpy array (1-D)
    time: numpy array (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH (dimensions: pressure x time)
    * GWL width SH (dimensions: pressure x time)

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lon, lat, pressure, time
    nlon=len(lon)
    nlat=len(lat)
    npressure=len(pressure_strat)
    ntimepoints=len(timepoints)

    nlat = np.where(lat > 0)[0]
    tracer_3d_strat=tracer_3d_strat[:,nlat,:,:]


    # arrays for widths at each longitude
    tracer_sigma = np.empty((nlon,npressure,ntimepoints))
    tracer_sigma[:] = np.nan

    tracer_sigma_equiv = np.empty((npressure,ntimepoints))
    tracer_sigma_equiv[:] = np.nan

    lat_in_rad = np.deg2rad(lat)

    for dt in np.arange(ntimepoints):
        for pressure in np.arange(npressure):
            for k in np.arange(nlon):

                lat_delta=np.nanmean(np.diff(lat))
                gap_ind=int(round(70 / lat_delta))

                # finding range of 70degs with biggest max values
                maxval = np.empty((len(lat) - gap_ind),)
                maxval[:] = np.nan

                for ind in np.arange(len(lat) - gap_ind):
                    maxval[ind] = np.nansum(tracer_3d_strat[k,ind:ind+gap_ind+1,pressure,dt])

                a = np.nanmax(maxval)
                maxind = np.where(maxval==a)[0][0]

                # mean and std 35N-35S
                mean70deg=np.nanmean(tracer_3d_strat[k,maxind:(maxind+gap_ind+1),pressure,dt])
                std70deg=np.nanstd(tracer_3d_strat[k,maxind:(maxind+gap_ind+1),pressure,dt], ddof=1)

                threshold=mean70deg - std70deg

                # finding latitudes less than this threshold
                nlatless = np.where(tracer_3d_strat[k,:,pressure,dt] < threshold)[0]

                if np.size(nlatless) != 0:
                    if nlatless[0] != 0:
                        tracer_sigma[k,pressure,dt]=lat_in_rad[nlat[nlatless[0]]]
                    else: # if lowest value is the equator, pick second one 
                        if len(nlatless) > 1: 
                            tracer_sigma[k,pressure,dt]=lat_in_rad[nlat[nlatless[1]]]


            # area equivalent latitude at this pressure and time (in degrees)
            tracer_sigma_equiv[pressure,dt]=np.rad2deg(np.arcsin(np.nansum(np.sin(tracer_sigma[:,pressure,dt]))/nlon))

    return tracer_sigma_equiv


    
def Shah_et_al_2020_one_sigma_zonalmean(tracer_2d_strat=None,lat=None,pressure_strat=None,timepoints=None,*args,**kwargs):
    '''Computes the one-sigma width from zonal mean tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_2d_strat: numpy array (dimensions: lat x pressure x time)
    latitude: numpy array in degrees (1-D)
    pressure: numpy array (1-D)
    time: numpy array (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH (dimensions: pressure x time)
    * GWL width SH (dimensions: pressure x time)

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lat, pressure, time
    npressure=len(pressure_strat)
    ntimepoints=len(timepoints)

    nlat = np.where(lat > 0)[0]
    tracer_2d_strat = tracer_2d_strat[nlat,:,:]


    # arrays for area-equivalent one sigma widths

    tracer_sigma_equiv = np.empty((npressure,ntimepoints))
    tracer_sigma_equiv[:] = np.nan

    for dt in np.arange(timepoints):
        for pressure in np.arange(npressure):
            
            lat_delta=np.nanmean(np.diff(lat))
            gap_ind=int(round(70 / lat_delta))

            # finding range of 70degs with biggest max values
            maxval = np.empty((len(lat) - gap_ind),)
            maxval[:] = np.nan
            for ind in np.arange(len(lat) - gap_ind):
                maxval[ind] = np.nansum(tracer_2d_strat[ind:ind+gap_ind+1,pressure,dt])

            a = np.nanmax(maxval)
            maxind = np.where(maxval==a)[0][0]

            # mean and std 35N-35S
            mean70deg=np.nanmean(tracer_2d_strat[maxind:(maxind+gap_ind+1),pressure,dt])
            std70deg=np.nanstd(tracer_2d_strat[maxind:(maxind+gap_ind+1),pressure,dt], ddof=1)

            threshold=mean70deg - std70deg

            # finding latitudes less than this threshold
            nlatless = np.where(tracer_2d_strat[:,pressure,dt] < threshold)[0]
            if np.size(nlatless) != 0:
                if nlatless[0] != 0:
                    tracer_sigma_equiv[pressure,dt]=lat[nlat[nlatless[0]]]
                else: # if lowest value is the equator, pick second one 
                    if len(nlatless) > 1: 
                        tracer_sigma_equiv[pressure,dt]=lat[nlat[nlatless[1]]]

    return tracer_sigma_equiv

def TropD_Metric_ONESIGMA(tracer_2d_strat=None,lat=None,*args,**kwargs):
    '''Computes the one-sigma width from zonal mean tracer data 
    Reference: Shah et al., JGR-A, 2020
  
    Parameters
    ==========
    tracer_2d_strat: numpy array (dimensions: lat)
    latitude: numpy array in degrees (1-D)
  
    Returns
    =======
    output: tuple
    * GWL width NH 
    * GWL width SH 

    Notes
    =====
    Note that this script assumes that the latitude array:
    (1) is IN DEGREES, and
    (2) starts with the SH & becomes increasingly positive, i.e. -90 to 90.
    ''' 

    # dimensions of lat, pressure, time

    nlat = np.where(lat > 0)[0]
    tracer_2d_strat = tracer_2d_strat[nlat]


    # arrays for area-equivalent one sigma widths

    lat_delta=np.nanmean(np.diff(lat))
    gap_ind=int(round(70 / lat_delta))

    # finding range of 70degs with biggest max values
    maxval = np.empty((len(lat) - gap_ind),)
    maxval[:] = np.nan
    for ind in np.arange(len(lat) - gap_ind):
        maxval[ind] = np.nansum(tracer_2d_strat[ind:ind+gap_ind+1])

    a = np.nanmax(maxval)
    maxind = np.where(maxval==a)[0][0]

    # mean and std 35N-35S
    mean70deg=np.nanmean(tracer_2d_strat[maxind:(maxind+gap_ind+1)])
    std70deg=np.nanstd(tracer_2d_strat[maxind:(maxind+gap_ind+1)], ddof=1)

    threshold=mean70deg - std70deg

    # finding latitudes less than this threshold
    nlatless = np.where(tracer_2d_strat[:] < threshold)[0]
    if np.size(nlatless) != 0:
        if nlatless[0] != 0:
            tracer_sigma=lat[nlat[nlatless[0]]]
        else: # if lowest value is the equator, pick second one 
            if len(nlatless) > 1: 
                tracer_sigma_equiv=lat[nlat[nlatless[1]]]

    return tracer_sigma_equiv

