from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
                "coordinates": [float(place.lng), float(place.lat)]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": reverse('place_detail', args=[place.pk])
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
        "short_description": place.short_description,
        "long_description": place.long_description,
        "coordinates": {
            "lng": float(place.lng),
            "lat": float(place.lat),
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
