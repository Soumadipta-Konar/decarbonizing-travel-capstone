import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"c:\Users\Soumadipta Konar\Desktop\Capstone Project- SA _26"
public_dir = os.path.join(data_dir, "Public Dataset")

trip_data = pd.read_csv(os.path.join(public_dir, "public_trip_data.csv"))
event_attr = pd.read_csv(os.path.join(public_dir, "public_trip_event_attributes.csv"))
event_log = pd.read_csv(os.path.join(public_dir, "public_trip_event_log.csv"))

# Mapping of countries to regions
country_regions = {
    'US': 'North America', 'CA': 'North America', 'MX': 'North America',
    'DE': 'Europe', 'GB': 'Europe', 'FR': 'Europe', 'IT': 'Europe', 'ES': 'Europe', 'NL': 'Europe',
    'BE': 'Europe', 'CH': 'Europe', 'AT': 'Europe', 'PL': 'Europe', 'RU': 'Europe', 'SE': 'Europe',
    'IE': 'Europe', 'CZ': 'Europe', 'DK': 'Europe', 'FI': 'Europe', 'HU': 'Europe', 'RO': 'Europe',
    'GR': 'Europe', 'PT': 'Europe',
    'SG': 'Asia', 'IN': 'Asia', 'JP': 'Asia', 'CN': 'Asia', 'KR': 'Asia', 'AE': 'Asia', 'SA': 'Asia',
    'TR': 'Asia', 'MY': 'Asia', 'TH': 'Asia', 'ID': 'Asia', 'VN': 'Asia', 'PH': 'Asia', 'HK': 'Asia', 'TW': 'Asia',
    'ZA': 'Africa',
    'AU': 'Oceania', 'NZ': 'Oceania',
    'BR': 'South America', 'AR': 'South America', 'CO': 'South America', 'PE': 'South America', 'CL': 'South America'
}
trip_data['DepartureRegion'] = trip_data['DepartureLocationCountry'].map(country_regions)
trip_data['ArrivalRegion'] = trip_data['ArrivalLocationCountry'].map(country_regions)
trip_data['Route'] = trip_data['DepartureLocationCity'] + " -> " + trip_data['ArrivalLocationCity']

print("==================================================")
print("1. EMISSIONS PROFILE")
print("==================================================")
total_trips = len(trip_data)
total_co2 = trip_data['TotalCO2e'].sum()
total_cost = trip_data['NetCosts'].sum()
dep_co2 = trip_data['Departure_CO2e'].sum()
ret_co2 = trip_data['Return_CO2e'].sum()
hotel_co2 = trip_data['Hotel_CO2e'].sum()
spend_co2 = trip_data['Spend_CO2e'].sum()

print(f"Total Trips: {total_trips:,}")
print(f"Total Emissions: {total_co2:,.2f} kgCO2e")
print(f"Total Costs: ${total_cost:,.2f}")
print(f"  - Departure CO2: {dep_co2:,.2f} kgCO2e ({dep_co2/total_co2*100:.1f}%)")
print(f"  - Return CO2: {ret_co2:,.2f} kgCO2e ({ret_co2/total_co2*100:.1f}%)")
print(f"  - Hotel CO2: {hotel_co2:,.2f} kgCO2e ({hotel_co2/total_co2*100:.1f}%)")
print(f"  - Spend CO2: {spend_co2:,.2f} kgCO2e ({spend_co2/total_co2*100:.1f}%)")

print("\nTransport Mode (ShippingTypeDescription) Detail:")
mode_stats = trip_data.groupby('ShippingTypeDescription').agg(
    Trips=('TripID', 'count'),
    Total_CO2=('TotalCO2e', 'sum'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Total_Cost=('NetCosts', 'sum'),
    Avg_Cost=('NetCosts', 'mean')
).sort_values(by='Total_CO2', ascending=False)
mode_stats['CO2_Share'] = mode_stats['Total_CO2'] / total_co2 * 100
mode_stats['Cost_Share'] = mode_stats['Total_Cost'] / total_cost * 100
print(mode_stats.to_markdown())

print("\n==================================================")
print("2. REGIONAL BENCHMARKING (ARRIVALS)")
print("==================================================")
region_stats = trip_data.groupby('ArrivalRegion').agg(
    Trips=('TripID', 'count'),
    Total_CO2=('TotalCO2e', 'sum'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Total_Cost=('NetCosts', 'sum'),
    Avg_Cost=('NetCosts', 'mean'),
    OutOfPolicy_Count=('OutOfPolicy', lambda x: (x == 'Yes').sum())
)
region_stats['OutOfPolicy_Rate_%'] = region_stats['OutOfPolicy_Count'] / region_stats['Trips'] * 100
region_stats['CO2_Share'] = region_stats['Total_CO2'] / total_co2 * 100
region_stats['Cost_Share'] = region_stats['Total_Cost'] / total_cost * 100
print(region_stats.sort_values(by='Total_CO2', ascending=False).to_markdown())

print("\n==================================================")
print("3. HOTSPOT IDENTIFICATION")
print("==================================================")
print("\nTop 10 High-Emission Routes:")
route_stats = trip_data.groupby(['Route', 'ShippingTypeDescription']).agg(
    Trips=('TripID', 'count'),
    Total_CO2=('TotalCO2e', 'sum'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Total_Cost=('NetCosts', 'sum')
).sort_values(by='Total_CO2', ascending=False).head(10)
print(route_stats.to_markdown())

print("\nTop 10 Business Units by Emissions:")
bu_stats = trip_data.groupby('BusinessUnit').agg(
    Trips=('TripID', 'count'),
    Total_CO2=('TotalCO2e', 'sum'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Total_Cost=('NetCosts', 'sum'),
    Avg_Cost=('NetCosts', 'mean')
).sort_values(by='Total_CO2', ascending=False)
print(bu_stats.to_markdown())

print("\n==================================================")
print("4. PAIN POINT & PROCESS INEFFICIENCIES")
print("==================================================")
# Check OutOfPolicy impact
print("Out of Policy vs In Policy:")
oop_compare = trip_data.groupby('OutOfPolicy').agg(
    Trips=('TripID', 'count'),
    Total_CO2=('TotalCO2e', 'sum'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Total_Cost=('NetCosts', 'sum'),
    Avg_Cost=('NetCosts', 'mean')
)
print(oop_compare.to_markdown())

# Merging attributes and trip data to see what attributes correlate with high emissions
merged = pd.merge(trip_data, event_attr, on='TripID')

print("\nTransportation Price Differences due to Changes:")
print(f"Total changes recorded: {len(event_attr[event_attr['NewModeOfTransportation'].notna()])}")
print(f"Sum of price differences: ${event_attr['TransportationPriceDifference'].sum():,.2f}")
print(f"Average price difference when change occurs: ${event_attr['TransportationPriceDifference'].mean():.2f}")

print("\nMost Common Reasons for Transportation Change:")
print(event_attr['ReasonForTransportationChange'].value_counts().to_markdown())

print("\nMost Common Reasons for Lodging Change (NewHotelSelection):")
print(event_attr['ReasonForNewHotel'].value_counts().to_markdown())

# Process log analysis - let's see which sequences of events (process paths) are most common.
# Find variants
print("\nTop 5 Process Variants in Event Log:")
# Group by TripID and get list of events ordered by StepOrder
trip_events = event_log.sort_values(by=['TripID', 'StepOrder']).groupby('TripID')['EventName'].apply(list)
# Convert list to tuple to make it hashable
trip_events_tuples = trip_events.apply(tuple)
variants = trip_events_tuples.value_counts().head(5)
for rank, (var, count) in enumerate(variants.items()):
    print(f"\nVariant {rank+1} (Count: {count}, {count/len(trip_events)*100:.2f}%):")
    print(" -> ".join(var))

print("\n==================================================")
print("5. QUANTIFYING RECOMMENDATIONS & POLICY SAVINGS")
print("==================================================")

# Policy 1: Flight class downgrade
# Let's see what we save if Business Class and First Class Flight trips are downgraded to Economy Class.
# To do this, let's find the average emission factor difference.
# Since we don't have distance, let's see if we can calculate the CO2 per cost ratio or average CO2 per trip for the same route!
# Let's group by route and see if we have both Economy and Business class trips on the same route.
route_class_compare = trip_data.groupby(['Route', 'ShippingTypeDescription']).agg(
    Avg_CO2=('TotalCO2e', 'mean'),
    Avg_Cost=('NetCosts', 'mean'),
    Trips=('TripID', 'count')
).unstack()

# Print some routes that have both Economy Flight and Business Class Flight
routes_with_both = route_class_compare[
    route_class_compare[('Trips', 'Economy Flight')].notna() & 
    route_class_compare[('Trips', 'Business Class Flight')].notna()
].head(10)
print("\nComparison of Economy vs Business Class on same routes:")
print(routes_with_both[[('Avg_CO2', 'Economy Flight'), ('Avg_CO2', 'Business Class Flight'), ('Avg_Cost', 'Economy Flight'), ('Avg_Cost', 'Business Class Flight')]].to_markdown())

# Let's calculate global averages to see emission differences.
avg_economy_co2 = trip_data[trip_data['ShippingTypeDescription'] == 'Economy Flight']['TotalCO2e'].mean()
avg_business_co2 = trip_data[trip_data['ShippingTypeDescription'] == 'Business Class Flight']['TotalCO2e'].mean()
avg_first_co2 = trip_data[trip_data['ShippingTypeDescription'] == 'First Class Flight']['TotalCO2e'].mean()

avg_economy_cost = trip_data[trip_data['ShippingTypeDescription'] == 'Economy Flight']['NetCosts'].mean()
avg_business_cost = trip_data[trip_data['ShippingTypeDescription'] == 'Business Class Flight']['NetCosts'].mean()
avg_first_cost = trip_data[trip_data['ShippingTypeDescription'] == 'First Class Flight']['NetCosts'].mean()

print(f"\nGlobal Flight class Averages:")
print(f"Economy: {avg_economy_co2:.2f} kgCO2e, ${avg_economy_cost:.2f}")
print(f"Business: {avg_business_co2:.2f} kgCO2e, ${avg_business_cost:.2f}")
print(f"First Class: {avg_first_co2:.2f} kgCO2e, ${avg_first_cost:.2f}")

# Policy 2: Shift from Flight to Train
# Let's check if there are routes where Train is used, and if those same routes are also flown.
print("\nRoutes with Train usage:")
train_routes = trip_data[trip_data['ShippingTypeDescription'] == 'Train']['Route'].unique()
print(train_routes)

# Let's see if flights are also taken on these routes!
train_flight_routes = trip_data[trip_data['Route'].isin(train_routes)].groupby(['Route', 'ShippingTypeDescription']).agg(
    Trips=('TripID', 'count'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Avg_Cost=('NetCosts', 'mean')
)
print(train_flight_routes.to_markdown())

# Policy 3: Shift Rental Cars to Hybrid or Electric
# Modes of transport:
# BMW 3 diesel: 6648 trips
# Volkswagen Golf diesel: 5452 trips
# Volkswagen Golf petrol: 4469 trips
# BMW 3 plugin hybrid: 1101 trips
# Fiat 500 electric: 1119 trips
print("\nRental Car emissions comparison:")
car_stats = trip_data[trip_data['ShippingTypeDescription'].isin([
    'BMW 3 diesel', 'Volkswagen Golf diesel', 'Volkswagen Golf petrol',
    'BMW 3 plugin hybrid', 'Fiat 500 electric'
])].groupby('ShippingTypeDescription').agg(
    Trips=('TripID', 'count'),
    Avg_CO2=('TotalCO2e', 'mean'),
    Avg_Cost=('NetCosts', 'mean')
)
print(car_stats.to_markdown())
