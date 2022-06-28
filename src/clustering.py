import random as rand, math, numpy as np, matplotlib.pyplot as plt, csv
from point import Point

class KMeans:
    def __init__(self, geo_locs_, k_):
        self.geo_locations = geo_locs_
        self.k = k_
        self.clusters = self.debug = None
        self.means = []

    def next_random(self, index, points, clusters):
        dist = {}
        for point_1 in points:
            if self.debug: print(f"point_1: {point_1.latit} {point_1.longit}")
            for cluster in clusters.values():
                point_2 = cluster[0]
                if self.debug: print(f"point_2: {point_2.latit} {point_2.longit}")
                dist[point_1] = math.sqrt((point_1.latit - point_2.latit)**2 + (point_1.longit - point_2.longit)**2) if point_1 not in dist else dist[point_1] + math.sqrt((point_1.latit - point_2.latit)**2 + (point_1.longit - point_2.longit)**2)
        if self.debug:
            for key, value in dist.items(): print(f"({key.latit}, {key.longit}) ==> {value}")
        count_ = max_ = 0
        for key, value in dist.items():
            if count_ == 0:
                max_ = value
                max_point = key
                count_ += 1
            elif value > max_:
                max_ = value
                max_point = key
        return max_point

    def initial_means(self, points):
        point_ = rand.choice(points)
        if self.debug: print(f"point#0: {point_.latit} {point_.longit}")
        clusters = dict()
        clusters.setdefault(0, []).append(point_)
        points.remove(point_)
        for i in range(1, self.k):
            point_ = self.next_random(i, points, clusters)
            if self.debug: print(f"point#{i}: {point_.latit} {point_.longit}")
            clusters.setdefault(i, []).append(point_)
            points.remove(point_)
        self.means = self.compute_means(clusters)
        if self.debug:
            print("initial means:")
            self.print_means(self.means)

    def compute_means(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Point(0, 0)
            cnt = 0
            for point in cluster:
                mean_point.latit += point.latit
                mean_point.longit += point.longit
                cnt += 1
            mean_point.latit /= cnt
            mean_point.longit /= cnt
            means.append(mean_point)
        return means

    def assign_points(self, points):
        if self.debug: print("assign points")
        clusters = dict()
        for point in points:
            dist = []
            if self.debug: print(f"point({point.latit},{point.longit})")
            for mean in self.means: dist.append(math.sqrt((point.latit - mean.latit)**2 + (point.longit - mean.longit)**2))
            if self.debug: print(dist)
            cnt_ = index = 0
            min_ = dist[0]
            for d in dist:
                if d < min_:
                    min_ = d
                    index = cnt_
                cnt_ += 1
            if self.debug: print(f"index: {index}")
            clusters.setdefault(index, []).append(point)
        return clusters

    def update_means(self, means, threshold):
        for i in range(len(self.means)):
            mean_1 = self.means[i]
            mean_2 = means[i]
            if self.debug: print(f"mean_1({mean_1.latit},{mean_1.longit}), mean_2({mean_2.latit},{mean_2.longit})")          
            if math.sqrt((mean_1.latit - mean_2.latit)**2 + (mean_1.longit - mean_2.longit)**2) > threshold: return False
        return True

    def save(self, filename="output.csv"):
        with open(filename, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['latitude', 'longitude', 'cluster_id'])
            cluster_id = 0
            for cluster in self.clusters.values():
                for point in cluster: writer.writerow([point.latit, point.longit, cluster_id])
                cluster_id += 1

    def print_clusters(self, clusters=None):
        if not clusters: clusters = self.clusters
        cluster_id = 0
        for cluster in clusters.values():
            print(f"nodes in cluster #{cluster_id}")
            cluster_id += 1
            for point in cluster: print(f"point({point.latit},{point.longit})")

    def print_means(self, means):
        for point in means: print(f"{point.latit} {point.longit}")

    def fit(self, plot_flag):
        if len(self.geo_locations) < self.k: return -1
        points_ = [point for point in self.geo_locations]
        self.initial_means(points_)
        stop = False
        iterations = 1
        print("Starting K-Means...")
        while not stop:
            points_ = [point for point in self.geo_locations]
            clusters = self.assign_points(points_)
            if self.debug: self.print_clusters(clusters)
            means = self.compute_means(clusters)
            if self.debug:
                print("means:")
                self.print_means(means)
                print("update mean:")
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = []
                self.means = means
            iterations += 1
        print("K-Means is completed in {} iterations. Check outputs.csv for clustering results!".format(iterations))
        self.clusters = clusters
        if plot_flag:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
            cnt = 0
            for cluster in clusters.values():
                latits = longits = []
                for point in cluster:
                    latits.append(point.latit)
                    longits.append(point.longit)
                ax.scatter(longits, latits, s=60, c=colors[cnt], marker=markers[cnt])
                cnt += 1
            plt.show()
        return 0
