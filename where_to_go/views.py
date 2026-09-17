from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from places.models import Place

def show_map(request):
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    features = places_geojson["features"]
    places = Place.objects.all()
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": f"./static/places/{place.pk}.json"
            }
        }
        features.append(feature)

    return render(request, "index.html", {"places_geojson": places_geojson})

def show_place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    return HttpResponse(place.title)