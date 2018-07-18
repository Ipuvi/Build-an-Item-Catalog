#Importing Flask...
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
@app.route('/restaurant')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html' , restaurants = restaurants)

#Add New Restaurant Page...
@app.route('/restaurant/new' , methods = ['GET' , 'POST'])
def newRestaurant():
	#return "This page will be for making a new restaurant..."
	if request.method == 'POST':
		newrestaurant = Restaurant(name = request.form['name'])
		session.add(newrestaurant)
		session.commit()
		flash("New Restaurant Created...!!!")
		return redirect(url_for('newMenuItem' , restaurant_id = newrestaurant.id))
	else:
		return render_template('newRestaurant.html')

#Edit an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/edit' , methods = ['GET' , 'POST'])
def editRestaurant(restaurant_id):
	#return "This page will be for editing restaurant"
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant edited...")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html' , i = editedRestaurant)

#Delete an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/delete' , methods =['GET' , 'POST'])
def deleteRestaurant(restaurant_id):
	#return "This page will be for deleting restaurant"
	deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	Menu = session.query(MenuItem).filter_by(restaurant = deletedRestaurant).all()
	if request.method =='POST':
		session.delete(deletedRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html' , i = deletedRestaurant , dishes = Menu)


#Restaurant Menu...
@app.route('/restaurant/<int:restaurant_id>' , methods = ['GET' , 'POST'])
@app.route('/restaurant/<int:restaurant_id>/menu' , methods = ['GET' , 'POST'])
def showMenu(restaurant_id):
	#return "This page is the menu for restaurant"
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	Menu = session.query(MenuItem).filter_by(restaurant = restaurant).all()
	return render_template('menu.html' , restaurant = restaurant, Menu = Menu)
#Add a New Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/new' , methods = ['GET' , 'POST'])
def newMenuItem(restaurant_id):
	#return "This page is for creating new menu item for restaurant"
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'] , price = request.form['price'] , description = request.form['description'] , course = request.form['course'] , restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New Menu Item Created...')
		return redirect(url_for('showMenu' , restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html' , restaurant_id = restaurant_id)
#Edit an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit' , methods = ['GET' , 'POST'])
def editMenuItem(restaurant_id, menu_id):
	#return "This page is for editing menu item"
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['price']:
			editedItem.price = request.form['price'] 
		if request.form['description']:
			editedItem.description = request.form['description'] 
		if request.form['course']:
			editedItem.course = request.form['course']
		editedItem.restaurant = restaurant
		editedItem.id = menu_id
		session.add(editedItem)
		session.commit()
		flash("Menu Item Edited...")
		return redirect(url_for('showMenu' , restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html' , i = editedItem , restaurant = restaurant)
#Delete an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete' , methods = ['GET' , 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	#return "This page is for deleting menu item"
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		return redirect(url_for('showMenu' , restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html' , i = deletedItem , restaurant = restaurant)

if __name__ == '__main__':
	app.secret_key = "no_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)