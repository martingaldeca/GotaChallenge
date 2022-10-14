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

    path('new_device/', core_views.CreateNewDeviceView.as_view(), name='create-device'),
    path('device/<uuid>/', core_views.RetrieveUpdateDestroyDeviceView.as_view(), name='device'),
    path('devices/', core_views.DeviceListView.as_view(), name='list-devices'),

    path('new_recipy/', core_views.CreateNewRecipyView.as_view(), name='create-recipy'),
    path('recipy/<uuid>/', core_views.RetrieveUpdateDestroyRecipyView.as_view(), name='recipy'),
    path('recipies/', core_views.RecipyListView.as_view(), name='list-recipies'),

    path('recipy_step/<uuid>/', core_views.RetrieveUpdateDestroyRecipyStepView.as_view(), name='recipy-step'),
]
