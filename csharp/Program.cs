string? secret = Environment.GetEnvironmentVariable("DEMO_SECRET");

if (string.IsNullOrEmpty(secret))
{
    Console.Error.WriteLine("DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.");
    return 1;
}

Console.WriteLine("Sotto demo: secret loaded successfully.");
return 0;
