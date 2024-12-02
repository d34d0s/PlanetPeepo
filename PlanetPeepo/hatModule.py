import blackforge

class HatSpec:
    def __init__(self, name:str, max:int, description:str="this is a special description.") -> None:
        self.name:str=name
        self.level:int=1
        self.description:str=description
        self.max:int=max
        self.resource:int=max

class Hat(blackforge.entity.StaticEntity):
    def __init__(
            self,
            player,
            size: list[int],
            location: list[float],
            hudOffset: list[float]=[0, 0],
            assetID:str="hat"
        ) -> None:
        super().__init__(0, player.app, size, location, assetID)
        self.player:blackforge.object.GameObject=player
        self.name:str="hat"
        self.level:int=1
        self.spec:HatSpec=None
        self.description:str="this is a hat description."
        self.state = {
            "flip-x": 0,
        }
        self.hudOffset:list[int]=hudOffset
        self.actionOffsets = {}
        self._getActionOffsets()
    
    def getState(self, key:str): return self.state[key]
    def setState(self, key:str, value):
        try:
            self.state[key] = value
        except (KeyError) as err: return None

    def _getActionOffsets(self) -> None:
        for action in self.player.actions:
            self.actionOffsets[action] = None

    def getActionOffset(self, action:str, direction:bool|int) -> None:
        try:
            return self.actionOffsets[action][bool(direction)]
        except (KeyError) as err: return None

    def setActionOffset(self, action:str, left:list[int], right:list[int]) -> None:
        try:
            if self.actionOffsets[action] is None:
                self.actionOffsets[action] = {0:[], 1:[]}
            self.actionOffsets[action][0] = right
            self.actionOffsets[action][1] = left
        except (KeyError) as err:
            self.actionOffsets[action] = {0:[], 1:[]}
            self.actionOffsets[action][0] = right
            self.actionOffsets[action][1] = left

    def getName(self) -> str: return self.name
    def getLevel(self) -> int: return self.level
    def getReForge(self) -> HatSpec: return self.spec
    def getDescription(self) -> str: return self.description
    def getInfo(self) -> dict:
        return {
            "name": self.name,
            "level": self.level,
            "special": self.spec,
            "desc": self.description,
        }
    
    def levelUp(self) -> bool: return False

    def render(self, showRect: bool = 0) -> None:
        image = self.app.assets.getImage(self.assetID)
        image = blackforge.asset.flipSurface(
            x=self.state.get("flip-x", False),
            y=False,
            surface=image
        )
        renderLocation = [
            self.location[0] - self.app.camera.scroll[0],
            self.location[1] - self.app.camera.scroll[1]
        ]

        self.app.window.blit(image, renderLocation)

    def renderHUD(self, hud) -> None:
        image = self.app.assets.getImage(self.assetID)
        self.app.window.display.blit(
            blackforge.asset.scaleSurface(image, [image.get_width()* hud.scale[0], image.get_height() * hud.scale[1]]),
            [
                (hud.location[0] - self.size[0]) - self.hudOffset[0],
                (hud.location[1] - (self.size[1] * (hud.scale[1] / 2))) - self.hudOffset[1]
            ]
        )

    def update(self) -> None:
        actionOffset = [0, 0]
        self.setState("flip-x", self.player.getState("flip-x"))
        try:
            actionOffset = self.actionOffsets[self.player.action].get(self.getState("flip-x"), False)
        except (AttributeError, KeyError) as err: pass
        self.location = [
            self.player.location[0] - actionOffset[0],
            self.player.location[1] - actionOffset[1]
        ]

# --------- HAT CLASSES ---------
class Smitty(Hat):
    def __init__(self, player, location: list[float]) -> None:
        super().__init__(player, [11, 10], location, hudOffset=[4, -6], assetID="smitty")
        self.name = "smitty"
        self.level = 1
        self.spec = None
        self.description = "love me not"

        self.setActionOffset("run", left=[2, 8], right=[3, 8])
        self.setActionOffset("idle", left=[2, 6], right=[1, 6])
        self.setActionOffset("jump", left=[0, 7], right=[3, 7])
        self.setActionOffset("slide", left=[-1, 3], right=[4, 3])
        self.setActionOffset("wall-slide", left=[3, 8], right=[0, 8])

    def update(self) -> None:
        super().update()
        if self.player.action == "wall-slide":
            self.setState("flip-x", not self.player.getState("flip-x"))

