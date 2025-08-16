from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Add sample images to properties'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding sample images to properties...'))
        
        # Path to the images directory
        image_dir = '/Users/arunbabu/Desktop/Code/DummyProject-VPS/real_estate/Images'
        
        # Available image files
        image_files = [
            '4b64c203-cc2e-4621-8f78-9e8e0965a66e.jpg',
            '05652eb8-ff6a-4a9f-9b07-128007270bda.jpg',
            'Gemini_Generated_Image_mjqm8ymjqm8ymjqm.png',
            'Gemini_Generated_Image_nltx7snltx7snltx.png'
        ]
        
        # Get all properties
        properties = Property.objects.all()
        
        for i, property_obj in enumerate(properties):
            # Check if property already has images
            if property_obj.images.exists():
                self.stdout.write(f'Property "{property_obj.title}" already has images, skipping...')
                continue
            
            # Select image file (cycle through available images)
            image_file = image_files[i % len(image_files)]
            image_path = os.path.join(image_dir, image_file)
            
            if os.path.exists(image_path):
                try:
                    # Copy image to media directory and create PropertyImage record
                    with open(image_path, 'rb') as f:
                        # Create PropertyImage instance
                        property_image = PropertyImage(
                            property=property_obj,
                            alt_text=f'{property_obj.title} - Main Image',
                            is_primary=True,
                            order=1
                        )
                        
                        # Save image to Cloudinary via Django
                        property_image.image.save(
                            f'property_{property_obj.id}_{image_file}',
                            File(f),
                            save=True
                        )
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Added image to property: {property_obj.title}')
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error adding image to {property_obj.title}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Image file not found: {image_path}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Finished adding property images!')
        )