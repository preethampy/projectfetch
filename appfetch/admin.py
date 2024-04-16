from django.contrib import admin
from . import models

admin.site.register(models.OffChainData)
admin.site.register(models.OnChainData)
