class RulesList:
    """
    Griptape Lists of Rules
    """

    DESCRIPTION = "Combine rules to give an agent a more complex set of rules."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "rules_1": (
                    "RULESET",
                    {
                        "tooltip": "A rule to add to the list. Connect an input to dynamically create more rules."
                    },
                ),
            }
        }

    RETURN_TYPES = ("RULESET",)
    RETURN_NAMES = ("RULESET",)
    FUNCTION = "create"
    # OUTPUT_IS_LIST = (True,)
    CATEGORY = "Griptape/Agent Rules"

    def create(self, **kwargs):
        # Clear the rule_list
        rule_list = []

        rules = [value for value in kwargs.values()]
        if len(rules) > 0:
            for rule in rules:
                rule_list.append(rule[0])
        # rule_list = [rule[0] for rule in [kwargs.values()] if rule is not None]
        return (rule_list,)
