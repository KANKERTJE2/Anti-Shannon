# Wukong 🐵🛡️: The Hostile Defense Framework

> [!IMPORTANT]
> **License Note**: Wukong is released under the [PolyForm Noncommercial License 1.0.0](LICENSE). 
> Commercial use, selling, or integration into paid services is strictly prohibited without a private license.

### Stop AI Pentesting Agents (Shannon, etc.) in their tracks.


**Wukong** is the first "Hostile" Defensive Framework designed to neutralize autonomous AI agents. Unlike traditional WAFs that simply block, Wukong turns your application into an asymmetric maze that drains an AI agent's time, money (API units), and context window.

> "The best defense is a hall of mirrors."

---

## 🚀 The Novelty: Why Wukong?

Autonomous AI agents (like **Shannon**) follow deterministic logic and have high operational costs. Wukong exploits these weaknesses:

1.  **Asymmetric Warfare**: Forces AI agents to wait 30s+ for a response, making automated hacking unprofitable.
2.  **Context Exhaustion**: Traps agents in loops of infinite generative data, exploding their token usage.
3.  **Behavioral Blinding**: Uses ML and dynamic route shifting to defeat the LLM's reasoning engine.


### 1. The Mist (Anti-Reconnaissance)
*   **Modules**: `wukong.defense.recon`, `wukong.defense.shifting`
*   **Function**:
    *   **HTML Obfuscation**: Injects random comments into responses to confuse static analysis agents.
    *   **Route Shifting**: Protects sensitive routes (like `/admin`) by requiring a dynamic, time-based `X-Wukong-Token`.

### 2. The Iron Body (Anti-Exploitation)
*   **Modules**: `wukong.detectors` (`probe`, `anomaly`, `fingerprint`), `wukong.defense.vacuum`
*   **Function**:
    *   **Probe Detection**: Uses regex to detect common attack patterns (SQLi, XSS).
    *   **ML Anomaly Detection**: Uses `IsolationForest` to detect atypical traffic patterns (e.g. machine-speed requests, unusual path lengths).
    *   **Client Fingerprinting**: Hashes header order to identify non-browser clients (bots/scripts).

### 3. The Deception (Honey Traps)
*   **Modules**: `wukong.traps` (`honey`, `tokens`, `genai`)
*   **Function**:
    *   **Generative Traps**: Serves infinite, procedurally generated fake data (users, transactions) to waste agent time.
    *   **Honey Tokens**: Fake JWTs/Keys. If used, the IP is instantly banned.

## 🌍 Universal Protection (Plug & Play Proxy)

Wukong is not limited to Python. By using the **Wukong Universal Proxy**, you can protect **any** infrastructure (Java, Go, PHP, Node.js, etc.) via a Docker Sidecar pattern.

### 🐳 Run via Docker

1.  **Configure your target**: Set the `TARGET_URL` to your existing application.
2.  **Start the Proxy**:
    ```bash
    docker-compose up --build
    ```

Wukong will now sit in front of your app, acting as a hostile gatekeeper.

## 🚀 Quick Start: Python Middleware

## ✅ Verification: Wukong vs. Shannon

To see Wukong in action against a simulated AI attacker (Shannon), run the following:

1.  **Start the Example App**:
    ```bash
    python examples/app.py
    ```
2.  **Run the Shannon Attack**:
    ```bash
    python scripts/simulate_shannon.py
    ```

Watch the terminal logs as Wukong detects, slows down, and eventually bans the attacker.


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Configuration
-   **Route Shifting**: Protects `/admin` and `/api/private` by requiring `X-Wukong-Token`.
-   **Honey Tokens**: Use `wukong.traps.tokens.HoneyTokenGenerator` to create fake tokens to plant in your frontend source code.

## Testing
Run the example app:
```bash
python examples/app.py
```
Then try to attack it!
