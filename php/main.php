<?php

$secret = getenv('DEMO_SECRET');

if ($secret === false || $secret === '') {
    fwrite(STDERR, "DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.\n");
    exit(1);
}

echo "Sotto demo: secret loaded successfully.\n";
