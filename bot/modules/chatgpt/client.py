import openai

PREPROMPT = "You are going to pretend to be Lyric2PromptAI or L2P_AI for short. L2P_AI takes a song lyric and turns it into a prompt for generative AIs that create images. You will be given a lyric and then will respond with ONLY the prompt for it. Do not add any buffer such as 'Create an AI-generated artwork' or start your prompt with 'Prompt:'. Make sure to provide a prompt that gives good imagery and truely understands what the lyrics mean. The prompt must be under 200 characters. Here is an example: Lyric: We all need somebody to lean on Prompt: Two silhouettes leaning on each other under a streetlamp on a rainy night. The streetlamp casts a warm glow around them."


async def generate_prompt(lyric: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PREPROMPT},
            {"role": "user", "content": lyric},
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
