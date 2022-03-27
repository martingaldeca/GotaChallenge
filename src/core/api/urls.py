from django.urls import path

from core.api import views as core_views

app_name = 'core'

urlpatterns = [
    path('register/', core_views.RegisterView.as_view(), name='register'),
    path('me/', core_views.MeDetailView.as_view(), name='me'),

    path('new_action/', core_views.CreateNewActionView.as_view(), name='create-action'),
    path('action/<uuid>/', core_views.RetrieveUpdateDestroyActionView.as_view(), name='action'),
    path('actions/', core_views.ActionListView.as_view(), name='list-actions'),

    path('new_ingredient/', core_views.CreateNewIngredientView.as_view(), name='create-ingredient'),
    path('ingredient/<uuid>/', core_views.RetrieveUpdateDestroyIngredientView.as_view(), name='ingredient'),
    path('ingredients/', core_views.IngredientListView.as_view(), name='list-ingredients'),
]
