extends Actor

class_name Octorok

@onready var rock = preload("res://scenes/weapons/OctorokRock.tscn")

## running speed
@export var speed = 40

## common settings
##################
@export var hurts_to_touch = true
@export var strength = 1
@export var energy = 2

@export var inputSource: InputSource

var directionMap = {InputSource.LEFT: Vector2.LEFT, InputSource.RIGHT: Vector2.RIGHT,
						InputSource.UP: Vector2.UP, InputSource.DOWN: Vector2.DOWN}

var facing = Vector2.ZERO

var pausingToShoot = false

func _ready():
	set_facing(Vector2.DOWN)


func _process(delta) -> void:
	if pausingToShoot:
		return

	var hitButtons = []
	var downButtons = []
	if inputSource == null:
		hitButtons = [InputSource.ATTACK]
	else:
		hitButtons = inputSource.get_hit_buttons()
		downButtons = inputSource.get_held_buttons()

	var direction = Vector2.ZERO
	if len(downButtons) > 0 and downButtons[0] in directionMap:
		direction = directionMap[downButtons[0]]
		var aligned = position_aligned_to_grid(direction)
		if aligned != position:
			teleport_to(aligned, func(ignore): return, true)
		move_delta(direction, speed, delta)

	var attack = InputSource.ATTACK in hitButtons

	# Animations
	if attack:
		pausingToShoot = true
		$ShootWaitTimer.start()
		return
	elif direction != Vector2.ZERO:
		$AnimationTree.get("parameters/playback").travel("Walk")
		set_facing(direction)

func set_facing(direction):
	$AnimationTree.set("parameters/Walk/blend_position", direction)
	facing = direction


## align to grid (8x8 px), if changing direction
func position_aligned_to_grid(new_direction):
	#print(position)
	if facing.x == new_direction.x or facing.y == new_direction.y:
		return position
	return position.snapped(Vector2(8, 8))

func instantiate_rock():
	var new_rock = rock.instantiate()
	new_rock.add_collision_exception_with(self)
	new_rock.direction = facing
	new_rock.position = self.position + Vector2(4, 3)
	get_parent().add_child(new_rock)
	pausingToShoot = false
