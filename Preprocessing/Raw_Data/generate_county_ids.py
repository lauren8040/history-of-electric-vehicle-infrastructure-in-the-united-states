import json
import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


#https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt#:~:text=WISCONSIN%0A%20%20%20%20%20%20%2056%20%20%20%20%20%20%20%20WYOMING-,county%2Dlevel,-place%0A%20%20FIPS%20code
#https://public.opendatasoft.com/explore/dataset/us-county-boundaries/export/?flg=en-us&disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InVzLWNvdW50eS1ib3VuZGFyaWVzIiwib3B0aW9ucyI6eyJmbGciOiJlbi11cyIsImRpc2p1bmN0aXZlLnN0YXRlZnAiOnRydWUsImRpc2p1bmN0aXZlLmNvdW50eWZwIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lbHNhZCI6dHJ1ZSwiZGlzanVuY3RpdmUuc3R1c2FiIjp0cnVlLCJkaXNqdW5jdGl2ZS5zdGF0ZV9uYW1lIjp0cnVlfX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImFsYW5kIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJzdGF0ZWZwIiwibWF4cG9pbnRzIjo1MCwic29ydCI6IiJ9XSwidGltZXNjYWxlIjoiIiwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D
      
def point_inside_polygon(x, y, poly):
    """
    Determine if a point is inside a given polygon.

    Args:
    x (float): x-coordinate of the point.
    y (float): y-coordinate of the point.
    poly (list of tuples): List of (x, y) tuples defining the polygon.

    Returns:
    bool: True if the point is inside the polygon, False otherwise.
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def plot_boundary_and_point(perimeter, point):
    """
    Plot the boundary defined by the perimeter and the given point.

    Args:
    perimeter (list of tuples): List of (x, y) tuples defining the perimeter.
    point (tuple): (x, y) coordinates of the point.
    """
    fig, ax = plt.subplots()

    # Plot boundary
    perimeter.append(perimeter[0])  # Close the polygon
    poly = Polygon(perimeter, closed=True, edgecolor="b", fill=False)
    ax.add_patch(poly)

    # Plot point
    ax.plot(point[0], point[1], "ro")  # Red circle for the point

    # Set axis limits
    ax.set_xlim(
        min(point[0] for point in perimeter) - 1,
        max(point[0] for point in perimeter) + 1,
    )
    ax.set_ylim(
        min(point[1] for point in perimeter) - 1,
        max(point[1] for point in perimeter) + 1,
    )

    point_inside = point_inside_polygon(point[0], point[1], perimeter)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Boundary and Point:  Inside : {point_inside}")
    plt.grid(True)
    plt.show()


def load_county_records(json_path_or_dir):
    """
    Load county boundary records from a single JSON file (array) or
    from a directory containing multiple chunk files. Returns a list of records.
    """
    if os.path.isdir(json_path_or_dir):
        records = []
        for name in sorted(os.listdir(json_path_or_dir)):
            if not name.endswith(".json"):
                continue
            with open(os.path.join(json_path_or_dir, name)) as f:
                records.extend(json.load(f))
        return records
    else:
        with open(json_path_or_dir) as f:
            return json.load(f)


def generate_county_df(json_link,df):
    
    #Reading Json
    data = load_county_records(json_link)
    
    #Preparing Data
    df = pd.read_csv(df)
    cols = ["OBJECTID", "longitude", "latitude", "city", "state"]
    df = df[cols]
    df.sort_values(by=["city"])
    df["completed"] = [False] * len(df)
    df["json_string"] = ["-1"] * len(df)

    num_completed = 0
    for j, k in tqdm(enumerate(data), total=len(data)):
        boundary = k["geo_shape"]["geometry"]["coordinates"][0]
        multi_pol = k["geo_shape"]["geometry"]["type"]
        boundaries = []
        if len(boundary) == 1:
            boundaries.append(boundary[0])
        elif multi_pol == "MultiPolygon":
            for bound in boundary:
                boundaries.append(bound)
        else:
            boundaries.append(boundary)

        for index, row in df.iterrows():
            if row["completed"]:
                continue
            if row["state"] != k["stusab"]: #verifies that the state for county in json file matches state in station data
                continue
            for bound in boundaries:
                if point_inside_polygon(row["longitude"], row["latitude"], bound):
                    print(
                        f"{row['city']}, {row['state']} is in County: {k['name']}, State: {k['state_name']}"
                    )
                    tmp_k = k.copy()
                    del tmp_k["geo_shape"]
                    df.at[index, "json_string"] = json.dumps(tmp_k)
                    # plot_boundary_and_point(bound, (row["longitude"], row["latitude"])) #optional plotting of the station inside the found county
                    df.at[index, "completed"] = True
                    num_completed += 1
                    break
            if num_completed % 1000 == 0:
                df.to_csv(f"tmp_{num_completed}_output.csv", index=False)

    df.to_csv("county_results.csv")


#WARNING: Running this function will take about 2 hours to complete when feeding in the raw dataframe
default_json_path = 'Preprocessing/Raw_Data/us-county-boundaries-chunks'
if not os.path.isdir(default_json_path):
    default_json_path = 'Preprocessing/Raw_Data/us-county-boundaries.json'

generate_county_df(json_link = default_json_path, 
                   df = 'Preprocessing/Raw_Data/Alternative_Fueling_Stations_Raw_Data.csv')