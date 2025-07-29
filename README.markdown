NerdsCorp Gallery 🖼️
NerdsCorp Gallery is a Flask-based web application for managing and displaying a photo gallery. Guests can view all images and their descriptions, while authenticated admins can upload images, delete individual images, add descriptions, and manage admin accounts. The application uses a SQLite database for admin authentication and image descriptions, and supports containerization with Docker.
Features

Guest Access: View all images and their descriptions in the gallery without logging in. Click images to view them full-screen. 🖼️
Admin Features:
Upload images (.png, .jpg, .jpeg, .gif) with a preview of selected files. 📤
Delete individual images from the gallery using trash icons. 🗑️
Add or edit descriptions for each image, displayed below the images. 📝
Add or remove admin users via a management interface. 👥


Authentication: Secure admin login with hashed passwords stored in a SQLite database. 🔒
Styling: Responsive, friendly design with a black background, light blue header and accents, Comic Neue font, emojis, and Tailwind CSS (via CDN) with Font Awesome icons. 😄
Docker Support: Run the app in a containerized environment with Gunicorn. 🐳

Project Structure
nerdscorp-gallery/
├── app.py
├── Dockerfile
├── requirements.txt
├── static/
│   ├── uploads/
│   └── css/ (optional, for local Tailwind CSS)
└── templates/
    └── index.html


app.py: Main Flask application with routes for gallery, login, admin actions, image deletion, description management, and admin management.
Dockerfile: Configures the Docker image for the app.
requirements.txt: Lists Python dependencies (Flask, Werkzeug, gunicorn).
static/uploads/: Stores uploaded images, scanned for gallery display.
static/css/: Optional directory for local Tailwind CSS (not included by default; uses CDN).
templates/index.html: HTML template for the web interface, styled with Tailwind CSS, Font Awesome, and Comic Neue, featuring a light blue header.
admins.db: SQLite database for admin credentials and image descriptions, created automatically on first run.

Prerequisites

Python 3.9+ (for non-Docker setup)
Docker (for containerized setup)
pip for installing Python dependencies
Write permissions for the static/uploads/ directory and project root (for admins.db)

Setup Instructions
Without Docker

Clone or Create the Project Directory:

Ensure the project structure matches the one above.
Create static/uploads/ if it doesn't exist:mkdir -p static/uploads
chmod -R 777 static/uploads




Install Dependencies:
pip install -r requirements.txt


Run the Application:
python app.py


Access the app at http://localhost:5000.



With Docker

Build the Docker Image:
docker build -t nerdscorp-gallery .


Run the Docker Container:
docker run -p 8000:8000 -v $(pwd)/static/uploads:/app/static/uploads -v $(pwd)/admins.db:/app/admins.db nerdscorp-gallery


The -v flags persist the uploads folder and admins.db on the host.
Access the app at http://localhost:8000.



Usage

Guest View:

Visit the root URL (/ or http://localhost:8000 for Docker) to view all images and their descriptions in the gallery. 🖼️
Click an image to view it full-screen in a modal; click the close button (❌) to exit.
No login is required to browse images and descriptions.


Admin Access:

Click "Admin Login" in the header to access the login page. 🔑
Use the default credentials (admin/gallery123) for initial login (created automatically on first run).
After logging in, admins can:
Upload Images: Drag and drop or browse files to select images, view previews, and click "Upload Images" to add them to the gallery. 📤
Delete Images: Click the trash icon (🗑️) on individual images to delete them.
Add Descriptions: Enter or edit descriptions in the text area below each image and click "Save" to store them. 📝
Manage Admins: Access the "Manage Admins" page to add new admins or delete existing ones (except the current user's account). 👥




Admin Management:

Navigate to "Manage Admins" from the header (when logged in).
Add new admins by entering a username and password. ➕
Delete existing admins (except your own account) from the list.



Notes

Default Admin Account: On first run, a default admin account (admin/gallery123) is created in admins.db. Use the "Manage Admins" page to add new admins or remove the default one.
Image Storage: Images are stored in static/uploads/. Ensure this directory has write permissions (chmod -R 777 static/uploads on Linux/macOS, or ensure writability on Windows).
Database: The admins.db file is created in the project root on first run and stores admin credentials and image descriptions with hashed passwords.
Styling: Uses Tailwind CSS (CDN), Font Awesome (CDN), Google Fonts (Comic Neue), and emojis for a fun, light blue-themed interface with a light blue header. To use a local Tailwind CSS file, download the compiled CSS, place it in static/css/tailwind.css, and update index.html to reference it: <link href="{{ url_for('static', filename='css/tailwind.css') }}" rel="stylesheet">.
Production Considerations:
Replace the secret key in app.py with a secure value.
Use HTTPS and consider a reverse proxy (e.g., Nginx).
For high traffic, replace SQLite with a more robust database like PostgreSQL.
Implement additional security measures (e.g., rate limiting, CSRF protection).



Troubleshooting

Permission Issues: Ensure static/uploads/ and the project root have write permissions for image uploads, deletions, and database creation.
Docker Volume Issues: Verify the -v paths in the docker run command match your host directory structure.
Login Failures: Check that admins.db is not corrupted and contains valid admin credentials. Delete it to reset to the default admin account.
Image Not Displaying: Confirm uploaded images are in static/uploads/ and have supported extensions (.png, .jpg, .jpeg, .gif).
Description Issues: Ensure descriptions are saved in admins.db and the image_descriptions table is created. Check for database errors in the console.
JavaScript Errors: Check the browser console for issues with the image preview or full-screen modal.

License
This project is unlicensed and provided as-is for educational purposes.