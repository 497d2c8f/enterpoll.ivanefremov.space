from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import render

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('enterpoll.urls')),
	path('api/', include('enterpoll.api.api_urls')),
]


handler404 = lambda request, exception: render(request, template_name='enterpoll/404.html', status=404)


admin.site.site_header = 'Enterpoll'
admin.site.index_title = 'Enterpoll'
admin.site.site_title = 'Admin'
admin.site.site_url = reverse('main_page')
