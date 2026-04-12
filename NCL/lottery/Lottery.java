package backend;

import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

public class Lottery {

    // Each session gets its own isolated Random instance.
    // Note: this map never shrinks — for a short-lived CTF deployment this is fine.
    private static final ConcurrentHashMap<String, Random> sessions = new ConcurrentHashMap<>();

    private Lottery() {}

    /**
     * Gets (or creates) a per-session Random instance. Each session's PRNG state is
     * completely isolated from all other sessions.
     *
     * @param sessionId The session identifier from the session cookie.
     * @return A Random instance isolated to this session.
     */
    public static Random getRandom(String sessionId) {
        return sessions.computeIfAbsent(sessionId, k -> new Random());
    }

    /**
     * Draws 6 lottery numbers between 0 and 99 inclusive using this session's PRNG.
     *
     * @param sessionId The session identifier.
     * @return An array of 6 integers representing the drawn lottery numbers.
     */
    public static int[] drawNumbers(String sessionId) {
        int[] numbers = new int[6];
        Random rand = getRandom(sessionId);
        for (int i = 0; i < 6; i++) {
            numbers[i] = rand.nextInt(100);
        }
        return numbers;
    }
}