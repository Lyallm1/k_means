import os, argparse, pandas as pd
from clustering import KMeans
from point import Point

def main(dataset_fn, output_fn, clusters_no):
    geo_locs = []
    for _, row in pd.read_csv(dataset_fn).iterrows(): geo_locs.append(Point(float(row['LAT']), float(row['LON'])))
    model = KMeans(geo_locs, clusters_no)
    print("No of points are less than cluster number!") if model.fit(true) == -1 else model.save(output_fn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run k-means for location data", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, default='NYC_Free_Public_WiFi_03292017.csv', dest='input', help='input location file name')
    parser.add_argument('--output', type=str, default='output.csv', dest='output',  help='clusters output file name')
    parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
    args = parser.parse_args()
    main(os.path.join('data', args.input), args.output, args.clusters)
