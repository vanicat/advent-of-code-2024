use std::collections::HashMap;

const EXEM:&str = "125 17";


fn main() {
    let mut pb_exem: HashMap<u128, u64> = read_input(EXEM);
    println!("{:?}", pb_exem);

    for _i in 1..=25 {
        pb_exem = blink(pb_exem);
    }
    println!("exemple after 25: {}", pb_exem.len());

    let mut pb: HashMap<u128, u64> = read_input("8793800 1629 65 5 960 0 138983 85629");

    for i in 1..=75 {
        pb = blink(pb);
        if i % 5 == 0 {
           println!("problem after {i}: {}", len_pb(pb.clone()));       
        }
    }

}

fn read_input(pb:&str) -> HashMap<u128, u64>{
    let nbs = pb.split(' ');
    let mut pb_exem: HashMap<u128, u64> = HashMap::new();

    for nb in nbs {
        let nb = &nb.parse().expect("should be an int");
        let old = pb_exem.get(nb);
        pb_exem.insert(*nb, old.unwrap_or(&0) + 1);
    }
    return pb_exem;

}

fn len_pb(pb: HashMap<u128, u64>) -> u64 {
    let mut res: u64 = 0;

    for val in pb.into_values() {
        res += val
    }

    return res;
}

fn add(mut map:HashMap<u128, u64>, value:u128, nb:u64) -> HashMap<u128, u64>{
    if map.contains_key(&value) {
        if let Some(x) = map.get_mut(&value) {
            *x = *x + nb
        }
    } else {
        let _a = map.insert(value, nb);
    }
    return map;
}

fn blink(pb: HashMap<u128, u64>) -> HashMap<u128, u64> {
    let mut result: HashMap<u128, u64> = HashMap::new();
    for (value, nb) in pb {
        if value == 0 {
            result = add(result, 1, nb);
        } else {
            let len: u32 = value.ilog10() + 1;
            if len % 2 == 0 {
                let div: u128 = 10_u128.pow(len / 2);
                result = add(result, value.div_euclid(div), nb);
                result = add(result, value % div, nb);
            } else {
                result = add(result, value * 2024, nb);
            }
        }
    }
    return result
}