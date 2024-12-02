import blackforge

def spawnPlayer(player:blackforge.object.GameObject) -> None:
    player.location = [*player.getState("spawn")]
    player.stats["spec"] = player.statCaps["spec"]
    player.stats["health"] = player.statCaps["health"]
    player.stats["reforge"] = player.statCaps["reforge"]

def configurePlayer(player:blackforge.object.GameObject) -> None:
    player.newState("rect", 0)
    player.newState("jumps", 1)
    player.newState("sliding", 0)

    spawnTile = player.app.getMap().getTile([544, 272], remove=1)
    player.newState("spawn", [
        spawnTile.location[0]* spawnTile.size[0],
        spawnTile.location[1]* spawnTile.size[1],
    ])

    def jump():
        if player.getState("jumps"):
            if player.action != "wall-slide":
                player.velocity[1] = -3.2
            else:
                player.velocity[1] = -2.5
                player.velocity[0] = 2.5 * -(player.movement["right"] - player.movement["left"])
                player.app.particleSystem.addParticle([8, 8], [
                    player.location[0] + (player.size[0] / 2) - 4,
                    player.location[1] + (player.size[1] / 2)
                ], 8, "slide-particle", dynamic=0, velocity=[player.movement["right"] - player.movement["left"], 0], loop=0)
            player.setState("jumps", player.getState("jumps")-1)
    
    def dash():
        if player.getState("grounded") and not player.getState("sliding"):
            if player.getState("flip-x"):
                player.velocity[0] = -4
            else: player.velocity[0] = 4
            player.setState("sliding", 1)

    player.jump = jump
    player.dash = dash
    player.addAnimation("wall-slide", "player-wall-slide", 0, 1, frameOffset=[0, 2])
    player.addAnimation("slide", "player-dash", 0, 1, frameOffset=[3, 3])
    player.addAnimation("jump", "player-jump", 0, 1, frameOffset=[1, 1])
    player.addAnimation("run", "player-run", 1, 8, frameOffset=[3, 2])
    player.addAnimation("idle", "player-idle", 1, 21)
    player.setAction("idle")

    # player equipment
    player.equipment = {
        "hat": None,
    }

    def equip(slot:str, item):
        if slot in player.equipment:
            player.equipment[slot] = item
    
    def unequip(slot:str):
        if slot in player.equipment:
            player.equipment[slot] = None
    
    def getEquip(slot:str):
        if slot in player.equipment:
            return player.equipment[slot]
    
    player.equip = equip
    player.unequip = unequip
    player.getEquip = getEquip

    # player stats
    player.stats = {
        "spec": 80,
        "reforge": 0,
        "health": 100,
    }
    
    player.statCaps = {
        "spec": 80,
        "reforge": 0,
        "health": 100,
    }

def managePlayerInput(player:blackforge.object.GameObject) -> None:
    if player.app.events.keyPressed(blackforge.input.Keyboard.A) and not player.getState("sliding"):
        player.move("left")
    else: player.stop("left")
    
    if player.app.events.keyPressed(blackforge.input.Keyboard.D) and not player.getState("sliding"):
        player.move("right")
    else: player.stop("right")
    
    if player.app.events.keyTriggered(blackforge.input.Keyboard.LShift):
        player.dash()
    
    if player.app.events.keyTriggered(blackforge.input.Keyboard.Space):
        player.setState("sliding", 0)
        player.jump()
    
    if player.app.events.keyTriggered(blackforge.input.Keyboard.F1):
        player.setState("rect", not player.getState("rect"))

def managePlayerState(player:blackforge.object.GameObject) -> None:
    if (player.movement["left"] or player.movement["right"] or player.velocity[0] != 0) and not player.getState("sliding"):
            player.setAction("run")
    elif (player.movement["left"] or player.movement["right"] or player.velocity[0] != 0) and player.getState("sliding"):
        player.setAction("slide")
        if player.getState("grounded"):
            player.app.particleSystem.addParticle([8, 8], [
                player.location[0] + (player.size[0] / 2) - 4,
                player.location[1] + (player.size[1] / 2)
            ], 2, "slide-particle", dynamic=0, velocity=[player.movement["right"] - player.movement["left"], 0], loop=0)
    else:
        player.setAction("idle")
        player.setState("sliding", 0)
    
    if not player.getState("grounded"):
        player.setAction("jump")

    if player.getState("air-time") > 15 and (player.collisions["left"] or player.collisions["right"]):
        player.velocity[1] = min(player.velocity[1], 0.5)
        player.setAction("wall-slide")
        player.setState("jumps", 1)
        
    if player.collisions["down"]:
        player.setState("jumps", 1)

    if player.location[1] > player.app.camera.bounds[1] + 100: spawnPlayer(player)

