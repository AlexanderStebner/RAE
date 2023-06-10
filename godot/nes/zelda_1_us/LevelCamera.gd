extends Camera2D

## Screen transition speed
@export var speed: float = 200

## Pixel size of screen. (Also change viewport size in Project Settings)
@export var screen_size = Vector2(256, 176)

## Size of HUD at screen top (to transition screen when reaching HUD)
@export var hud_offset = Vector2(0, 48)

@onready var sceneManager = get_node("../SceneManager")
var player: Node = null

func _ready():
	player = sceneManager.player

func _physics_process(delta: float):
	if player == null:
		return
	
	# Actual movement
	global_position = global_position.move_toward(desired_position(), delta * speed)
	#TODO send signal to animate but not move

# Calculating the gridsnapped position
func desired_position():
	return (player.global_position / screen_size).floor() * screen_size + screen_size/2 - hud_offset/2
