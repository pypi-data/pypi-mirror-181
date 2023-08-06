import shutil
import tempfile
import traceback

from matplotlib import pyplot as plt
from pylatex import Figure, NoEscape, SubFigure

import pyfeyn2
from pyfeyn2.render.latex.latex import LatexRender


class AllRender(LatexRender):
    """Render all diagrams to PDF."""

    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["varwidth"]
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )

    def render(
        self,
        file=None,
        show=True,
        subfigure=False,
        resolution=None,
        width=None,
        height=None,
    ):
        fd = self.fd
        self.dirpath = tempfile.mkdtemp()
        dirpath = self.dirpath

        dynarg = {}
        if show and not subfigure:
            dynarg["show"] = True
            if resolution is not None:
                dynarg["resolution"] = resolution
            if width is not None:
                dynarg["width"] = width
            if height is not None:
                dynarg["height"] = height
        else:
            dynarg = {"show": False}

        with self.create(Figure(position="h!")):
            for i, name in enumerate(pyfeyn2.renders):
                render = pyfeyn2.renders[name]
                if name == "all":
                    continue
                try:
                    if not subfigure:
                        print(name + ":")
                    render(fd).render(dirpath + "/" + name + ".pdf", **dynarg)
                    plt.close()
                except Exception:
                    print(name + " failed:")
                    print(traceback.format_exc())
                with self.create(SubFigure(position="b")) as subfig:
                    subfig.add_image(
                        dirpath + "/" + name + ".pdf",
                        width=NoEscape("0.49\\textwidth"),
                    )
                    subfig.add_caption(name)
                if i % 2 == 1:
                    self.append(NoEscape(r"\\"))

        if subfigure:
            super().render(file, show, resolution, width, height)
        shutil.rmtree(self.dirpath)

    @staticmethod
    def valid_style( style: str) -> bool:
        return True in [r.valid_style(style) for r in pyfeyn2.renders.values()]

    @staticmethod
    def valid_attribute( attr: str) -> bool:
        return True in [r.valid_attribute(attr) for r in pyfeyn2.renders.values()]

    @staticmethod
    def valid_type( typ: str) -> bool:
        return True in [r.valid_type(typ) for r in pyfeyn2.renders.values()]
