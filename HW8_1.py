from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
import json
import uvicorn
import re

app = FastAPI()

class Appeal(BaseModel):
   surname: str
   name: str 
   birth_date: str
   phone_number: str 
   email: str

   @field_validator("surname")
   def check_surname(cls, value):
        if not value[0].isupper():
            raise ValueError("Фамилия должна начинаться с заглавной буквы")
        if not re.fullmatch('[а-яА-Я]{1,' + str(len(value)) + '}', value):
            raise ValueError("Фамилия должна быть записана кирилицей")
        
   @field_validator("name")
   def check_name(cls, value):
        if not value[0].isupper():
            raise ValueError("Имя должно начинаться с заглавной буквы")
        if not re.fullmatch('[а-яА-Я]{1,' + str(len(value)) + '}', value):
            raise ValueError("Имя должно быть записано кирилицей")

def process_appeal(appeal: Appeal):
    res = json.dumps(appeal.__dict__)
    with open(file='D:/Учеба/Python/ДЗ8/file.json', mode='w', encoding='utf-8') as file_to_write:
        file_to_write.write(res) 
    return res     

@app.post("/")
async def add_appeal(appeal: Appeal):
   return process_appeal(appeal)