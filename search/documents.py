from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from listings.models import PropertyForSale, RentalProperty


@registry.register_document
class HomesForSaleDocument(Document):
    class Index:
        #name of elasticsearh index
        name = 'homes_for_sale'
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0,
        }
    class Django:
        model = PropertyForSale
        fields = [
            'property_name','type', 'price','location_name','thumb',
            'bathrooms', 'bedrooms', 'floor_area', 'size_units','id',

        ]

@registry.register_document
class HomesForRentDocument(Document):
    class Index:
        #name of elasticsearh index
        name = 'homes_for_rent'
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0,
        }
    class Django:
        model = RentalProperty
        fields = [
            'property_name', 'type', 'price','location_name','thumb',
            'bathrooms', 'bedrooms', 'floor_area', 'size_units','id',

        ]
