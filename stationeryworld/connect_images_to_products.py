#!/usr/bin/env python
"""
Script to connect images to products in the Stationery World database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stationaryworld.settings')
django.setup()

from main.models import Product, ProductImage

def main():
    try:
        print("Setting up products with images...")
        
        # Verify media directory exists
        media_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'products')
        if not os.path.exists(media_path):
            print(f"Warning: Media directory not found at {media_path}")
        
        # List of image files in media/products/
        # Standardized naming convention: consistent naming without spaces
        image_files = [
            'image1.png',
            'image2.png',
            'image3.png',
            'image4.png',
            'image5.png',
            'image6.png',
            'image7.png',
            'image8.png',
            'image9.png',
            'image10.png',
            'image11.png'
        ]
        
        # Sample product data
        products_data = [
            {
                'name': 'Premium Notebook Set',
                'description': 'High-quality notebook set perfect for students and professionals. Contains multiple sizes and designs.',
                'price': 25000.00,
                'category': 'stationery',
                'image_file': 'image1.png'
            },
            {
                'name': 'Colorful Pens Collection',
                'description': 'Set of vibrant colored pens for all your writing and drawing needs. Smooth ink flow.',
                'price': 15000.00,
                'category': 'stationery',
                'image_file': 'image2.png'
            },
            {
                'name': 'Office Stationery Kit',
                'description': 'Complete office stationery kit including staples, clips, folders, and more essentials.',
                'price': 45000.00,
                'category': 'stationery',
                'image_file': 'image3.png'
            },
            {
                'name': 'Designer Paper Set',
                'description': 'Beautiful designer paper set for crafts, printing, and creative projects.',
                'price': 18000.00,
                'category': 'design',
                'image_file': 'image41.png'
            },
            {
                'name': 'Professional Calculator',
                'description': 'Advanced calculator with multiple functions perfect for business and academic use.',
                'price': 35000.00,
                'category': 'electronics',
                'image_file': 'image5.png'
            },
            {
                'name': 'Art Supplies Bundle',
                'description': 'Complete art supplies bundle including brushes, paints, canvas, and drawing tools.',
                'price': 55000.00,
                'category': 'design',
                'image_file': 'image6.png'
            },
            {
                'name': 'Business Cards Printing',
                'description': 'Professional business card printing service with various designs and paper options.',
                'price': 25000.00,
                'category': 'printing',
                'image_file': 'image71.png'
            },
            {
                'name': 'Sticky Notes Collection',
                'description': 'Multi-colored sticky notes perfect for organizing and reminders. Strong adhesive.',
                'price': 8000.00,
                'category': 'stationery',
                'image_file': 'image8.png'
            },
            {
                'name': 'File Organization System',
                'description': 'Complete file organization system with folders, dividers, and labels.',
                'price': 22000.00,
                'category': 'stationery',
                'image_file': 'image9.png'
            },
            {
                'name': 'Custom Printing Services',
                'description': 'Professional custom printing services for flyers, brochures, and marketing materials.',
                'price': 75000.00,
                'category': 'printing',
                'image_file': 'image10.png'
            },
            {
                'name': 'Desktop Organizer',
                'description': 'Elegant desktop organizer to keep your workspace neat and efficient.',
                'price': 28000.00,
                'category': 'stationery',
                'image_file': 'image110.png'
            },
            {
                'name': 'USB Flash Drive',
                'description': 'High-speed USB flash drives for data storage and transfer. Various capacities available.',
                'price': 15000.00,
                'category': 'electronics',
                'image_file': 'image16.png'
            }
        ]
        
        # Clear existing products and images
        print("Clearing existing data...")
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        
        # Create products with images
        for i, product_data in enumerate(products_data):
            print(f"Creating product: {product_data['name']}")
            
            # Create the product
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=product_data['category'],
                image=f"products/{product_data['image_file']}"
            )
            
            # Add the main image as a ProductImage as well
            ProductImage.objects.create(
                product=product,
                image=f"products/{product_data['image_file']}"
            )
            
            # Add additional images (rotate through available images)
            additional_images = image_files[(i+1) % len(image_files):(i+3) % len(image_files) + 1]
            for img_file in additional_images:
                ProductImage.objects.create(
                    product=product,
                    image=f"products/{img_file}"
                )
            
            print(f"  - Created with {product.images.count()} images")
        
        print(f"\nSetup complete!")
        print(f"Created {Product.objects.count()} products with images")
        
        # Display summary
        print("\nProduct Summary:")
        for product in Product.objects.all():
            print(f"- {product.name}: {product.images.count()} images")
        
        print("\nSetup completed successfully!")
        
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()