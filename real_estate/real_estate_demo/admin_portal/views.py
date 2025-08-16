from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from properties.models import Property, Inquiry


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_portal/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_properties'] = Property.objects.count()
        context['featured_properties'] = Property.objects.filter(is_featured=True).count()
        context['recent_inquiries'] = Inquiry.objects.filter(status='new').count()
        return context


class AdminPropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'admin_portal/property_list.html'
    context_object_name = 'properties'
    paginate_by = 20


class AdminPropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'admin_portal/property_form.html'
    fields = '__all__'


class AdminPropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    template_name = 'admin_portal/property_form.html'
    fields = '__all__'


class AdminInquiryListView(LoginRequiredMixin, ListView):
    model = Inquiry
    template_name = 'admin_portal/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 20


class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_portal/analytics.html'
