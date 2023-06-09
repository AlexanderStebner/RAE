extends Node

@export var player: Node

func _ready():
	if player == null:
		push_error("Player node must be attached to the SceneManager")
	
