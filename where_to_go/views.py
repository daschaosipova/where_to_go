from django.shortcuts import render
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