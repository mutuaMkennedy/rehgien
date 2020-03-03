"""
import datetime
from haystack import indexes
from .models import PropertyForSale, RentalProperty

class ForSaleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,
    template_name='search/indexes/listings/for_sale_text.txt')
    name = indexes.CharField(model_attr='name')
    publishdate = indexes.DateTimeField(model_attr='publishdate')
    location_name = indexes.CharField(model_attr='location_name', faceted=True)
    type = indexes.CharField(model_attr='type', faceted=True)
    bathrooms = indexes.CharField(model_attr='bathrooms', faceted=True)
    bedrooms = indexes.CharField(model_attr='bedrooms', faceted=True)
    thumb = indexes.CharField(model_attr='thumb')
    price = indexes.CharField(model_attr='price')
    floor_area = indexes.CharField(model_attr='floor_area')
    size_units = indexes.CharField(model_attr='size_units')

    def get_model(self):
        return  PropertyForSale

    def index_queryset(self, using=None):
        #Used when the entire index for model is updated.
        return self.get_model().objects.filter(publishdate__lte=datetime.datetime.now())

class RentalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,
    template_name='search/indexes/listings/for_rent_text.txt')
    name = indexes.CharField(model_attr='name')
    publishdate = indexes.DateTimeField(model_attr='publishdate')
    location_name = indexes.CharField(model_attr='location_name', faceted=True)
    type = indexes.CharField(model_attr='type', faceted=True)
    bathrooms = indexes.CharField(model_attr='bathrooms', faceted=True)
    bedrooms = indexes.CharField(model_attr='bedrooms', faceted=True)
    thumb = indexes.CharField(model_attr='thumb')
    price = indexes.CharField(model_attr='price')
    floor_area = indexes.CharField(model_attr='floor_area')
    size_units = indexes.CharField(model_attr='size_units')

    def get_model(self):
        return  RentalProperty

    def index_queryset(self, using=None):
        #Used when the entire index for model is updated.
        return self.get_model().objects.filter(publishdate__lte=datetime.datetime.now())
"""
