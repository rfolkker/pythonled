#Python LED Web Handler
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from gpiozero import StatusZero
from time import sleep

sz = StatusZero()
sz.off() # initialize off

app = Flask(__name__)
api = Api(app)

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
			light_color=light_index.green
		else:
			raise InvalidUsage("Invalid color value", \
				status_code=422)

		if  status=='on':
			light_status=light_color.on
		elif status=='off':
			light_status=light_color.off
		else:
			raise InvalidUsage("Invalid Light status", \
				status_code=422)
		light_status()
		print(sz.value)
		#result = {'data':dict(zip(sz.value.StatusZeroValue))}
		return jsonify(sz.value)

class all_on(Resource):
	def get(self):
		sz.one.green.on()
		sz.one.red.on()
		sz.two.green.on()
		sz.two.red.on()
		sz.three.red.on()
		sz.three.green.on()
		return jsonify(sz.value)
class all_off(Resource):
	def get(self):
		sz.one.green.off()
		sz.one.red.off()
		sz.two.green.off()
		sz.two.red.off()
		sz.three.green.off()
		sz.three.red.off()
		return jsonify(sz.value)
class red_on(Resource):
	def get(self):
		sz.one.red.on()
		sz.two.red.on()
		sz.three.red.on()
		return jsonify(sz.value)
class red_off(Resource):
	def get(self):
		sz.one.red.off()
		sz.two.red.off()
		sz.three.red.off()
		return jsonify(sz.value)
class green_on(Resource):
	def get(self):
		sz.one.green.on()
		sz.two.green.on()
		sz.three.green.on()
		return jsonify(sz.value)
class green_off(Resource):
	def get(self):
		sz.one.green.off()
		sz.two.green.off()
		sz.three.green.off()
		return jsonify(sz.value)
class all_status(Resource):
	def get(self):
		return jsonify(sz.value)
   

api.add_resource(all_status, "/status")
api.add_resource(all_on, '/on') 
api.add_resource(all_off, '/off')
api.add_resource(red_on, '/red/on') # Route_1
api.add_resource(red_off, '/red/off') # Route_2
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
	app.run(host='0.0.0.0', port='5555')
