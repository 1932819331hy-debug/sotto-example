package main

import (
	"fmt"
	"os"
)

func main() {
	if os.Getenv("DEMO_SECRET") == "" {
		fmt.Fprintln(os.Stderr, "DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.")
		os.Exit(1)
	}

	fmt.Println("Sotto demo: secret loaded successfully.")
}
