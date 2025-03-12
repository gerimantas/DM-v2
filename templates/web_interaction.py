"""
Pre-built templates for common web interaction tasks.
These templates include API requests, web scraping, and data retrieval patterns.
"""

# Template for basic API requests
API_REQUEST_TEMPLATE = """
import requests
import json
from pathlib import Path

def make_api_request(url, method='GET', params=None, headers=None, data=None, 
                     json_data=None, auth=None, timeout=10, save_to=None):
    \"\"\"
    Make an API request with customizable parameters.
    
    Args:
        url (str): The API endpoint URL
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
        params (dict, optional): Query parameters for the request
        headers (dict, optional): HTTP headers
        data (dict or str, optional): Form data for the request
        json_data (dict, optional): JSON data for the request
        auth (tuple or object, optional): Authentication credentials
        timeout (int): Timeout in seconds
        save_to (str, optional): Path to save response to a file
        
    Returns:
        dict or str: Response data (parsed JSON or raw text)
    \"\"\"
    # Default headers
    if headers is None:
        headers = {
            'User-Agent': 'Python Client/1.0',
            'Accept': 'application/json'
        }
    
    # Make the request
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            params=params,
            headers=headers,
            data=data,
            json=json_data,
            auth=auth,
            timeout=timeout
        )
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Try to parse JSON response
        try:
            result = response.json()
        except ValueError:
            # If not JSON, return text
            result = response.text
        
        # Save response to file if specified
        if save_to:
            save_path = Path(save_to)
            
            # Create directory if it doesn't exist
            save_path.parent.mkdir(exist_ok=True, parents=True)
            
            # Determine file format and save accordingly
            if isinstance(result, (dict, list)):
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4)
            else:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(str(result))
            
            print(f"Response saved to {save_path}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example: Get GitHub user information
    api_url = "https://api.github.com/users/octocat"
    response = make_api_request(api_url, save_to="github_user.json")
    
    if response:
        print(f"Username: {response.get('login')}")
        print(f"Name: {response.get('name')}")
        print(f"Followers: {response.get('followers')}")
"""

# Template for web scraping with BeautifulSoup
WEB_SCRAPING_TEMPLATE = """
import requests
from bs4 import BeautifulSoup
import csv
import json
from pathlib import Path

def scrape_website(url, selector=None, save_to=None, save_format='csv'):
    \"\"\"
    Scrape content from a website using BeautifulSoup.
    
    Args:
        url (str): The URL to scrape
        selector (str, optional): CSS selector to extract specific elements
        save_to (str, optional): Path to save scraped data
        save_format (str): Format to save data ('csv', 'json', or 'txt')
        
    Returns:
        list: Scraped data as a list of elements or text
    \"\"\"
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data based on selector
        if selector:
            elements = soup.select(selector)
            data = [element.get_text(strip=True) for element in elements]
        else:
            # If no selector, just return the page title and description
            title = soup.title.string if soup.title else "No title found"
            description = ""
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                description = meta_desc.get("content", "")
            
            data = [{"title": title, "description": description, "url": url}]
        
        # Save data if path specified
        if save_to:
            save_path = Path(save_to)
            
            # Create directory if it doesn't exist
            save_path.parent.mkdir(exist_ok=True, parents=True)
            
            # Save according to specified format
            if save_format.lower() == 'csv':
                with open(save_path, 'w', newline='', encoding='utf-8') as f:
                    if isinstance(data[0], dict):
                        fieldnames = data[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)
                    else:
                        writer = csv.writer(f)
                        writer.writerow(['content'])
                        writer.writerows([[item] for item in data])
            
            elif save_format.lower() == 'json':
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            
            else:  # txt
                with open(save_path, 'w', encoding='utf-8') as f:
                    for item in data:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                f.write(f"{key}: {value}\\n")
                            f.write("\\n")
                        else:
                            f.write(f"{item}\\n")
            
            print(f"Scraped data saved to {save_path}")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")
        return []
"""

# Dictionary mapping template names to their content
TEMPLATES = {
    "api_request": API_REQUEST_TEMPLATE,
    "web_scraping": WEB_SCRAPING_TEMPLATE
}

def get_template(template_name):
    """
    Get a template by name.
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: Template content
    """
    return TEMPLATES.get(template_name, "Template not found")

def list_templates():
    """
    List all available templates.
    
    Returns:
        list: Names of available templates
    """
    return list(TEMPLATES.keys())