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
	return "This page will show all my restaurants..."

#Add New Restaurant Page...
@app.route('/restaurant/new')
def newRestaurant():
	return "This page will be for making a new restaurant..."

#Edit an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return "This page will be for editing restaurant"

#Delete an Existing Restaurant Page...
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return "This page will be for deleting restaurant"


#Restaurant Menu...
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	return "This page is the menu for restaurant"

#Add a New Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return "This page is for creating new menu item for restaurant"

#Edit an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	return "This page is for editing menu item"

#Delete an Existing Menu Item...
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	return "This page is for deleting menu item"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)