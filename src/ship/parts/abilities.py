import math
from debug import log
from phys import phys
from geometry import Vector
from part import WIDTH, HEIGHT
from ents.bullet import Bullet, DIAMETER as BULLET_DIAMETER

def is_thruster(part):

	orig_init = part.__init__

	def __init__(self, *args, **kwargs):
		orig_init(self, *args, **kwargs)
		self.can_thrust = True

	def apply_thrust(self):

		MAGIC_IMPULSE_VALUE = 0.05

		pos = self.get_position()
		ang = self.get_rotation()
		wb2 = WIDTH*0.5
		applyPoint = (math.cos(math.radians(ang-180)) * wb2,
				math.sin(math.radians(ang-180)) * wb2)

		pos[0] += applyPoint[0]
		pos[1] += applyPoint[1]

		phys.apply_impulse(self.body,
				phys.make_impulse(self.get_rotation(), MAGIC_IMPULSE_VALUE),
				pos=pos)

	part.__init__ = __init__
	part.apply_thrust = apply_thrust
	return part

def is_blaster(part):

	orig_init = part.__init__
	orig_update = part.update

	def __init__(self, *args, **kwargs):
		orig_init(self, *args, **kwargs)
		self.can_shoot = True
		self.shot_cooldown = 1000
		self.shot_time = 0

	def shoot(self):
		if self.can_shoot:
			self.can_shoot = False
			self.shot_timer = self.shot_cooldown
			my_pos = self.get_position()
			my_ang = self.get_rotation()
			shot_pos = my_pos + Vector(
					math.cos(math.radians(my_ang+180)) * (WIDTH + BULLET_DIAMETER + 0.05) / 2.,
					math.sin(math.radians(my_ang+180)) * (WIDTH + BULLET_DIAMETER + 0.05) / 2.)
			shot = self.arena.make(
					Bullet,
					position=shot_pos,
					direction=my_ang+180)

	def update(self, dt):
		orig_update(self, dt)

		if not self.can_shoot:
			if self.shot_timer > 0:
				self.shot_timer -= dt
			else:
				self.can_shoot = True

	part.__init__ = __init__
	part.shoot = shoot
	part.update = update
	return part
