from rest_framework_gis.pagination import GeoJsonPagination

class ListingGeoJsonPagination(GeoJsonPagination):
    page_size = 1
