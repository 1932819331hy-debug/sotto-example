# Rust demo

Requires **Rust and Cargo** (stable toolchain). Follow the [root quick start](../README.md#quick-start-with-python)
to install Sotto, run `sotto init` once, and set `DEMO_SECRET`.

Run from the **repository root**:

```sh
sotto run -- cargo run --quiet --manifest-path rust/Cargo.toml
```

Cargo compiles and runs this single binary crate using only the Rust standard library. No external crates are needed.

Expected output:

```text
Sotto demo: secret loaded successfully.
```

The program reads `DEMO_SECRET` through the standard environment API and never
prints its value. A missing or empty value produces a helpful stderr message
and exit code `1`; any non empty value returns `0`.

To see the failure, run the same program command without `sotto run --` while
`DEMO_SECRET` is unset in your shell.
