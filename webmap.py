import folium
import pandas
from geopy.geocoders import Nominatim

def col_guess(col):
    if (col<1000):
        return "green"
    elif (col<1500):
        return "blue"
    elif (col <2000):
        return "red"
    else:
        return "black"


map1 = folium.Map(location=[38.58, -99.09], tiles='MapBox Bright', zoom_start=6)

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=5, fill=True,
                                      popup=str(el)+" m", color="grey", fill_color=col_guess(el), fill_opacity=0.9))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json","r", encoding = 'utf-8-sig').read(),
style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else "yellow" if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

church = pandas.read_csv("church_data.txt")                     #Loading the church data file
nom = Nominatim()
church["Address"] = church["Address"].apply(nom.geocode)        #extracting the coordintes for the respective addresses
church['Longitude'] = church["Address"].apply(lambda x: x.longitude if x != None else None) #extracting the longitude
church['Latitude'] = church["Address"].apply(lambda x: x.latitude if x != None else None)   #extracting the latitude
lat1 = list(church["Latitude"])
lon1 = list(church["Longitude"])
nam = list(church["Name"])

fgc = folium.FeatureGroup(name="Churches")

for lt, ln, nam in zip(lat1, lon1, nam):
    fgc.add_child(folium.Marker(location=[lt, ln], popup=str(nam), icon=folium.Icon(color="grey")))   #second layer of map

map1.add_child(fgc)
map1.add_child(fgv)
map1.add_child(fgp)
map1.add_child(folium.LayerControl())
map1.save("map1.html")