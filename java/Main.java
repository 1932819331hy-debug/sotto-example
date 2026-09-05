public class Main {
    public static void main(String[] args) {
        String secret = System.getenv("DEMO_SECRET");
        if (secret == null || secret.isEmpty()) {
            System.err.println("DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.");
            System.exit(1);
        }

        System.out.println("Sotto demo: secret loaded successfully.");
    }
}
