import requests

url = "http://lnx1073302govt:11434/api/chat"
prompt = input("Prompt> ")
msg = {
  "model": "mistral-long:latest",
  "messages": [
    {
      "role": "user",
      "content": prompt
    }
  ],
  "stream": False
}

try:
    response = requests.post(url, json=msg)

    if response.status_code == 200:
        print("Success")
        print(f"Answer> {response.json()["message"]["content"]}")
    else:
        print("Error!")
        print(f"Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print("ERROR!")
    print(e)