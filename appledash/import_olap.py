# import_olap.py
import csv
from visualisasi.models import AppleSales

def run():
    with open('OLAP_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            AppleSales.objects.create(
                state=row['State'],
                region=row['Region'],
                iphone_sales=float(row['iPhone Sales (in million units)']),
                ipad_sales=float(row['iPad Sales (in million units)']),
                mac_sales=float(row['Mac Sales (in million units)']),
                wearables=float(row['Wearables (in million units)']),
                services_revenue=float(row['Services Revenue (in billion $)']),
            )
