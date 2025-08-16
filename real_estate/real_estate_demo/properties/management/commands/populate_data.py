from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import (
    PropertyType, Location, Agent, PropertyFeature, 
    Property, PropertyImage, Testimonial
)
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create Property Types
        property_types_data = [
            {'name': 'House', 'slug': 'house', 'description': 'Single family homes and houses', 'icon': 'fas fa-home'},
            {'name': 'Apartment', 'slug': 'apartment', 'description': 'Apartments and condominiums', 'icon': 'fas fa-building'},
            {'name': 'Villa', 'slug': 'villa', 'description': 'Luxury villas and estates', 'icon': 'fas fa-crown'},
            {'name': 'Commercial', 'slug': 'commercial', 'description': 'Commercial properties and offices', 'icon': 'fas fa-briefcase'},
            {'name': 'Townhouse', 'slug': 'townhouse', 'description': 'Modern townhouses', 'icon': 'fas fa-city'},
        ]
        
        for data in property_types_data:
            property_type, created = PropertyType.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created PropertyType: {property_type.name}')

        # Create Locations
        locations_data = [
            {'name': 'Dhaka', 'slug': 'dhaka', 'parent': None, 'latitude': Decimal('23.8103'), 'longitude': Decimal('90.4125')},
            {'name': 'Mirpur', 'slug': 'mirpur', 'parent_slug': 'dhaka', 'latitude': Decimal('23.8223'), 'longitude': Decimal('90.3654')},
            {'name': 'Gulshan', 'slug': 'gulshan', 'parent_slug': 'dhaka', 'latitude': Decimal('23.7925'), 'longitude': Decimal('90.4078')},
            {'name': 'Dhanmondi', 'slug': 'dhanmondi', 'parent_slug': 'dhaka', 'latitude': Decimal('23.7461'), 'longitude': Decimal('90.3742')},
            {'name': 'Uttara', 'slug': 'uttara', 'parent_slug': 'dhaka', 'latitude': Decimal('23.8759'), 'longitude': Decimal('90.3795')},
            {'name': 'Chittagong', 'slug': 'chittagong', 'parent': None, 'latitude': Decimal('22.3569'), 'longitude': Decimal('91.7832')},
            {'name': 'Sylhet', 'slug': 'sylhet', 'parent': None, 'latitude': Decimal('24.8949'), 'longitude': Decimal('91.8687')},
        ]
        
        location_objects = {}
        for data in locations_data:
            parent = None
            if 'parent_slug' in data:
                parent = location_objects.get(data['parent_slug'])
                data.pop('parent_slug')
            
            data['parent'] = parent
            location, created = Location.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            location_objects[data['slug']] = location
            if created:
                self.stdout.write(f'Created Location: {location.name}')

        # Create Property Features
        features_data = [
            {'name': 'Swimming Pool', 'icon': 'fas fa-swimming-pool'},
            {'name': 'Garage', 'icon': 'fas fa-car'},
            {'name': 'Garden', 'icon': 'fas fa-leaf'},
            {'name': 'Balcony', 'icon': 'fas fa-building'},
            {'name': 'Fireplace', 'icon': 'fas fa-fire'},
            {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
            {'name': 'Security System', 'icon': 'fas fa-shield-alt'},
            {'name': 'Elevator', 'icon': 'fas fa-arrows-alt-v'},
            {'name': 'Gym', 'icon': 'fas fa-dumbbell'},
            {'name': 'Rooftop Terrace', 'icon': 'fas fa-building'},
        ]
        
        for data in features_data:
            feature, created = PropertyFeature.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created Feature: {feature.name}')

        # Create Agents
        agents_data = [
            {
                'username': 'john_doe',
                'email': 'john@truster.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+1-555-0101',
                'bio': 'Experienced real estate agent with 8 years in luxury properties.',
                'experience_years': 8,
                'license_number': 'RE123456',
                'rating': Decimal('4.8'),
                'total_sales': 45,
            },
            {
                'username': 'sarah_miller',
                'email': 'sarah@truster.com',
                'first_name': 'Sarah',
                'last_name': 'Miller',
                'phone': '+1-555-0102',
                'bio': 'Specialist in residential properties and first-time home buyers.',
                'experience_years': 5,
                'license_number': 'RE123457',
                'rating': Decimal('4.9'),
                'total_sales': 32,
            },
            {
                'username': 'mike_johnson',
                'email': 'mike@truster.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'phone': '+1-555-0103',
                'bio': 'Commercial real estate expert with extensive market knowledge.',
                'experience_years': 12,
                'license_number': 'RE123458',
                'rating': Decimal('4.7'),
                'total_sales': 67,
            },
        ]
        
        agents = []
        for data in agents_data:
            user_data = {
                'username': data.pop('username'),
                'email': data.pop('email'),
                'first_name': data.pop('first_name'),
                'last_name': data.pop('last_name'),
            }
            
            user, user_created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            
            agent, created = Agent.objects.get_or_create(
                user=user,
                defaults=data
            )
            agents.append(agent)
            if created:
                self.stdout.write(f'Created Agent: {agent.get_full_name()}')

        # Create Properties
        properties_data = [
            {
                'title': 'Modern Villa in Gulshan',
                'slug': 'modern-villa-gulshan',
                'description': 'Beautiful modern villa with contemporary design, spacious rooms, and premium finishes. Perfect for families looking for luxury living in the heart of Gulshan.',
                'property_type_slug': 'villa',
                'location_slug': 'gulshan',
                'address': '123 Gulshan Avenue, Gulshan, Dhaka',
                'price': Decimal('750000'),
                'price_per_sqft': Decimal('425'),
                'bedrooms': 4,
                'bathrooms': Decimal('3.5'),
                'area_sqft': 1800,
                'lot_size': 2500,
                'year_built': 2020,
                'parking_spaces': 2,
                'is_featured': True,
                'latitude': Decimal('23.7925'),
                'longitude': Decimal('90.4078'),
            },
            {
                'title': 'Luxury Apartment in Dhanmondi',
                'slug': 'luxury-apartment-dhanmondi',
                'description': 'Stunning luxury apartment with panoramic city views. Features modern amenities, high-end finishes, and excellent location near shopping and dining.',
                'property_type_slug': 'apartment',
                'location_slug': 'dhanmondi',
                'address': '456 Dhanmondi Road, Dhanmondi, Dhaka',
                'price': Decimal('420000'),
                'price_per_sqft': Decimal('350'),
                'bedrooms': 3,
                'bathrooms': Decimal('2.0'),
                'area_sqft': 1200,
                'year_built': 2019,
                'parking_spaces': 1,
                'is_featured': True,
                'latitude': Decimal('23.7461'),
                'longitude': Decimal('90.3742'),
            },
            {
                'title': 'Family House in Mirpur',
                'slug': 'family-house-mirpur',
                'description': 'Spacious family house in a quiet neighborhood. Perfect for growing families with excellent schools nearby and easy transportation access.',
                'property_type_slug': 'house',
                'location_slug': 'mirpur',
                'address': '789 Mirpur Road, Mirpur, Dhaka',
                'price': Decimal('320000'),
                'price_per_sqft': Decimal('280'),
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'area_sqft': 1150,
                'lot_size': 1800,
                'year_built': 2018,
                'parking_spaces': 2,
                'is_featured': False,
                'latitude': Decimal('23.8223'),
                'longitude': Decimal('90.3654'),
            },
            {
                'title': 'Modern Townhouse in Uttara',
                'slug': 'modern-townhouse-uttara',
                'description': 'Contemporary townhouse with modern design and premium amenities. Great for young professionals and small families.',
                'property_type_slug': 'townhouse',
                'location_slug': 'uttara',
                'address': '321 Uttara Sector 7, Uttara, Dhaka',
                'price': Decimal('480000'),
                'price_per_sqft': Decimal('320'),
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'area_sqft': 1500,
                'lot_size': 2000,
                'year_built': 2021,
                'parking_spaces': 2,
                'is_featured': True,
                'latitude': Decimal('23.8759'),
                'longitude': Decimal('90.3795'),
            },
            {
                'title': 'Commercial Office Space',
                'slug': 'commercial-office-space',
                'description': 'Prime commercial office space in the business district. Ideal for startups and established businesses looking for a prestigious address.',
                'property_type_slug': 'commercial',
                'location_slug': 'gulshan',
                'address': '555 Gulshan Business Center, Gulshan, Dhaka',
                'price': Decimal('920000'),
                'price_per_sqft': Decimal('460'),
                'bedrooms': 0,
                'bathrooms': Decimal('4.0'),
                'area_sqft': 2000,
                'year_built': 2022,
                'parking_spaces': 5,
                'listing_type': 'rent',
                'is_featured': False,
                'latitude': Decimal('23.7925'),
                'longitude': Decimal('90.4078'),
            },
        ]
        
        for data in properties_data:
            property_type = PropertyType.objects.get(slug=data.pop('property_type_slug'))
            location = Location.objects.get(slug=data.pop('location_slug'))
            
            data['property_type'] = property_type
            data['location'] = location
            data['agent'] = random.choice(agents)
            
            property_obj, created = Property.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created Property: {property_obj.title}')
                
                # Add random features to properties
                features = list(PropertyFeature.objects.all())
                random_features = random.sample(features, random.randint(2, 5))
                property_obj.features.set(random_features)

        # Create Testimonials
        testimonials_data = [
            {
                'name': 'Emily Johnson',
                'role': 'Happy Homeowner',
                'content': 'TRUSTER helped me find my dream home! The process was smooth and the agent was incredibly helpful throughout.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'name': 'David Brown',
                'role': 'Property Investor',
                'content': 'Excellent service and great properties. I\'ve purchased multiple properties through TRUSTER and always had a positive experience.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'name': 'Lisa Davis',
                'role': 'First-time Buyer',
                'content': 'As a first-time buyer, I was nervous about the process. The TRUSTER team made everything easy and stress-free.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'name': 'Robert Wilson',
                'role': 'Business Owner',
                'content': 'Found the perfect office space for my business. Professional service and great market knowledge.',
                'rating': 4,
                'is_featured': False,
            },
        ]
        
        for data in testimonials_data:
            data['agent'] = random.choice(agents)
            if random.choice([True, False]):
                data['property'] = random.choice(Property.objects.all())
            
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created Testimonial: {testimonial.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write(
            self.style.WARNING('Note: Property images need to be added manually through the admin panel.')
        )