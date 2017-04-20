#! /usr/bin/env python3


import json
import decimal
import itertools
import pygame
import pygame.gfxdraw
import random


class UniversalConstants:
	GRAVITATIONAL_CONSTANT = decimal.Decimal("6.67408e-11")
	ASTRONOMICAL_UNIT      = decimal.Decimal("1.495978707e11")


class SolarBody(UniversalConstants):
	def __init__(self, attributes=None):
		""" TODO """
		assert(type(attributes) == dict), "attributes must be a dictionary"
		self.set_default_attributes()
		if attributes != None:
			self.set_attributes(attributes)
		return

	def set_default_attributes(self):
		""" TODO """
		self.name     = None
		self.mass     = decimal.Decimal("0.0")
		self.radius   = decimal.Decimal("0.0")
		self.location = {
			"x": decimal.Decimal("0.0"),
			"y": decimal.Decimal("0.0")
		}
		self.velocity = {
			"x": decimal.Decimal("0.0"),
			"y": decimal.Decimal("0.0")
		}
		return

	def set_attributes(self, attributes):
		""" TODO """
		assert(type(attributes) == dict), "attributes must be a dictionary"
		for key, value in attributes.items():
			if key == "name":
				assert(type(value) == str), "solar body name must be a string"
				self.name = value
			elif key == "mass":
				assert(
					type(value) == int   or
					type(value) == float or
					type(value) == str   or
					isinstance(value, decimal.Decimal)
				), "solar body mass must be either an: integer, float, long, string, or instance of decimal.Decimal"
				self.mass = value
			elif key == "radius":
				assert(
					type(value) == int   or
					type(value) == float or
					type(value) == str   or
					isinstance(value, decimal.Decimal)
				), "solar body radius must be either an: integer, float, long, string, or instance of decimal.Decimal"
				self.radius = value
			elif key == "location":
				assert(type(value) == dict), "solar body location must be a dictionary"
				assert("x" in value), "solar body location must contain a x-axis"
				assert("y" in value), "solar body location must contain a y-axis"
				for axis, magnitude in value.items():
					assert(
						type(axis) == str and
						(axis == "x" or axis == "y")
					), "solar body location axis must be either x or y"
					assert(
						type(magnitude) == int   or
						type(magnitude) == float or
						type(magnitude) == str   or
						isinstance(magnitude, decimal.Decimal)
					), "solar body location magnitude must be either an: integer, float, long, string, or instance of decimal.Decimal"
				self.location = {}
				for axis, magnitude in value.items():
					self.location[axis] = decimal.Decimal(magnitude)
			elif key == "velocity":
				assert(type(value) == dict), "solar body velocity must be a dictionary"
				assert("x" in value), "solar body velocity must contain a x-axis"
				assert("y" in value), "solar body velocity must contain a y-axis"
				for axis, magnitude in value.items():
					assert(
						type(axis) == str and
						(axis == "x" or axis == "y")
					), "solar body velocity axis must be either x or y"
					assert(
						type(magnitude) == int   or
						type(magnitude) == float or
						type(magnitude) == str   or
						isinstance(magnitude, decimal.Decimal)
					), "solar body velocity magnitude must be either an: integer, float, long, string, or instance of decimal.Decimal"
				self.velocity = {}
				for axis, magnitude in value.items():
					self.velocity[axis] = decimal.Decimal(magnitude)
			elif key == "acceleration":
				assert(type(value) == dict), "solar body acceleration must be a dictionary"
				assert("x" in value), "solar body acceleration must contain a x-axis"
				assert("y" in value), "solar body acceleration must contain a y-axis"
				for axis, magnitude in value.items():
					assert(
						type(axis) == str and
						(axis == "x" or axis == "y")
					), "solar body acceleration axis must be either x or y"
					assert(
						type(magnitude) == int   or
						type(magnitude) == float or
						type(magnitude) == str   or
						isinstance(magnitude, decimal.Decimal)
					), "solar body acceleration magnitude must be either an: integer, float, long, string, or instance of decimal.Decimal"
				self.acceleration = {}
				for axis, magnitude in value.items():
					self.acceleration[axis] = decimal.Decimal(magnitude)
		return

	def speed(self):
		speed = decimal.Decimal(
			self.velocity['x'] ** 2 +
			self.velocity['y'] ** 2
		).sqrt()
		return speed

	def distance(self, remote_body):
		""" TODO """
		assert(isinstance(remote_body, SolarBody) == True)
		diff_x = remote_body.location["x"] - self.location["x"]
		diff_y = remote_body.location["y"] - self.location["y"]
		distance = decimal.Decimal(
			diff_x ** 2 + diff_y ** 2
		).sqrt()
		return distance

	def acceleration(self, remote_body):
		""" TODO """
		assert(isinstance(remote_body, SolarBody) == True)
		# Find: Total Gravitational Force
		distance = self.distance(remote_body)
		if distance == decimal.Decimal("0.0"):
			return {
				"x": decimal.Decimal("0.0"),
				"y": decimal.Decimal("0.0")
			}

		force_magnitude = -1 * (self.GRAVITATIONAL_CONSTANT * self.mass * remote_body.mass) / (distance ** 2)

		# Find: F_X
		force_x = force_magnitude * (self.location["x"] / distance)

		# Find: F_Y
		force_y = force_magnitude * (self.location["y"] / distance)

		acceleration = {
			"x": force_x / self.mass,
			"y": force_y / self.mass
		}
		return acceleration

	def commit_net_acceleration(self, acceleration, tick_period):
		""" TODO """
		assert(type(acceleration) == dict), "acceleration must be a dictionary"
		assert("x" in acceleration), "acceleration must contain a x-axis"
		assert("y" in acceleration), "acceleration must contain a y-axis"
		for axis, magnitude in acceleration.items():
			assert(
				type(axis) == str and
				(axis == "x" or axis == "y")
			), "acceleration axis must be either x or y"
			assert(isinstance(magnitude, decimal.Decimal)), "acceleration magnitude must be a decimal.Decimal instance"
		assert(isinstance(tick_period, decimal.Decimal)), "tick period must be a decimal.Decimal instance"
		self.velocity['x'] += acceleration['x'] * tick_period
		self.velocity['y'] += acceleration['y'] * tick_period
		self.location['x'] += self.velocity['x'] * tick_period
		self.location['y'] += self.velocity['y'] * tick_period
		return

	def collides_with(self, remote_body):
		# https://stackoverflow.com/questions/345838
		radii = self.radius + remote_body.radius
		if self.distance(remote_body) < radii:
			return True
		return False

	def commit_collision(self, remote_body):
		# https://stackoverflow.com/questions/345838
		# https://en.wikipedia.org/wiki/Elastic_collision
		print("COLLISION")
		for axis, magnitude in self.velocity.items():
			self.velocity[axis] = -1 * magnitude
		for axis, magnitude in remote_body.velocity.items():
			remote_body.velocity[axis] = -1 * magnitude
		return

	def __str__(self):
		""" TODO """
		string  = 'name:     {}\n'.format(self.name)
		string += 'location: {}\n'.format(self.location)
		string += 'velocity: {}'.format(self.velocity)
		return string

	def __hash__(self):
		""" TODO """
		return hash(self.name)


class SolarSystem(UniversalConstants):
	def __init__(self, configuration=None):
		""" TODO """
		assert(
			configuration == None or
			type(configuration) == dict
		), "solar system configuration must be either None or a dictionary"
		self.set_default_configuration()
		if configuration != None:
			self.set_configuration(configuration)
		return

	def set_default_configuration(self):
		""" TODO """
		self.bodies      = []
		self.tick_period = 1.0
		return

	def set_configuration(self, configuration):
		""" TODO """
		assert(type(configuration) == dict), "solar system configuration must be a dictionary"
		for key, value in configuration.items():
			if key == "decimal_accuracy":
				assert(type(value) == int or 0 < value), "decimal accuracy must be a positive integer"
				decimal.getcontext().prec = value
			elif key == "tick_period":
				assert(
					type(value) == int   or
					type(value) == float or
					type(value) == str   or
					isinstance(value, decimal.Decimal)
				), "tick period must be either a: int, float, long, string, or decimal.Decimal instance"
				self.tick_period = decimal.Decimal(value)
			elif key == "au_ratio":
				assert(type(value) == int), "AU ratio must be an int"
				self.au_ratio = value
			elif key == "frame_buffer":
				assert(
					type(value) == int   or
					type(value) == float or
					type(value) == str   or
					isinstance(value, decimal.Decimal)
				)
				self.frame_buffer = int(value)
			elif key == "bodies":
				assert(type(value) == list), "bodies must be a list"
				for body_configuration in value:
					assert(type(body_configuration) == dict), "body must be a dictionary"
					assert("name" in body_configuration), "body must contain a name"
					assert(type(body_configuration["name"]) == str), "body name must be a string"

					assert("mass" in body_configuration), "body must contain a mass"
					assert(
						type(body_configuration["mass"]) == int   or
						type(body_configuration["mass"]) == float or
						type(body_configuration["mass"]) == str
					), "body mass must be either a: int, float, long, or string"
					body_configuration["mass"] = decimal.Decimal(body_configuration["mass"])

					assert("radius" in body_configuration), "body must contain a radius"
					assert(
						type(body_configuration["radius"]) == int   or
						type(body_configuration["radius"]) == float or
						type(body_configuration["radius"]) == str
					), "body radius must be either a: int, float, long, or string"
					body_configuration["radius"] = decimal.Decimal(body_configuration["radius"])

					assert("location" in body_configuration), "body must contain a location"
					assert(type(body_configuration["location"]) == dict), "body location must be a dictionary"
					for axis, magnitude in body_configuration["location"].items():
						assert(
							type(axis) == str and
							(axis == "x" or axis == "y")
						), "body location axis must be either x or y"
						assert(
							type(magnitude) == int   or
							type(magnitude) == float or
							type(magnitude) == str
						), "body location magnitude be either a: int, float, long, or string"
						body_configuration["location"][axis] = decimal.Decimal(magnitude)

					assert("velocity" in body_configuration), "body must contain a velocity"
					assert(type(body_configuration["velocity"]) == dict), "body location must be a dictionary"
					for axis, magnitude in body_configuration["velocity"].items():
						assert(
							type(axis) == str and
							(axis == "x" or axis == "y")
						), "body velocity axis must be either x or y"
						assert(
							type(magnitude) == int   or
							type(magnitude) == float or
							type(magnitude) == str
						), "body velocity magnitude be either a: int, float, long, or string"
						body_configuration["velocity"][axis] = decimal.Decimal(magnitude)

					body = SolarBody(body_configuration)
					self.add_body(body)
		return

	def add_body(self, body):
		# TODO - check if body name already exists, raise runtime error
		assert(isinstance(body, SolarBody)), "body must be an instance of SolarBody"
		assert(body.name not in self.bodies), "body name must be unique"
		self.bodies.append(body)
		return

	def tick(self):
		net_acceleration = {}
		# TODO - randomize order of bodies (for collisions)
		random.shuffle(self.bodies)
		combinations = itertools.combinations(self.bodies, 2)
		for body_a, body_b in combinations:
			# http://www.petercollingridge.co.uk/book/export/html/6
			if body_a.collides_with(body_b):
				print("COLLISION")
				body_a.commit_collision(body_b)


			if body_a not in net_acceleration:
				net_acceleration[body_a] = {
					"x": decimal.Decimal("0.0"),
					"y": decimal.Decimal("0.0")
				}
			if body_b not in net_acceleration:
				net_acceleration[body_b] = {
					"x": decimal.Decimal("0.0"),
					"y": decimal.Decimal("0.0")
				}
			acceleration_a = body_a.acceleration(body_b)
			acceleration_b = body_b.acceleration(body_a)
			for axis, magnitude in acceleration_a.items():
				net_acceleration[body_a][axis] += magnitude
			for axis, magnitude in acceleration_b.items():
				net_acceleration[body_b][axis] += magnitude
		for body, acceleration in net_acceleration.items():
			body.commit_net_acceleration(acceleration, self.tick_period)
		return

	def graphical_interface(self):
		initial_window_dimension_x = 800
		initial_window_dimension_y = 640
		initial_window_dimensions  = (initial_window_dimension_x, initial_window_dimension_y)

		initial_window_background = (255, 255, 255)
		initial_line_background   = (0, 0, 0)

		pygame.init()

		window = pygame.display.set_mode(initial_window_dimensions) #, pygame.FULLSCREEN)
		
		pygame.display.set_caption("n-body simulator")

		window.fill(initial_window_background)

		window_width, window_height = pygame.display.get_surface().get_size()
		window_center_x = window_width  // 2
		window_center_y = window_height // 2

		mainloop = True

		lines = {}

		while mainloop:
			initial_position = {}
			for body in self.bodies:
				initial_position[body] = {}
				x = int(self.au_ratio * body.location['x'] / self.ASTRONOMICAL_UNIT) + window_center_x
				y = int(self.au_ratio * body.location['y'] / self.ASTRONOMICAL_UNIT) + window_center_y
				initial_position[body]['x'] = x
				initial_position[body]['y'] = y

			self.tick()

			# erase
			window.fill(initial_window_background)

			for body in self.bodies:
				x_i = initial_position[body]['x']
				y_i = initial_position[body]['y']
				x_f = int(self.au_ratio * body.location['x'] / self.ASTRONOMICAL_UNIT) + window_center_x
				y_f = int(self.au_ratio * body.location['y'] / self.ASTRONOMICAL_UNIT) + window_center_y

				radius = self.au_ratio * body.radius / self.ASTRONOMICAL_UNIT

				if body not in lines:
					lines[body] = []

				lines[body].append( ( (x_i, y_i), (x_f, y_f) ) )
				if self.frame_buffer < len(lines[body]):
					lines[body] = lines[body][-self.frame_buffer:]

				pygame.gfxdraw.aacircle(window, x_f, y_f, radius, initial_line_background)
				
				for line in lines[body]:
					initial, final = line
					x_a, y_a = initial
					x_b, y_b = final
					pygame.gfxdraw.line(window, x_a, y_a, x_b, y_b, initial_line_background)

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.VIDEORESIZE:
					window_width, window_height = pygame.display.get_surface().get_size()
					window_center_x = window_width  // 2
					window_center_y = window_height // 2
					window.fill(initial_window_fill)
				elif event.type == pygame.QUIT:
					mainloop = False
		return


def main():
	with open("environment.json", "r") as handler:
		configuration = json.loads(handler.read())
	system = SolarSystem(configuration)
	system.graphical_interface()
	return


if __name__ == "__main__":
	main()
