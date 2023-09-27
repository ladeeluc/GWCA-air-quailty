import pystac_client
import planetary_computer

import pandas as pd

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
search = catalog.search(collections=["eclipse"], datetime="2021-07-01/2023-07-01", sortby=["date"])
items = search.get_all_items()
print(f"Found {len(items)} item")

for i, item in enumerate(items):
  asset = item.assets["data"]
  try:
    df = pd.read_parquet(
        asset.href, storage_options=asset.extra_fields["table:storage_options"]
    )

    # filter where LocationName is "Irving & Clark (EB)"
    df = df[df["LocationName"] == "Irving & Clark (EB)"]

    # save data frame to csv
    if i == 0:
      df.to_csv("irving-clark-sensor.csv", index=False, header=True)
    else:
      df.to_csv("irving-clark-sensor.csv", mode='a', index=False, header=False)
    print("Wrote data to irving-clark-sensor.csv")
  except FileNotFoundError as e:
    print("FlieNotFound:", e)