import blackforge
import blackforge.utils

import playerModule

class HatGame(blackforge.app.Application):
    def __init__(self):
        super().__init__("Hat Game", [800, 600])
        self.config()

    def getMap(self) -> None:
        return self.maps.get(self.map, None)
    
    def getMapInfo(self) -> None:
        return self.getMap().info

    def config(self) -> None:
        self.loadAssets()
        self.loadMapData()
        self.loadGameObjects()
        self.configureGameObjects()
        
        self.window.color = [39, 137, 205]
        self.camera.setBounds([1000, 432])
        self.camera.setTarget(self.player)
        self.particleSystem = blackforge.gfx.ParticleSystem(self, [0, 0], 10000)

    def loadAssets(self) -> None:
        self.assets.loadImage("enemy", "assets/images/entities/enemy.png")
        self.assets.loadImage("player", "assets/images/entities/player.png")
        self.assets.loadImageDir("player-jump", "assets/images/entities/player/jump")
        self.assets.loadImageDir("player-dash", "assets/images/entities/player/slide")
        self.assets.loadImageDir("clouds", "assets/images/clouds", colorKey=[0, 0, 0])
        self.assets.loadImageDir("player-wall-slide", "assets/images/entities/player/wall_slide")
        self.assets.loadImageSheet("player-run", "assets/images/entities/player/run/run-sheet.png", [12, 17])
        self.assets.loadImageSheet("player-idle", "assets/images/entities/player/idle/idle-sheet.png", [8, 15])
        self.assets.loadImageSheet("slide-particle", "assets/images/particles/slide.png", [8, 8])

        self.tilesets = {
            "sanctuary": "D:/dev/python/HatGame/assets/images/tiles/PB-sanctuary.png"
        }
        for ts in self.tilesets:
            self.assets.loadImageSheet(self.tilesets[ts], self.tilesets[ts], [16, 16])

    def loadMapData(self) -> None:
        self.map = "sanctuary"
        self.maps = {
            "sanctuary": None
        }
        
        for map in self.maps:
            self.newTilemap(map, f"assets/map-data/{map}/{map}.wf2")
            self.maps[map] = self.getTilemap(map)
        
        self.skybox = blackforge.world.SkyBox(self, self.getTilemap(self.map), [55, 20], 100)

    def loadGameObjects(self) -> None:
        self.player = blackforge.object.GameObject(self, [8, 15], [100, 100])
        self.enemy = blackforge.object.GameObject(self, [8, 15], [146, 100], assetID="enemy")

    def configureGameObjects(self) -> None:
        playerModule.configurePlayer(self.player)
        playerModule.spawnPlayer(self.player)
        self.enemy.location = [*self.player.location]

    def manageMapInteraction(self) -> None:
        worldLocation = self.getMap().getMouseMapLocation()
        get = self.getMap().getTile(worldLocation, remove=self.events.mousePressed(blackforge.input.Mouse.LeftClick))
        if get: blackforge.asset.drawRect(self.window.canvas, get.size, [
            (get.location[0] * get.size[0]) - self.camera.scroll[0],
            (get.location[1] * get.size[1]) - self.camera.scroll[1],
        ], color=[0, 0, 255])

    def preProcess(self) -> None:
        self.clock.tick()
        self.window.clear()
        self.events.process()
        self.camera.centerTarget()
        # self.camera.setBox([*self.player.location, *self.player.size])
        # self.camera.boxMode()

    def process(self) -> None:
        if self.events.keyPressed(blackforge.input.Keyboard.Escape):
            self.events.quit = 1

        if self.events.mouseWheelUp:
            self.window.modZoom(.1)
        
        if self.events.mouseWheelDown:
            self.window.modZoom(-.1)

        if self.events.keyTriggered(blackforge.input.Keyboard.F2):
            self.camera.setTarget(self.player)
        if self.events.keyTriggered(blackforge.input.Keyboard.F3):
            self.camera.setTarget(self.enemy)

        playerModule.managePlayerInput(self.player)

        self.skybox.update()
        self.player.update(self.getMap())

        self.skybox.render()
        self.particleSystem.update(self.getMap())
        self.getMap().render(showRects=self.player.getState("rect"))
        
        self.player.render(showRect=self.player.getState("rect"))
        
        self.enemy.render(showRect=self.player.getState("rect"))
        blackforge.AI.roamStopWL(
            tilemap=self.getMap(),
            object=self.enemy,
            minDist=30, maxDist=60,
            showChecks=self.player.getState("rect")
        )

        self.manageMapInteraction()
        self.particleSystem.render(showRects=self.player.getState("rect"))

    def postProcess(self) -> None:
        self.clock.rest()
        self.window.render()
        playerModule.managePlayerState(self.player)

HatGame().run()