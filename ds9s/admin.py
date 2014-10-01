from django.contrib import admin
from ds9s.models import Users, Roles



class UsersAdmin(admin.ModelAdmin):
	list_display  	= ('EMAIL_USER','FIRSTNAME_USER','LASTNAME_USER','REGISTRATIONDATE_USER')
	list_filter		= ('role',)
	#date_hierarchy	= 'REGISTRATIONDATE_USER'
	ordering		= ('REGISTRATIONDATE_USER',)
	search_fields 	= ('EMAIL_USER','FIRSTNAME_USER','LASTNAME_USER')


	fieldsets = (
	   ('Log informations', {
	        'fields': ('EMAIL_USER', 'PASSWORD_USER')
	    }),
	    ('User informations', {
	       'fields': ('FIRSTNAME_USER','LASTNAME_USER',)
	    }),
	)

admin.site.register(Users, UsersAdmin)
admin.site.register(Roles)