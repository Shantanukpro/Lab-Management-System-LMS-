from django.urls import path
from .views import LabListView, LabCreateView, LabUpdateView, LabDeleteView, LabDetailView

urlpatterns = [
    path('', LabListView.as_view(), name='lab-list'),
    path('add/', LabCreateView.as_view(), name='lab-add'),
    path('<int:pk>/', LabDetailView.as_view(), name='lab-detail'),  # NEW
    path('<int:pk>/edit/', LabUpdateView.as_view(), name='lab-edit'),
    path('<int:pk>/delete/', LabDeleteView.as_view(), name='lab-delete'),
]
