# Contributing to Wukong 🐵🛡️

We welcome contributions to make the web a more hostile place for malicious AI agents!

## How to Contribute

1. **Fork the repo** and create your branch from `main`.
2. **Implement your defense**: Whether it's a new "Mist" obfuscation technique or a "Tar Pit" optimization, make sure it targets AI behavioral patterns.
3. **Add Tests**: No PR will be merged without corresponding tests in the `tests/` directory.
4. **Update Docs**: If you add a new module, update the `README.md` and `walkthrough.md`.
5. **Submit a PR**: Provide a clear description of what your addition does and why it helps defeat AI agents.

## Defensive Philosophy
Every contribution should follow the **Wukong Philosophy**:
- **Asymmetric**: It must cost the attacker more (in time/tokens/money) than it costs the defender.
- **Deceptive**: It should provide "fake success" rather than simple blocking where possible.
- **Universal**: Aim for compatibility with the Universal Proxy mode.

## Development Setup

```bash
git clone https://github.com/your-username/wukong.git
cd wukong
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

Thank you for helping us protect the open web!
