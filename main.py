import folium
import pandas


def extract_location():
    pd = pandas.read_csv("Volcanoes.txt")
    # print(pd)
    lat = list(pd["LAT"])
    lon = list(pd["LON"])
    names = list(pd["NAME"])
    elev = list(pd["ELEV"])
    elev = ['%.2f' % ele for ele in elev]
    # print(elev)

    values = [lat, lon, names, elev]
    # print(values[0][0])
    # print(values)
    return values


def color_classifier(el):
    if el < 1000:
        return "green"
    if 1000 <= el < 3000:
        return "orange"
    if el >= 3000:
        return "red"


def color_classifier2(x):
    if x["properties"]["POP2005"] < 100000000 :
        return {'fillColor': 'green'}
    elif 100000000 <= x["properties"]["POP2005"] < 400000000 :
        return {'fillColor': 'yellow'}
    elif 40000000 <= x["properties"]["POP2005"] < 800000000 :
        return {'fillColor': 'orange'}
    elif 80000000 <= x["properties"]["POP2005"] < 1000000000:
        return {'fillColor': 'red'}
    else:
        return {'fillColor':'purple'}



def get_iframe(name, height):
    html = "<h4>Volcano information:</h4>Name: {}<br>Height: {} m"
    iframe = folium.IFrame(html=html.format(name, height), width=200, height=100)
    return iframe


def create_marker():
    coords = extract_location()
    mymap = folium.Map(location=[48.7767982, -121.810997], tiles="Stamen Terrain", zoom_start=5)
    fg = folium.FeatureGroup("Volcanoes")

    for i in range(len(coords[0])):
        location = (coords[0][i], coords[1][i])
        iframe = get_iframe(coords[2][i], coords[3][i])  # HTML Popup generated
        # pop = "Name: "+coords[2][i] + " , Height: " + coords[3][i] + "m"
        tooltip = coords[2][i]
        # fg.add_child(folium.Marker(location=location, popup=folium.Popup(iframe),
        #                            tooltip=tooltip,
        #                            icon=folium.Icon(color=color_classifier(float(coords[3][i])),
        #                            icon="glyphicon-unchecked")))
        fg.add_child(folium.CircleMarker(location=location, radius=7,
                                         popup=folium.Popup(iframe),tooltip=tooltip,
                                         fill_color=color_classifier(float(coords[3][i])),
                                         color=color_classifier(float(coords[3][i])),fill_opacity=0.7)
                                         )
    fgp = folium.FeatureGroup("Population")
    fgp.add_child(folium.GeoJson(data=(open("world.json", "r", encoding="utf-8-sig").read()),
                                style_function=color_classifier2))
    mymap.add_child(fgp)
    mymap.add_child(fg)
    mymap.add_child(folium.LayerControl())
    mymap.save("map1.html")


create_marker()
