---
name: "lang-bash"
description: "Provides software engineering patterns in Bash/Shell Scripting. Covers strict and safe execution (set -euo pipefail), defensive variable and quoting handling, modular functions, dependency checks, file handling/redirection, and integration with ShellCheck and portability best practices."
---

# AI Skill: Bash Engineering (Bash & Shell Scripting Specialist)

This skill guides the AI to act as a **Bash and Shell Scripting** specialist, with a focus on safe, predictable, portable scripts with strict error handling for systems automation, CI/CD routines, and Linux/Unix server administration.

---

## 🧭 Bash Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Strict Mode and Execution Safety
- **Strict Initial Setup**: Every Bash script must start by setting strict mode:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  IFS=$'\n\t'
  ```
  - `set -e`: Stops execution immediately if any command returns a non-zero (failure) status.
  - `set -u`: Treats the use of undeclared/uninitialized variables as an error.
  - `set -o pipefail`: Ensures pipelines (`cmd1 | cmd2`) return the error code of the first failing command in the pipeline, not just the last one.
  - `IFS=$'\n\t'`: Prevents unwanted *word splitting* on whitespace.

### 2. Defensive Variable and Quoting Handling
- **Quote Variables**: Always wrap variable usage in double quotes: `"$var"` or `"${var}"`. This prevents leaks from *word splitting* or *globbing* expansion.
- **Use Braces**: Prefer the `${var}` syntax for clarity and syntactic disambiguation.
- **Default Values**: Use parameter expansion to handle optional variables defensively:
  ```bash
  LOG_LEVEL="${LOG_LEVEL:-INFO}"
  PORT="${1:-8080}"
  ```

### 3. Modular Functions and Local Scope
- **Local Variables**: Declare ALL function-internal variables with the `local` keyword.
- **Return Values**: Bash functions return a numeric status code (`return 0` for success, `return 1-255` for errors). To "return" data, print to `stdout` and capture with command substitution: `result=$(my_function)`.
- **Separate Logs from Useful Output**: Send log and diagnostic messages to `stderr` (`>&2`) so they do not pollute the main output captured by the caller.

### 4. Resource Management and Cleanup with `trap`
- **Guaranteed Cleanup**: Use `trap` to catch termination signals (`EXIT`, `INT`, `TERM`) and guarantee the removal of temporary files, release of locks, or restoration of system state.

### 5. Portability and Dependency Checks
- **Portable Shebang**: Use `#!/usr/bin/env bash` instead of fixed paths such as `#!/bin/bash`.
- **Validate External Binaries**: Before invoking utilities such as `jq`, `curl`, or `docker`, check that they exist in `PATH`:
  ```bash
  command -v jq >/dev/null 2>&1 || { echo "Error: 'jq' is required but is not installed." >&2; exit 1; }
  ```
- **ShellCheck Compliance**: Write clean code in line with ShellCheck's static analysis rules.

---

## 🧰 Recommended Code Patterns

### Professional, Robust Script Template with Cleanup and Option Parsing

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Settings and Globals
readonly SCRIPT_NAME="$(basename "$0")"
readonly TMP_DIR="$(mktemp -d -t "${SCRIPT_NAME}.XXXXXX")"

# Cleanup Function (Executed automatically on EXIT)
cleanup() {
    local exit_code=$?
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
    exit "$exit_code"
}
trap cleanup EXIT INT TERM

# Logging Functions (Directed to stderr)
log_info() {
    printf '[INFO] %s\n' "$*" >&2
}

log_error() {
    printf '[ERROR] %s\n' "$*" >&2
}

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] -i <input_file>

Options:
  -i, --input FILE    Path to the input file (required)
  -o, --output FILE   Path to the output file (optional)
  -h, --help          Displays this help
EOF
}

# Argument Parsing
parse_args() {
    local input_file=""
    local output_file=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--input)
                input_file="${2:-}"
                shift 2
                ;;
            -o|--output)
                output_file="${2:-}"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    if [[ -z "$input_file" ]]; then
        log_error "The --input parameter is required."
        usage
        exit 1
    fi

    echo "$input_file" "$output_file"
}

# Main Function
main() {
    local input_file=""
    local output_file=""

    read -r input_file output_file <<< "$(parse_args "$@")"

    if [[ ! -f "$input_file" ]]; then
        log_error "Input file not found: $input_file"
        exit 1
    fi

    log_info "Processing the file: $input_file"
    local temp_output="${TMP_DIR}/processed.txt"

    # Example of safe line-by-line processing
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Processes only non-empty lines that are not comments
        if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
            printf 'PROCESSED: %s\n' "$line" >> "$temp_output"
        fi
    done < "$input_file"

    if [[ -n "$output_file" ]]; then
        mv "$temp_output" "$output_file"
        log_info "Result saved to: $output_file"
    else
        cat "$temp_output"
    fi
}

main "$@"
```

### Dependency Checking and Safe JSON File Reading

```bash
#!/usr/bin/env bash
set -euo pipefail

# Ensures dependencies before execution
check_dependencies() {
    local dep
    for dep in jq curl; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            printf '[ERROR] Missing dependency: %s\n' "$dep" >&2
            return 1
        fi
    done
}

fetch_github_user() {
    local username="${1:-}"
    if [[ -z "$username" ]]; then
        printf '[ERROR] Username not provided.\n' >&2
        return 1
    fi

    local response
    response=$(curl -sSL "https://api.github.com/users/${username}")

    local name
    name=$(echo "$response" | jq -r '.name // "N/A"')

    printf 'User: %s | Name: %s\n' "$username" "$name"
}

main() {
    check_dependencies || exit 1
    fetch_github_user "octocat"
}

main "$@"
```

## 🔒 Security Issues and Safe Practices

- **Command Injection**: Avoid expanding variables directly into system commands. Use double quotes whenever possible (`"$var"` instead of `$var`) to prevent word splitting and globbing.
- **Safe Startup Settings**: Always use `set -euo pipefail` at the top of scripts so the interpreter stops immediately on errors, undefined variables, or hidden pipeline failures.
- **$PATH Handling**: Avoid running relative binaries or relying on an uncontrolled inherited `$PATH`. Define an explicit `$PATH` at the top of SUID or administrative scripts.
- **Temporary Files**: Never create fixed temporary files (e.g., `/tmp/temp.txt`). Use the `mktemp` command to generate random, safe temporary filenames.
