import sdformat14 as sdf
import sys
import math
import random

from gz.math7 import Vector3d, Pose3d

ENABLE_OBSTACLE = False

world_file = './worlds/safmc_d2.sdf.template'

num_small_pillar_obstacles = 15

drop_zone_coords = [
    (-6.2, 5.6),
    (-5.0, -4.5),
    (7.2, 0.4),
    (5, 8.5),  # Bonus zone
]

large_pillar_obstacle_coord = (3.22409, -3.19984)

bonus_zone_coord = (5.0, 8.5, 1.0)


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
        if math.dist(new_coord, bonus_zone_coord[0:2]) < 5.3:
            continue
        if any(math.dist(new_coord, coord) < 1.3 for coord in drop_zone_coords):
            continue
        coords.append(new_coord)

    return coords


def generate_random_entrance(entrance_size, left_coord, right_coord):
    entance_position = random.uniform(left_coord + entrance_size / 2 + 0.1, right_coord - entrance_size / 2 - 0.1)
    left_wall_length = entance_position - entrance_size / 2 - left_coord
    left_wall_position = left_coord + left_wall_length / 2.0
    right_wall_length = right_coord - entrance_size / 2 - entance_position
    right_wall_position = right_coord - right_wall_length / 2.0
    return left_wall_length, left_wall_position, right_wall_length, right_wall_position, entance_position


def load_model(filename: str):
    root = sdf.Root()
    try:
        root.load(filename)
    except sdf.SDFErrorsException as e:
        print(e, file=sys.stderr)
    return root.model()


def main():
    drop_zone_model = load_model('./models/drop_zone/model.sdf')
    large_pillar_obstacle_model = load_model(
        './models/large_pillar_obstacle/model.sdf')
    small_pillar_obstacle_model = load_model(
        './models/small_pillar_obstacle/model.sdf')
    bonus_zone_model = load_model('./models/bonus_zone/model.sdf')

    root = sdf.Root()
    root.load(world_file)
    world = root.world_by_index(0)

    # Drop Zone
    for i in range(4):
        drop_zone_model.set_name(f'drop_zone_{i+1}')
        if i == 2:
            drop_zone_model.set_raw_pose(
                Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 1.570796))
        else:
            drop_zone_model.set_raw_pose(
                Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 0))
        world.add_model(drop_zone_model)

    if ENABLE_OBSTACLE:
        # Large Pillar Obstacle
        large_pillar_obstacle_model.set_name(f'large_pillar_obstacle_1')
        large_pillar_obstacle_model.set_raw_pose(Pose3d(
            large_pillar_obstacle_coord[0], large_pillar_obstacle_coord[1], 0, 0, 0, 0))
        world.add_model(large_pillar_obstacle_model)

        # Small Pillar Obstacle
        small_pillar_obstacle_coords = generate_small_pillar_obstacle_coords(
            num_small_pillar_obstacles,
            1.0 + 2 * 0.15,
            (-10.0, 10.0),
            (-6.0, 10.0),
        )
        for i in range(num_small_pillar_obstacles):
            small_pillar_obstacle_model.set_name(f'small_pillar_obstacle_{i+1}')
            small_pillar_obstacle_model.set_raw_pose(Pose3d(
                small_pillar_obstacle_coords[i][0], small_pillar_obstacle_coords[i][1], 0, 0, 0, 0))
            world.add_model(small_pillar_obstacle_model)

    # Bonus zone
    entrance_size = 2
    left_wall_length, left_wall_position, right_wall_length, right_wall_position, entrance_position = generate_random_entrance(
        entrance_size, -5, 5)

    left_wall_link = bonus_zone_model.link_by_name("link")

    left_wall_collision = left_wall_link.collision_by_name("bonus_zone_front_wall_left_part_collision")
    left_wall_collision.geometry().box_shape().set_size(Vector3d(left_wall_length, 0.05, 2.0))
    left_wall_collision.set_raw_pose(Pose3d(left_wall_position, -1.5, 0, 0, 0, 0))

    right_wall_collision = left_wall_link.collision_by_name("bonus_zone_front_wall_right_part_collision")
    right_wall_collision.geometry().box_shape().set_size(Vector3d(right_wall_length, 0.05, 2.0))
    right_wall_collision.set_raw_pose(Pose3d(right_wall_position, -1.5, 0, 0, 0, 0))

    high_beam_collision = left_wall_link.collision_by_name("bonus_zone_high_beam_collision")
    high_beam_collision.geometry().box_shape().set_size(Vector3d(entrance_size, 0.5, 0.5))
    high_beam_collision.set_raw_pose(Pose3d(entrance_position, -1.25, 0.75, 0, 0, 0))

    left_wall_visual = left_wall_link.visual_by_name("bonus_zone_front_wall_left_part_visual")
    left_wall_visual.geometry().box_shape().set_size(Vector3d(left_wall_length, 0.05, 2.0))
    left_wall_visual.set_raw_pose(Pose3d(left_wall_position, -1.5, 0, 0, 0, 0))

    right_wall_visual = left_wall_link.visual_by_name("bonus_zone_front_wall_right_part_visual")
    right_wall_visual.geometry().box_shape().set_size(Vector3d(right_wall_length, 0.05, 2.0))
    right_wall_visual.set_raw_pose(Pose3d(right_wall_position, -1.5, 0, 0, 0, 0))

    high_beam_visual = left_wall_link.visual_by_name("bonus_zone_high_beam_visual")
    high_beam_visual.geometry().box_shape().set_size(Vector3d(entrance_size, 0.5, 0.5))
    high_beam_visual.set_raw_pose(Pose3d(entrance_position, -1.25, 0.75, 0, 0, 0))

    bonus_zone_model.set_raw_pose(
        Pose3d(bonus_zone_coord[0],
               bonus_zone_coord[1],
               bonus_zone_coord[2],
               0, 0, 0)
    )
    bonus_zone_model.set_name('bonus_zone')
    world.add_model(bonus_zone_model)

    with open('worlds/safmc_d2.sdf', "w") as f:
        f.write(root.to_string())


if __name__ == "__main__":
    main()
