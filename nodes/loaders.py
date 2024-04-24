from griptape.loaders import PdfLoader
import urllib.request


class gtUIWebPdfLoader:
    """
    The Griptape Web PDF Loader
    """

    def __init__(self):
        self.node_class = "gt-tool"
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
            }
        }

    RETURN_TYPES = ("TEXT_ARTIFACT",)
    RETURN_NAMES = ("output",)

    FUNCTION = "create"

    CATEGORY = "Griptape"

    def create(self, url):
        urllib.request.urlretrieve(url, "temp.pdf")
        loader = PdfLoader().load("temp.pdf")
        return (loader,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {"DateTime": DateTime}

# A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {"DateTime": "Tool: DateTime"}
