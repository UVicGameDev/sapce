import math
import random
from pygame import Color
from pygame import draw
from draw import PPM


class Jucoid:
	color = None
	vertices = None

	def __init__(self):

		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		self.color = Color( r, g, b, 255 )

		numberOfVertices = random.randint( 6, 10 )
		degreeSplinter = 360 / numberOfVertices

		self.vertices = []
		for vertexIndex in range( numberOfVertices ):

			angle = vertexIndex * degreeSplinter + random.uniform( -degreeSplinter/2, degreeSplinter/2 )
			length = random.uniform( 0.5, 3 )
			vertex = ( math.cos( math.radians(angle) ) * length,
					-math.sin( math.radians(angle) ) * length )
			self.vertices.append( vertex )

	def draw(self, surface):

		drawVertices = []
		for vertex in self.vertices:
			drawVertices.append( ( (5 + vertex[0]) * PPM,
					(5 + vertex[1]) * PPM ) )
		draw.polygon( surface, self.color, drawVertices, 0 )

