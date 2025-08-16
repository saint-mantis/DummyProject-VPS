#!/usr/bin/env python3
"""
Cloudinary Image Upload Script for TRUSTER Real Estate
This script uploads property images to Cloudinary and updates the database
"""

import os
import sys
import django
from pathlib import Path

# Add the parent directory to sys.path to import credentials
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from credentials import CLOUD_NAME, API_KEY, API_SECRET

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_demo.settings')
django.setup()

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
from properties.models import Property, PropertyImage

# Configure cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

def upload_images_to_cloudinary():
    """Upload static property images to Cloudinary and create PropertyImage records"""
    
    # Define the images and their corresponding properties
    property_images = [
        {
            'property_title': 'Modern Townhouse in Uttara',
            'image_path': 'static/images/properties/4b64c203-cc2e-4621-8f78-9e8e0965a66e.jpg',
            'public_id': 'truster/properties/modern_townhouse_uttara',
            'alt_text': 'Modern Townhouse in Uttara - Main Image'
        },
        {
            'property_title': 'Luxury Apartment in Dhanmondi',
            'image_path': 'static/images/properties/05652eb8-ff6a-4a9f-9b07-128007270bda.jpg',
            'public_id': 'truster/properties/luxury_apartment_dhanmondi',
            'alt_text': 'Luxury Apartment in Dhanmondi - Main Image'
        },
        {
            'property_title': 'Modern Villa in Gulshan',
            'image_path': 'static/images/properties/Gemini_Generated_Image_mjqm8ymjqm8ymjqm.png',
            'public_id': 'truster/properties/modern_villa_gulshan',
            'alt_text': 'Modern Villa in Gulshan - Main Image'
        }
    ]
    
    print("🏠 TRUSTER Real Estate - Cloudinary Image Upload")
    print("=" * 50)
    
    # Clear existing PropertyImage records
    print("🧹 Cleaning up existing property images...")
    PropertyImage.objects.all().delete()
    print("✅ Cleanup complete")
    
    successful_uploads = 0
    failed_uploads = 0
    
    for img_data in property_images:
        try:
            print(f"\n📤 Uploading: {img_data['property_title']}")
            print(f"   File: {img_data['image_path']}")
            
            # Check if file exists
            if not os.path.exists(img_data['image_path']):
                print(f"❌ File not found: {img_data['image_path']}")
                failed_uploads += 1
                continue
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                img_data['image_path'],
                public_id=img_data['public_id'],
                folder="truster/properties",
                resource_type="image",
                overwrite=True,
                transformation=[
                    {'width': 800, 'height': 600, 'crop': 'fill', 'quality': 'auto'},
                    {'fetch_format': 'auto'}
                ]
            )
            
            print(f"   ✅ Cloudinary upload successful")
            print(f"   🔗 URL: {upload_result['secure_url']}")
            print(f"   📏 Size: {upload_result['width']}x{upload_result['height']}")
            print(f"   📦 Format: {upload_result['format']}")
            
            # Find the property in database
            try:
                property_obj = Property.objects.get(title=img_data['property_title'])
                print(f"   🏡 Found property: {property_obj.title}")
                
                # Create PropertyImage record
                property_image = PropertyImage.objects.create(
                    property=property_obj,
                    image=upload_result['public_id'],  # Store Cloudinary public_id
                    alt_text=img_data['alt_text'],
                    is_primary=True,
                    order=1
                )
                
                print(f"   ✅ Database record created: {property_image}")
                successful_uploads += 1
                
            except Property.DoesNotExist:
                print(f"   ❌ Property not found in database: {img_data['property_title']}")
                failed_uploads += 1
                
        except Exception as e:
            print(f"   ❌ Upload failed: {str(e)}")
            failed_uploads += 1
    
    print("\n" + "=" * 50)
    print("📊 UPLOAD SUMMARY")
    print("=" * 50)
    print(f"✅ Successful uploads: {successful_uploads}")
    print(f"❌ Failed uploads: {failed_uploads}")
    print(f"📱 Total properties with images: {Property.objects.filter(images__isnull=False).distinct().count()}")
    
    if successful_uploads > 0:
        print("\n🎉 Success! Your property images are now hosted on Cloudinary")
        print("🌐 Images will be automatically optimized and delivered via CDN")
    
    return successful_uploads, failed_uploads

def test_cloudinary_connection():
    """Test Cloudinary connection and configuration"""
    print("🔧 Testing Cloudinary connection...")
    try:
        # Try to get account details
        result = cloudinary.api.usage()
        print(f"✅ Connected to Cloudinary account: {CLOUD_NAME}")
        print(f"📊 Storage used: {result.get('credits_usage', {}).get('total', 0)} credits")
        return True
    except Exception as e:
        print(f"❌ Cloudinary connection failed: {str(e)}")
        return False

def list_uploaded_images():
    """List all uploaded images from database"""
    print("\n📋 Current Property Images in Database:")
    print("-" * 40)
    
    for prop in Property.objects.filter(images__isnull=False).distinct():
        primary_img = prop.get_primary_image()
        if primary_img:
            # Generate Cloudinary URL
            img_url, _ = cloudinary_url(primary_img.url, 
                                      width=300, height=200, 
                                      crop="fill", quality="auto")
            print(f"🏠 {prop.title}")
            print(f"   📷 Image: {primary_img}")
            print(f"   🔗 URL: {img_url}")
            print()

if __name__ == "__main__":
    print("🚀 Starting Cloudinary upload process...")
    
    # Test connection first
    if not test_cloudinary_connection():
        print("❌ Aborting upload due to connection issues")
        sys.exit(1)
    
    # Upload images
    success_count, fail_count = upload_images_to_cloudinary()
    
    # List uploaded images
    if success_count > 0:
        list_uploaded_images()
    
    print("\n🏁 Upload process completed!")