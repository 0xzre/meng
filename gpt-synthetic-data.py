import json

import os
import time
from openai import OpenAI

client = OpenAI(
    api_key="",
)

def generate_learning_path(topic):

    prompt = f"""Generate detailed multiple learning paths for {topic} in the following JSON format(dont add ```json at the start and end of the prompt, just the JSON object):
    {{
      "output": [
        {{
          "request": "Medium length Human-like request(randomly choose its either: question or statement(wish)) based on the topic",
          "response": [
            {{
              "title": "Title",
              "description": "Description (detailed, helpful, show purpose and meaning) of step 1, just be like a human explaining to another human in relaxed manner",
              "keywords": ["keyword1", "keyword2", "keyword3"]
            }}
          ]
        }}
      ]
    }}
    Provide at least 10 different learning paths (inside the 'output' list) with at 5-10 steps in each learning path (make number of steps is sufficent, optimal become the master of the topic) and more than 5 keywords that can be for searching for materials from google in each step, and each step is actionable by the requester himself, not 'collaboration with other, attend seminar, showcase, engage community,Stay Updated' which require other human, and not confusing thing like 'catchup with latest development'."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates structured learning paths."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def generate_learning_paths_for_topics(topics, filename):
    dataset = []
    i = 0
    for topic in topics:
        print(f"Generating learning path for topic: {topic}, {i+1}/{len(topics)}")
        i += 1
        learning_path = generate_learning_path(topic)
        try:
            path_json = json.loads(learning_path)
            dataset.extend(path_json["output"])
        except json.JSONDecodeError:
            print(f"Error parsing JSON for topic: {topic}")
            print(f"Raw output: {learning_path}")

    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)


with open('keywords_processed.txt', 'r') as f:
    topics = f.read().splitlines()
    curtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    generate_learning_paths_for_topics(topics, f"learning_paths_dataset_{curtime}.json")

    print(f"Dataset has been saved to 'learning_paths_dataset_{curtime}.json'.")