from enum import Enum
from typing import Optional

from .dilemma_wrapper import DilemmaWrapper, InvertableDilemmaWrapper, get_dilemma


class DecisionOption(Enum):
    YES = "YES"
    NO = "NO"
    UNDECIDED = "UNDECIDED"


class OutputComponentType(Enum):
    DECISION = "DECISION"
    NORMATIVE_ETHICAL_THEORY_EXPLANATION = "NORMATIVE_ETHICAL_THEORY_EXPLANATION"
    DECISION_REASON = "DECISION_REASON"


class OutputStructure:
    sorted_output_components: list[OutputComponentType]
    sorted_decision_options: list[DecisionOption]
    first_unstructured_output: bool

    def __init__(self, sorted_output_components: list[OutputComponentType], sorted_decision_options: list[DecisionOption], first_unstructured_output: bool):
        self.sorted_output_components = sorted_output_components
        self.sorted_decision_options = sorted_decision_options
        self.first_unstructured_output = first_unstructured_output

    @property
    def default_order_output_components(self) -> list[OutputComponentType]:
        """Returns the contained decision options in the default order"""
        return [component for component in OutputComponentType if component in self.sorted_output_components]

    @property
    def has_unstructured_decision_text(self) -> bool:
        return (
            OutputComponentType.DECISION_REASON in self.sorted_output_components
            or self.first_unstructured_output
        )

    @property
    def has_unstructured_decision_text_before_decision(self) -> bool:
        if self.first_unstructured_output:
            return True

        sorted_output_options = self.sorted_output_components
        if OutputComponentType.DECISION_REASON in sorted_output_options:
            decision_reason_index = sorted_output_options.index(OutputComponentType.DECISION_REASON)
            decision_index = sorted_output_options.index(OutputComponentType.DECISION)
            return decision_reason_index < decision_index

        return False

    def get_decision_option_index(self, decision_option: DecisionOption) -> int:
        return self.sorted_decision_options.index(decision_option)

    def get_has_output_component(self, output_component: OutputComponentType) -> bool:
        return output_component in self.sorted_output_components

    def get_json_schema(self) -> object:
        """
        Get the OpenAI structured output schema for the current OutputStructure object.
        """

        sorted_output_components_schema = {}
        for output_component in self.sorted_output_components:
            if output_component == OutputComponentType.DECISION:
                output_component_schema = {
                    "type": "string",
                    "description": "The decision options",
                    "enum": [item.value for item in self.sorted_decision_options]
                }

            else:
                output_component_schema = {
                    "type": "string",
                    "description": f"The {output_component.value.lower()} content"
                }
            sorted_output_components_schema[output_component.value.lower(
            )] = output_component_schema

        json_schema = {
            "type": "object",
            "properties": sorted_output_components_schema,
            "additionalProperties": False,
            "required": [component.value.lower() for component in self.sorted_output_components],
        }
        return json_schema

    def to_dict(self):
        return {
            "sorted_output_components": [component.value for component in self.sorted_output_components],
            "sorted_decision_options": [option.value for option in self.sorted_decision_options],
            "first_unstructured_output": self.first_unstructured_output,
        }

    def to_analysis_dict(self):
        res = self.to_dict()
        res.update({
            # New fields
            "has_unstructured_decision_text": self.has_unstructured_decision_text,
            "has_unstructured_decision_text_before_decision": self.has_unstructured_decision_text_before_decision,
            "default_order_output_components": [component.value for component in self.default_order_output_components],
        })

        for component in OutputComponentType:
            res[f"has_{component.value.lower()}"] = self.get_has_output_component(component)
        for option in DecisionOption:
            res[f"decision_option_index_{option.value.lower()}"] = self.get_decision_option_index(option)
        return res

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an OutputStructure object from a dictionary.
        """
        return cls(
            sorted_output_components=[OutputComponentType(
                component) for component in data["sorted_output_components"]],
            sorted_decision_options=[DecisionOption(
                option) for option in data["sorted_decision_options"]],
            first_unstructured_output=data["first_unstructured_output"],
        )


class PromptWrapper:
    prompts: list[str]
    dilemma_identifier: str
    ethical_framework_identifier: str
    base_prompt_identifier: str
    prompt_has_output_structure_description: bool
    prompt_has_output_structure_json_schema: bool
    output_structure: OutputStructure
    version: str

    def add_id(self, _id: str):
        self._id = _id

    def __init__(
        self,
        prompts: list[str],
        dilemma_identifier: str,
        ethical_framework_identifier: str,
        base_prompt_identifier: str,
        prompt_has_output_structure_description: bool,
        prompt_has_output_structure_json_schema: bool,
        output_structure: OutputStructure,
        version: str,
    ):
        self._id = None
        self.prompts = prompts
        self.dilemma_identifier = dilemma_identifier
        self.ethical_framework_identifier = ethical_framework_identifier
        self.base_prompt_identifier = base_prompt_identifier
        self.prompt_has_output_structure_description = prompt_has_output_structure_description
        self.prompt_has_output_structure_json_schema = prompt_has_output_structure_json_schema
        self.output_structure = output_structure
        self.version = version

    @property
    def dilemma(self) -> DilemmaWrapper:
        return get_dilemma(self.dilemma_identifier)

    def __str__(self):
        res = "--------PromptWrapper--------"
        for prompt in self.prompts:
            res += f"\nprompt:\n{prompt}"
        res += "-----------------------------"
        return res

    def to_dict(self):
        if self._id is None:
            raise Exception("PromptWrapper ID is None")
        return {
            "_id": self._id,
            "prompts": self.prompts,
            "dilemma_identifier": self.dilemma_identifier,
            "ethical_framework_identifier": self.ethical_framework_identifier,
            "base_prompt_identifier": self.base_prompt_identifier,
            "prompt_has_output_structure_description": self.prompt_has_output_structure_description,
            "prompt_has_output_structure_json_schema": self.prompt_has_output_structure_json_schema,
            "output_structure": self.output_structure.to_dict(),
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a PromptWrapper object from a dictionary.
        """
        res = cls(
            prompts=data["prompts"],
            dilemma_identifier=data["dilemma_identifier"],
            ethical_framework_identifier=data.get("ethical_framework_identifier", data.get("framework_identifier")),
            base_prompt_identifier=data["base_prompt_identifier"],
            prompt_has_output_structure_description=data.get("prompt_has_output_structure_description", True),
            prompt_has_output_structure_json_schema=data.get("prompt_has_output_structure_json_schema", True),
            output_structure=OutputStructure.from_dict(
                data["output_structure"]),
            version=data["version"],
        )

        # TODO remove this. version1.5 called id "id" and now it is called "_id"
        _id = data.get("_id")
        if not _id:
            _id = data.get("id")
        res.add_id(_id)

        return res

    def to_analysis_dict(self):
        res = self.to_dict()
        res.update({
            # Overwrite fields
            "output_structure": self.output_structure.to_analysis_dict(),
            # New fields
            "dilemma": self.dilemma.to_dict(),
        })
        return res


class LlmName(Enum):
    GPT4O = "gpt-4o"


class LlmMessageRole(Enum):
    SYSTEM = "system"
    ASSISSANT = "assistant"


class LlmMessage:
    def __init__(self, role: LlmMessageRole, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role.value,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            role=LlmMessageRole(data["role"]),
            content=data["content"],
        )


class Response:
    wrapped_prompt: PromptWrapper
    decision: DecisionOption
    llm_identifier: LlmName
    unparsed_messages: list[LlmMessage]
    parsed_response: dict
    # Optional as this was only introduced in v1.5
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]

    def __init__(
        self,
        wrapped_prompt: PromptWrapper,
        decision: DecisionOption,
        llm_identifier: LlmName,
        unparsed_messages: list[LlmMessage],
        parsed_response: dict,
        prompt_tokens: Optional[int],
        completion_tokens: Optional[int]
    ):
        self.wrapped_prompt = wrapped_prompt
        self.decision = decision
        self.llm_identifier = llm_identifier
        self.unparsed_messages = unparsed_messages
        self.parsed_response = parsed_response
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def to_dict(self):
        return {
            "wrapped_prompt": self.wrapped_prompt.to_dict(),
            "decision": self.decision.value,
            "llm_identifier": self.llm_identifier.value,
            "unparsed_messages": [message.to_dict() for message in self.unparsed_messages],
            "parsed_response": self.parsed_response,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            wrapped_prompt=PromptWrapper.from_dict(data["wrapped_prompt"]),
            decision=DecisionOption(data["decision"]),
            llm_identifier=LlmName(data["llm_identifier"]),
            unparsed_messages=[LlmMessage.from_dict(item) for item in data["unparsed_messages"]],
            parsed_response=data.get("parsed_response"),
            prompt_tokens=data.get("prompt_tokens"),
            completion_tokens=data.get("completion_tokens"),
        )

    def to_analysis_dict(self):
        """Extends the to_dict method to include additional fields that are useful for analysis"""

        res = self.to_dict()
        analysis_fields = {
            # Overwrite fields
            "wrapped_prompt": self.wrapped_prompt.to_analysis_dict(),
            # New fields
            "normalized_decision": self.normalized_decision.value,
        }
        res.update(analysis_fields)
        return res

    def get_messages_by_role(self, role: LlmMessageRole) -> list[LlmMessage]:
        return [message for message in self.unparsed_messages if message.role == role]

    @property
    def normalized_decision(self) -> DecisionOption:
        """InvertableDilemmaWrapper allows for the decision to be inverted. This property returns the normalized decision."""

        if not isinstance(self.wrapped_prompt.dilemma, InvertableDilemmaWrapper):
            return self.decision

        assert self.decision in [
            option for option in DecisionOption], f"Invalid decision value: {self.decision}. \n Check if restarting the jupyter kernel helps"

        if self.decision == DecisionOption.UNDECIDED:
            return DecisionOption.UNDECIDED

        if self.wrapped_prompt.dilemma.action_is_inverted:
            if self.decision == DecisionOption.YES:
                return DecisionOption.NO
            elif self.decision == DecisionOption.NO:
                return DecisionOption.YES

        return self.decision
