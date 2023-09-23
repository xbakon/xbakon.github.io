from django.contrib import admin
from django.urls import path
from hotel.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name="home"),
    path('login/', login_page, name="login"),
    path('new-employee/', new_employee, name="new_employee"),
    path('logout/', logout_user, name="logout"),
    path('forgot-password/', forgot_password, name="forgot_password"),
    path('generate-otp/', generate_otp, name="generate_otp"),
    path('change-password/', change_password, name="change_password"),
    path('rooms/', rooms, name="rooms"),
    path('hotel-room/<roomId>', hotel_room, name="hotel_room"),
    path('reservation/', reservation, name="reservation"),
    path('get-id/', get_id, name="get_id"),
    path('lookup-email/', lookup_email, name="lookup_email"),
    path('make-reservation/', make_resrvation, name="make_resrvation"),
    path('search/', search, name="search"),
    path('edit-reservation/', edit_reservation, name="edit_reservation"),
    path('edit/', edit, name="edit"),
    path('display-reservation/<reservation_number>', display_reservation, name="display_reservation"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

