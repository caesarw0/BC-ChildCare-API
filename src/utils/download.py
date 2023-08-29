import requests

def download_csv_and_store(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the CSV data to the destination
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return 1
        else:
            print("Failed to download CSV. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Provide the URL of the CSV file and the desired save path
csv_url = "https://catalogue.data.gov.bc.ca/dataset/4cc207cc-ff03-44f8-8c5f-415af5224646/resource/9a9f14e1-03ea-4a11-936a-6e77b15eeb39/download/childcare_locations.csv"
save_path = "../data/childcare_locations.csv"

# Call the function to download, store, and load the CSV data
data_frame = download_csv_and_store(csv_url, save_path)

if data_frame is not None:
    print("CSV data downloaded.")
else:
    print("Failed to load CSV data.")
