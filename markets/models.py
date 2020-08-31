from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from django.urls import reverse
from multiselectfield import MultiSelectField


# Request are published as leads

class PropertyRequestLead(models.Model):
    PROPERTY_TYPE_CHOICES = {
    ('APARTMENT', 'Apartment'), ('BUNGALOW', 'Bungalow'),
    ('CONDOMINIUM', 'Condominium'), ('DORMITORY', 'Dormitory'),
    ('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'),
    ('SINGLEFAMILY', 'Single family'), ('TERRACED', 'Terraced house'),
    ('TOWNHOUSE', 'Townhouse'), ('LAND', 'Land'),('OTHER', 'Other'),
    }
    OWNERSHIP = (
    ('BUY', 'Buy'),
    ('RENT', 'Rent'),
    ('LEASE','Lease' )
    )
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )
    property_type = models.CharField(max_length = 20, choices = PROPERTY_TYPE_CHOICES , \
                    blank = False)
    max_price = models.PositiveIntegerField(blank = False)
    min_price = models.PositiveIntegerField(blank = False)
    max_beds = models.PositiveIntegerField(blank = False)
    min_beds = models.PositiveIntegerField(blank = False)
    property_size = models.PositiveIntegerField(blank = False)
    location = models.CharField(max_length = 50, blank = False)
    general_features = MultiSelectField(choices = GENERAL_FEATURES , \
                        blank = True)
    parking_choices = MultiSelectField(choices = PARKING_CHOICES , \
                        blank = True)
    additional_details = models.TextField()
    number_of_units = models.PositiveIntegerField(default = 1)
    ownership = models.CharField(max_length = 20 ,choices = OWNERSHIP, blank = False)
    timeline = models.DateField(auto_now=False, auto_now_add=False, blank = False)
    name = models.CharField(max_length = 25, blank = False)
    phone = models.PositiveIntegerField(blank = False)
    email = models.EmailField(blank = True)
    qualified = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Prop_lead_owner', on_delete=models.CASCADE)
    claimer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Prop_lead_claimer', blank=True)
    referrer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Prop_lead_referrer', blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    # def get_absolute_url(self):
    #     return reverse('markets:p_req_lead_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.property_type + ' ' + self.ownership + ' ' + str(self.min_price) \
            + ' ' + str(self.max_price) + ' ' + str(self.qualified)

    class Meta:
        verbose_name_plural = 'PropertyRequestLeads'


class ProffesionalRequestLead(models.Model):
    TYPE= (
    ('AGENT', 'Agent'), ('PROPERTYMANAGER', 'Property Manager'),
    ('INTERIORDESIGNER', 'Interior Designer'), ('ARCHITECT','Architect'),
    ('LANDSCAPEARCHITECT','Landscape architect'), ('HOMEMOVER','Home mover'),
    ('PLUMBING','Plumbing'), ('PHOTOGRAPHER','Photographer'),
    )

    type_of_proffesional = models.CharField(max_length = 20, choices = TYPE , blank = False)
    location = models.CharField(max_length = 50, blank = False)
    service_details = models.TextField()
    timeline = models.DateField(auto_now=False, auto_now_add=False, blank = False)
    name = models.CharField(max_length = 25, blank = False)
    phone = models.PositiveIntegerField(blank = False)
    email = models.EmailField(blank = True)
    qualified = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Prof_lead_owner', on_delete=models.CASCADE)
    claimer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Prof_lead_claimer', blank=True)
    referrer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Prof_lead_referrer', blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    # def get_absolute_url(self):
    #     return reverse('markets:prof_req_lead_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.type_of_proffesional + ' ' + self.location  + ' ' + str(self.timeline) + ' ' + str(self.qualified)

    class Meta:
        verbose_name_plural = 'ProffesionalRequestLeads'


class OtherServiceLead(models.Model):
    location = models.CharField(max_length = 50, blank = False)
    service_details = models.TextField()
    timeline = models.DateField(auto_now=False, auto_now_add=False, blank = False)
    name = models.CharField(max_length = 25, blank = False)
    phone = models.PositiveIntegerField(blank = False)
    email = models.EmailField(blank = True)
    qualified = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Other_request_owner', on_delete=models.CASCADE)
    claimer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Other_request_claimer', blank=True)
    referrer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Other_lead_referrer', blank=True)
    created_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    # def get_absolute_url(self):
    #     return reverse('markets:oth_req_lead_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.service_details + ' ' + self.location  + ' ' + str(self.timeline) + ' ' + str(self.qualified)

    class Meta:
        verbose_name_plural = 'OtherServiceLeads'

# Agent - Agent leads
class AgentLeadRequest(models.Model):
        PROPERTY_TYPE_CHOICES = {
        ('APARTMENT', 'Apartment'), ('BUNGALOW', 'Bungalow'),
        ('CONDOMINIUM', 'Condominium'), ('DORMITORY', 'Dormitory'),
        ('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'),
        ('SINGLEFAMILY', 'Single family'), ('TERRACED', 'Terraced house'),
        ('TOWNHOUSE', 'Townhouse'), ('LAND', 'Land'),('OTHER', 'Other'),
        }
        OWNERSHIP = (
        ('BUYER', 'Buyer'),
        ('RENTER', 'Renter'),
        ('LESSEE','Lessee' )
        )
        GENERAL_FEATURES = (
            ('FURNISHED', 'Furnished'),
            ('SERVICED', 'Serviced')
        )
        PARKING_CHOICES = (
        			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
        			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
        			('ONST', 'On-street'), ('NON', 'None'),
        )
        NEGOTIABLE_CHOICES = (
    			('YES', 'Yes'),
                ('NO', 'No')
        )
        property_type = models.CharField(max_length = 20, choices = PROPERTY_TYPE_CHOICES , \
                        blank = False)
        price = models.PositiveIntegerField(blank = False)
        price_negotiable = models.CharField(max_length = 3, choices = NEGOTIABLE_CHOICES , \
                        blank = False)
        beds = models.PositiveIntegerField(blank = False)
        property_size = models.PositiveIntegerField(blank = False)
        location_name = models.CharField(max_length = 50, blank = False)
        location = models.PointField(srid=4326, default=None)
        general_features = MultiSelectField(choices = GENERAL_FEATURES, blank = True)
        parking_choices = MultiSelectField(choices = PARKING_CHOICES, blank = True)
        additional_details = models.TextField()
        market_value = models.PositiveIntegerField(default=None, blank=False)
        number_of_units = models.PositiveIntegerField(default = 1)
        ownership = models.CharField(max_length = 20 ,choices = OWNERSHIP, blank = False)
        timeline = models.DateField(auto_now=False, auto_now_add=False, blank = False)
        name = models.CharField(max_length = 25, blank = False)
        phone = models.PositiveIntegerField(blank = False)
        email = models.EmailField(blank = True)
        qualified = models.BooleanField(default = False)
        active = models.BooleanField(default=True)
        owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Ag_lead_owner', on_delete=models.CASCADE)
        claimer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Ag_lead_claimer', blank=True)
        referrer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Ag_lead_referrer', blank=True)
        created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
        updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

        @property
        def longitude(self):
        	return self.location.x

        @property
        def latitude(self):
        	return self.location.y

        # def get_absolute_url(self):
        #     return reverse('markets:ag_req_lead_detail', kwargs={'pk':self.pk})

        def __str__(self):
            return self.property_type + ' ' + self.ownership + ' ' + str(self.qualified)

        class Meta:
            verbose_name_plural = 'AgentLeadRequests'

class AgentPropertyRequest(models.Model):
        PROPERTY_TYPE_CHOICES = {
            ('APARTMENT', 'Apartment'), ('BUNGALOW', 'Bungalow'),
            ('CONDOMINIUM', 'Condominium'), ('DORMITORY', 'Dormitory'),
            ('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'),
            ('SINGLEFAMILY', 'Single family'), ('TERRACED', 'Terraced house'),
            ('TOWNHOUSE', 'Townhouse'), ('LAND', 'Land'),('OTHER', 'Other'),
        }
        OWNERSHIP = (
            ('BUY', 'Buy'),
            ('RENT', 'Rent'),
            ('LEASE','Lease' )
        )
        GENERAL_FEATURES = (
            ('FURNISHED', 'Furnished'),
            ('SERVICED', 'Serviced')
        )
        PARKING_CHOICES = (
        			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
        			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
        			('ONST', 'On-street'), ('NON', 'None'),
        )
        property_type = models.CharField(max_length = 20, choices = PROPERTY_TYPE_CHOICES , \
                        blank = False)
        max_price = models.PositiveIntegerField(blank = False)
        min_price = models.PositiveIntegerField(blank = False)
        max_beds = models.PositiveIntegerField(blank = False)
        min_beds = models.PositiveIntegerField(blank = False)
        property_size = models.PositiveIntegerField(blank = False)
        location_name = models.CharField(max_length = 50, blank = False)
        general_features = MultiSelectField(choices = GENERAL_FEATURES, blank = True)
        parking_choices = MultiSelectField(choices = PARKING_CHOICES, blank = True)
        additional_details = models.TextField()
        market_value = models.PositiveIntegerField(default=None, blank=False)
        number_of_units = models.PositiveIntegerField(default = 1)
        ownership = models.CharField(max_length = 20 ,choices = OWNERSHIP, blank = False)
        timeline = models.DateField(auto_now=False, auto_now_add=False, blank = False)
        name = models.CharField(max_length = 25, blank = False)
        phone = models.PositiveIntegerField(blank = False)
        email = models.EmailField(blank = True)
        qualified = models.BooleanField(default = False)
        active = models.BooleanField(default=True)
        owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='AgProp_Lead_owner', on_delete=models.CASCADE)
        claimer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='AgProp_lead_claimer', blank=True)
        referrer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='AgProp_lead_referrer', blank=True)
        created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
        updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)


        # def get_absolute_url(self):
        #     return reverse('markets:ag_prop_lead_detail', kwargs={'pk':self.pk})

        def __str__(self):
            return self.property_type + ' ' + self.ownership + ' ' + str(self.qualified)

        class Meta:
            verbose_name_plural = 'AgentPropertyRequests'
