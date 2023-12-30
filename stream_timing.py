import time
import json
import argparse
import requests


def main(args):
    endpoint_id = args.endpoint
    base_url = f"https://api.runpod.ai/v2/{endpoint_id}"

    headers = {
        "Authorization": f"Bearer {args.api_key}",
        "Content-Type": "application/json"
    }

    MOCK_PAYLOAD = {
        "input": {
            "mock_return": [f"Mock return {i} or 50" for i in range(50)],
            "mock_delay": 0.01
        }
    }

    run_url = f"{base_url}/run"
    MOCK_PAYLOAD = json.dumps(MOCK_PAYLOAD)
    print(MOCK_PAYLOAD)
    print(run_url)
    response = requests.post(run_url, headers=headers, data=MOCK_PAYLOAD, timeout=10)
    print(response)
    job_id = response.json()["id"]

    stream_url = base_url + "/stream/" + job_id

    while True:
        start_request_time = time.time()
        response = requests.get(stream_url, headers=headers, timeout=10).json()
        end_request_time = time.time()

        print(f"Response: {response}")
        print(f"Request time: {end_request_time - start_request_time}")
        print("\n\n\n")

        if response["status"] == "COMPLETED":
            break
        time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", type=str, default="http://localhost:8000")
    parser.add_argument("--api_key", type=str, default="test")
    args = parser.parse_args()

    main(args)
