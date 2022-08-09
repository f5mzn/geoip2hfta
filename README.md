# geoip2hfta
Create a terrain profile using the geoportail (IGN) database API.

## Generate a profile

The following command will request the geoportail API to get obtain a terrain
profile in every direction, degrees per degrees. This process is quite long
because some delays are introduced in the loop in order not to strees the API.

```
python geo2hfta.py --lat=<latitude> --lon=<longitude> --pxf=<file_prefix> [--samples=<samples>] [--radius=<meters>]
```
where:
- lat and long are decimal coordinates
- pfx is the name prefix which will be added in front of each profile file. Pay attention that `HFTA` requires file of 8 characters long at maximum.
- samples is the number of samples in the files (`HTFA` limit is 150)
- radius is the radius of the generated terrain profile.

Example :
```
python geo2hfta.py --lat=49.012691 --lon=2.301487 --pxf=AND --samples=150 --radius=4400
```

## Plot a profile

Also a quick and dirty app which can plot the profile, degrees per degrees. Use
key '+' and '-' to change the plotted azimuth (pay attention to click on the 
window so that it gets the focus).

```
python plot.py --ant=<antenna height in meters> --pfx=<file_prefix>
```
