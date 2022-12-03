from django.contrib import admin
from .models import Cliente, FacturaEnc, FacturaDet

# Register your models here.
admin.site.register(Cliente)
admin.site.register(FacturaEnc)
admin.site.register(FacturaDet)