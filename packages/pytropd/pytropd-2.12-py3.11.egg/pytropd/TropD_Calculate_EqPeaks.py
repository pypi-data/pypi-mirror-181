#________________________________________________
# added by Molly Menzel July.2019
def TropD_Calculate_EqPeaks(F,lat):
  ''' Find latitude and magnitude of most equatorward peak for a given interval

      Args:

        F: 1D array

        lat: equally spaced latitude array

      Returns:

        float: location and magnitude of equatorward peak of F along lat
  '''

  # finding the peaks of the field in the given latitudinal interval
  peaks, _  = sp.signal.find_peaks(F)

  if 0 == len(peaks): # if no peaks
    Ymax = np.nan
    maxval = np.nan

  else:
    if 1 == len(peaks): # if only one peak
      ind = int(peaks)
    else:
      min_lat = np.nanmin(abs(lat[peaks])) # if multiple peaks, find the most equatorward peak
      ind = int(f.find_nearest(abs(lat),min_lat))

    # applying a quadratic fit to the field around its maximum
    latt = lat[ind-1:ind+2]
    Ff = F[ind-1:ind+2]
    new_lat = np.arange(latt[0],latt[2],0.01) 
    p = np.polyfit(latt, Ff,2) 
    quad_fit = p[0]*new_lat**2+p[1]*new_lat+p[2] # apply a quadratic fit to the field around its maximum

    # finding the location and magnitude of the quadratic fit's maximum
    maxval = np.nanmax(quad_fit)
    indd = f.find_nearest(quad_fit,maxval)
    Ymax = new_lat[indd]

  return Ymax, maxval
