# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import base64
import json
import os
from groq import Groq
from pathlib import Path



def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

schema = {
        "type": "object",
        "properties": {
            "triples": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "object": {"type": "string"},
                        "relation": {"type": "string"}
                    },
                    "required": ["subject", "object", "relation"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["triples"],
        "additionalProperties": False
    }

def get_triplets(img):
    resp = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            { "role": "system", "content":
                ( "Ты извлекаешь граф знаний из изображения. Верни только JSON. "
                        "Извлекай только визуально наблюдаемые сущности и отношения. "
                        "Не выдумывай невидимые детали. "
                        "Используй короткие русские подписи. "
                        "Отношение должно быть глаголом или короткой связью."
                 )
             },
            { "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Построй по изображению граф знаний, который опишет сцену происходящего в сюжете события."
                            "Выдели следующие типы сущностей: герой, предметы, фон, атмосфера."
                            " Граф должен быть ориентированный."
                            "Ребра графа подписаны типами связей, например положение, назначение, признак, принадлежность. "
                            "Глядя на граф можно описать что происходит на фотографии"
                            "Нужно вернуть triples[]. "
                            "Каждый элемент имеет поля subject, object, relation. "
                            "Пример: "
                            '{"triples":[{"subject":"Игрок","object":"Кубок","relation":"держит"}]}'
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "knowledge_graph",
                "strict": False,  # Scout: best-effort, не strict
                "schema": schema
            }
        },
        temperature=0
    )
    data = json.loads(resp.choices[0].message.content)
    triples = [(t["subject"], t["object"], t["relation"]) for t in data["triples"]]
    return triples

if __name__ == '__main__':
    api_key = os.environ.get("GROQ_API_KEY")
    print("Ключ найден:", bool(api_key))

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    results = []

    for image_path in Path("images").iterdir():
        if image_path.is_file() and image_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            image_b64 = encode_image(str(image_path))
            triples = get_triplets(image_b64)
            results.append({
                "image": image_path.name,
                "triples": triples
            })

    #image_b64 = encode_image("images/баскетбол1.jpg")


    # сохранение результата
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "triples.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nСохранено {len(results)} триплетов в results/triples.json")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
