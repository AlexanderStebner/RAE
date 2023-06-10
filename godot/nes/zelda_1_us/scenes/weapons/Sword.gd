extends Actor

class_name Sword

@export var direction: Vector2

func _ready():
	set_facing(direction)

func set_facing(direction):
	if direction == Vector2.RIGHT:
		$AnimationPlayer.play("right")
	elif direction == Vector2.LEFT:
		$AnimationPlayer.play("left")
	elif direction == Vector2.UP:
		$AnimationPlayer.play("up")
	elif direction == Vector2.DOWN:
		$AnimationPlayer.play("down")

	remove_sword()
	
func remove_sword():
	await $AnimationPlayer.animation_finished
	queue_free()
