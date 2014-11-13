from django.contrib import admin
from ds9s.models import ParFolder, Galaxy, GalaxyFeatures, GalaxyFields, EmissionLine, EmissionLineFields, Analysis

admin.site.register(ParFolder)
admin.site.register(Galaxy)
admin.site.register(GalaxyFeatures)
admin.site.register(GalaxyFields)
admin.site.register(EmissionLine)
admin.site.register(EmissionLineFields)
admin.site.register(Analysis)

