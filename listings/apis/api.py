# from tastypie.resources import ModelResource
# from listings.models import PropertyForSale,RentalProperty
#
# class MyModelResource(ModelResource):
#     class Meta:
#         queryset = PropertyForSale.objects.all().values('location')
# 
#     def dehydrate(self, bundle):
#         # remove unneeded point-field from the response data
#         del bundle.data['point']
#         # add required fields back to the response data in the form we need it
#         bundle.data['lat'] = bundle.obj.point.y
#         bundle.data['lng'] = bundle.obj.point.x
#         return bundle
