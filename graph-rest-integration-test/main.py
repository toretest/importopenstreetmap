# python
from customer.CustomerApiClient import CustomerApiClient


def main():
    print("Test customer API. If exist create new")
    # Use the client so the base URL is defined once
    with CustomerApiClient(base_url="http://localhost:8080/customers/customer") as client:
        # Reads customerId and payload from the file at project root
        result = client.create_or_update_from_file("customer1.json")
        print("API response:", result)
    customer_ode_id = result["id"]
    print("TODO create project 1 and project2 with customerId:", customer_ode_id)
    print("TODO create dataset1 and dataset 2")
    print("TODO create route 1 and route 2")
    print("TODO create a zone")

if __name__ == "__main__":
    main()