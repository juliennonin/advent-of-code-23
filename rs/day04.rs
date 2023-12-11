fn parse_numbers_str(numbers_str: &str) -> Vec<i32> {
    return numbers_str
        .replace("  ", " ")
        .split(" ")
        .map(|number_str| number_str.parse().unwrap())
        .collect();
}

fn parse_line(line: &str) -> [Vec<i32>; 2] {
    let (_, numbers_str) = line.split_once(": ").unwrap();
    let (winning_str, numbers_str) = numbers_str.split_once(" | ").unwrap();

    let winning_numbers = parse_numbers_str(winning_str);
    let my_numbers = parse_numbers_str(numbers_str);

    return [winning_numbers, my_numbers];
}

fn main() {
    let cards: Vec<[Vec<i32>; 2]> = include_str!("../data/day04.txt")
        .lines()
        .map(|line| parse_line(line))
        .collect();

    println!("{:?}", cards[0]);
}
