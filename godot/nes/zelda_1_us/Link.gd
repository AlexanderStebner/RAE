extends Actor

## running speed
@export var speed = 50

func _ready():
	set_facing(Vector2.DOWN)
	$AnimationTree.get("parameters/playback").travel("Walk")
	move_to(Vector2(1,2), func(x): pass, false)
	
	

func _process(delta):
	if $AnimationTree.get("parameters/playback").get_current_node() == "Attack":
		return
	velocity = Vector2.ZERO
	if Input.is_action_pressed("ui_left"):
		velocity = Vector2.LEFT * speed
	if Input.is_action_pressed("ui_right"):
		velocity = Vector2.RIGHT * speed
	if Input.is_action_pressed("ui_up"):
		velocity = Vector2.UP * speed
	if Input.is_action_pressed("ui_down"):
		velocity = Vector2.DOWN * speed
	var attack = Input.is_action_just_pressed("Attack")

	if attack:
		$AnimationTree.get("parameters/playback").travel("Attack")
	elif velocity != Vector2.ZERO:
		$AnimationTree.get("parameters/playback").travel("Walk")
		set_facing(velocity)
	else:
		$AnimationTree.get("parameters/playback").travel("Idle")
	
func set_facing(velocity):
	$AnimationTree.set("parameters/Walk/blend_position", velocity)
	$AnimationTree.set("parameters/Attack/blend_position", velocity)
	
	move_and_slide()

func test(callback: Callable):
	print("Hallo")
	callback.call("Done")
