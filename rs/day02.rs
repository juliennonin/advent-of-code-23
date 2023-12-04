const MAX_BALLS_NUMBER: [i32; 3] = [12, 13, 14];

type BallsSet = [i32; 3];

fn parse_set(set_line: &str) -> BallsSet {
    let mut set_array: BallsSet = [0; 3];
    set_line
        .split(", ")
        .map(|cube| {
            let (count, color) = cube.split_once(" ").unwrap();
            (count.parse().unwrap(), color)
        })
        .for_each(|(count, color)| match color {
            "red" => set_array[0] = count,
            "green" => set_array[1] = count,
            "blue" => set_array[2] = count,
            _ => panic!("Invalid color"),
        });
    return set_array;
}

fn infer_minimum_set(sets: Vec<BallsSet>) -> BallsSet {
    let minimum_set: Vec<i32> = (0..3)
        .map(|i| sets.iter().map(|set| set[i]).max().unwrap())
        .collect();
    return [minimum_set[0], minimum_set[1], minimum_set[2]];
}

fn parse_game(game_line: &str) -> (i32, BallsSet) {
    let (game_id_str, sets_str) = game_line.split_once(": ").unwrap();
    let game_id: i32 = game_id_str.split_once(" ").unwrap().1.parse().unwrap();
    let sets = sets_str
        .split("; ")
        .map(|set_line| parse_set(set_line))
        .collect::<Vec<BallsSet>>();
    return (game_id, infer_minimum_set(sets));
}

fn is_game_possible(minimum_set: BallsSet) -> bool {
    return minimum_set
        .iter()
        .zip(MAX_BALLS_NUMBER.iter())
        .all(|(a, b)| a <= b);
}

fn main() {
    let games: Vec<(i32, BallsSet)> = include_str!("../data/day02.txt")
        .lines()
        .map(|line| parse_game(line))
        .collect();

    let possible_games: i32 = games
        .iter()
        .filter(|(_, minimum_set)| is_game_possible(*minimum_set))
        .map(|(game_id, _)| game_id)
        .sum();

    let minimum_set_powers: i32 = games
        .iter()
        .map(|(_, minimum_set)| minimum_set.iter().product::<i32>())
        .sum();

    println!("Part 1 — {:?}", &possible_games);
    println!("Part 2 — {:?}", &minimum_set_powers)
}
