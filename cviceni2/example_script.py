#!/usr/bin/env python3
"""
Simple Geoinformatics Showcase Script

This script demonstrates how to create an interactive map using the folium library.
It displays a world map with markers for a few notable cities and a circle marker for visual interest.
Map tiles are loaded online, so no additional data download is required.
"""

# Import necessary libraries
import folium        # For map creation
import webbrowser    # To open the map automatically in a browser
import os            # To work with file paths

# Create a map centered at latitude 20 and longitude 0 with a zoom level to show most of the world.
map_center = [20, 0]
map_zoom = 2
my_map = folium.Map(location=map_center, zoom_start=map_zoom)

# Define a list of cities with their names and geographic coordinates.
cities = [
    ("New York", [40.7128, -74.0060]),
    ("London", [51.5074, -0.1278]),
    ("Tokyo", [35.6895, 139.6917]),
    ("Paris", [48.8566, 2.3522]),
    ("Olomouc", [49.5956, 17.2488])
]

# Add a marker for each city to the map.
for name, coords in cities:
    folium.Marker(
        location=coords,                    # Marker position
        popup=name,                         # Text displayed on click
        icon=folium.Icon(color='blue', icon='info-sign')  # Customized marker icon
    ).add_to(my_map)

# Add a circle marker at the center of the map for extra visualization.
folium.Circle(
    location=map_center,   # Center of the circle
    radius=1000000,        # Radius in meters
    color='green',         # Outline color
    fill=True,             # Enable filling the circle
    fill_color='green'     # Fill color
).add_to(my_map)

# Save the generated map to an HTML file in the same directory as the script.
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, "simple_geoinformatics_showcase.html")
my_map.save(output_file)

# Automatically open the created HTML file in the default web browser.
webbrowser.open("file://" + output_file)

# Inform the user that the map has been created.
print("The interactive map has been created and opened in your default web browser.")
