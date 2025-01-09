class Paynet:
    def __init__(self, text):
        self.text = text

    def paynet_data(self):
        lines = self.text.split("\n")
        data = {}
        for line in lines:
            if ": " in line:  # Split only if the line contains ': '
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()
                data[key] = value

        # Further process the 'Клиент' field
        if "Клиент" in data:
            client_info = data["Клиент"]
            try:
                # Extract 'first_name', 'last_name', 'middle_name', 'contract_number', and 'pnfl'
                parts = client_info.split("-")
                if len(parts) == 3:
                    first_last_middle_name = parts[0].split(" ")
                    data["first_name"] = first_last_middle_name[0].strip()
                    data["last_name"] = first_last_middle_name[1].strip()
                    
                    # Check if 'middle_name' exists
                    if len(first_last_middle_name) > 2:
                        data["middle_name"] = " ".join(first_last_middle_name[2:]).strip()
                    else:
                        data["middle_name"] = ""  # Assign an empty string if not present
                    
                    data["contract_number"] = parts[1].strip()
                    data["pnfl"] = parts[2].strip()
                    data["payment"] = data["Сумма транзакции"].replace(" сум", "")
                    data["payment_app"] = "paynet"

                # Remove the original 'Клиент' field if no longer needed
                del data["Клиент"], data["Сумма транзакции"]
            except Exception as e:
                print(f"Error parsing 'Клиент' field: {e}")

        return data
