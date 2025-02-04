import json

import os
import openai

from library.prompt_wrapper import *


def test_openai_api(api_key: str):
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Hello World"}
            ],
            max_tokens=5
        )
        print("WORKED")
    except Exception as e:
        print("An error occurred")
        raise e


def query_openai_api(api_key: str, wrapped_prompt: PromptWrapper, model: Model = Model.GPT4O) -> Response:
    openai.api_key = api_key

    messages = []
    responses = []

    try:
        safeguard = 5  # We never have more than 5 prompts
        count = 0
        for prompt in wrapped_prompt.prompts:
            if count >= safeguard:
                raise Exception("Too many prompts")
            count += 1

            messages.append({"role": "system", "content": prompt})
            kwargs = {}
            if not wrapped_prompt.output_structure.first_unstructred_output or count == 2:
                response_format = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "response",
                        "strict": True,
                        "schema": wrapped_prompt.output_structure.get_json_schema()
                    }
                }
                kwargs["response_format"] = response_format

            response = openai.chat.completions.create(
                model=model.value,
                messages=messages,
                n=1,
                **kwargs
            )

            if len(response.choices) == 0:
                raise Exception("No response from OpenAI API")
            if len(response.choices) > 1:
                raise Exception("More than one response from OpenAI API")
            if response.choices[0].message.role != "assistant":
                raise Exception("Response from OpenAI API is not from the assistant")
            if response.choices[0].message.content == "":
                raise Exception("Response from OpenAI API is empty")
            if response.choices[0].finish_reason != "stop":
                raise Exception("Response finish_reason is not 'stop'")

            response_str = response.choices[0].message.content
            messages.append(
                {"role": "assistant", "content": response_str})
            responses.append(response_str)

        parsed_response = json.loads(responses[-1])
        if not parsed_response.get("decision"):
            raise Exception("No decision in response")

        decision = DecisionOption(parsed_response["decision"])

        return Response(
            wrapped_prompt=wrapped_prompt,
            decision=decision,
            llm_identifier=model,
            unparsed_messages=[GPTMessage.from_dict(item) for item in messages],
            parsed_response=parsed_response,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


if __name__ == '__main__':
    api_key = os.getenv("ETHICS_OPENAI_API_KEY")
    response = test_openai_api(api_key)
