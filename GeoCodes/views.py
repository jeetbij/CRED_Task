from rest_framework.views import APIView
from rest_framework.response import Response

import requests
from django.core.cache import cache
from django.conf import settings

class GeoCodeView(APIView):

	def get(self, request, format=None):
		'''Returns lat & lng for a given city.
		If city parameter is missing, default city is Banglore.'''

		data = request.GET.copy()
		address = data.get('city', 'Banglore')
		coords = cache.get(address.lower())

		if not coords:
			response = requests.get(url=settings.GOOGLE_MAP_API.format(address, settings.API_KEY))
			response = response.json()

			coords = response['results'][0]['geometry']['location']
			cache.set(address.lower(), coords, settings.CACHE_TIME)
			print('map api called.')
			
		return Response({
			"latitude": coords['lat'],
			"longitude": coords['lng']
			})