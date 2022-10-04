"""This file runs the estimation stage of Pythia"""
import configparser
import csv
from geovoronoi import voronoi_regions_from_coords
from shapely.geometry import box, Point, LineString
import numpy as np

def estimate(mec_hosts,
             UEs,
             base_stations,
             latency,
             upload,
             download):
  """This method estimates the connections 
  between UEs and Base Stations"""
  UEs = obtain_contacts(UEs, base_stations)

  return obtain_links(UEs,
                      base_stations,
                      latency,
                      upload,
                      download)

def obtain_contacts(UEs, base_stations):
  print("Obtaining contacts")
  #This will be used to define the experiment area
  lats = []
  lngs = []

  #Making sure we hold the order of the base stations
  base_names = list(base_stations.keys())
  for b in base_names:
    lats.append(base_stations[b].position[0])
    lngs.append(base_stations[b].position[1])
  #Read UEs positions files
  for ue in UEs.values():
    with open(ue.positions_file) as csvfile:
      reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
      for r in reader:
        ue.positions.append(tuple(r))
        lats.append(r[1])
        lngs.append(r[2])

  #Obtain the area where the experiment takes place
  lat_margin = (max(lats) - min(lats))*0.1
  lng_margin = (max(lngs) - min(lngs))*0.1
  area = box(min(lats) - lat_margin,
               min(lngs) - lng_margin,
               max(lats) + lat_margin,
               max(lngs) + lng_margin)#"""


  #Obtain the positions of the base stations
  bs_positions = \
    np.array([[base_stations[b].position[0], \
              base_stations[b].position[1]] for b in base_names])

  #print(f"Region = {list(area.exterior.coords)}")
  #print(f"Positions = {bs_positions}")

  #Obtaining the voronoi polygons
  region_polys, region_pts = voronoi_regions_from_coords(bs_positions, area)

  #Sorting the voronoi polygons to their base stations
  coverage_region = {}

  for i in region_pts:
    coverage_region[base_names[region_pts[i][0]]] = region_polys[i]

  for ue in UEs.values():
    #Voronoi polygons are always convex.
    #For this reason, a UE walking on a straight line
    #will not get inside the same polygon twice.
    for i in range(len(ue.positions)-1):
      pos_i = ue.positions[i]  #starting position
      pos_j = ue.positions[i+1]  #final position
      #Ignoring two positions in same place, to avoid aritmetic errors
      if pos_i == pos_j:
        continue
      shapely_line = LineString(((pos_i[1],pos_i[2]),(pos_j[1],pos_j[2])))
      for b in base_names:
        intersection_line = list(coverage_region[b].intersection(shapely_line).coords)
        #Obtaining the instants when every point is touched
        #Making sure we analyse an axis with movement
        x = 1
        if (pos_j[x] - pos_i[x]) == 0: 
          x = 2
        speed = (pos_j[0] - pos_i[0])/(pos_j[x] - pos_i[x])
        for intersection_point in intersection_line:
          t = speed * (intersection_point[x-1] - pos_i[x]) + pos_i[0]
          ue.contacts.append((t,b))

  #Comment to see the the voronoi and the trajectories plotted
  """
  for ue in UEs:
    print(f"{ue} contacts = {UEs[ue].contacts}")
  print_voronoi(area, region_polys, base_stations, region_pts, UEs)#"""

  return UEs

def obtain_links(UEs,
                 base_stations,
                 latency,
                 upload,
                 download):
  for ue in UEs:
    UEs[ue].build_links_from_contacts(latency,
                                      upload,
                                      download)
  return UEs

def print_voronoi(region, region_polys, base_stations, region_pts, UEs):
  import matplotlib.pyplot as plt
  from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area


  bs_positions = \
    np.array([[base_stations[b].position[0], \
              base_stations[b].position[1]] for b in base_stations])

  fig, ax = subplot_for_map()

  #Plotting the voronoi and the base stations
  plot_voronoi_polys_with_points_in_area(ax, region, region_polys, bs_positions, region_pts)

  
  for b in base_stations:
    print(f"{b} position: {base_stations[b].position[0]},{base_stations[b].position[1]}")
    plt.annotate(b,
                 (base_stations[b].position[0], 
                 base_stations[b].position[1]))#"""

  for ue in UEs:
    pathx = [x[1] for x in UEs[ue].positions]
    pathy = [y[2] for y in UEs[ue].positions]
    ax.plot(pathx, pathy)
    for p in UEs[ue].positions:
      ax.annotate(p[0],(p[1],p[2]))
  plt.show()





