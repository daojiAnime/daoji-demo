from genson import SchemaBuilder


def main():
    data = [
        {
            "date": "2024-02-01",
            "sector": "Basic Materials",
            "exchange": "NASDAQ",
            "averageChange": -0.31481377464310634,
        },
        {
            "date": "2024-02-01",
            "sector": "Communication Services",
            "exchange": "NASDAQ",
            "averageChange": 0.8507016628132006,
        },
        {
            "date": "2024-02-01",
            "sector": "Consumer Cyclical",
            "exchange": "NASDAQ",
            "averageChange": 1.8112982659586416,
        },
        {
            "date": "2024-02-01",
            "sector": "Consumer Defensive",
            "exchange": "NASDAQ",
            "averageChange": 1.7434715175984574,
        },
        {"date": "2024-02-01", "sector": "Energy", "exchange": "NASDAQ", "averageChange": 0.6397534025664513},
        {
            "date": "2024-02-01",
            "sector": "Financial Services",
            "exchange": "NASDAQ",
            "averageChange": -1.5273756492183397,
        },
        {"date": "2024-02-01", "sector": "Healthcare", "exchange": "NASDAQ", "averageChange": 0.05694856084430991},
        {"date": "2024-02-01", "sector": "Industrials", "exchange": "NASDAQ", "averageChange": 0.803667816001016},
        {"date": "2024-02-01", "sector": "Real Estate", "exchange": "NASDAQ", "averageChange": 1.7404175921532465},
        {"date": "2024-02-01", "sector": "Technology", "exchange": "NASDAQ", "averageChange": 1.3264361672207303},
        {"date": "2024-02-01", "sector": "Utilities", "exchange": "NASDAQ", "averageChange": 2.018568297511109},
    ]

    builder = SchemaBuilder()
    builder.add_object(data)

    schema = builder.to_schema()
    print(schema)


if __name__ == "__main__":
    main()
