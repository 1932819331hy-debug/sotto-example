# C# demo

Requires **.NET 8 SDK or newer**. Follow the [root quick start](../README.md#quick-start-with-python)
to install Sotto, run `sotto init` once, and set `DEMO_SECRET`.

Run from the **repository root**:

```sh
sotto run -- dotnet run --project csharp/Demo.csproj
```

The SDK builds the project on first run. It has no external package dependencies.

Expected output:

```text
Sotto demo: secret loaded successfully.
```

The program reads `DEMO_SECRET` through the standard environment API and never
prints its value. A missing or empty value produces a helpful stderr message
and exit code `1`; any non-empty value returns `0`.

To see the failure, run the same program command without `sotto run --` while
`DEMO_SECRET` is unset in your shell.
