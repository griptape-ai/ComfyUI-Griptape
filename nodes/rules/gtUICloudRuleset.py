from typing import Any, Tuple

from griptape.drivers.ruleset.griptape_cloud import GriptapeCloudRulesetDriver
from griptape.rules import Ruleset


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class gtUICloudRuleset:
    DESCRIPTION = "Use a Griptape Cloud Ruleset"
    CATEGORY = "Griptape/Agent Rules"
    RETURN_TYPES = ("RULESET",)
    RETURN_NAMES = ("RULES",)

    FUNCTION = "run"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "ruleset_id": (
                    "STRING",
                    {
                        "placeholder": "xxxx-xxxx-xxxx-xxxx",
                        "default": "",
                        "tooltip": "The id of your ruleset to run.",
                    },
                ),
            },
        }

    def run(self, **kwargs) -> Tuple[Any, ...]:
        ruleset_id = kwargs.get("ruleset_id", "")
        if ruleset_id == "":
            print("No ruleset id provided")
            return (None,)

        ruleset = [
            Ruleset(ruleset_driver=GriptapeCloudRulesetDriver(ruleset_id=ruleset_id))
        ]

        return (ruleset,)
