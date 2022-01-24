from io import BufferedRandom
from django.shortcuts import render

# Create your views here.

# Add the following import
from django.http import HttpResponse

class Guitar:  # Note that parens are optional if not inheriting from another class
    def __init__(self, name, brand, description, year):
        self.name = name
        self.brand = brand
        self.description = description
        self.year = year

guitars = [
    Guitar('HD-28', 'Martin', 'Dreadnought style.  Solid Indian rosewood back and sides.  Solid sitka spruce top.  Herringbone trim.  Scalloped X bracing pattern.', 1977),
    Guitar('FT 570-BL', 'Epiphone', 'Jumbo style.  Maple back and sides.  Sitka spruce top.', 1974),
    Guitar('5014', 'Alvarez', '000 Style.  Laminated mahogany back and sides.  Solid sitka spruce top.  Aftermarket electronics.', 1972),
    Guitar('114ce', 'Taylor', 'Grand Auditorium cutaway style.  Laminated walnut back and sides.  Solid sitka spruce top.  Factory electronics', 2019)
]


# Define the home view
# art credit: https://ascii.co.uk/art/guitar 
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def guitars_index(request):
    return render(request, 'guitars/index.html', { 'guitars': guitars })
