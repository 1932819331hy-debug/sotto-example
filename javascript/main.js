const secret = process.env.DEMO_SECRET;

if (!secret) {
  console.error("DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.");
  process.exit(1);
}

console.log("Sotto demo: secret loaded successfully.");
