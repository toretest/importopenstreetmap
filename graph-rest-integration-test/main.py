# python
from CustomerApiClient import CustomerApiClient
from models.ReaderV1 import load_customer_document

def main():
    print("Test customer API. If exist create new")
    doc = load_customer_document("customer1.json").payload
    print(doc.customerId)
    for project in doc.projects:
        print("Project name:", project.name)
        print("Project description:", project.description)
    print("*******")
    # Use the client so the base URL is defined once
    with CustomerApiClient(customer_base_url="http://localhost:8080/customers/customer") as client:
        # Reads customerId and payload from the file at project root
        result = client.create_or_update(doc)
        print("API response:", result)

    #customer_ode_id = result["id"]
    #print("TODO create project 1 and project2 with customerId:", customer_ode_id)
    print("TODO create dataset1 and dataset 2")
    print("TODO create route 1 and route 2")
    print("TODO create a zone")

if __name__ == "__main__":
    main()