class Uzum:
    def __init__(self, text):
        self.text = text

    def uzum_data(self):
        lines = self.text.split("\n")
        data = {}
        provider_name = ""
        service_name = "Оплата"  # Default service name
        amount = ""
        full_name_line = ""  # To store the line with 👤

        for line in lines:
            if ": " in line:  # Split only if the line contains ': '
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()

                # Extract specific fields
                if key == "✅Статус" and value == "Успешно":
                    data["Сервис"] = service_name
                elif key == "💰Сумма":
                    amount = value
                elif key == "📩№ транзакции":
                    data["№ транзакции"] = value
                elif key == "⏱️Время":
                    data["Дата"] = value
                elif key == "🏷Данные пользователя":
                    try:
                        user_data = eval(value)  # Convert string representation of dict to actual dict
                        if "fio" in user_data:
                            fio_parts = user_data["fio"].split(" ")
                            data["first_name"] = fio_parts[0].strip()
                            data["last_name"] = fio_parts[1].strip() if len(fio_parts) > 1 else ""
                            data["middle_name"] = " ".join(fio_parts[2:]).strip() if len(fio_parts) > 2 else ""
                        if "Shartnoma raqami" in user_data:
                            data["contract_number"] = user_data["Shartnoma raqami"]
                        if "ПИНФЛ" in user_data:
                            data["pnfl"] = user_data["ПИНФЛ"]
                    except Exception as e:
                        print(f"Error parsing user data: {e}")
            elif line.startswith("👤"):
                full_name_line = line.replace("👤", "").strip()
            elif line.startswith("🖍") or line.startswith("🖌"):
                provider_name = line.replace("🖍", "").replace("🖌", "").strip()

        # If the full name line is present, process it for middle name
        if full_name_line:
            name_parts = full_name_line.split(" ")
            data["middle_name"] = " ".join(name_parts[2:]).strip() if len(name_parts) > 2 else ""

        # Add additional fields
        data["Провайдер"] = provider_name
        data["payment_app"] = "uzum"
        if amount:
            amount_cleaned = amount.replace(" ", "")
            data["payment"] = f"{amount_cleaned}"

        return data
