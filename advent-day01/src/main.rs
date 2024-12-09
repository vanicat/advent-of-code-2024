use std::fs;

fn main() {
    let file_path="../input-01-1.txt";
    // --snip--
    println!("In file {file_path}");

    let contents: String = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let (mut left_content, mut right_content) = lines(&contents);

    left_content.sort();
    right_content.sort();

    let mut c: u64  = 0;

    for (l, r) in left_content.iter().zip(right_content.iter()) {
        if l < r {
            c += r - l;
        } else {
            c += l - r;
        }
    }
    println!("{c}");

    let mut c: u64  = 0;

    for l in left_content {
        for r in right_content.as_slice() {
            if l == *r {
                c += l;
            }
        }
    }
    println!("{c}");
}

fn lines(contents: &String) -> (Vec<u64 >, Vec<u64 >){
    let mut left_result: Vec<u64 > = Vec::new();
    let mut right_result: Vec<u64 > = Vec::new();

    let contents = contents.split("\n");
    for line in contents {
        let line: Vec<&str> = line.trim().split_whitespace().collect();
        if line.len() > 0 {
            left_result.push(line[0].parse().expect("not an int"));
            right_result.push(line[1].parse().expect("not an int"));
        }
    }

    (left_result, right_result)
}