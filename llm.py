import openai


async def llm(
    system_prompt: str, user_prompt: str, fast: bool = True, tokens=2048
) -> str:
    if not fast:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=tokens,
            temperature=0.0,
        )
        return response.choices[0].message["content"]
    else:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": system_prompt + "\n" + user_prompt},
            ],
            max_tokens=tokens,
            temperature=0.7,
        )
        return response.choices[0].message["content"]
