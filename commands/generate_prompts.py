import os

from library.prompt_factory import get_all_possible_prompts, base_prompts
from library.prompt_wrapper import OutputComponentType, PromptWrapper
from library.prompts_json import generate_prompt_json
from library.version import VERSION


prompts_folder_path = os.path.join(os.path.dirname(__file__), "../data/prompts")


def generate_promopts_v1_6():
    # Generate wrapped prompts for - v1.6
    prompts = get_all_possible_prompts()
    print(f"There are a total of {len(prompts)} prompts before filtering")
    print(f"Performing filtering...")

    # Selected dilemmas
    prompts: list[PromptWrapper] = [x for x in prompts if x.dilemma.context_identifier in [
        "child_abuse_prevention",
        "public_health",
        "trolley_problem",
        "surveillance",
    ]]

    # We found the base_prompt not to have a significant impact, so we will only use base_prompt_1
    selected_base_prompt = next(iter(base_prompts))
    prompts: list[PromptWrapper] = [x for x in prompts if x.base_prompt_identifier == selected_base_prompt]

    # Our current dilemmas do not include the LLM as a subject, thus the egoism theory might not applicable
    # prompts: list[PromptWrapper] = [x for x in prompts if not x.normative_ethical_theory == "ethical_egoism"]

    # This is a newly added variable we do not yet want to test
    # Previously the prompt always containted the output structure json and description
    prompts: list[PromptWrapper] = [x for x in prompts if x.prompt_has_output_structure_description is True]
    prompts: list[PromptWrapper] = [x for x in prompts if x.prompt_has_output_structure_json_schema is True]

    prompts_file_path = os.path.join(prompts_folder_path, f"wrapped_prompts_v{VERSION}.json")
    generate_prompt_json(prompts, prompts_file_path)



def generate_promopts_v1_7():
    # Generate wrapped prompts for - v1.6
    prompts = get_all_possible_prompts()
    print(f"There are a total of {len(prompts)} prompts before filtering")
    print(f"Performing filtering...")

    # Selected dilemmas
    prompts: list[PromptWrapper] = [x for x in prompts if x.dilemma.context_identifier in [
        "child_abuse_prevention",
        "public_health",
        "trolley_problem",
        "surveillance",
    ]]

    # prompts: list[PromptWrapper] = [x for x in prompts if x.dilemma.identifier in [
    #     # "public_health_1",
    #     # "public_health_2",
    #     # "public_health_3",
    #     # "public_health_4",
    #     # "child_abuse_prevention_3",
    #     # "child_abuse_prevention_4",
    # ]]
    # We found the base_prompt not to have a significant impact, so we will only use base_prompt_1
    selected_base_prompt = next(iter(base_prompts))
    prompts: list[PromptWrapper] = [x for x in prompts if x.dilemma.identifier in ["public_health_1", "public_health_2"] or x.base_prompt_identifier == selected_base_prompt]

    # Our current dilemmas do not include the LLM as a subject, thus the egoism theory might not applicable
    # prompts: list[PromptWrapper] = [x for x in prompts if not x.normative_ethical_theory == "ethical_egoism"]

    # This is a newly added variable we do not yet want to test
    # Previously the prompt always containted the output structure json and description
    prompts: list[PromptWrapper] = [x for x in prompts if x.prompt_has_output_structure_description is True]
    prompts: list[PromptWrapper] = [x for x in prompts if x.prompt_has_output_structure_json_schema is True]

    # prompts: list[PromptWrapper] = [x for x in prompts if not x.output_structure.get_has_output_component(OutputComponentType.NORMATIVE_ETHICAL_THEORY_EXPLANATION) is True]

    prompts_file_path = os.path.join(prompts_folder_path, f"wrapped_prompts_v{VERSION}.json")
    generate_prompt_json(prompts, prompts_file_path)


if __name__ == '__main__':
    if VERSION == "1.6":
        generate_promopts_v1_6()
    elif VERSION == "1.7":
        generate_promopts_v1_7()
    else:
        raise ValueError(f"Version {VERSION} is not supported")
