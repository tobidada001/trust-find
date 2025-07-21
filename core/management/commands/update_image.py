import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from core.models import Item  # Adjust this if Item is in another app

class Command(BaseCommand):
    help = 'Assign images to items that have no image, based on category name or title'

    def handle(self, *args, **kwargs):
        # Define keyword → list of image filenames
        image_map = {
            'wristwatch': ['wristwatch.jpeg'],
            'wristband': ['wristband.jpeg'],
            'shirt': ['red-long-shirt.jpeg', 'long-shirt.jpeg'],
            'usb': ['usb.jpeg'],
            'jewel': ['yellow-jewel1.jpeg', 'yellow-jewel2.jpeg'],
            'calculator': ['calculator1.webp', 'calculator2.jpg', 'calculator3.jpg'],
            'wallet': ['wallet1.jpg', 'wallet2.jpg'],
            'jacket': ['jacket.webp'],
        }

        default_image_filename = 'defaultimage.png'
        image_dir = os.path.join(settings.MEDIA_ROOT, 'items')

        items = Item.objects.filter()  # Only items with no image

        if not items.exists():
            self.stdout.write(self.style.WARNING("No items without images found."))
            return

        for item in items:
            title = item.title.lower()
            category_name = item.category.name.lower()
            matched = False

            # 1. Try matching by category name
            for keyword, image_list in image_map.items():
                if keyword in category_name:
                    selected_image = random.choice(image_list)
                    image_path = os.path.join(image_dir, selected_image)

                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            item.image.save(f"{item.pk}.jpg", File(img_file), save=True)
                            self.stdout.write(self.style.SUCCESS(f"[CATEGORY] {selected_image} → {item.title}"))
                            matched = True
                            break

            # 2. Try matching by title if no category match
            if not matched:
                for keyword, image_list in image_map.items():
                    if keyword in title:
                        selected_image = random.choice(image_list)
                        image_path = os.path.join(image_dir, selected_image)

                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img_file:
                                item.image.save(f"{item.pk}.jpg", File(img_file), save=True)
                                self.stdout.write(self.style.SUCCESS(f"[TITLE] {selected_image} → {item.title}"))
                                matched = True
                                break

   