extends Camera2D

# Camera script follwing a target (usually the player)
# This camera is snapped to a grid, therefore only moves when the character exits a screen.

@export var target : NodePath
@export var speed : float = 1000
@export var screen_size := Vector2(256, 224)

@onready var Target = get_node_or_null(target)

func _physics_process(delta: float) -> void:
	if not is_instance_valid(Target):
		return
	
	# Actual movement
	#var tween = create_tween().set_trans(Tween.TRANS_LINEAR).set_ease(Tween.EASE_OUT_IN)
	#tween.tween_property(self, "global_position", desired_position(), align_time)
	global_position = global_position.move_toward(desired_position(), delta * speed)

# Calculating the gridnapped position
func desired_position() -> Vector2:
	return (Target.global_position / screen_size).floor() * screen_size + screen_size/2
