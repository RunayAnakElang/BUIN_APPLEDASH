from django.shortcuts import render
from .models import AppleSales
import pandas as pd

def dashboard(request):
    qs = AppleSales.objects.all().values()
    df = pd.DataFrame(list(qs))

    # Grafik 1: Penjualan per region (dalam unit)
    region_sales = df.groupby('region')[
        ['iphone_sales', 'ipad_sales', 'mac_sales', 'wearables']
    ].sum().reset_index()

    # Grafik 2: Total semua produk (global)
    total_sales = df[['iphone_sales', 'ipad_sales', 'mac_sales', 'wearables']].sum()

    # Grafik 3: Market Potential Index per Region
    region_totals = df.groupby('region')[
        ['iphone_sales', 'ipad_sales', 'mac_sales', 'wearables']
    ].sum()
    
    market_index = {}
    for region in region_totals.index:
        region_data = region_totals.loc[region]
        total_region_sales = region_data.sum()
        
        market_index[region] = {}
        for product in ['iphone_sales', 'ipad_sales', 'mac_sales', 'wearables']:
            if total_region_sales > 0:
                market_index[region][product] = round((region_data[product] / total_region_sales) * 100, 1)
            else:
                market_index[region][product] = 0

    context = {
        'region_state_sales': region_sales.to_dict(orient='records'),
        'total_sales': total_sales.to_dict(),
        'market_potential_index': market_index,
        'total_units': total_sales.sum()
    }
    return render(request, 'visualisasi/dashboard.html', context)
