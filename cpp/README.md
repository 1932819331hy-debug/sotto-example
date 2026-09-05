# C++ demo

Requires **CMake 3.20 or newer and a C++17 compiler**. Follow the [root quick start](../README.md#quick-start-with-python)
to install Sotto, run `sotto init` once, and set `DEMO_SECRET`.

Run from the **repository root**:

```sh
cmake -S cpp -B cpp/build
cmake --build cpp/build --config Release
sotto run -- ./cpp/build/demo
```

On Windows PowerShell, use `sotto run -- .\cpp\build\demo.exe` for the final command. Install Visual Studio Build Tools with the Desktop development with C++ workload. On macOS/Linux, use Clang or GCC.

Expected output:

```text
Sotto demo: secret loaded successfully.
```

The program reads `DEMO_SECRET` through the standard environment API and never
prints its value. A missing or empty value produces a helpful stderr message
and exit code `1`; any non-empty value returns `0`.

To see the failure, run the same program command without `sotto run --` while
`DEMO_SECRET` is unset in your shell.
