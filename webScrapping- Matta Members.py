import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_matta_members():
    # can put URL that you want to scrap. for this one im using matta members
    base_url = "https://www.matta.org.my/members?page="
    members = []

    for page in range(1, 50): #page 1 to 49
        url = f"{base_url}{page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to load page {page}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the section containing the member details
        # From the website, there is class card-box that can be used
        member_list = soup.find_all('div', class_='card-box')
        if not member_list:
            print(f"No members found on page {page}")
            continue
        
        # Iterate over each member entry and extract details
        for member in member_list:
            name = member.find('a', class_='search-title').get_text(strip=True)
            reg_number = member.find('span', class_='reg-number').get_text(strip=True)
            contact_number = member.find('span', class_='contact-number').get_text(strip=True)
            web_address = member.find('span', class_='web-address').get_text(strip=True)
            location = member.find('span', class_='location').get_text(separator=", ", strip=True)
            
            members.append({
                'name': name,
                'reg_number': reg_number,
                'contact_number': contact_number,
                'web_address': web_address,
                'location': location
            })
        print(f"Page {page} scraped successfully.")
    
    # Convert to DataFrame
    df = pd.DataFrame(members)
    return df

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    full_path = os.path.abspath(filename)
    print(f"Data successfully saved to {full_path}")

# Run the function and get the dataframe
df = scrape_matta_members()

# Save the dataframe to a CSV file
csv_filename = 'matta_members.csv'
save_to_csv(df, csv_filename)
