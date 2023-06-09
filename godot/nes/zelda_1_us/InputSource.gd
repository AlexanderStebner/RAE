extends Node

class_name InputSource

## Must correspond to actions defined in Project Settings/Input Map
@export_group("Action IDs")
@export var moveLeft = "ui_left"
@export var moveRight = "ui_right"
@export var moveUp = "ui_up"
@export var moveDown = "ui_down"
@export var attack = "Attack"

const LEFT = "left"
const RIGHT = "right"
const UP = "up"
const DOWN = "down"
const ATTACK = "attack"

var allActions = [moveLeft, moveRight, moveUp, moveDown, attack]
var commonNames = {moveLeft: LEFT, moveRight: RIGHT, moveUp: UP, moveDown: DOWN, attack: ATTACK}

var buttonDownMap = {}
var buttonHitMap = {}

func translate(buttons):
	return buttons.map(func(name): return commonNames[name])

func _ready():
	for action in allActions:
		buttonDownMap[action] = false
		buttonHitMap[action] = false

func _process(delta):
	for action in allActions:
		buttonHitMap[action] = Input.is_action_just_pressed(action)
		buttonDownMap[action] = Input.is_action_pressed(action)
	
	
func get_held_buttons():
	return translate(buttonDownMap.keys().filter(func(key): return buttonDownMap[key]))
	

func get_hit_buttons():
	var hitButtons = []
	for action in allActions:
		if buttonHitMap[action]:
			hitButtons.append(action)
			buttonHitMap[action] = false
	return translate(hitButtons)
