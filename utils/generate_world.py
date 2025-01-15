import sdformat14 as sdf
import sys
import math
import random

from gz.math7 import Vector3d, Pose3d

world_file = './worlds/safmc_d2.sdf.template'

num_small_pillar_obstacles = 10

drop_zone_coords = [
    (-6.2135, 5.65797),
    (-4.98951, -4.52046),
    (7.21815, 0.43991),
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
    entance_position = random.uniform(left_coord + entrance_size / 2, right_coord - entrance_size / 2)
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
    for i in range(3):
        drop_zone_model.set_name(f'drop_zone_{i:02d}')
        if i == 2:
            drop_zone_model.set_raw_pose(
                Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 1.570796))
        else:
            drop_zone_model.set_raw_pose(
                Pose3d(drop_zone_coords[i][0], drop_zone_coords[i][1], 0, 0, 0, 0))
        world.add_model(drop_zone_model)

    # Large Pillar Obstacle
    large_pillar_obstacle_model.set_name(f'large_pillar_obstacle_{0:02d}')
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
        small_pillar_obstacle_model.set_name(f'small_pillar_obstacle_{i:02d}')
        small_pillar_obstacle_model.set_raw_pose(Pose3d(
            small_pillar_obstacle_coords[i][0], small_pillar_obstacle_coords[i][1], 0, 0, 0, 0))
        world.add_model(small_pillar_obstacle_model)

    # Bonus zone
    entrance_size = 2
    left_wall_length, left_wall_position, right_wall_length, right_wall_position, entrance_position = generate_random_entrance(entrance_size, -5, 5)

    for i_link in range(bonus_zone_model.link_count()):
        link = bonus_zone_model.link_by_index(i_link)
        
        # Change collision geometry
        for i_collision in range(link.collision_count()):
            collision = link.collision_by_index(i_collision)
            if collision.name() == 'bonus_zone_front_wall_left_part_collision':
                collision.geometry().box_shape().set_size(
                    Vector3d(left_wall_length, 0.05, 2.0)
                )
                collision.set_raw_pose(Pose3d(left_wall_position, -1.5, 0, 0, 0, 0))
            elif collision.name() == 'bonus_zone_front_wall_right_part_collision':
                collision.geometry().box_shape().set_size(
                    Vector3d(right_wall_length, 0.05, 2.0)
                )
                collision.set_raw_pose(Pose3d(right_wall_position, -1.5, 0, 0, 0, 0))
            elif collision.name() == 'bonus_zone_high_beam_collision':
                collision.geometry().box_shape().set_size(
                    Vector3d(entrance_size, 0.5, 0.5)
                )
                collision.set_raw_pose(Pose3d(entrance_position, -1.25, 0.75, 0, 0, 0))
        
        # Change visual geometry
        for i_visual in range(link.visual_count()):
            visual = link.visual_by_index(i_visual)
            if visual.name() == 'bonus_zone_front_wall_left_part_visual':
                visual.geometry().box_shape().set_size(
                    Vector3d(left_wall_length, 0.05, 2.0)
                )
                visual.set_raw_pose(Pose3d(left_wall_position, -1.5, 0, 0, 0, 0))
            elif visual.name() == 'bonus_zone_front_wall_right_part_visual':
                visual.geometry().box_shape().set_size(
                    Vector3d(right_wall_length, 0.05, 2.0)
                )
                visual.set_raw_pose(Pose3d(right_wall_position, -1.5, 0, 0, 0, 0))
            elif visual.name() == 'bonus_zone_high_beam_visual':
                visual.geometry().box_shape().set_size(
                    Vector3d(entrance_size, 0.5, 0.5)
                )
                visual.set_raw_pose(Pose3d(entrance_position, -1.25, 0.75, 0, 0, 0))

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
