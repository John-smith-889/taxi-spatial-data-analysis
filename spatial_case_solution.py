
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


#=================================================================#
# Charts #
#========#

#================================================#
# Draw a map #
#============#

#=====================#
# Create geopandas df #
#=====================#

# Add pandas series scores as a column to df for visualization
taxi_zone_geom['scores'] = list_scores['col1']
taxi_zone_geom.iloc[0,:]


# Convert polygons and multipolygons to shapely objects
import shapely
list_polygons = []
for i in range(len(taxi_zone_geom)):
    P = shapely.wkt.loads(taxi_zone_geom.loc[i,:][3])
    list_polygons.append(P)

# assign object to new column 'geometry'
taxi_zone_geom['geometry'] = list_polygons

# Convert 'taxi_zone_geom' df to geodf
my_geo_df = gpd.GeoDataFrame(taxi_zone_geom, geometry='geometry')
type(my_geo_df)


#======================#
# Plot NY taxi pickups #
#======================#
import descartes
%matplotlib
my_geo_df.plot(legend=True)

# Plot New York taxi pick ups with an accurate legend
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
# Create figure and axis
#fig, ax = plt.subplots(1, 1)
fig, ax = plt.subplots(figsize=(20, 10))

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)


# Add a plot
my_geo_df.plot(column='scores', ax=ax, legend=True, cax=cax)

# Add title and axis names
ax.set_title("Taxi pick ups in New York 2014", fontsize=25)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)



#===============================================================#
# Draw charts #
#=============#

#====================================================#
# Wykres przejazdow w poszczegolnych dniach tygodnia #
#====================================================#

# libraries
import numpy as np
import matplotlib.pyplot as plt
 
# dataset
height = [2886558, 2529861, 2403479, 2166242, 2116223, 1901826, 1832812]
bars = ('Saturday', 'Friday', 'Sunday', 'Thursday', 'Wednesday', 'Tuesday','Monday' )
y_pos = np.arange(len(bars))
 
# Create bars and choose color
plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))
 
# Add title and axis names
plt.title('Liczba przejazdów taksówkami SHL w Nowym Jorku w 2014 roku')
plt.xlabel('Dzień tygodnia')
plt.ylabel('liczba przejazdów')
 
# Limits for the Y axis
plt.ylim(0,60)
 
# Create names
plt.xticks(y_pos, bars)
 
# Show graphic
plt.show()


#=============================================#
# wykres liczby przejazdów z płatnoscia karta #
#=============================================#

# dataset
height = [284612, 353284, 479830, 512879, 579003, 552074, 531051,568535,598759,670519,703034,719046]
bars = ('Jan', 'Feb', 'March', 'April', 'May', 'June','July','Aug','Sept', 'Oct', 'Nov', 'Dec'  )
y_pos = np.arange(len(bars))
 
# Create bars and choose color
plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))
 
# Add title and axis names
plt.title('Liczba przejazdów taksówkami SHL z płatnością kartą w Nowym Jorku w 2014 roku' )
plt.xlabel('Miesiąc')
plt.ylabel('liczba przejazdów')
 
# Limits for the Y axis
#plt.ylim(0,60)
 
# Create names
plt.xticks(y_pos, bars)
 
# Show graphic
plt.show()


#========================================================#
# wykres sum płatnosci karta w poszczegolnych miesiacach #
#========================================================#


# dataset
height = [5.067846, 6.343703, 8.628222, 9.353807, 11.054191, 10.500344, 9.920291,10.583308,11.148563,12.159160,12.519116,12.905380]
bars = ('Jan', 'Feb', 'March', 'April', 'May', 'June','July','Aug','Sept', 'Oct', 'Nov', 'Dec'  )
y_pos = np.arange(len(bars))
 
# Create bars and choose color
plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))
 
# Add title and axis names
plt.title('Płatności kartą podczas przejazdów taksówkami SHL w Nowym Jorku w 2014 roku' )
plt.xlabel('Miesiąc')
plt.ylabel('Suma płatności w danym miesiącu (miliony dolarów)')
 
# Limits for the Y axis
#plt.ylim(0,60)
 
# Create names
plt.xticks(y_pos, bars)
 
# Show graphic
plt.show()


#===============================================#
# wykres liczby przejazdów z płatnoscia gotowka #
#===============================================#

# dataset
height = [514779, 647402, 808091, 791204, 837085, 780533, 736623,769610,756047,812702,835802,916998]
bars = ('Jan', 'Feb', 'March', 'April', 'May', 'June','July','Aug','Sept', 'Oct', 'Nov', 'Dec'  )
y_pos = np.arange(len(bars))
 
# Create bars and choose color
plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))
 
# Add title and axis names
plt.title('Liczba przejazdów taksówkami SHL z płatnością gotówką w Nowym Jorku w 2014 roku' )
plt.xlabel('Miesiąc')
plt.ylabel('liczba przejazdów')
 
# Limits for the Y axis
#plt.ylim(0,60)
 
# Create names
plt.xticks(y_pos, bars)
 
# Show graphic
plt.show()



#==========================================================#
# wykres sum płatnosci gotowka w poszczegolnych miesiacach #
#==========================================================#

# dataset
height = [5.891990, 7.540944, 9.384446, 9.340737, 10.187642, 9.473473, 89.25931,9.399270,9.130888,9.664547,9.768032,10.675385]
bars = ('Jan', 'Feb', 'March', 'April', 'May', 'June','July','Aug','Sept', 'Oct', 'Nov', 'Dec'  )
y_pos = np.arange(len(bars))
 
# Create bars and choose color
plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))
 
# Add title and axis names
plt.title('Płatności gotówką podczas przejazdów taksówkami SHL w Nowym Jorku w 2014 roku' )
plt.xlabel('Miesiąc')
plt.ylabel('Suma płatności w danym miesiącu (dolary)')
 
# Limits for the Y axis
#plt.ylim(0,60)
 
# Create names
plt.xticks(y_pos, bars)
 
# Show graphic
plt.show()



