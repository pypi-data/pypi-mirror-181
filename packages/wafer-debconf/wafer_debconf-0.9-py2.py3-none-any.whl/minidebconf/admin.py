from django.contrib import admin

from minidebconf.models import Diet, Registration, ShirtSize


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'involvement', 'gender', 'country', 'diet', 'shirt_size')
    list_filter = ('involvement', 'gender', 'days', 'diet', 'shirt_size')

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Diet)
admin.site.register(ShirtSize)
