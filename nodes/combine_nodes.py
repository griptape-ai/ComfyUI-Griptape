class MergeTexts:
    """
    Merge Texts
    """

    DESCRIPTION = "Merge multiple strings into one."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": (
                    "STRING",
                    {"multiline": False, "default": "", "forceInput": True},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(
        self,
        **kwargs,
    ):
        merged_text = ""

        inputs = [value for value in kwargs.values()]

        for input in inputs:
            merged_text += "\n\n" + input
        return (merged_text,)


class gtUIMergeInputs:
    """
    Takes any inputs and merges them.. like strings, but just any inputs instead.
    """

    DESCRIPTION = "Merge multiple inputs into one."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": ("*",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(
        self,
        **kwargs,
    ):
        concatenated_value = ""
        inputs = [value for value in kwargs.values()]
        for input in inputs:
            concatenated_value += "\n\n" + str(input)
        return (concatenated_value,)


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
                "rules_1": ("RULESET",),
            }
        }

    RETURN_TYPES = ("RULESET",)
    RETURN_NAMES = ("RULESET",)
    FUNCTION = "create"

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


class ToolList:
    """
    Griptape Tool List
    """

    DESCRIPTION = "Combine tools to give an agent a more complex set of tools."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "tool_1": ("TOOL_LIST",),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL_LIST",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Tools"

    def create(self, **kwargs):
        tool_list = []

        tools = [value for value in kwargs.values()]
        if len(tools) > 0:
            for tool in tools:
                tool_list.append(tool[0])
        return (tool_list,)
