extends StaticBody2D

class_name Actor

## Moves (or tries to move) this actor to a target location.
##
## @param target	final location using global coordinates
## @param callback	gets called when movement is complete (or failed)
## @param collide	set false, if movement should stop just before a 
## collision would happen (e.g. move an NPC right up until a wall)
## @param override	this is now the only movement of this actor
## @param cancel_if_target_blocked	does not move, if target location
## is blocked
func move_to(target: Vector2,
			callback: Callable, 
			collide=true, 
			override=true,
			cancel_if_target_blocked=false):
	pass
	
	
## Teleports this actor to a target location. For callback,
## see move_to(). Fails, if target is blocked, unless force is true.
func teleport_to(target: Vector2, callback: Callable, force=false):
	var original_position = position
	
	# teleport to target
	position = target
	
	# try moving slightly in all directions
	var collisionInfo = move_and_collide(Vector2(0.1, 0.1), true)
	if collisionInfo == null:
		collisionInfo = move_and_collide(Vector2(-0.1, -0.1), true)
	
	# if colliding and not forced, return
	if collisionInfo != null and force == false:
		position = original_position
	
	# otherwise move to location
	if force == true or collisionInfo == null:
		position = target
		callback.call(collisionInfo)
	callback.call(collisionInfo)
	
	
## Moves by delta in the given direction. For "collide", see move_to().
func move_delta(direction: Vector2, speed: float, delta: float, collide=true):
	var collisionInfo = move_and_collide(direction * speed * delta, false)
	if collisionInfo != null and collide:
		var obj = collisionInfo.get_collider()
		var position = collisionInfo.get_position()
		if obj is TileMap:
			collide_tile_map(position)
		elif obj is Actor:
			_collide(obj as Actor)
		else:
			push_error("collision with unrecognized object type")
	
	
## Override to check if self and target_obj are blocking each other.
## I.e., couldn't overlap. (player and enemy, player and wall etc.)
func is_blocking_me(target_obj: Actor):
	push_error("is_blocking_me() not overridden.")


## Makes sure that any collision is registered by both parties once.
func _collide(other: Actor, is_first = true):
	if is_first:
		other._collide(self, false)
	collide(other)


## Override to execute any collision logic
func collide(other: Actor):
	push_error("collide() not overridden")
	
	
## Override to execute when colliding with tilemap
func collide_tile_map(position: Vector2):
	pass

