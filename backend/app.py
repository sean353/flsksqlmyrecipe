from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/shondb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use SQLite database named 'database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'blabla'

# Define the Recipe model
class Recipe(db.Model):
    __tablename__ = 'Recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    Ingredients = db.Column(db.String(50))
    recipe_name = db.Column(db.String(50))
    How_much_timetomake = db.Column(db.Integer)

# Uncomment the line below to create the table (execute it only once)
# db.create_all()

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Retrieve form data
        ingredients = request.form['ingredients']
        recipe_name = request.form['recipe_name']
        time_to_make = request.form['time_to_make']

        # Validate form data
        if not ingredients or not recipe_name or not time_to_make:
            flash('Please fill in all the fields', 'danger')
            return redirect(url_for('add_recipe'))

        # Convert time_to_make to integer
        try:
            time_to_make = int(time_to_make)
        except ValueError:
            flash('Invalid value for time to make. Please enter a valid number', 'danger')
            return redirect(url_for('add_recipe'))

        # Create a new recipe and add it to the database
        new_recipe = Recipe(Ingredients=ingredients, recipe_name=recipe_name, How_much_timetomake=time_to_make)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')
        return redirect(url_for('list_recipe'))
    
    # Handle 'GET' request (display the form)
    return render_template('add_recipe.html')


@app.route('/delete_recipe/<int:id>', methods=['GET'])
def delete_recipe(id):
    # Retrieve the recipe to be deleted
    recipe = Recipe.query.get(id)
    if recipe:
        # Delete the recipe from the database
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully', 'success')
    return redirect(url_for('list_recipe'))

@app.route('/update_recipe/<int:id>', methods=['GET', 'POST'])
def update_recipe(id=-1):
    # Retrieve the recipe to be updated
    recipe = Recipe.query.get(id)
    if request.method == 'POST':
        # Update recipe details
        recipe.Ingredients = request.form['ingredients']
        recipe.recipe_name = request.form['recipe_name']
        recipe.How_much_timetomake = int(request.form['time_to_make'])
        db.session.commit()
        flash('Recipe updated successfully', 'success')
        return redirect(url_for('list_recipe'))
    return render_template('update_recipe.html', recipe=recipe)

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    if 'search_term' in request.form:
        # Retrieve search term
        search_term = request.form['search_term']
        # Search for recipes based on ingredients or recipe name
        recipes = Recipe.query.filter(Recipe.Ingredients.ilike(f'%{search_term}%') | 
                                      Recipe.recipe_name.ilike(f'%{search_term}%')).all()
        return render_template('list_recipe.html', recipes=recipes)
    else:
        flash('No search term provided', 'warning')
        return redirect(url_for('list_recipe'))

@app.route('/list_recipe')
def list_recipe():
    # Retrieve all recipes from the database
    recipes = Recipe.query.all()
    return render_template('list_recipe.html', recipes=recipes)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they do not exist
        db.create_all()
        # Run the application in debug mode
        app.run(debug=True)
