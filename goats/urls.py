from django.urls import path
from .views import list_goats, create_goat, update_goat, delete_goat, update_goat_is_inside

urlpatterns = [
    path('', list_goats, name='list_goats'),
    path('new', create_goat, name='create_goat'),
    path('update/<int:id>/', update_goat, name='update_goat'),
    path('delete/<int:id>/', delete_goat, name='delete_goat'),
    path('updateinside/<int:id>/', update_goat_is_inside, name='update_goat_is_inside'),
]
