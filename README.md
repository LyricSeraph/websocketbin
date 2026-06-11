# WebsocketBin

Welcome to the WebSocketBin service. This project is a tool for inspecting connections in websocket developments.

It's inspired by [Httpbin](https://github.com/postmanlabs/httpbin)

Below are the available endpoints and usage examples.

### Current Connection Info
- **Host:** `{{ host }}`
- **Protocol:** `{{ protocol }}`

---

## 1. /echo
**Description:** Echoes back exactly what it receives.

**Example (websocat):**
```bash
echo "Hello WebSocket" | websocat -n1 {{ protocol }}://{{ host }}/echo
```

---

## 2. /inspect
**Description:** Returns connection information (IP, headers, etc.) as JSON upon connection, then continues as an echo server.

**Example (websocat):**
```bash
websocat {{ protocol }}://{{ host }}/inspect
```

---

## 3. /random-echo
**Description:** For every byte received, it responds with an equal number of random bytes (0-255).

**Example (websocat with binary output):**
```bash
echo "randomize me" | websocat -n1 -b {{ protocol }}://{{ host }}/random-echo | hexdump -C
```

---

## 4. /random
**Description:** For every message received, it responds with a random number of bytes (0 to 100 times the length of the input).

**Example (websocat with binary output):**
```bash
echo "data" | websocat -n1 -b {{ protocol }}://{{ host }}/random | hexdump -C
```

## 5. /random-zero
**Description:** For every message received, it responds with a random number of 0 (0 to 100 times the length of the input).

**Example (websocat with binary output):**
```bash
echo "data" | websocat -n1 -b {{ protocol }}://{{ host }}/random-zero | hexdump -C
```

---

## 6. /json
**Description:** Every JSON object received is met with a static JSON response defined in the `Response-Format` HTTP header during the initial WebSocket handshake. If a JSON array is provided in the header, the endpoint will rotate through the responses in a round-robin fashion for each received message.

**Example (websocat with custom response):**
```bash
# Define a single response
echo '{"request": "hello"}' | websocat -H 'Response-Format: {"status": "ok"}' -n1 {{ protocol }}://{{ host }}/json

# Define multiple responses to rotate
echo '{"req1": "a"}' | websocat -H 'Response-Format: [{"id": 1}, {"id": 2}]' -n1 {{ protocol }}://{{ host }}/json
echo '{"req2": "b"}' | websocat -H 'Response-Format: [{"id": 1}, {"id": 2}]' -n1 {{ protocol }}://{{ host }}/json
```
