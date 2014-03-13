TODO
====

2014-03-13
----------

- https://github.com/ethz-asl/libpointmatcher
- http://pointclouds.org/documentation/tutorials/#registration-tutorial
- consider points < 20m as clean, merge live stream p3d
  for the others, filter points < 20m and do ICP
- atlaas.cpp:311 (atlaas::merge) : add field number of swap to classify
  if a cell is stable or not and it first seen / first swap time
- atlaas.cpp:43  (atlaas::merge) : add I/O for playback (rosbag like)
- drop atlaas::map use array<gdal>
- unbounded index_pix modulo to find the tile
- break tile frame (-1,-1) -> (0,0)
- use tile(0,0) as georeference utm(x0,y0)


07-02-2014
----------

* after benchmark with `valgrind --tool=callgrind atlaas`*

![callgrind](http://homepages.laas.fr/pkoch/wm/callgrind.png "callgrind")

- divide atlaas in 2 class
  - 1 map manager -> {9->25} maplets of 256x256 px (standard)
  - speed up and simplify slide_to / sub_{load,save}
  - externalize export8u, save all
  - let another node ``gdal_merge.py atlaas.*x*.tif`` for display (no critic)
  - use a map<index, cell_info> for ground-swap instead of vector?
- use standard convention for maplets names ``$PWD/$zoom/$x/$y.tif``
  - http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_servers
