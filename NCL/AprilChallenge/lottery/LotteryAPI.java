package backend;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.List;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSyntaxException;

public class LotteryAPI {

    private static final int DEFAULT_PORT = 8080;

    public static void main(String[] args) throws IOException {
        // Just some boilerplate to start an HTTP server, nothing worth seeing here.
        int port = DEFAULT_PORT;
        String envPort = System.getenv("PORT");
        if (envPort != null) {
            try { port = Integer.parseInt(envPort); } catch (NumberFormatException ignored) {}
        }
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/buy", new BuyHandler());
        server.createContext("/redeem", new RedeemHandler());
        server.createContext("/ticket", new TicketHandler());
        server.createContext("/tickets", new TicketsHandler());
        server.setExecutor(null);
        server.start();
        System.out.println("Lottery API started on port " + port);
    }

    private static final Gson GSON = new Gson();

    /**
     * Extracts the session_id from the Cookie request header. If no valid session cookie
     * is present, generates a new UUID session ID. Does not write any headers.
     */
    private static String getOrCreateSession(HttpExchange exchange) {
        List<String> cookieHeaders = exchange.getRequestHeaders().get("Cookie");
        if (cookieHeaders != null) {
            for (String header : cookieHeaders) {
                for (String part : header.split(";")) {
                    part = part.trim();
                    if (part.startsWith("session_id=")) {
                        String sid = part.substring("session_id=".length()).trim();
                        if (sid.length() == 36 && sid.matches("[0-9a-fA-F\\-]+")) {
                            return sid;
                        }
                    }
                }
            }
        }
        return java.util.UUID.randomUUID().toString();
    }

    /**
     * Appends a Set-Cookie header for the session to the pending response.
     * Must be called before sendResponseHeaders().
     */
    private static void setSessionCookie(HttpExchange exchange, String sessionId) {
        exchange.getResponseHeaders().add("Set-Cookie",
                "session_id=" + sessionId + "; HttpOnly; Path=/; SameSite=Strict");
    }

    /**
     * Handles ticket purchase requests.
     *
     * Expected request: POST /buy
     *   JSON body: { "numbers": [int, int, int, int, int, int] }
     *
     * Response: 201 Created
     *   JSON body: { "status": "created", "ticket": { ...ticket info... } }
     *
     * This is not a web challenge, focus on the logic with cryptographic implications.
     */
    static class BuyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // for CORS preflight
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "POST, OPTIONS");
                exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String sessionId = getOrCreateSession(exchange);

            // get numbers from JSON body, if any
            String body = new String(exchange.getRequestBody().readAllBytes()).trim();
            int[] numbers = null;
            if (!body.isEmpty()) {
                JsonElement je;
                try {
                    je = GSON.fromJson(body, JsonElement.class);
                } catch (JsonSyntaxException ex) {
                    setSessionCookie(exchange, sessionId);
                    sendError(exchange, 400, "invalid JSON");
                    return;
                }

                try {
                    if (je.isJsonObject() && je.getAsJsonObject().has("numbers")) {
                        numbers = je.getAsJsonObject().get("numbers").isJsonArray()
                                ? GSON.fromJson(je.getAsJsonObject().get("numbers"), int[].class)
                                : null;
                    } else {
                        setSessionCookie(exchange, sessionId);
                        sendError(exchange, 400, "expected JSON object with 'numbers' array or a JSON array");
                        return;
                    }
                } catch (IllegalArgumentException e) {
                    setSessionCookie(exchange, sessionId);
                    sendError(exchange, 400, "invalid numbers: " + e.getMessage());
                    return;
                }
            }

            // make a new ticket
            Ticket ticket = TicketRepository.getInstance().createTicket(numbers, sessionId);
            JsonObject resp = new JsonObject();
            resp.add("ticket", GSON.toJsonTree(ticket));
            resp.addProperty("status", "created");
            setSessionCookie(exchange, sessionId);
            sendJsonResponse(exchange, 201, resp);
        }
    }

    private static void sendJsonResponse(HttpExchange exchange, int status, JsonObject obj) throws IOException {
        byte[] out = GSON.toJson(obj).getBytes();
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
        exchange.sendResponseHeaders(status, out.length);
        try (OutputStream os = exchange.getResponseBody()) { os.write(out); }
    }

    private static void sendError(HttpExchange exchange, int status, String message) throws IOException {
        JsonObject obj = new JsonObject();
        obj.addProperty("error", message);
        sendJsonResponse(exchange, status, obj);
    }

    /**
     * Handles ticket redemption requests.
     *
     * Expected request: POST /redeem
     *   JSON body: { "uuid": <number> }
     *
     * Response: 200 OK
     *   JSON body: { "result": "JACKPOT!!!" | "LOSE", "ticket": { ...ticket info... }, "winning": [int, int, int, int, int, int], "flag": <flag if jackpot> }
     *
     * Redemption is session-scoped: you can only redeem tickets purchased in your session.
     */
    static class RedeemHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String sessionId = getOrCreateSession(exchange);

            String body = new String(exchange.getRequestBody().readAllBytes()).trim();
            if (body.isEmpty()) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 400, "missing uuid in body");
                return;
            }

            // Require JSON object with a `uuid` field
            JsonElement je;
            try {
                je = GSON.fromJson(body, JsonElement.class);
            } catch (JsonSyntaxException ex) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 400, "invalid JSON");
                return;
            }

            if (je == null || !je.isJsonObject()) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 400, "expected JSON object with 'uuid'");
                return;
            }

            JsonObject jo = je.getAsJsonObject();
            if (!jo.has("uuid")) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 400, "missing uuid key in JSON");
                return;
            }

            JsonElement u = jo.get("uuid");
            long uuid;
            if (!u.isJsonPrimitive()) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 400, "invalid uuid type");
                return;
            }

            JsonPrimitive up = u.getAsJsonPrimitive();
            if (up.isNumber()) {
                uuid = up.getAsLong();
            } else {
                String numStr = up.getAsString().trim();
                try {
                    if (numStr.startsWith("0x") || numStr.startsWith("0X")) {
                        uuid = Long.parseUnsignedLong(numStr.substring(2), 16);
                    } else {
                        uuid = Long.parseUnsignedLong(numStr);
                    }
                } catch (NumberFormatException ex) {
                    setSessionCookie(exchange, sessionId);
                    sendError(exchange, 400, "invalid uuid: " + numStr);
                    return;
                }
            }

            // Session-scoped lookup: only the session that bought the ticket can redeem it
            Ticket ticket = TicketRepository.getInstance().getTicketByUUID(uuid, sessionId);
            if (ticket == null) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 404, "ticket not found");
                return;
            }

            if (ticket.isRedeemed()) {
                setSessionCookie(exchange, sessionId);
                sendError(exchange, 409, "ticket already redeemed");
                return;
            }

            int[] winning = Lottery.drawNumbers(sessionId);
            boolean match = java.util.Arrays.equals(ticket.getNumbers(), winning);
            JsonObject out = new JsonObject();
            if (match) {
                boolean ok = TicketRepository.getInstance().redeemTicketByUuid(uuid, sessionId);
                if (ok) ticket.setRedeemed(true);
                out.addProperty("result", "JACKPOT!!!");
                String flag = System.getenv("APP_FLAG");
                if (flag != null && !flag.isEmpty()) out.add("flag", GSON.toJsonTree(flag));
            } else {
                out.addProperty("result", "LOSE");
            }

            ticket.setRedeemed(true);

            out.add("ticket", GSON.toJsonTree(ticket));
            out.add("winning", GSON.toJsonTree(winning));
            setSessionCookie(exchange, sessionId);
            sendJsonResponse(exchange, 200, out);
        }
    }

    /**
     * Returns ticket information for a given uuid without redeeming it.
     * GET /ticket?uuid=<number>
     *
     * This endpoint is public — no session required. Anyone with the UUID can look it up.
     */
    static class TicketHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, OPTIONS");
                exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"GET".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String query = exchange.getRequestURI().getQuery();
            if (query == null || !query.contains("uuid=")) {
                sendError(exchange, 400, "missing uuid query parameter");
                return;
            }

            String uuidStr = null;
            for (String part : query.split("&")) {
                if (part.startsWith("uuid=")) {
                    uuidStr = java.net.URLDecoder.decode(part.substring(5), "UTF-8");
                    break;
                }
            }

            if (uuidStr == null || uuidStr.isEmpty()) {
                sendError(exchange, 400, "missing uuid value");
                return;
            }

            long uuid;
            try {
                if (uuidStr.startsWith("0x") || uuidStr.startsWith("0X")) {
                    uuid = Long.parseUnsignedLong(uuidStr.substring(2), 16);
                } else {
                    uuid = Long.parseUnsignedLong(uuidStr);
                }
            } catch (NumberFormatException ex) {
                sendError(exchange, 400, "invalid uuid: " + uuidStr);
                return;
            }

            Ticket ticket = TicketRepository.getInstance().getTicketByUUID(uuid);
            if (ticket == null) {
                sendError(exchange, 404, "ticket not found");
                return;
            }

            JsonObject out = new JsonObject();
            out.add("ticket", GSON.toJsonTree(ticket));
            sendJsonResponse(exchange, 200, out);
        }
    }

    /**
     * Returns all tickets for the current session.
     * GET /tickets
     *
     * Response: 200 OK
     *   JSON body: { "tickets": [ ...ticket objects... ] }
     */
    static class TicketsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, OPTIONS");
                exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"GET".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String sessionId = getOrCreateSession(exchange);
            List<Ticket> tickets = TicketRepository.getInstance().getTicketsBySession(sessionId);

            JsonArray arr = new JsonArray();
            for (Ticket t : tickets) {
                arr.add(GSON.toJsonTree(t));
            }
            JsonObject out = new JsonObject();
            out.add("tickets", arr);
            setSessionCookie(exchange, sessionId);
            sendJsonResponse(exchange, 200, out);
        }
    }
}