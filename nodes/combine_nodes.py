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
        # Join strings by newline
        input_1 = kwargs.get("input_1", "")
        del kwargs["input_1"]
        inputs = [value for value in kwargs.values()]

        if len(inputs) == 0:
            return (input_1,)
        else:
            for input in inputs:
                input_1 += "\n\n" + input
            return (input_1,)


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
        # Join strings by newline
        input_1 = kwargs.get("input_1", "")
        del kwargs["input_1"]
        inputs = [value for value in kwargs.values()]
        concatenated_value = str(input_1)
        if len(inputs) == 0:
            return (concatenated_value,)
        else:
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
                "rules_2": ("RULESET",),
                "rules_3": ("RULESET",),
                "rules_4": ("RULESET",),
                "rules_5": ("RULESET",),
                "rules_6": ("RULESET",),
            }
        }

    RETURN_TYPES = ("RULESET",)
    RETURN_NAMES = ("RULESET",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Rules"

    def create(
        self,
        rules_1=None,
        rules_2=None,
        rules_3=None,
        rules_4=None,
        rules_5=None,
        rules_6=None,
    ):
        rule_list = [
            rule[0]
            for rule in [
                rules_1,
                rules_2,
                rules_3,
                rules_4,
                rules_5,
                rules_6,
            ]
            if rule is not None
        ]
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
                "tool_2": ("TOOL_LIST",),
                "tool_3": ("TOOL_LIST",),
                "tool_4": ("TOOL_LIST",),
                "tool_5": ("TOOL_LIST",),
                "tool_6": ("TOOL_LIST",),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL_LIST",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Tools"

    def create(
        self,
        tool_1=None,
        tool_2=None,
        tool_3=None,
        tool_4=None,
        tool_5=None,
        tool_6=None,
    ):
        tool_list = [
            tool[0]
            for tool in [
                tool_1,
                tool_2,
                tool_3,
                tool_4,
                tool_5,
                tool_6,
            ]
            if tool is not None
        ]
        return (tool_list,)
