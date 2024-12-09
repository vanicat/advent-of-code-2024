use std::fs;

const EXEM:&str = "\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
";

fn main() {
    let exem_pb = read_pbs(String::from(EXEM));
    
    match first_error(&exem_pb[0]) {
        Some(x) => {
            println!("{}", x);
        },
        None => {
            println!("nothing");
        }
    }
}

fn read_pbs(contents:String) -> Vec<Vec<i32>> {
    let mut result:Vec<Vec<i32>> = Vec::new();
    let lines = contents.split("\n");
    for line in lines {
        let line = line.split_whitespace();
        let mut new_line:Vec<i32> = Vec::new();
        for v in line {
            new_line.push(v.parse().expect("expected a number"));
        }
        result.push(new_line);
    }
    
    return result

}

fn first_error(report:&Vec<i32>) -> Option<usize> {
    if report.len() <= 1 {
        return None
    } else {
        let increasing:bool = report[0] < report[1];
        for i in 2..report.len() {
            if (increasing && report[i-1] >= report[i]) || (! increasing && report[i-1] <= report[i])
                 || report[i-1] - report[i] > 3 || report[i] - report[i-1] > 3 {
                    return Some(i)
            }
        }
        return None
    }
}