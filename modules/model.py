class Model:

    class Material:

        def __init__(self, **kwargs) -> None:
            self.diffuse = kwargs["diffuse"] # 漫反射颜色
            self.specular = kwargs["specular"] # 高光反射颜色
            