import google.generativeai as genai
import json
import textwrap
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

class TextToJson:
    def __init__(self, text: str) -> None:
        self.txt = text

    def check(self) -> dict:

        try:
            
            prompt = textwrap.dedent(f"""
                I am sending a text data:
                
                "{self.txt}"

                "Данные пользователя" includes first_name, last_name, middle_name, contract_number, passport_issue(ПИНФЛ) and course. Do not get words as a name next to the 👤.

                If there is a word "Клиент" in the text I sent, it includes info like this: full name-contract number-passport issue. The words before the first dash "-" is all name(first name, last name and middle name(optional)), between two dashes "-" is contract number(contains 3 or 4 digit number, no any string), the last one after second dash "-" is passport issue(contains 14 digit number).

                If there is a character like this: "ʻ" in the text I sent, replace it with "'".
                Convert the text into json format like this:

                '{{
                    "payment": 45000,
                    "transaction_number": 338036667,
                    "date": 07/01/2025 15:00:00,
                    "last_name": "Aliyev",
                    "first_name": "Alisher",
                    "middle_name": "Kamolovich" or "Kamol o'g'li" or "Kamol qizi",
                    "contract_number": 158,
                    "passport_issue": 12822232945845,
                    "course": "python" or null,
                    "payment_app": "paynet"(If the text I sent includes 'Клиент') otherwise "uzum"
                }}'

                Ensure the JSON is well-formed, complete, and valid. Do not write anything other than the JSON object itself. Only provide data inside {{}}.
            """)
            
            Gemini_KEY = os.getenv("Gemini_KEY")
            genai.configure(api_key=Gemini_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            response_data = response.candidates[0].content.parts[0].text
            cleaned_res = json.loads(response_data.replace("```json", "").replace("```", "").strip())

            with open("json.json", "w") as f:
                json.dump(cleaned_res, f, indent=4, ensure_ascii=False)

            return cleaned_res

        except Exception as e:
            print("error", e)


if __name__ == '__main__':
    text = """
        ✅Статус: Успешно

        💰Сумма: 2 020 000
        📩№ транзакции: 327207108
        ⏱Время: 07.12.2024 19:08:35

        🖍MAAB INNOVATION
        🖌MCHJ MAAB INNOVATION

        👤BAXODIROV NODIRBEK
        💳860006******7152
        🏷Данные пользователя: {"fio":"Baxodirov Nodirbek Sardorbek oʻgʻli","Shartnoma raqami":"232","Kurs":"SQL","ПИНФЛ":"32112996860049"}
    """

    txt = TextToJson(text)
    txt.check()
    