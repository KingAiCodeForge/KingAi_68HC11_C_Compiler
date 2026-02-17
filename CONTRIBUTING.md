# Contributing to KingAI 68HC11 C Compiler

Contributions are welcome! By participating, you agree to abide by our Code of Conduct.

## Most Useful Contributions Right Now

1. **Hardware validation** — compile a C function, use `hc11kit patch` to inject it, burn it to real hardware, and report what happened
2. **Bug reports** — provide C input + expected assembly vs. actual assembly output
3. **Array/struct codegen** — the parser handles these, but codegen still needs implementation
4. **New target profiles** — if you know the memory map of a Delco PCM not listed in the README

## How to Contribute

1.  **Fork the Repository**: Fork `KingAi_68HC11_C_Compiler` to your GitHub account.
2.  **Clone Your Fork**:
    ```bash
    git clone https://github.com/your-username/KingAi_68HC11_C_Compiler.git
    cd KingAi_68HC11_C_Compiler
    ```
3.  **Create a New Branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make Your Changes**: Follow the project's coding style and guidelines.
5.  **Test Your Changes**: Run `pytest tests/ -v` and ensure all tests pass.
6.  **Commit Your Changes**:
    ```bash
    git commit -m "feat: Add new feature X" # or "fix: Resolve bug Y"
    ```
7.  **Push to Your Fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Create a Pull Request**: Open a PR from your branch to `main` on the original repository with a clear description of your changes.

## Coding Style

-   Follow PEP 8 for Python code.
-   Use clear and descriptive variable and function names.
-   Comment your code where necessary to explain complex logic.

## Reporting Bugs

If you find a bug, please open an issue on GitHub with the following information:

-   A clear and concise description of the bug.
-   Steps to reproduce the behavior.
-   Expected behavior.
-   Screenshots or error messages, if applicable.

## Feature Requests

For feature requests, please open an issue on GitHub and describe the feature, why it's needed, and how it would benefit the project.

## Code of Conduct

We are committed to fostering an open and welcoming environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for more details.
