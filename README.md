Micro Project - Full Stack Contact Book Application

Team Members

4MC23IS006 -	Anish jrall
4MC23IS012 -	Appu H A
4MC23IS063 -	Mokshith A H
4MC23IS054	- Keshav singh
4MC23IS062 -	Mohammed Ahmed Raza

Project Description

Contact book is a full-stack web application built with Django that provides a secure and intuitive platform for managing personal contacts. The application features user authentication and allows each user to maintain their private contact database with complete CRUD (Create, Read, Update, Delete) functionality.

 Key Features :
 
User Authentication - Secure registration and login system
Contact Management - Add, view, edit, and delete contacts
Advanced Search - Find contacts by name, email, or phone number
Favorite System - Star important contacts for quick access
Profile Pictures - Upload and display contact photos
Birthday Tracking - Never miss a birthday with reminders
Import/Export - Bulk operations using CSV files
Dark/Light Theme - Toggle between themes for comfortable viewing
Responsive Design - Works seamlessly on all devices



Setup Instructions

Follow these steps to set up and run the application locally.

1. Clone the repository

Open your terminal and clone the project, then navigate into the main project directory:

git clone [https://github.com/anishjrall/Micro-project-fullstack-15.git](https://github.com/anishjrall/Micro-project-fullstack-15.git)
cd Micro-project-fullstack-15/contactbook_project


2. Install dependencies

Install the necessary Python packages, including Django and Pillow (for image handling, like profile pictures):

pip install django Pillow


3. Run migrations

Apply the database schema changes to set up the necessary tables (including user authentication and contacts model):

python manage.py makemigrations
python manage.py migrate


4. Run server

Start the local development server:

python manage.py runserver

