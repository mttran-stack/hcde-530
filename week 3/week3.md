# Week 3 — Competency claim

## Recognizing when a Python script has crashed

I can tell that a script has **crashed** (stopped unexpectedly with an error) rather than finished normally by looking at what the terminal shows and how the shell behaves afterward.

**What a crash often looks like**

- **Python traceback:** A block of text starting with `Traceback (most recent call last):`, followed by file names, line numbers, and a final line naming the error type (for example `ValueError`, `FileNotFoundError`, `KeyError`) and a short message. That means Python hit something it could not handle and exited from that run.
- **Explicit error before exit:** Messages such as `raise ValueError("CSV must include a 'role' column.")` from our cleaning script mean the program stopped on purpose at that check because the input did not meet expectations.
- **Shell “command not found”:** If I type the wrong interpreter (for example `python` when only `python3` exists) or mistype the command, the shell prints `command not found` and no Python script actually ran—this is a failed invocation, not a Python traceback, but it still means the script did not run successfully.
- **No success message:** When a script is written to print something at the end (for example `Wrote N rows to ...`) and that line never appears after a traceback or error, I treat that as confirmation the run did not complete the happy path.

**What “did not crash” looks like by contrast**

- The script runs to the end, prints the expected summary (if any), and the prompt returns with **no** traceback.
- The exit code is 0 (in practice, I usually infer success from the lack of errors rather than checking `$?` every time, but a non-zero exit code means failure).

**Competency claim**

I claim competency in **recognizing a crashed or failed script run**: I can read terminal output and distinguish a Python traceback and error type from a successful run, interpret common shell errors (wrong command name, wrong path), and connect error messages to what went wrong (missing file, bad CSV header, wrong working directory) so I can fix the issue and re-run.
