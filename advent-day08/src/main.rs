use std::{collections::{HashMap, HashSet}, fs, isize, iter::{self, Iterator}};
use colored::Colorize;

const EXEM:&str = "\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
";

fn main() {
    let pb = reading(EXEM);
    println!("{:?} {} {}", pb.antena, pb.height, pb.width );

    debug_assert_eq!(pb.height, 12);
    debug_assert!(find_spot(&(2, 5), &(4, 3), &pb).contains(&(6, 1)));
    debug_assert!(! find_spot(&(2, 10), &(4, 12), &pb).contains(&(6, 14)));
    debug_assert!(find_spot(&(7, 5), &(4, 3), &pb).contains(&(10, 7)));
    
    let exem_spot = find_all_spot(&pb);

    println!("{:?} {}", exem_spot, exem_spot.len());

    let exem_spot2 = find_all_spot2(&pb);
    
    print_map_and_spot(&pb, &exem_spot2);

    println!("{}", exem_spot2.len());

    let file_path: &str="../input-08-1.txt";
    let contents: String = fs::read_to_string(file_path)
            .expect("Should have been able to read the file");

    let map = reading(&contents);
    let spot = find_all_spot(&map);

    // print_map_and_spot(&map, &spot);

    // println!("spots {:?}", spot);

    println!("soluce 1 is {}", spot.len());

    let spot2 = find_all_spot2(&map);

    // print_map_and_spot(&map, &spot2);

    println!("soluce 2 is {}", spot2.len());
}

struct Map {
    antena: HashMap<char, Vec<(usize, usize)>>,
    width: usize,
    height: usize   
}

fn reading(content: &str) -> Map {
    let mut antena: HashMap<char, Vec<(usize, usize)>> = HashMap::new();
    let mut width: Option<usize> = None;
    let height: Option<usize>;

    let mut i: usize = 0;
    
    for line in content.split("\n") {
        let mut j: usize = 0;
        for c in line.chars() {
            if c != '.' {
                if ! antena.contains_key(&c) {
                    antena.insert(c, Vec::new());
                }

                match antena.get_mut(&c) {
                    None => panic!("Should not be empty"),
                    Some(tab) => {
                        tab.push((i, j));
                    }
                }
                
            }
            j = j + 1;
        }
        i = i + 1;
        if j != 0 { width = Some(j)}
        else { i = i - 1 };

    }
    height = Some(i);
    return Map {
        antena: antena,
        width: width.expect("should have a width"),
        height: height.expect("should have a height")
    }
}

fn find_spot(pos1: &(usize, usize), pos2: &(usize, usize), map:&Map) -> Vec<(usize, usize)> {
    let mut result: Vec<(usize, usize)> = Vec::new();

    let (i1, j1) = pos1;
    let (i2, j2) = pos2;

    let i1: isize = *i1 as isize;
    let j1: isize = *j1 as isize;
    let i2: isize = *i2 as isize;
    let j2: isize = *j2 as isize;

    for (i, j) in [(2 * i1 - i2, 2 * j1 - j2), (2 * i2 - i1, 2 * j2 - j1)] {
        if 0 <= i && i < map.height as isize && 0 <= j && j < map.width as isize {
            result.push((i as usize, j as usize));
        }
    } 

    return  result;

}

fn simplify_delta(delta_i: isize, delta_j: isize) -> (isize, isize) {
    let mut a = delta_i.abs();
    let mut b = delta_j.abs();
    while b != 0 {
        let tmp = a % b;
        a = b;
        b = tmp;
    }
    return (delta_i / a, delta_j / a);
}


fn find_all_spot(map: &Map) -> HashSet<(usize, usize)> {
    let mut result: HashSet<(usize, usize)> = HashSet::new();
    for (_freq, pos_vec) in &map.antena {
        for pos1 in pos_vec {
            for pos2 in pos_vec {
                if pos1 < pos2 {
                    for blind_spot in find_spot(pos1, pos2, map) {
                        result.insert(blind_spot);
                    }
                }
            }
        }
    }
    return result;
}


fn find_spot2(pos1: &(usize, usize), pos2: &(usize, usize), map:&Map) -> impl Iterator<Item = (usize, usize)> {
    let (i1, j1) = pos1;
    let (i2, j2) = pos2;

    let height = map.height as isize;
    let width = map.width as isize;

    let delta_i: isize = (*i1 as isize) - (*i2 as isize);
    let delta_j: isize = (*j1 as isize) - (*j2 as isize);

    let (delta_i, delta_j) = simplify_delta(delta_i, delta_j);

    let mut posi = *i1 as isize;
    let mut posj = *j1 as isize;

    while posi >= 0 && posj >= 0 && posi < height && posj < width {
        posi -= delta_i;
        posj -= delta_j;
    }

    iter::from_fn(move || {
        posi += delta_i;
        posj += delta_j;
    
        if posi >= 0 && posj >= 0 && posi < height && posj < width {
            return Some((posi as usize, posj as usize))
        } else {
            return None
        }
    })

}


fn find_all_spot2(map: &Map) -> HashSet<(usize, usize)> {
    let mut result: HashSet<(usize, usize)> = HashSet::new();
    for (_freq, pos_vec) in &map.antena {
        for pos1 in pos_vec {
            for pos2 in pos_vec {
                if pos1 < pos2 {
                    for blind_spot in find_spot2(pos1, pos2, map) {
                        result.insert(blind_spot);
                    }
                    // println!("{} ({}, {}) ({}, {})", _freq, pos1.0, pos1.1, pos2.0, pos2.1);
                    // print_map_and_spot(&map, &result);

                }
            }
        }
    }
    return result;
}


fn print_map_and_spot(map: &Map, spot: &HashSet<(usize, usize)>) {
    let mut to_disp: Vec<Vec<char>> = Vec::new();
    for _i in 0..map.height {
        to_disp.push(['.'].repeat(map.width.try_into().unwrap()));
    }

    for (freq, coords) in &map.antena {
        for (i, j) in coords.as_slice() {
            to_disp[*i][*j] = *freq
        }
    }

    for i in 0..map.height {
        for j in 0..map.width {
            let c = String::from(to_disp[i][j]);
            if spot.contains(&(i, j)) {
                if c == "." {
                    print!("{}", "#".color("pink"));
                } else {
                    print!("{}", c.color("pink"));
                }
            } else {
                print!("{}", c);
            }
        }
        println!("");
    }
}