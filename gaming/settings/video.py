from const import *

class Settings:


    def __init__(self, **kwargs) -> None:
        self.anti_aliasing: Sequence[str | None] = kwargs["anti_aliasing"]
        self.fovy: Sequence[str | None] = kwargs["fovy"]

        self.load()
        pass

    def load(self):
        anti_aliasing: list[str] | list[None] = self.anti_aliasing[0].split(' ') if self.anti_aliasing[0] != None else [None]
        match anti_aliasing[0]:
            case "MSAA":
                # MSAA抗锯齿，第二个选项是采样倍率
                game.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, int(anti_aliasing[1]))
            case "FXAA":
                ...
            case None:
                ...