import requests
import json

def query_ollama_stream(prompt, model="llama2", output_filename="ollama_output.txt"):
    url = "http://localhost:11434/api/generate"
    data = {
        "prompt": prompt,
        "model": model,
        "stream": True
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        with open(output_filename, 'w') as outfile:
            response = requests.post(url, headers=headers, json=data, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        response_part = json_data.get('response', '')
                        outfile.write(response_part)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}, line: {line.decode('utf-8')}")
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")

if __name__ == "__main__":
    user_prompt = input("Enter your prompt for Ollama: ")
    query_ollama_stream(user_prompt)
    print("Ollama's streamed response has been written to ollama_output.txt")