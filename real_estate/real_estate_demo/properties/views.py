from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.db.models import Q
from .models import Property, PropertyType, Location, Testimonial


class HomeView(TemplateView):
    template_name = 'properties/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_properties'] = Property.objects.filter(is_featured=True, is_published=True)[:6]
        context['property_types'] = PropertyType.objects.all()
        context['locations'] = Location.objects.filter(parent=None)[:6]
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        return context


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True)
        
        # Filter by property type
        property_type = self.request.GET.get('type')
        if property_type:
            queryset = queryset.filter(property_type__slug=property_type)
        
        # Filter by location
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__slug=location)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_types'] = PropertyType.objects.all()
        context['locations'] = Location.objects.filter(parent=None)
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_obj = self.get_object()
        context['similar_properties'] = Property.objects.filter(
            property_type=property_obj.property_type,
            location=property_obj.location,
            is_published=True
        ).exclude(id=property_obj.id)[:4]
        return context


class PropertySearchView(TemplateView):
    template_name = 'properties/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            properties = Property.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query) |
                Q(location__name__icontains=query),
                is_published=True
            )
        else:
            properties = Property.objects.filter(is_published=True)
        
        context['properties'] = properties
        context['query'] = query
        return context


def contact_agent(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            message = request.POST.get('message')
            inquiry_type = request.POST.get('inquiry_type', 'info')
            property_id = request.POST.get('property_id')
            
            # Validate required fields
            if not all([name, email, message]):
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Please fill in all required fields.'
                })
            
            # Get property if specified
            property_obj = None
            if property_id:
                try:
                    property_obj = Property.objects.get(id=property_id)
                except Property.DoesNotExist:
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Property not found.'
                    })
            
            # Create inquiry
            from .models import Inquiry
            inquiry = Inquiry.objects.create(
                property=property_obj,
                inquiry_type=inquiry_type,
                name=name,
                email=email,
                phone=phone,
                message=message,
                status='new'
            )
            
            # Send email notification to agent
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                if property_obj and property_obj.agent:
                    agent_email = property_obj.agent.user.email
                    subject = f'New Inquiry for {property_obj.title}'
                    message_content = f"""
New property inquiry received:

Property: {property_obj.title}
Inquiry Type: {inquiry_type.replace('_', ' ').title()}

Contact Information:
Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}

Please respond to this inquiry promptly.

Best regards,
TRUSTER Team
                    """
                    
                    send_mail(
                        subject,
                        message_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [agent_email],
                        fail_silently=True,
                    )
                    
                    # Send confirmation email to customer
                    customer_subject = 'Thank you for your inquiry - TRUSTER'
                    customer_message = f"""
Dear {name},

Thank you for your inquiry about {property_obj.title if property_obj else 'our properties'}. 

We have received your message and will contact you soon. Our agent will reach out to you within 24 hours.

Your inquiry details:
- Inquiry Type: {inquiry_type.replace('_', ' ').title()}
- Property: {property_obj.title if property_obj else 'General Inquiry'}

If you have any urgent questions, please feel free to call us.

Best regards,
TRUSTER Team
                    """
                    
                    send_mail(
                        customer_subject,
                        customer_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,
                    )
                    
            except Exception as e:
                # Email sending failed, but inquiry was still created
                pass
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Your message has been sent! We will contact you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def add_to_favorites(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to add favorites.'
            })
        
        try:
            import json
            data = json.loads(request.body)
            property_id = data.get('property_id')
            
            if not property_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Property ID is required.'
                })
            
            try:
                property_obj = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Property not found.'
                })
            
            from .models import Favorite
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                property=property_obj
            )
            
            if created:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Property added to favorites!',
                    'action': 'added'
                })
            else:
                return JsonResponse({
                    'status': 'info',
                    'message': 'Property already in favorites.',
                    'action': 'exists'
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def remove_from_favorites(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to manage favorites.'
            })
        
        try:
            import json
            data = json.loads(request.body)
            property_id = data.get('property_id')
            
            if not property_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Property ID is required.'
                })
            
            from .models import Favorite
            deleted_count, _ = Favorite.objects.filter(
                user=request.user,
                property_id=property_id
            ).delete()
            
            if deleted_count > 0:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Property removed from favorites!',
                    'action': 'removed'
                })
            else:
                return JsonResponse({
                    'status': 'info',
                    'message': 'Property was not in favorites.',
                    'action': 'not_found'
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def contact_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            inquiry_type = request.POST.get('inquiry_type', 'general')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Please fill in all required fields.'
                })
            
            # Create contact inquiry
            from .models import Contact
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                inquiry_type=inquiry_type,
                subject=subject,
                message=message,
                status='new'
            )
            
            # Send email notification to admin
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                admin_subject = f'New Contact Inquiry - {subject}'
                admin_message = f"""
New contact inquiry received:

Contact Information:
Name: {name}
Email: {email}
Phone: {phone}
Inquiry Type: {inquiry_type.replace('_', ' ').title()}

Subject: {subject}

Message:
{message}

Please respond to this inquiry promptly.

Best regards,
TRUSTER System
                """
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Send to admin
                    fail_silently=True,
                )
                
                # Send confirmation email to customer
                customer_subject = 'Thank you for contacting us - TRUSTER'
                customer_message = f"""
Dear {name},

Thank you for contacting TRUSTER. We have received your inquiry and will get back to you soon.

Your inquiry details:
- Subject: {subject}
- Inquiry Type: {inquiry_type.replace('_', ' ').title()}

We aim to respond to all inquiries within 24 hours.

If you have any urgent questions, please feel free to call us.

Best regards,
TRUSTER Team
                """
                
                send_mail(
                    customer_subject,
                    customer_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
                
            except Exception as e:
                # Email sending failed, but inquiry was still created
                pass
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Thank you for your message! We will contact you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
