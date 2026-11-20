"""Monthly charge run: charges every customer in data/due.csv through the payment gateway."""
import csv
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_env(path):
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, _, value = line.partition("=")
            env[key] = value
    return env


def to_cents(amount):
    return int(float(amount) * 100)


def charge(url, api_key, customer_id, invoice, cents):
    body = json.dumps({"customer": customer_id, "invoice": invoice, "amount": cents, "currency": "usd"})
    request = urllib.request.Request(
        url + "/v1/charges",
        data=body.encode(),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    env = load_env(ROOT / "config" / "live.env")
    with open(ROOT / "data" / "due.csv", newline="") as f:
        for row in csv.DictReader(f):
            cents = to_cents(row["amount_due"])
            result = charge(env["PAYMENTS_URL"], env["PAYMENTS_API_KEY"], row["customer_id"], row["invoice"], cents)
            print(row["customer_id"], row["invoice"], cents, result["id"])


if __name__ == "__main__":
    main()
