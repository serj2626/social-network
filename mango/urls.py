from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import handler403, handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),

    path('', include('core.urls')),
    path('feedback/', include('feedback.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),

]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = handler403
handler404 = handler404
handler500 = handler500
