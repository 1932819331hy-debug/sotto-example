use std::env;
use std::process;

fn main() {
    let has_secret = env::var_os("DEMO_SECRET").is_some_and(|value| !value.is_empty());
    if !has_secret {
        eprintln!("DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.");
        process::exit(1);
    }

    println!("Sotto demo: secret loaded successfully.");
}
