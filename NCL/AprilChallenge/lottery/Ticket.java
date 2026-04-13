package backend;

import com.google.gson.Gson;

public class Ticket {

    private static final Gson GSON = new Gson();

    private long id;
    private long uuid;
    private int[] numbers;
    private long purchasedAt;
    private boolean redeemed;

    public Ticket(long id, long uuid, int[] numbers, long purchasedAt, boolean redeemed) {
        this.id = id;
        this.uuid = uuid;
        this.numbers = numbers;
        this.purchasedAt = purchasedAt;
        this.redeemed = redeemed;
    }

    /**
     * Generates a ticket UUID using the session's PRNG. The UUID is the upper 32 bits
     * of the next Random output, stored as an unsigned long.
     *
     * @param sessionId The session identifier.
     * @return A UUID derived from the session's java.util.Random instance.
     */
    public static long generateUUID(String sessionId) {
        return Integer.toUnsignedLong(Lottery.getRandom(sessionId).nextInt());
    }

    public long getUUID() { return uuid; }
    public long getId() { return id; }
    public int[] getNumbers() { return numbers; }
    public long getPurchasedAt() { return purchasedAt; }
    public boolean isRedeemed() { return redeemed; }

    public void setId(long id) { this.id = id; }
    public void setRedeemed(boolean redeemed) { this.redeemed = redeemed; }

    /**
     * Utility method to convert numbers to/from CSV strings for database storage.
     */
    public static String numbersToCsv(int[] numbers) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < numbers.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(numbers[i]);
        }
        return sb.toString();
    }

    /**
     * Utility method to convert numbers to/from CSV strings for database storage.
     */
    public static int[] csvToNumbers(String csv) {
        String[] parts = csv.split(",");
        int[] numbers = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            numbers[i] = Integer.parseInt(parts[i]);
        }
        return numbers;
    }

    public String toJson() {
        return GSON.toJson(this);
    }
}