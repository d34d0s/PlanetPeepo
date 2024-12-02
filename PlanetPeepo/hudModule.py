import blackforge

class HUD:
    def __init__(self, app, scale:list[int]=[6, 6]) -> None:
        self.scale = scale
        self.app:blackforge.app.Application = app
        self.app.assets.setImage("HUD", blackforge.asset.scaleSurface(self.app.assets.getImage("HUD"), [33*self.scale[0], 8*self.scale[1]]))
        
        self.image = self.app.assets.getImage("HUD")
        self.location = [16, self.app.window.size[1] - self.image.get_height()]
        
        self.reforgeMax:int=100
        self.specMax:int=80
        self.healthMax:int=100

        self.colors:dict = {
            "reforge": [[156, 139, 219], [252, 228, 255]],
            "spec": [[43, 78, 149], [115, 239, 232]],
            "health": [[97, 39, 33], [255, 0, 0]],
        }

        self.reforgeBar = blackforge.asset.createRect(
            size=[24 * self.scale[0], 1 * self.scale[1]],
            location=[
                self.location[0] + 8 * self.scale[0],
                self.location[1] + 2 * self.scale[1]
            ]
        )

        self.specBar = blackforge.asset.createRect(
            size=[24 * self.scale[0], 1 * self.scale[1]],
            location=[
                self.location[0] + 8 * self.scale[0],
                self.location[1] + 4 * self.scale[1]
            ]
        )

        self.healthBar = blackforge.asset.createRect(
            size=[24 * self.scale[0], 1 * self.scale[1]],
            location=[
                self.location[0] + 8 * self.scale[0],
                self.location[1] + 6 * self.scale[1]
            ]
        )
    
    def manageReforge(self) -> None:
        blackforge.asset.drawRect(
            self.app.window.display,
            self.reforgeBar.size,
            self.reforgeBar.topleft,
            self.colors["reforge"][0],
            width=0
        )
        
        if self.app.player.stats["reforge"] > 0:
            blackforge.asset.drawRect(
                self.app.window.display,
                [
                    self.reforgeBar.size[0] * (self.app.player.stats["reforge"] / self.app.player.statCaps["reforge"]) ,
                    self.reforgeBar.size[1]
                ],
                self.reforgeBar.topleft,
                self.colors["reforge"][1],
                width=0
            )
        
    def manageSpec(self) -> None:
        blackforge.asset.drawRect(
            self.app.window.display,
            self.specBar.size,
            self.specBar.topleft,
            self.colors["spec"][0],
            width=0
        )
        if self.app.player.stats["spec"] > 0:
            blackforge.asset.drawRect(
                self.app.window.display,
                [
                    self.specBar.size[0] * (self.app.player.stats["spec"] / self.app.player.statCaps["spec"]) ,
                    self.specBar.size[1]
                ],
                self.specBar.topleft,
                self.colors["spec"][1],
                width=0
            )

    def manageHealth(self) -> None:
        blackforge.asset.drawRect(
            self.app.window.display,
            self.healthBar.size,
            self.healthBar.topleft,
            self.colors["health"][0],
            width=0
        )
        if self.app.player.stats["health"] > 0:
            blackforge.asset.drawRect(
                self.app.window.display,
                [
                    self.healthBar.size[0] * (self.app.player.stats["health"] / self.app.player.statCaps["health"]) ,
                    self.healthBar.size[1]
                ],
                self.healthBar.topleft,
                self.colors["health"][1],
                width=0
            )

    def render(self):
        self.app.window.display.blit(self.image, self.location)
        self.manageReforge()
        self.manageSpec()
        self.manageHealth()

