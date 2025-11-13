from datetime import date, datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
import json
import uvicorn
import re

app = FastAPI()

reasons = ['нет доступа к сети', 'не работает телефон', 'не приходят письма']

class Appeal(BaseModel):
   surname: str
   name: str 
   birth_date: date
   phone_number: str 
   email: str
   reason: str
   problem_date: datetime

   @field_validator("surname")
   def check_surname(cls, value):
        if not value[0].isupper():
            raise ValueError("Фамилия должна начинаться с заглавной буквы")
        if not re.fullmatch('[а-яА-Я]{1,' + str(len(value)) + '}', value):
            raise ValueError("Фамилия должна быть записана кирилицей")
        return value
        
   @field_validator("name")
   def check_name(cls, value):
        if not value[0].isupper():
            raise ValueError("Имя должно начинаться с заглавной буквы")
        if not re.fullmatch('[а-яА-Я]{1,' + str(len(value)) + '}', value):
            raise ValueError("Имя должно быть записано кирилицей")
        return value
        
   @field_validator("reason")
   def check_reason(cls, value):
        if value not in reasons:
            raise ValueError("Недопустимая причина обращения")
        return value
   
   @field_validator("birth_date")
   def check_birth_date(cls, value):
        year = timedelta(days=365)
        if value > (date.today() - 18*year):
            raise ValueError("Заявитель не может быть несовершеннолетним")
        return value
   
   @field_validator("email")
   def check_email(cls, value):
        if "@" not in value:
            raise ValueError("Некорректный формат email")
        return value
   
   @field_validator("problem_date")
   def check_problem_date(cls, value):
        if value.date() > date.today():
            raise ValueError("Некорректная дата обнаружения проблемы")
        return value

def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        else:
            return obj

def process_appeal(appeal: Appeal):
    res = json.dumps(appeal.__dict__, default=json_serial)
    with open(file='D:/Учеба/Python/ДЗ8/file.json', mode='w', encoding='utf-8') as file_to_write:
        file_to_write.write(res) 
    return res     

@app.post("/")
async def add_appeal(appeal: Appeal):
   return process_appeal(appeal)