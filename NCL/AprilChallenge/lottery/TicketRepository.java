package backend;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TicketRepository {
    private static final String DB_URL = buildDbUrl();
    private static TicketRepository instance;

    private TicketRepository() {
        init();
    }

    private static String buildDbUrl() {
        String path = System.getenv("DB_PATH");
        if (path == null || path.isEmpty()) path = "./lottery.db";
        return "jdbc:sqlite:" + path;
    }

    public static synchronized TicketRepository getInstance() {
        if (instance == null) instance = new TicketRepository();
        return instance;
    }

    private void init() {
        try (Connection conn = DriverManager.getConnection(DB_URL)) {
            String sql = "CREATE TABLE IF NOT EXISTS tickets ("
                    + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    + "uuid INTEGER NOT NULL UNIQUE,"
                    + "numbers TEXT NOT NULL,"
                    + "purchased_at INTEGER NOT NULL,"
                    + "redeemed INTEGER NOT NULL DEFAULT 0,"
                    + "session_id TEXT NOT NULL DEFAULT ''"
                    + ")";
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(sql);
                // Migration: add session_id to existing databases that predate this column
                try {
                    stmt.execute("ALTER TABLE tickets ADD COLUMN session_id TEXT NOT NULL DEFAULT ''");
                } catch (SQLException ignored) {
                    // Column already exists — that's fine
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public synchronized Ticket createTicket(int[] numbers, String sessionId) {
        if (numbers == null) numbers = Lottery.drawNumbers(sessionId);
        String csv = Ticket.numbersToCsv(numbers);
        long now = System.currentTimeMillis();
        long uuid = Ticket.generateUUID(sessionId);
        String sql = "INSERT INTO tickets(uuid, numbers, purchased_at, redeemed, session_id) VALUES(?,?,?,0,?)";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setLong(1, uuid);
            ps.setString(2, csv);
            ps.setLong(3, now);
            ps.setString(4, sessionId);
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    long id = rs.getLong(1);
                    return new Ticket(id, uuid, numbers, now, false);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        throw new RuntimeException("Failed to create ticket");
    }

    public synchronized List<Ticket> getTicketsBySession(String sessionId) {
        String sql = "SELECT id, uuid, numbers, purchased_at, redeemed FROM tickets WHERE session_id = ? ORDER BY purchased_at DESC";
        List<Ticket> tickets = new ArrayList<>();
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, sessionId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    long id = rs.getLong("id");
                    long uuid = rs.getLong("uuid");
                    String csv = rs.getString("numbers");
                    int[] numbers = Ticket.csvToNumbers(csv);
                    long purchasedAt = rs.getLong("purchased_at");
                    boolean redeemed = rs.getInt("redeemed") != 0;
                    tickets.add(new Ticket(id, uuid, numbers, purchasedAt, redeemed));
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return tickets;
    }

    public synchronized Ticket getTicketByUUID(long uuidVal) {
        String sql = "SELECT id, uuid, numbers, purchased_at, redeemed FROM tickets WHERE uuid = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, uuidVal);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    long id = rs.getLong("id");
                    String csv = rs.getString("numbers");
                    int[] numbers = Ticket.csvToNumbers(csv);
                    long purchasedAt = rs.getLong("purchased_at");
                    boolean redeemed = rs.getInt("redeemed") != 0;
                    return new Ticket(id, uuidVal, numbers, purchasedAt, redeemed);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    public synchronized Ticket getTicketByUUID(long uuidVal, String sessionId) {
        String sql = "SELECT id, uuid, numbers, purchased_at, redeemed FROM tickets WHERE uuid = ? AND session_id = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, uuidVal);
            ps.setString(2, sessionId);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    long id = rs.getLong("id");
                    String csv = rs.getString("numbers");
                    int[] numbers = Ticket.csvToNumbers(csv);
                    long purchasedAt = rs.getLong("purchased_at");
                    boolean redeemed = rs.getInt("redeemed") != 0;
                    return new Ticket(id, uuidVal, numbers, purchasedAt, redeemed);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    public synchronized boolean redeemTicketByUuid(long uuidVal, String sessionId) {
        String sql = "UPDATE tickets SET redeemed = 1 WHERE uuid = ? AND session_id = ? AND redeemed = 0";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, uuidVal);
            ps.setString(2, sessionId);
            int updated = ps.executeUpdate();
            return updated > 0;
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}