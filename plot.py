import matplotlib.pyplot as plt
import numpy as np
import getopt, sys

ylim = 0
az = 0
ant_h = 0
pfx = ''

def update(az):
  global h, pfx, ylim

  h = 0
  dist = 0

  x = []
  y = []

  with open("%s-%03d.PRO" % (pfx, az), "r") as fp:
    lines = fp.readlines()
    for line in lines:
      cols = line.split()
      if len(cols) == 2:
        dist = float(cols[0])
        h = float(cols[1])
        x.append(dist)
        y.append(h)

  plt.cla()
  plt.ylim([0, ylim])
  plt.title("Profile @%d°" % az)
  # terrain profile
  plt.plot(x, y)
  # antenna
  plt.scatter(0, ant_h, s = 25, c = 'yellow', marker = '^', edgecolors = 'green')
  # horizon
  plt.plot([0, dist], [ant_h, ant_h], linestyle = 'dotted')
  plt.draw()

def on_press(event):
  global az
  if event.key == '+':
    az = az + 1
    if az > 359:
      az = 0
    update(az)
  elif event.key == '-':
    az = az - 1
    if az < 0:
      az = 359
    update(az)
  elif event.key == 'escape':
        sys.exit(0)

def help():
  print("plot.py --ant=<antenna height> --pfx=<file_prefix>")
  print("plot.py --ant=211 --pfx=AND")

def main(argv):
  global ylim, pfx, ant_h

  try:
    opts, args = getopt.getopt(argv, "hp:", ["ant=","pfx="])
  except getopt.GetoptError:
    print("Bad argument(s): exiting.")
    help()
    sys.exit(1)
  for opt, arg in opts:
    if opt == '-h':
      help()
      sys.exit()
    elif opt == '--ant':
      ant_h = float(arg)
    elif opt in ("-p", "--pfx"):
      pfx = arg
    else:
      print("Arg '%s' unknow: exiting" % opt)
      sys.exit(2)
  
  ylim = float(ant_h) + 50

  plt.ion()
  fig = plt.figure()
  fig.canvas.mpl_connect('key_press_event', on_press)
  update(az)

  while True:
    plt.pause(0.1)

if __name__ == "__main__":
    main(sys.argv[1:])
