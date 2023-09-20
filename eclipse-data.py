import pystac_client
import planetary_computer

import pandas as pd

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
search = catalog.search(collections=["eclipse"], datetime="2022-03-01")
items = search.get_all_items()
print(f"Found {len(items)} item")
item = items[0]
item

asset = item.assets["data"]
df = pd.read_parquet(
    asset.href, storage_options=asset.extra_fields["table:storage_options"]
)

# filter where LocationName is "Irving & Clark (EB)"
df = df[df["LocationName"] == "Irving & Clark (EB)"]

# save data frame to csv
df.to_csv("irving-clark-sensor.csv", index=False)
print("Saved data to irving-clark-sensor.csv")