#Importing Flask...
from flask import Flask, render_template, redirect, url_for, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem 
#Importing Flask Name Function... 
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#All Restaurant Page...
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html' , restaurants = restaurants)

#Add New Restaurant Page...
@app.route('/restaurant/new' , methods = ['GET' , 'POST'])
def newRestaurant():
	#return "This page will be for making a new restaurant..."
	if request.method == 'POST':
		newrestaurant.name = Restaurant(name = request.form['name'])
		session.add(newrestaurant)
		session.commit()
		flash("New Restaurant Created...!!!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html' , restaurants = restaurants)

#Edit an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	#return "This page will be for editing restaurant"
	return render_template('editRestaurant.html' , i = editedRestaurant)

#Delete an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	#return "This page will be for deleting restaurant"
	return render_template('deleteRestaurant.html' , i = deletedRestaurant)


#Restaurant Menu...
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	#return "This page is the menu for restaurant"
	return render_template('menu.html' , restaurant_id = restaurant_id)
#Add a New Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	#return "This page is for creating new menu item for restaurant"
	return render_template('newMenuItem.html' , restaurant_id = restaurant_id)
#Edit an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	#return "This page is for editing menu item"
	return render_template('editMenuItem.html' , i = editedItem)
#Delete an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	#return "This page is for deleting menu item"
	return render_template('deleteMenuItem.html' , i = deletedItem)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)