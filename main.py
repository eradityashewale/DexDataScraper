from dbconnection import DBConnection
import requests

# Establish database connection
conn = DBConnection.get_connection()
if conn:
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Endpoint to get specific token pair data (modify the pair if needed)
    url = "https://api.dexscreener.com/token-profiles/latest/v1"

    # Make the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        print(data)  # Print the data (for debugging)

        # Iterate through tokens if they exist
        for token in data:
            # Use .get() to safely access keys
            url = token.get('url', 'N/A')
            chainid = token.get('chainId', 'N/A')
            tokenAddress = token.get('tokenAddress', 'N/A')
            icon = token.get('icon', 'N/A')
            header = token.get('header', 'N/A')  # Handle missing 'header'
            openGraph = token.get('openGraph', 'N/A')
            description = token.get('description', 'N/A')

            # Convert links to string (if necessary for SQL insertion)
            links = str(token.get('links', []))

            try:
                # Prepare SQL query to insert the data into a table
                cur.execute(
                    """INSERT INTO token_data (url, chainid, tokenaddress, icon, header, 
                        opengraph, description, links) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (url, chainid, tokenAddress, icon, header, openGraph, description, links)
                )
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print(f"Missing data for token: {token}")

        # Commit the transaction to make changes persistent
        conn.commit()
        print('Data added successfully')
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    # Close the cursor and connection
    cur.close()
    conn.close()
else:
    print("Failed to connect to the database")
