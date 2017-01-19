'''
Purpose: Flask server provides backend for the app

Author Name: Md. Tanvir Islam

Command to execute: python app.py 

'''
from flask import Flask
from flask import render_template
from flask import json
from flask import request
import random
import sys
import ast # module to transform a string to a dictionary

app = Flask(__name__)

users = {}

@app.route("/")
def index():
	return render_template("index.html"), 200

@app.route("/intro", methods = ["POST"])
def intro():
	post_obj = request.json
	post_obj["board"] = make_board(post_obj["level"])
	users[post_obj["username"]] = post_obj
	return json.dumps(post_obj), 200

@app.route("/card", methods = ["POST"])
def card():
	post_obj = request.json
	choice = post_obj["choice"]
	choice = ast.literal_eval(choice) # converts the str to dict
	client_name = post_obj["username"]
	client = users[client_name]
	client_board = client["board"]
	info = {}
	info["value"] = client_board[int(choice["bigBox"])][int(choice["smallerBox"])]
	info["id"] = choice["id"]
	return json.dumps(info), 200

@app.errorhandler(404)
def page_not_found(err):
	return render_template("404.html"), 400

'''
	Function: make_board
	 Purpose: Creates and returns an array containing a 2-D array of a size provided
			  through the function parameters.
		  in: size 
'''
def make_board(size):
	double = size * size
	pool = []
	pool_two = []
	board = []
	for i in range(int(double / 2)):
		pool.append(i)
		pool_two.append(i)
	larger_pool = []
	for i in range(double):
		if len(pool) != 0:
			random_draw = pool[random.randint(0, len(pool) - 1)]
			pool.remove(random_draw)
			larger_pool.append(random_draw)
		elif len(pool) == 1:
			random_draw = pool[0]
			pool.remove(random_draw)
			larger_pool.append(random_draw)
		if len(pool_two) != 0:
			random_draw = pool_two[random.randint(0, len(pool_two) - 1)]
			pool_two.remove(random_draw)
			larger_pool.append(random_draw)
		elif len(pool_two) == 1:
			random_draw = pool_two[0]
			pool_two.remove(random_draw)
			larger_pool.append(random_draw)

	for i in range(size):	
		mini_board = []
		for j in range(size):
			mini_board.append(larger_pool[0])
			larger_pool.remove(larger_pool[0])
		board.append(mini_board)	
	return board

if __name__ == "__main__":
	app.run(host = "localhost", port = 2406, debug = True)