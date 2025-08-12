from customer.CreateOrUpdateCustomer import create_or_update_customer

def main():
    print("create custom. If exist create new")
    print("create project 1 and project2")
    print("create dataset1 and dataset 2")
    print("create route 1 and route 2")
    print("create a zone")
    customer=create_or_update_customer(
        customer_id="12345",
        data={
            "id": "12345",
            "name": "Test Customer",
            "email": ""
              }
    )
    print("Customer created or updated:", customer)

if __name__ == "__main__":
    main()