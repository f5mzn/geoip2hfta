#!/usr/bin/env python

import geopy
from geopy.distance import geodesic
import getopt, sys
import requests
import time

samples = 149
radius = 4.400

def get_elevations(lat1, lat2, lon1, lon2):
  global samples

  query = {'sampling':samples, 'lat':"%f|%f" % (lat1, lat2), 'lon':"%f|%f" % (lon1, lon2)}
  response = requests.get('https://wxs.ign.fr/calcul/alti/rest/elevationLine.json', params=query)
  response.raise_for_status()

  data = response.json()
  return data['elevations']

def help():
  print("geo2hfta.py --lat=<latitude> --lon=<longitude> --pxf=<file_prefix> [--samples=<samples>] [--step=1] [--radius=<meters>] [--from-az=<degrees>] [--to-az=<degrees>] [--at-az=<degrees>]")
  print("geo2hfta.py --lat=49.012691 --lon=2.301487 --pxf=AND --samples=150 --radius=4400 --step=10")
  print("geo2hfta.py --lat=49.012691 --lon=2.301487 --pxf=AND --samples=150 --radius=4400 --from-az=0 --to-az=180 --step=10")
  print("geo2hfta.py --lat=49.012691 --lon=2.301487 --pxf=AND --samples=150 --radius=4400 --at-az=300")
  
def main(argv):
  global samples, radius

  lat = lon = pfx = ''
  from_az = 0
  to_az = 360
  step = 1

  try:
    opts, args = getopt.getopt(argv, "hp:", ["lat=","lon=","pfx=","samples=","radius=","step=","from-az=","to-az=","at-az="])
  except getopt.GetoptError:
    print("Bad argument(s): exiting.")
    help()
    sys.exit(1)
  for opt, arg in opts:
    if opt == '-h':
      help()
      sys.exit()
    elif opt == '--lat':
      lat = float(arg)
    elif opt == '--lon':
      lon = float(arg)
    elif opt in ("-p", "--pfx"):
      pfx = arg
    elif opt == "--samples":
      samples = int(arg)
    elif opt == "--radius":
      radius = float(arg) / 1000
    elif opt == "--step":
      step = int(arg)
    elif opt == "--from-az":
      from_az = int(arg)
    elif opt == "--to-az":
      to_az = int(arg)
    elif opt == "--at-az":
      from_az = int(arg)
      to_az = from_az + 1
      step = 1
    else:
      print("Arg '%s' unknow: exiting" % opt)
      sys.exit(2)

  if lat == 0.0 or lon == 0.0 or pfx == '':
    print("Missing argument(s): exiting.")
    help()
    sys.exit(3)

  if to_az < from_az:
    to_az = from_az

  if from_az < 0:
    from_az = 0
  
  if from_az > 360:
    from_az = 360

  if to_az < 0:
    to_az = 0

  if to_az > 360:
    to_az = 360

  if from_az == to_az:
    to_az += step

  tower = (lat, lon)
  origin = geopy.Point(lat, lon)

  for bearing in range(from_az, to_az, step):
    while True:
      print("Creating altitude profile for az=%3d ..." % bearing)
      destination = geodesic(kilometers=radius).destination(origin, bearing)
      elevations = get_elevations(lat, destination.latitude, lon, destination.longitude)

      f = open("%s-%03d.PRO" % (pfx, bearing), "w")
      f.write("meters\r\n")
      for elevation in elevations:
        sample = (float(elevation['lat']), float(elevation['lon']))
        dist = geodesic(tower, sample).km * 1000
        if elevation['z'] == '-99999':
          time.sleep(15)
          print("Error getting profile for az=%3d: retrying" % bearing)
          continue
        f.write("        %10.1f   %-4.1f\r\n" % (dist, float(elevation['z'])))
      f.close()
      break

    # Be gent
    time.sleep(5)

if __name__ == "__main__":
    main(sys.argv[1:])
