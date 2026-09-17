from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
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

    place_images = place.images.all()
    image_urls = []
    for img in place_images:
        image_urls.append(img.image.url)

    place_data = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat,
        }
    }
    
    return JsonResponse(
        place_data, 
        safe=False, 
        json_dumps_params={
            "ensure_ascii": False, 
            "indent": 2
        }
    )
