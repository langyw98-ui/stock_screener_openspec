# Project Context

## Purpose
This project is a modular stock backtesting software. Its primary goal is to concurrently download stock K-line data from the specified data source (xtquant), process it, and return it in memory as pandas.DataFrame objects for further analysis.

## Tech Stack
- Python
- Pandas
- xtquant
- PyYAML
- tqdm

## Project Conventions

### Code Style
- Adhere to general Python code style guidelines, primarily PEP 8, for clarity, readability, and maintainability.
- Ensure error messages are clear, concise, and easy to understand.
- Maintain modular separation as defined by the project's file structure.
- All modules must include appropriate logging for debugging, monitoring, and auditing purposes.

### Architecture Patterns
- The program will exist as an independent collection of Python scripts.
- The main entry point is `run.py`.
- Program behavior is controlled by variables in `run.py` (e.g., time range, data frequency) and `config.yaml`.
- Configuration is managed by `config.yaml` and loaded by `stock_backtester/config.py`.
- The Data Download Module (`engine.py`, `xtquant_feed.py`) is responsible for fetching stock K-line data concurrently using multi-threading.
- No complex command-line interfaces or graphical user interfaces will be developed.
- The project adheres to a defined modular file structure.
- The logging module (`stock_backtester/logger.py`) provides centralized logging functionality across all modules.

### Testing Strategy
- Implement both unit tests and integration tests to ensure code quality and functionality.
- Utilize the `pytest` framework for all testing activities.
- Error handling for critical issues (e.g., missing config files) should lead to immediate program termination with clear error messages.
- Errors during individual stock data downloads (e.g., invalid stock code, network issues) should be logged, and the program should continue processing other stocks.
- Test cases should verify that appropriate log messages are generated for different scenarios.

### Git Workflow
- Employ the Git Flow branching strategy to manage development, features, releases, and hotfixes.
- [Specific commit message conventions and code review processes will be defined as the project progresses.]

## Domain Context
- Stock backtesting software.
- K-line data (Open, High, Low, Close, Volume, Amount).
- Stock codes (e.g., 600519.SH, 000001.SZ).
- Data frequencies: 1m, 5m, 30m, 1d.
- Pre-ex-dividend adjustment for K-line data.

## Important Constraints
- No complex command-line interfaces or graphical user interfaces will be developed.
- `pandas` library must be exclusively used for all Excel file reading operations and for the in-memory representation of K-line data.
- `xtquant` is the sole specified data source interface for fetching K-line data.
- The data download module is explicitly not responsible for any form of data persistence or storage. All fetched data is held in memory as `pandas.DataFrame` objects and returned to the caller (`run.py`), with memory being released upon program termination.

## External Dependencies
- `xtquant`: Primary data source interface.
- `PyYAML`: Used for parsing `config.yaml` configuration file.
- `tqdm`: Used for displaying progress bars in the console during data download.
- `logging`: Python standard library for logging functionality.

