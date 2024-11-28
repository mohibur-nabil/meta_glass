from flask import Flask, request, jsonify, render_template
import requests
import base64
import re
import json
import time
import os
import random
import socket
import urllib3
import whois
from proxy_req import get_tor_session  # Import the Tor proxy handler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)


BLOCKLIST_CACHE_FILE = "blocklist_cache.txt"
CACHE_EXPIRY_TIME = 3600  # Cache expiry time in seconds (1 hour)

# Global variable to hold the blocklist
blocked_domains = set()


def load_blocklist(url):
    current_time = time.time()
    print(f"Checking if cache is valid...")  # Debug log
    # Check if cached blocklist exists and is not expired
    if os.path.exists(BLOCKLIST_CACHE_FILE):
        cache_age = current_time - os.path.getmtime(BLOCKLIST_CACHE_FILE)
        print(f"Cache age: {cache_age} seconds")  # Debug log
        if cache_age < CACHE_EXPIRY_TIME:
            print("Using cached blocklist.")  # Debug log
            with open(BLOCKLIST_CACHE_FILE, "r") as file:
                return set(file.read().splitlines())

    print("Fetching blocklist from URL...")  # Debug log
    # Fetch the blocklist from the URL if the cache is expired or doesn't exist
    try:
        response = requests.get(url)
       
        if response.status_code == 200:
            # Decode byte strings to normal strings and collect them into a set
            blocklist = set(
                line.decode("utf-8").strip() for line in response.iter_lines()
            )
            print(f"Fetched {len(blocklist)} domains.")  # Debug log
            # Save the blocklist to the cache file
            with open(BLOCKLIST_CACHE_FILE, "w") as cache_file:
                cache_file.write("\n".join(blocklist))
            print(f"Blocklist cached to {BLOCKLIST_CACHE_FILE}.")  # Debug log
            return blocklist
        else:
            print(f"Failed to fetch blocklist. Status code: {response.status_code}")
            return set()
    except requests.RequestException as e:
        print(f"Error fetching blocklist: {e}")
        return set()


# Load the blocklist at startup (and cache it for future use)
blocklist_url = "https://raw.githubusercontent.com/Bon-Appetit/porn-domains/refs/heads/master/block.txt"
blocked_domains = load_blocklist(blocklist_url)

# Set the maximum upload size to 100MB
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB


def select_random_user_agent(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("The file is empty")
            return random.choice(lines).strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except ValueError as ve:
        print(ve)


def upload_image(base64_image, use_tor=False):
    try:
        data = {"image": base64_image}
        url = "https://pimeyes.com/api/upload/file"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # If Tor proxy is enabled, use it
        if use_tor:
            session = get_tor_session()
            response = session.post(url, headers=headers, json=data, verify=False)
        else:
            response = requests.post(url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            print("Image uploaded successfully.")
            if not response.json().get("faces"):
                print("No faces found in uploaded image.")
                return None, None
            return response.cookies, response.json().get("faces")[0]["id"]
        else:
            print(f"Failed to upload image. Status code: {response.status_code}")
            print(response.text)
            return None, None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None, None


def get_ip_address_through_tor():
    try:
        session = get_tor_session()
        response = session.get("https://httpbin.org/ip", verify=False)
        if response.status_code == 200:
            return response.json().get("origin")
        else:
            return "Could not retrieve IP address"
    except Exception as e:
        return f"Error retrieving IP: {e}"


def exec_search(cookies, search_id, user_agent, use_tor=False):
    headers = {
        "sec-ch-ua": '"Not;A=Brand";v="99", "Chromium";v="106"',
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "user-agent": user_agent,
        "origin": "https://pimeyes.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://pimeyes.com/en",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
    }
    url = "https://pimeyes.com/api/search/new"
    data = {
        "faces": [search_id],
        "time": "any",
        "type": "PREMIUM_SEARCH",
        "g-recaptcha-response": None,
    }
    # If Tor proxy is enabled, use it
    if use_tor:
        session = get_tor_session()
        response = session.post(url, headers=headers, json=data, cookies=cookies)
    else:
        response = requests.post(url, headers=headers, json=data, cookies=cookies)

    if response.status_code == 200:
        json_response = response.json()
        return json_response.get("searchHash"), json_response.get("searchCollectorHash")
    else:
        print(f"Failed to get searchHash. Status code: {response.status_code}")
        print(response.text)
        return None, None


def extract_url_from_html(html_content):
    pattern = r'api-url="([^"]+)"'
    url = re.search(pattern, html_content)
    if url:
        return re.search(r"https://[^\"]+", url.group()).group()
    return None


def get_ip_address_through_tor():
    try:
        session = get_tor_session()
        response = session.get("https://httpbin.org/ip", verify=False)
        if response.status_code == 200:
            return response.json().get("origin")
        else:
            return "Could not retrieve IP address"
    except Exception as e:
        return f"Error retrieving IP: {e}"


def find_results(search_hash, search_collector_hash, search_id, cookies, use_tor=False):
    url = f"https://pimeyes.com/en/results/{search_collector_hash}_{search_hash}?query={search_id}"

    # If Tor proxy is enabled, use it
    if use_tor:
        session = get_tor_session()
        response = session.get(url, cookies=cookies)
    else:
        response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        print("Found correct server.")
        return extract_url_from_html(response.text)
    else:
        print(f"Failed to find results. Status code: {response.status_code}")
        print(response.text)
        return None


def get_results(url, search_hash, user_agent):
    print(url)
    data = {"hash": search_hash, "limit": 250, "offset": 0, "retryCount": 0}
    headers = {
        "sec-ch-ua": '"Not;A=Brand";v="99", "Chromium";v="106"',
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "user-agent": user_agent,
        "origin": "https://pimeyes.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://pimeyes.com/en",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        print("Results obtained successfully.")
        return response.json()
    else:
        print(f"Failed to obtain results. Status code: {response.status_code}")
        print(response.text)
        return None


def hex_to_ascii(hex_string):
    hex_string = hex_string.lstrip("0x")
    bytes_data = bytes.fromhex(hex_string)
    return bytes_data.decode("ascii", errors="ignore")


def normalize_domain(domain):
    """
    Normalize the domain name to ensure it matches the blocklist format.
    This includes removing common subdomains like 'www.', 'pic.', 'static.' and converting to lowercase.
    """
    domain = domain.lower()

    # Remove common subdomains if they exist
    subdomains_to_remove = [
        "www.",
        "pic.",
        "static.",
        "m.",
        "cdn.",
        "api.",
        "public.",
    ]  # Add more subdomains as needed
    for subdomain in subdomains_to_remove:
        if domain.startswith(subdomain):
            domain = domain[len(subdomain) :]
            break  # Only remove the first matching subdomain

    return domain


def process_thumbnails(json_data):
    results = json_data.get("results", [])
    if not results:
        return "Search successful, but no matches found."

    processed_results = []
    for result in results:
        thumbnail_url = result.get("thumbnailUrl", "")
        match = re.search(r"/proxy/([0-9a-fA-F]+)", thumbnail_url)
        if match:
            hex_part = match.group(1)
            ascii_text = hex_to_ascii(hex_part)
            try:
                ascii_data = json.loads(ascii_text)
                page_url = ascii_data.get("url")
                site = result.get("site", "")

                # Resolve the domain from the page URL if needed
                if not site and page_url:
                    site = (
                        re.search(r"https?://([^/]+)", page_url).group(1)
                        if page_url
                        else "Unknown site"
                    )

                # Resolve domain classification
                domain = (
                    re.search(r"https?://([^/]+)", page_url).group(1)
                    if page_url
                    else ""
                )

                if page_url:
                    processed_results.append(
                        {
                            "page_url": page_url,
                            "account_info": result.get("accountInfo", "Not available"),
                            "thumbnail_url": thumbnail_url,
                            "site": site,
                        }
                    )
            except json.JSONDecodeError:
                print("Failed to decode JSON from ASCII text.")

    return processed_results


@app.route("/", methods=["GET", "POST"])
def index():
    use_tor = request.form.get("use_tor") == "on"  # Check if user wants to use Tor
    tor_ip = None
    if use_tor:
        tor_ip = get_ip_address_through_tor()  # Get the IP address used by Tor

    if request.method == "POST":
        file = request.files.get("file")
        pasted_image = request.form.get("pasted_image")

        if not file and not pasted_image:
            return render_template(
                "index.html", error="No selected file or pasted image", tor_ip=tor_ip
            )

        if file:
            base64_image = base64.b64encode(file.read()).decode("utf-8")
            base64_image = f"data:image/jpeg;base64,{base64_image}"

        elif pasted_image:
            base64_image = re.sub("^data:image/.+;base64,", "", pasted_image)
            base64_image = f"data:image/jpeg;base64,{base64_image}"

        cookies, search_id = upload_image(base64_image, use_tor)
        if not cookies or not search_id:
            return render_template(
                "index.html", error="Failed to upload image", tor_ip=tor_ip
            )

        cookies.set("payment_gateway_v3", "fastspring", domain="pimeyes.com")
        cookies.set(
            "uploadPermissions", str(time.time() * 1000)[:13], domain="pimeyes.com"
        )

        user_agent = select_random_user_agent("user-agents.txt")

        search_hash, search_collector_hash = exec_search(
            cookies, search_id, user_agent, use_tor
        )
        if not (search_hash and search_collector_hash):
            return jsonify({"error": "Could not proceed with further API calls."}), 404

        server_url = find_results(
            search_hash, search_collector_hash, search_id, cookies, use_tor
        )
        if not server_url:
            return jsonify({"error": "Failed to find server URL."}), 404

        res = get_results(server_url, search_hash, user_agent)
        if res:
            results = process_thumbnails(res)
            save_results_to_file(results=results)
            if not results:
                return render_template("404.html", error="No matches found."), 404
            return render_template("results.html", results=results, tor_ip=tor_ip)
        else:
            return render_template(
                "index.html", error="Failed to get results", tor_ip=tor_ip
            )

    return render_template("index.html", tor_ip=tor_ip)

def save_results_to_file(results, file_path="results.txt"):
    with open(file_path, 'w') as file:
        for result in results:
            file.write(f"{result}\n")

def find_available_port(start_port=5000, max_port=65535):
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except socket.error:
                continue
    return None


if __name__ == "__main__":
    # Load the blocklist when the app starts
    blocked_domains = load_blocklist(blocklist_url)

    port = find_available_port()
    if port:
        print(f"Starting server on port {port}")
        app.run(debug=True, port=port)
    else:
        print("No available ports found.")
