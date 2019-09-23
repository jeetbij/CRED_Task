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
		cached_address = address.strip().replace(' ', '_')
		coords = cache.get(cached_address.lower())

		try:
			if not coords:
				response = requests.get(url=settings.GOOGLE_MAP_API.format(address, settings.API_KEY))
				response = response.json()
				print(response)
				coords = response['results'][0]['geometry']['location']
				cache.set(cached_address.lower(), coords, settings.CACHE_TIME)
				print('map api called.')
		except Exception as e:
			print(e)
			return Response({
				"error": "Google Api is not responding or it is taking too much time."
				})
		return Response({
			"latitude": coords['lat'],
			"longitude": coords['lng']
			})