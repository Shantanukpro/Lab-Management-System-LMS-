from django.urls import path, include
from .views import (
    LabListView, LabDetailView, LabCreateView, LabUpdateView, LabDeleteView,
    PCCreateView, PCUpdateView, PCDeleteView
)


urlpatterns = [
    path('', LabListView.as_view(), name='lab-list'),
    path('add/', LabCreateView.as_view(), name='lab-add'),
    path('<int:pk>/', LabDetailView.as_view(), name='lab-detail'),
    path('<int:pk>/edit/', LabUpdateView.as_view(), name='lab-edit'),
    path('<int:pk>/delete/', LabDeleteView.as_view(), name='lab-delete'),

    # PC CRUD
    path('<int:lab_id>/pcs/add/', PCCreateView.as_view(), name='pc-add'),
    path('pcs/<int:pk>/edit/', PCUpdateView.as_view(), name='pc-edit'),
    path('pcs/<int:pk>/delete/', PCDeleteView.as_view(), name='pc-delete'),

    path('api/', include('labs.api.urls')),
    # Optional: if you have API endpoints
]

