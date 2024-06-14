import dataclasses
import time
from datetime import datetime, timedelta

import requests

amo_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjZkMWQ4Njg4ZmQxN2Q3MzVhYzJiMmJhM2NkNzI4MzlmYjA2NTFiMWViYjE4ZDllMjU4MzNiOTk0MmRlZDU3ZmMxZThmMDRlMzQ5ZDhlYzM4In0.eyJhdWQiOiJkY2YxMTExNi1lYWEyLTQ5YTUtODlmZC00NTcyOWYwNDhjYTQiLCJqdGkiOiI2ZDFkODY4OGZkMTdkNzM1YWMyYjJiYTNjZDcyODM5ZmIwNjUxYjFlYmIxOGQ5ZTI1ODMzYjk5NDJkZWQ1N2ZjMWU4ZjA0ZTM0OWQ4ZWMzOCIsImlhdCI6MTcxODM3MDEwNSwibmJmIjoxNzE4MzcwMTA1LCJleHAiOjE3MTkwMTQ0MDAsInN1YiI6IjExMTUyNzQyIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzk3NjkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZjQyODk4N2EtN2M0MC00YTkwLTgwODktNDRlMDg5Yzg3NTE3In0.j18kQw1tLSrk5qf2yAhbljmtd-ZvTPZti7L5nAj7VoBMjgBVqCGJEgJAnn5UUXnJDqavfwiIuhHNcaGTT3Prpbsr9yhK_MTeRqyVQJhwlMI7HvCFzTRlBTdJqQXrCL2OnDXG25zqlO5GwYp3Px0jX17xxUKM2vEQc6cAk1lSyrwK__0yXIwgdYCaFe8dl-Sf48OyrcpFzdsvDhFhlvxgCC-zaRn1-PELQnolObreDGKwfgf3gCfqfUZB8rOmXssfu5Y8QBP2eRh2ycrTEY6qIMQYD5ixX52GmbPxF3Hiy9MasnS4OX40Qi8c2ZoPXW1iEdHkdkAEtubmr22EPx2e9A"





def main():
    url = "https://forvantar.amocrm.ru/api/v4/leads"
    headers = {
        'Authorization': f'Bearer {amo_token}',
        'Content-Type': 'application/json'
    }

    deals = [
        DealDTO("API TEST 1", 1000, "Пастильная", "Экскурсия", "Взрослый", 100, 10,
                datetime.now() - timedelta(hours=1)),
    ]

    x = requests.post(url, json=list(map(deal_to_json, deals)), headers=headers)
    print(x.text)


if __name__ == '__main__':
    main()
