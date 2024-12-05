import sdformat14 as sdf
import sys
import math
import random

from gz.math7 import Vector3d, Pose3d

world_file = './safmc.world'

num_small_pillar_obstacles = 10

drop_zone_coords = [
    (-6.2135, 5.65797),
    (-4.98951, -4.52046),
    (7.21815, 0.43991),
]

large_pillar_obstacle_coord = (3.22409, -3.19984)

bonus_zone_coord = (5.0, 8.5)

def generate_small_pillar_obstacle_coords(num_coords, min_distance, x_range, y_range):
    coords = []
    
    while len(coords) < num_coords:
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        new_coord = (x, y)
        if any(math.dist(new_coord, coord) < min_distance for coord in coords):
            continue
        if math.dist(new_coord, large_pillar_obstacle_coord) < 2:
            continue
        if math.dist(new_coord, bonus_zone_coord) < 5.3:
            continue
        if any(math.dist(new_coord, coord) < 1.3 for coord in drop_zone_coords):
            continue
        coords.append(new_coord)
    
    return coords


def load_model(filename: str):
    root = sdf.Root()
    try:
        root.load(filename)
    except sdf.SDFErrorsException as e:
        print(e, file=sys.stderr)
    return root.model()

def main():
    drop_zone_model = load_model('./models/drop_zone/model.sdf')
    large_pillar_obstacle_model = load_model('./models/large_pillar_obstacle/model.sdf')
    small_pillar_obstacle_model = load_model('./models/small_pillar_obstacle/model.sdf')

    root = sdf.Root()
    try:
        root.load(world_file)
    except sdf.SDFErrorsException as e:
        print(e, file=sys.stderr)

    world = root.world_by_index(0)

    # Drop Zone
    for i in range(3):
        drop_zone_model.set_name(f'drop_zone_{i:02d}')
        if i == 2:
            drop_zone_model.set_raw_pose(Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 1.570796))
        else:
            drop_zone_model.set_raw_pose(Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 0))
        world.add_model(drop_zone_model)

    # Large Pillar Obstacle
    large_pillar_obstacle_model.set_name(f'large_pillar_obstacle_{0:02d}')
    large_pillar_obstacle_model.set_raw_pose(Pose3d(large_pillar_obstacle_coord[0], large_pillar_obstacle_coord[1], 0, 0, 0, 0))
    world.add_model(large_pillar_obstacle_model)

    # Small Pillar Obstacle
    small_pillar_obstacle_coords = generate_small_pillar_obstacle_coords(
        num_small_pillar_obstacles,
        1.0 + 2 * 0.15,
        (-10.0, 10.0),
        (-6.0, 10.0),
    )
    for i in range(num_small_pillar_obstacles):
        small_pillar_obstacle_model.set_name(f'small_pillar_obstacle_{i:02d}')
        small_pillar_obstacle_model.set_raw_pose(Pose3d(small_pillar_obstacle_coords[i][0], small_pillar_obstacle_coords[i][1], 0, 0, 0, 0))
        world.add_model(small_pillar_obstacle_model)

    with open('new.world', "w") as f:
        f.write(root.to_string())

if __name__ == "__main__":
    main()
