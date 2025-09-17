from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Lab
from .forms import LabForm
from django.urls import reverse_lazy

# -------------------------
# List Labs (Read)
# -------------------------
class LabListView(ListView):
    model = Lab
    template_name = 'labs/lab_list.html'
    context_object_name = 'labs'

# -------------------------
# Create Lab
# -------------------------
class LabCreateView(CreateView):
    model = Lab
    form_class = LabForm
    template_name = 'labs/lab_form.html'
    success_url = reverse_lazy('lab-list')

# -------------------------
# Update Lab
# -------------------------
class LabUpdateView(UpdateView):
    model = Lab
    form_class = LabForm
    template_name = 'labs/lab_form.html'
    success_url = reverse_lazy('lab-list')

# -------------------------
# Delete Lab
# -------------------------
class LabDeleteView(DeleteView):
    model = Lab
    template_name = 'labs/lab_confirm_delete.html'
    success_url = reverse_lazy('lab-list')

# -------------------------
# Lab Detail View
# -------------------------

class LabDetailView(DetailView):
    model = Lab
    template_name = "labs/lab_detail.html"
    context_object_name = "lab"
