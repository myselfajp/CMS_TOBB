from serpapi import GoogleSearch
import json

# params = {
#     "engine": "google_maps",
#     "q": "izmir çeşme",
"@41.0687783,29.0110649,13z"
"@38.4708221,27.0892593,14z"
"@38.518399599999995,27.138240399999997z"
#     "type": "search",
#     'hl': 'tr',
#     "api_key": "4ff1227f026bf5e610fb7cc6275ba237396cd2cdf3e4fcadf17c718ea2ed7b0c",
#     "start" : 0,
#     }
params={
    "engine": "google_maps",
    "q": "izmir çeşme",
    "type": "search",
    'hl': 'tr',
    "api_key": "4ff1227f026bf5e610fb7cc6275ba237396cd2cdf3e4fcadf17c718ea2ed7b0c",
    }

search = GoogleSearch(params)
results = search.get_dict()["place_results"]
# la=results['latitude']
# lo=results['longitude']
# ll=f"@{la},{lo}z"
results = json.dumps(results, indent=2)
print(results)