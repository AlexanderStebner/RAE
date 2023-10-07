extends Actor

class_name Link

@onready var sword = preload("res://scenes/weapons/Sword.tscn")

## running speed
@export var speed = 80

@export var inputSource: InputSource

@export var hasSword = true

var directionMap = {InputSource.LEFT: Vector2.LEFT, InputSource.RIGHT: Vector2.RIGHT, 
						InputSource.UP: Vector2.UP, InputSource.DOWN: Vector2.DOWN}

var facing = Vector2.ZERO	

func _ready():
	set_facing(Vector2.DOWN)
	

func _process(delta) -> void:
	if inputSource == null:
		return
		
	var hitButtons = inputSource.get_hit_buttons()
	var downButtons = inputSource.get_held_buttons()

	# Block movement if attacking
	if $AnimationTree.get("parameters/playback").get_current_node() == "Attack":
		return
	
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
		$AnimationTree.get("parameters/playback").travel("Attack")
		if hasSword:
			instantiate_sword()
	elif direction != Vector2.ZERO:
		$AnimationTree.get("parameters/playback").travel("Walk")
		set_facing(direction)
	else:
		$AnimationTree.get("parameters/playback").travel("Idle")
	
func set_facing(direction):
	$AnimationTree.set("parameters/Walk/blend_position", direction)
	$AnimationTree.set("parameters/Attack/blend_position", direction)
	facing = direction
	
	
## align to grid (8x8 px), if changing direction
func position_aligned_to_grid(new_direction):
	#print(position)
	if facing.x == new_direction.x or facing.y == new_direction.y:
		return position
	return position.snapped(Vector2(8, 8))
	
	
func instantiate_sword():
	var new_sword = sword.instantiate()
	new_sword.direction = facing
	self.add_child(new_sword)
