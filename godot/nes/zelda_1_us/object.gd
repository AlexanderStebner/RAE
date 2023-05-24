extends CharacterBody2D

class_name Actor

## Moves (or tries to move) this actor to a target location.
## params:
## - target = final location using global coordinates
## - callback = gets called when movement is complete (or failed)
## - collide = set false, if movement should stop just before a 
##   collision would happen (e.g. move an NPC right up until a wall)
## - override = this is now the only movement of this actor
## - cancel_if_target_blocked = does not move, if target location
##   is blocked
func move_to(target: Vector2,
			callback: Callable, 
			collide=true, 
			override=true,
			cancel_if_target_blocked=false):
	pass
	
## Teleports this actor to a target location. For callback,
## see move_to(). Fails, if target is blocked.
func teleport_to(target: Vector2, callback: Callable):
	pass
	
## Moves by delta in the given direction. For "collide", see move_to().
func move_delta(direction: Vector2, delta: float, collide=true):
	pass
	
## Override to check if self and target_obj are blocking each other.
## I.e., couldn't overlap. (player and enemy, player and wall etc.)
func is_blocking_me(target_obj: Actor):
	push_error("is_blocking_me() not overridden.")

## Makes sure that any collision is registered by both parties once.
func _collide(other: Actor, is_first = true):
	if is_first:
		other._collide(self, false)
	print("I collided")

## Override to execute any collision logic
func collide(other: Actor):
	push_error("collide() not overridden")
