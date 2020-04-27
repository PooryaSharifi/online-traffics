"""
01 motors list of queue of points and times -> osrm match service -> edge nodes (if not lat, lng lookup (node -> latlng from osmium)) ->
    mid, dir + rho, frame -> net_node -> distance(lats, lngs) / deltaT = v -> the input
"""
import osmium as o
import pickle
locations = {}


class RoadLengthHandler(o.SimpleHandler):
    def __init__(self):
        super(RoadLengthHandler, self).__init__()

    # def way(self, w):
    #     for node in w.nodes:
    #         if node.ref == 5419662412:
    #             print('ewfdsa')
    #     # if 'highway' in w.tags:
    #     #     print(w.nodes[0].lat)
    #     #     w.nodes[0].lon
    #     #     print(w.nodes[0].ref)

    def node(self, n):
        locations[n.id] = (n.location.lat, n.location.lon)


def main(osmfile):
    h = RoadLengthHandler()
    h.apply_file(osmfile, locations=True)
    with open('locations.pkl') as f:
        pickle.dump(locations, f)
    return 0


if __name__ == '__main__':
    exit(main('/home/poorya/Documents/map/tehran.osm'))