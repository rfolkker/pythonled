#Python LED Web Handler
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from gpiozero import StatusZero
from time import sleep

sz = StatusZero()
sz.off() # initialize off

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('index')
parser.add_argument('color')

class InvalidUsage(Exception):
	status_code = 400
	def __init(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload
	def to_dict(self):
		retval = dict(self.payload or ())
		retval['message'] = self.message
		return retval

class trigger_light(Resource):
	def get(self, index, color, status):
		light_index=None
		light_color=None
		light_status=None

		if index=='1':
			light_index = sz.one
		elif index=='2':
			light_index = sz.two
		elif index=='3':
			light_index = sz.three
		else:
			raise InvalidUsage("Invalid Light index specified", \
				status_code=422)

		if color=='red':
			light_color=light_index.red
		elif color=='green':
			light_color_light_index.green
		else:
			raise InvalidUsage("Invalid color value", \
				status_code=422)

		if  status=='on':
			light_status=light_color.on
		elif status='off':
			light_status=light_color.off
		else:
			raise InvalidUsage("Invalid Light status", \
				status_code=422)
		light_status()
		result = {'data':dict(zip(sz.value))}
		return jsonify(result)

class red_on(Resource):
	def get(self):
		sz.one.red.on()
		sz.two.red.on()
		sz.three.red.on()
		result = {'data':dict(zip(sz.value))}
		return jsonify(result)
class red_off(Resource):
	def get(self):
		sz.one.red.off()
		sz.two.red.off()
		sz.three.red.off()
		result = {'data':dict(zip(sz.value))}
		return jsonify(result)
class green_on(Resource):
	def get(self):
		sz.one.green.on()
		sz.two.green.on()
		sz.three.green.on()
		result = {'data':dict(zip(sz.value))}
		return jsonify(result)
class green_off(Resource):
	def get(self):
		sz.one.green.off()
		sz.two.green.off()
		sz.three.green.off()
		result= {'data':dict(zip(sz.value))}

api.add_resource(red_on, '/red/on') # Route_1
api.add_resource(red_off, '/red/0ff') # Route_2
api.add_resource(green_on, '/green/on') # Route_3
api.add_resource(green_off, '/green/off') # Route_4
api.add_resource(trigger_light, '/<index>/<color>/<status>') #Dynamic route

# Routes
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response=jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(port='5555')
