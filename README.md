
## 🛡️ PAF – *Protection Anti Fouineurs*

**PAF**  is a source-to-source transformation tool that automatically injects **anti-debugging techniques** into C programs. Its goal is to help developers defend sensitive functions against reverse engineering and forensic inspection (“fouineurs”).

PAF uses [`comby`](https://comby.dev), a syntax-aware code rewriting engine, to safely inject runtime anti-debug checks into user-specified functions. You can also control the intensity of the protection using predefined overhead levels.

---

## 🚀 How to Run

Make the script executable:

```bash
chmod +x PAF.py
```

Then run:

```bash
./PAF.py -c <file.c> [functions...] [-category <cat1> <cat2> ...] [-d <density>]
```

---

## 🔧 Options

| Option                                 | Description                                                                                        |
| -------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `-c <file.c>`                          | C source file to protect. Can be used multiple times for different files.                          |
| `[functions...]`                       | One or more function names to protect. If omitted, defaults to `main`.                             |
| `-category <cat1> <cat2> ...`          | *(Optional)* Restrict injection to specific technique categories like `time`, `memory`, `process`. |
| `-d <density>` or `-density <density>` | *(Optional)* Adjust the strength of protection: `low`, `medium` (default), or `high`.              |

---

## 📘 Examples

```bash
# Protect the 'main' function in main.c with default settings
./PAF.py -c main.c

# Protect 'main' and 'login' with only time-based techniques
./PAF.py -c secure.c main login -category time

# Apply high-overhead techniques to 'auth'
./PAF.py -c auth.c auth -d high

# Inject protections into multiple files with memory techniques
./PAF.py -c a.c main -c b.c check integrity -category memory -d medium
```

---

## 🧩 Adding Your Own Anti-Debugging Techniques

PAF reads techniques from a central C source file (here `antidebug.c`). Techniques are grouped by category and overhead using comment markers like:

```c
// === TIME BASED ===
// == HIGH ==
void time_check() {
    // your technique code
}
// == LOW == 
void time_check2() {
    // your technique code
}
// === PROCESS BASED ===
// == LOW ==
void detect_tracer() {
    // your technique code
}
```

### To add a new technique:

1. Choose a category or create a new one.
2. Add your anti-debugging function(s) under the relevant category with a clear name.
3. PAF will automatically detect and make these techniques available for injection.
4. You can now use your custom technique via the `-category` option.

---


👥 Contributors

This project was developed as part of a research initiative at Cyberschool – University of Rennes. The team behind PAF includes:

    Vincent Michel
    
    Rayane Jelidi–Daniel

    Yann Galmel

    Florian Verdes

Supervisor:
Mohamed Sabt

We worked in close collaboration to design, benchmark, and implement this tool as a hands-on exploration of software protection techniques.

