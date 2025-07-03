# Langgraph Basics

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reproducible Python dependency management. If you don't have uv installed, install it with:

```
pipx install uv
```

To set up your environment and install all dependencies, simply run:

```
uv sync
```

This will create a virtual environment (if one doesn't exist) and install all dependencies as specified in `pyproject.toml` and locked in `uv.lock`.

If you add new dependencies, use:

```
uv add <package-name>
```

To update the lockfile after adding/removing dependencies:

```
uv lock
```

## Usage

The main entry point for the application is the `7_HITL.py` file. This file contains the core functionality of the chatbot and the tools it uses.

To run the chatbot, execute the following code:

```python
# 1. Get the current price of AAPL stocks
state = graph.invoke({"messages":[{"role":"user","content":"What is the current price of AAPL stocks?"}]},config=config)
print(state["messages"][-1].content)

# 2. Buy 10 shares of AAPL stocks
state = graph.invoke({"messages":[{"role":"user","content":"Buy 10 stokes of AAPL for me at current price"}]},config=config)
print(state.get("__interrupt__"))

decision = input("Approve (yes/no)")
state = graph.invoke(Command(resume=decision), config=config)
print(state["messages"][-1].content)
```

## API

The project provides the following API:

1. `get_stock_price(stock_name: str) -> float`:

   - This tool returns the current stock price for the given stock symbol.

2. `buy_stocks(symbol: str, quantity: int, total: float) -> str`:
   - This tool allows the user to buy stocks for a given symbol and quantity, and returns the result of the transaction.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests for this project, use the following command:

```
uv pip install pytest  # Only needed once to add pytest to your environment
pytest
```

This will execute the test suite and report the results.
