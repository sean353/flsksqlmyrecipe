# Recipe Management App

This is a simple Flask web application for managing recipes. Users can add, delete, update, and search for recipes.

## Features

- **Add Recipe:** Add a new recipe with ingredients, recipe name, and time to make.
- **Delete Recipe:** Remove a recipe from the list.
- **Update Recipe:** Modify existing recipes.
- **Search Recipe:** Search for recipes based on ingredients or recipe name.

## Prerequisites

Make sure you have the following installed:

- Python
- Flask
- SQLAlchemy
- MySQL (or another database of your choice)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/recipe-management-app.git
   cd backend , py app.py
2. If you want to use sqllite you need to put in comment the :
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/shondb'

and instead you need to activate the sqliteconnector: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use SQLite database named 'database.db'


