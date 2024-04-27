import os
import requests
import pandas as pd
import json


def test_engine(base_url, directories_with_csv, request_settings):
    for directory, csv_file_name in directories_with_csv:
        csv_file_path = os.path.join(directory, csv_file_name)

        if not os.path.exists(csv_file_path):
            print(f"CSV file not found: {csv_file_path}")
            continue

        df = pd.read_csv(csv_file_path, sep=",")

        for _, row in df.iterrows():
            html_file = row["html"].strip()
            query = row.get("task definiton", row.get("task_definition", "")).strip()
            html_file_path = os.path.join(directory, html_file)

            if not os.path.exists(html_file_path):
                print(f"File not found: {html_file_path}")
                continue

            try:
                with open(html_file_path, "r") as f:
                    html_content = f.read()
            except Exception as e:
                print(f"Error reading file {html_file_path}: {e}")
                continue

            for extractor_type in ["ai", "non-ai"]:
                for output_type in ["js", "selenium"]:
                    prompt_template = "js" if output_type == "js" else "selenium"
                    request_data = {
                        "query": query,
                        "html_content": html_content,
                        "extractor_type": extractor_type,
                        "prompt_template": prompt_template,
                        **request_settings,
                    }

                    try:
                        response = requests.post(f"{base_url}/query", json=request_data)
                        if response.status_code == 200:
                            result = response.json()["result"]
                            print(f"File: {html_file_path}")
                            print(f"Query: {query}")
                            print(f"Extractor: {extractor_type}, Output: {output_type}")
                            print("Response:")
                            print(result)
                            print()
                        else:
                            print(f"Error: {response.status_code}")
                    except requests.RequestException as e:
                        print(f"Request failed: {e}")


if __name__ == "__main__":
    with open("./examples/config.json") as config_file:
        config = json.load(config_file)

    base_url = config["base_url"]
    directories_with_csv = config["directories_with_csv"]
    request_settings = config["request_settings"]

    test_engine(base_url, directories_with_csv, request_settings)
