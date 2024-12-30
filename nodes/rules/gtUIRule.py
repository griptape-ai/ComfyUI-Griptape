from griptape.rules import Rule, Ruleset


class gtUIRule:
    def __init__(self):
        pass

    DESCRIPTION = "Create a set of rules for an agent"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "My rules"}),
                "rules": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "Always be kind and friendly\nKeep resposnses brief, but not curt",
                    },
                ),
            },
        }

    RETURN_TYPES = ("RULESET", "STRING")
    RETURN_NAMES = ("RULES", "NAME")
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Rules"

    def create(
        self,
        name,
        rules,
    ):
        rules = rules.split("\n")
        my_rules = []
        for rule in rules:
            my_rules.append(Rule(rule))

        ruleset = [Ruleset(name=name, rules=my_rules)]

        return (ruleset, name)
