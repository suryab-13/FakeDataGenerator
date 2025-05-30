from faker import Faker
import random
import re
from datetime import datetime

fake = Faker()

def extract_length(data_type):
    match = re.search(r'\((\d+)\)', data_type)
    return int(match.group(1)) if match else None

def generate_fake_value(column_name, data_type, foreign_keys=None):
    column_name = column_name.lower().strip()
    data_type = data_type.lower().strip()
    length = extract_length(data_type) or 255

 
    if foreign_keys and column_name in foreign_keys:
        return random.choice(foreign_keys[column_name])

    if data_type.startswith("tinyint") and ("(1)" in data_type or data_type == "tinyint"):
        return random.choice([0, 1])

    elif "int" in data_type:
        if "age" in column_name:
            return random.randint(1, 100)
        if "quantity" in column_name or "qty" in column_name:
            return random.randint(1, 500)
        if "price" in column_name or "amount" in column_name or "salary" in column_name:
            return random.randint(1000, 100000)
        if "id" in column_name:
            return random.randint(1, 99999)

        if "tinyint" in data_type:
            return random.randint(0, 127)
        elif "smallint" in data_type:
            return random.randint(0, 32767)
        elif "mediumint" in data_type:
            return random.randint(0, 8388607)
        elif "bigint" in data_type:
            return random.randint(0, 9223372036854775807)
        else:
            return random.randint(0, 2147483647)

    elif "float" in data_type or "double" in data_type or "decimal" in data_type:
        return round(random.uniform(1, 10000), 2)

    elif "datetime" in data_type or "timestamp" in data_type:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif "date" in data_type:
        return fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
    elif "time" in data_type:
        return datetime.now().strftime('%H:%M:%S')

    elif "char" in data_type or "text" in data_type:
        if "email" in column_name:
            return fake.email()[:length]
        elif "phone" in column_name or "mobile" in column_name:
            return fake.phone_number()[:length]
        elif "first_name" in column_name:
            return fake.first_name()[:length]
        elif "last_name" in column_name:
            return fake.last_name()[:length]
        elif "name" in column_name:
            return fake.name()[:length]
        elif "address" in column_name:
            return fake.address().replace("\n", ", ")[:length]
        elif "city" in column_name:
            return fake.city()[:length]
        elif "state" in column_name:
            return fake.state()[:length]
        elif "zip" in column_name or "postal" in column_name:
            return fake.postcode()[:length]
        elif "country" in column_name:
            return fake.country()[:length]
        elif "desc" in column_name or "description" in column_name:
            return fake.text(max_nb_chars=min(length, 200))
        elif "title" in column_name:
            return fake.sentence(nb_words=4)[:length]
        else:
            return fake.word()[:length]

    return "NA" 