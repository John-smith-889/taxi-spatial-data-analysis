
import os
os.getcwd()
os.chdir(r"C:\Users\X")

#=============================================================================#
# Solution #
#==========#

#======================#
# Import polygons data #
#======================#

import pandas as pd
taxi_zone_geom = pd.read_csv('taxi-zone-geom.csv')
type(taxi_zone_geom)

#=========================#
# Import coordinates data #
#=========================#

coordinates_query_2014 = pd.read_csv('coordinates-query-2014.csv')
type(coordinates_query_2014)


#=========================#
# Create list of polygons # 
#=========================#
# Create list of all shapely polygon points
list_polygons = []
for i in range(len(taxi_zone_geom)):
    P = shapely.wkt.loads(taxi_zone_geom.loc[i,:][3])
    list_polygons.append(P)

#=======================#
# Create list of points # 
#=======================#
# Create list of all shapely object points
import time


list_points = []
# Start time measuring
start = time.time()
for i in range(len(coordinates_query_2014)):
    list_points.append(Point(coordinates_query_2014.loc[i,:][0],coordinates_query_2014.loc[i,:][1]))
    if i % 10_000 == 0:
        end = time.time()
        print(i, "Iterations passed in ",\
              round((end - start)/60, 2), "minutes." )
        

#===============================#
# Create scoring list of points # 
#===============================#
# Write sores for every zone if a 

# Create list of scores with 263+ zeros
list_scores = [0] * len(taxi_zone_geom)
# iterate over all points
for i in range(len(list_points)):    
    # iterate over all polygons
    for j in range(len(list_polygons)):
        # add score to list if point matching polygon and break this one loop
        if list_polygons[j].contains(list_points[i]) == True:
            list_scores[j] +=1
    if i % 100_000 == 0:
        print(str(i) + " iterations passed.")
    

#==============================#
# Save list_scores to csv file #
#==============================#
import pandas as pd
df = pd.DataFrame(data={"col1": list_scores})
df.to_csv("./list_scores.csv", sep=',',index=True)



#================================#
# Load list_scores from csv file #
#================================#
list_scores = pd.read_csv("./list_scores.csv", sep=',')
#x.col1.sum()

#===================================================#
# Check if all pick-ups consist in defined polygons #
#===================================================#


sum(list_scores)
Out[193]: 15830475

len(coordinates_query_2014)
Out[194]: 15837001

len(coordinates_query_2014) - sum(list_scores)
Out[195]: 6526

6526/15837001
Out[197]: 0.000412072967602894
# Very small percentage of pick-ups is out of defined polygons


#=========================#
# Show most pick up areas #
#=========================#
pd.options.display.max_colwidth = 100

taxi_zone_geom.iloc[0,:]
taxi_zone_geom.iloc[1,:]
taxi_zone_geom.iloc[2,:]
taxi_zone_geom.iloc[3,:]
taxi_zone_geom.iloc[4,:]

taxi_zone_geom.sort_values('scores', ascending=False, inplace = True)
pd.set_option('display.max_rows', 400)

# Show top 20 zones with biggest number of pick-ups
taxi_zone_geom[0:20][['zone_name','borough', 'scores']]

"""
Williamsburg (North Side), Brooklyn, 809111
Astoria, Queens, 788806
East Harlem North, Manhattan, 783504
Central Harlem, Manhattan, 763478
East Harlem South, Manhattan, 700492
"""


