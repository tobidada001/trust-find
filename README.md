# TrustFind - Lost and Found Platform

TrustFind is a Django-based web application for managing lost and found items, designed for the University of Ibadan community. Users can report lost or found items, search for items, manage their own listings, and communicate securely with other users.


## Features

- **User Authentication:** Register, login, logout, and manage user profiles with profile photos and contact information.
- **Item Management:** Post, edit, delete, and view lost or found items with images and detailed metadata.
- **Advanced Search:** Filter items by keywords, status, category, location, date range, and sort order.
- **Messaging System:** Send and receive messages about items, with an inbox and threaded conversations.
- **Admin Interface:** Manage users, items, categories, images, and messages via Django admin.
- **Responsive UI:** Modern, mobile-friendly interface using Tailwind CSS.


## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- [Pillow](https://pypi.org/project/Pillow/) for image handling

### Setup Steps

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd LostAndFound
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv env
   env\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.


## Usage

- **Register** for an account or **login** if you already have one.
- **Post** a lost or found item with details and images.
- **Search** for items using keywords and filters.
- **View** item details and contact the poster via message or WhatsApp.
- **Manage** your items from the "My Items" page (edit, delete, mark as resolved/active).
- **Check your inbox** for messages and reply to conversations.


## Admin Panel

- Visit `/admin/` and login with your superuser credentials.
- Manage users, items, categories, images, and messages.


## Customization

- **Settings:** See `LostAndFound/settings.py` for configuration (media, static, authentication, etc).
- **User Model:** Custom user model in `authapp/models.py`.
- **Item Model:** See `core/models.py` for item, category, image, and message models.
- **Forms:** Custom forms in `authapp/forms.py` and `core/forms.py`.
- **Views:** Main logic in `authapp/views.py` and `core/views.py`.
- **Templates:** All HTML templates in the `templates/` directory.



## Media & Static Files

- **Media files** (user uploads) are stored in the `media/` directory.
- **Static files** (images, CSS, JS) are in the `static/` directory.
- Update `MEDIA_URL`, `MEDIA_ROOT`, `STATIC_URL`, and `STATICFILES_DIRS` in `LostAndFound/settings.py` as needed.


## Dependencies

- Django==4.2.14
- mysqlclient==2.1.1 (optional, default DB is SQLite)
- Pillow==9.5.0

See `requirements.txt` for the full list.


## License

This project is for educational purposes at the University of Ibadan. Please contact the maintainer for reuse or contributions.

## Credits

- Developed by @tobidada001
- UI powered by [Tailwind CSS](https://tailwindcss.com/)


## Contact

For support or questions, please open an issue or contact the project maintainer.