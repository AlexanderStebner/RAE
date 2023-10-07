extends Actor

class_name OctorokRock

@export var direction: Vector2

@export var speed = 120

func _ready():
	pass

func _process(delta):
	move_delta(direction, speed, delta)

func collide(other: Actor):
	queue_free()

func collide_tile_map(position: Vector2):
	queue_free()
