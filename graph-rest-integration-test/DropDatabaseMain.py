from DatabaseAdminClient import AdminApiClient

def main():
    with AdminApiClient(base_url="http://localhost:8080/admin/graphdb") as client:
        # Reads customerId and payload from the file at project root
        result = client.drop_database()
        print("API response:", result)

if __name__ == "__main__":
    main()