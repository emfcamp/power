#!/usr/bin/env python
# EMFCamp
# Auto generate power distro labeles form build maps power.csv export
# Avery L7173
import labels
import os.path
from reportlab.graphics import shapes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib import colors
from reportlab.lib.units import mm
import datetime
import csv
import urllib2
import random

# config
logo = './resources/logo-white.png'
power = './resources/powerpower.png'
url = 'https://map.emfcamp.org/csv/Power.csv'

# down load the csv and setup a dict reader
response = urllib2.urlopen(url)
nodes = csv.DictReader(response)

# define the label paper (Avery L7173)
specs = labels.Specification(210, 297, 2, 5, 99, 57, corner_radius=2)

# load up the fonts
registerFont(TTFont('Raleway', './resources/Raleway-Regular.ttf'))
registerFont(TTFont('Raleway-Bold', './resources/Raleway-Bold.ttf'))

# what goes on a label
def draw_label(label, width, height, node):
    label.add(shapes.Image(4*mm, 4*mm, 17.49*mm, 49*mm, logo))
    label.add(shapes.String(26*mm, 125, node['name'], fontName="Raleway-Bold", fontSize=18, fillColor=colors.purple))
    label.add(shapes.String(26*mm, 95, node['type'], fontName="Raleway", fontSize=16))
    
    latlong = "{}, {}".format(node['lat'], node['long'])
    label.add(shapes.String(26*mm, 75, latlong, fontName="Raleway", fontSize=14))

    label.add(shapes.Image(92*mm, 0.77*mm, 3.39*mm, 55.46*mm, power))

sheet = labels.Sheet(specs, draw_label, border=False)

# draw each node as a label
for node in nodes:
    sheet.add_label(node)

# save it
sheet.save('node-labels.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))