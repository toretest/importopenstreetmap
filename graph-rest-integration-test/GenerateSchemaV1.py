from models.ReaderV1 import generate_customer_json_schema, write_customer_json_schema


def main():
    schema = generate_customer_json_schema()
    print("Top-level schema keys:", list(schema.keys()))
    # Write the schema to a file
    out_path = write_customer_json_schema("customer_schema.json")
    print("Wrote JSON Schema to:", out_path)

if __name__ == "__main__":
    main()