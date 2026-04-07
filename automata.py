# =============================================================================
#
#   AUTOMATA SIMULATOR TOOL  v2.0
#   Theory of Computation (TOC) — Academic Project
#   Pure Python · No External Libraries · Single File
#
# =============================================================================
#
#  Supported Problems
#  ──────────────────
#  1. Strings ending with "01"           → DFA
#  2. Strings containing substring "aba" → NFA
#  3. Binary numbers divisible by 3      → DFA
#  4. Even number of a's and b's         → DFA
#
#  Features
#  ────────
#  • Step-by-step DFA / NFA simulation
#  • Formal definition  (Q, Σ, δ, q₀, F)
#  • Transition table
#  • JFLAP drawing guide
#  • State explanations  (viva helper)
#  • Predefined test cases with verbose mode
#  • Robust input handling throughout
#
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 ── AUTOMATON DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_automaton(problem_name):
    """
    Returns the full automaton dictionary for a given problem key.

    Parameters
    ----------
    problem_name : str
        One of: "ends_with_01", "contains_aba", "div_by_3", "even_a_even_b"

    Returns
    -------
    dict  with keys:
        type        → "DFA" or "NFA"
        states      → set of state names
        alphabet    → set of valid input symbols
        start       → name of the start state
        final       → set of accept / final state names
        transitions → dict mapping (state, symbol) to next state (DFA)
                      or to a set of next states (NFA)
    """

    # ── Problem 1 ─────────────────────────────────────────────────────────
    # Language : Σ = {0,1} — strings that END with the pattern "01"
    #
    # State logic:
    #   q0  — initial state; no useful suffix seen yet
    #   q1  — the most recent symbol was '0'  (one step toward "01")
    #   q2  — the last two symbols were '01'  ← ACCEPT STATE
    # ──────────────────────────────────────────────────────────────────────
    if problem_name == "ends_with_01":
        return {
            "type"       : "DFA",
            "states"     : {"q0", "q1", "q2"},
            "alphabet"   : {"0", "1"},
            "start"      : "q0",
            "final"      : {"q2"},
            "transitions": {
                ("q0", "0"): "q1",   # saw '0' — possible start of "01"
                ("q0", "1"): "q0",   # '1' is useless at q0; stay
                ("q1", "0"): "q1",   # new '0' resets; still at "last was 0"
                ("q1", "1"): "q2",   # '1' after '0' = complete "01" → accept
                ("q2", "0"): "q1",   # new '0' starts fresh chance
                ("q2", "1"): "q0",   # '1' kills the match; back to start
            }
        }

    # ── Problem 2 ─────────────────────────────────────────────────────────
    # Language : Σ = {a,b} — strings that CONTAIN "aba" as a substring
    #
    # Implemented as an NFA (nondeterminism makes the design natural).
    # State logic:
    #   q0  — no part of "aba" matched yet
    #   q1  — matched "a"   (1st char of "aba")
    #   q2  — matched "ab"  (2nd char of "aba")
    #   q3  — matched "aba" ← ACCEPT (trap state — stays here forever)
    # ──────────────────────────────────────────────────────────────────────
    elif problem_name == "contains_aba":
        return {
            "type"       : "NFA",
            "states"     : {"q0", "q1", "q2", "q3"},
            "alphabet"   : {"a", "b"},
            "start"      : "q0",
            "final"      : {"q3"},
            "transitions": {
                # q0: on 'a' we nondeterministically try to start matching
                ("q0", "a"): {"q0", "q1"},   # stay in q0 OR begin match
                ("q0", "b"): {"q0"},          # 'b' — stay, not useful
                # q1: we have seen the leading 'a'
                ("q1", "a"): {"q1"},          # another 'a' — restart match attempt
                ("q1", "b"): {"q2"},          # 'b' advances match to "ab"
                # q2: we have seen "ab"
                ("q2", "a"): {"q3"},          # final 'a' completes "aba" → accept
                ("q2", "b"): {"q0"},          # mismatch — fall back to start
                # q3: accept trap — consume remaining input, stay accepting
                ("q3", "a"): {"q3"},
                ("q3", "b"): {"q3"},
            }
        }

    # ── Problem 3 ─────────────────────────────────────────────────────────
    # Language : Σ = {0,1} — binary strings whose INTEGER VALUE mod 3 = 0
    #
    # Key insight:
    #   If the current value has remainder r and we append bit b, the new
    #   remainder = (2*r + b) mod 3
    #
    # State logic:
    #   q0 — remainder is 0  ← START & ACCEPT  (0 is divisible by 3)
    #   q1 — remainder is 1
    #   q2 — remainder is 2
    # ──────────────────────────────────────────────────────────────────────
    elif problem_name == "div_by_3":
        return {
            "type"       : "DFA",
            "states"     : {"q0", "q1", "q2"},
            "alphabet"   : {"0", "1"},
            "start"      : "q0",
            "final"      : {"q0"},
            "transitions": {
                # rem 0: append 0 → (2*0+0)=0 mod3=0 | append 1 → (2*0+1)=1 mod3=1
                ("q0", "0"): "q0",
                ("q0", "1"): "q1",
                # rem 1: append 0 → (2*1+0)=2 mod3=2 | append 1 → (2*1+1)=3 mod3=0
                ("q1", "0"): "q2",
                ("q1", "1"): "q0",
                # rem 2: append 0 → (2*2+0)=4 mod3=1 | append 1 → (2*2+1)=5 mod3=2
                ("q2", "0"): "q1",
                ("q2", "1"): "q2",
            }
        }

    # ── Problem 4 ─────────────────────────────────────────────────────────
    # Language : Σ = {a,b} — strings where count(a) is even AND count(b) is even
    #
    # State logic (parity pair):
    #   q0 — even a's, even b's  ← START & ACCEPT
    #   q1 — odd  a's, even b's
    #   q2 — even a's, odd  b's
    #   q3 — odd  a's, odd  b's
    # ──────────────────────────────────────────────────────────────────────
    elif problem_name == "even_a_even_b":
        return {
            "type"       : "DFA",
            "states"     : {"q0", "q1", "q2", "q3"},
            "alphabet"   : {"a", "b"},
            "start"      : "q0",
            "final"      : {"q0"},
            "transitions": {
                ("q0", "a"): "q1",   # flip a-parity: even→odd
                ("q0", "b"): "q2",   # flip b-parity: even→odd
                ("q1", "a"): "q0",   # flip a-parity: odd→even
                ("q1", "b"): "q3",   # flip b-parity: even→odd
                ("q2", "a"): "q3",   # flip a-parity: even→odd
                ("q2", "b"): "q0",   # flip b-parity: odd→even
                ("q3", "a"): "q2",   # flip a-parity: odd→even
                ("q3", "b"): "q1",   # flip b-parity: odd→even
            }
        }

    else:
        raise ValueError(
            f"  Unknown problem: '{problem_name}'.\n"
            "  Valid keys: ends_with_01 | contains_aba | div_by_3 | even_a_even_b"
        )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 ── DFA SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────

def simulate_dfa(automaton, input_string, verbose=True):
    """
    Simulates a Deterministic Finite Automaton step by step.

    Parameters
    ----------
    automaton    : dict  — the DFA definition
    input_string : str   — string to test
    verbose      : bool  — if True, print each transition line

    Returns
    -------
    bool — True if accepted, False if rejected
    """

    if verbose:
        print(f"\n  {'─'*54}")
        print(f"  DFA Simulation  |  Input: \"{input_string}\"")
        print(f"  {'─'*54}")

    current_state = automaton["start"]
    transitions   = automaton["transitions"]

    # ── Empty string ──────────────────────────────────────────────────────
    if input_string == "":
        if verbose:
            print(f"  (empty string — no transitions taken)")
            print(f"  Start state: {current_state}")
        accepted = current_state in automaton["final"]
        if verbose:
            _print_result(accepted)
        return accepted

    # ── Process symbols ───────────────────────────────────────────────────
    for symbol in input_string:

        # Detect invalid symbol before attempting transition
        if symbol not in automaton["alphabet"]:
            if verbose:
                print(f"  ✖  Symbol '{symbol}' is NOT in the alphabet "
                      f"{sorted(automaton['alphabet'])}")
                print(f"\n  Invalid symbol '{symbol}' → Rejected ❌")
            return False

        key = (current_state, symbol)

        # Implicit dead/trap state — no transition defined
        if key not in transitions:
            if verbose:
                print(f"  {current_state} --{symbol}--> [DEAD STATE — no transition defined]")
                print(f"\n  Rejected ❌  (implicit dead state)")
            return False

        next_state = transitions[key]
        if verbose:
            print(f"  {current_state} --{symbol}--> {next_state}")
        current_state = next_state

    # ── Final verdict ─────────────────────────────────────────────────────
    accepted = current_state in automaton["final"]
    if verbose:
        tag = "∈ F — ACCEPT" if accepted else "∉ F — REJECT"
        print(f"\n  Final state reached: {current_state}  ({tag})")
        _print_result(accepted)
    return accepted


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 ── NFA SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────

def simulate_nfa(automaton, input_string, verbose=True):
    """
    Simulates a Nondeterministic Finite Automaton using the subset
    (powerset) construction — tracking ALL currently reachable states.

    Parameters
    ----------
    automaton    : dict  — the NFA definition
    input_string : str   — string to test
    verbose      : bool  — if True, print each transition line

    Returns
    -------
    bool — True if any active state is an accept state, else False
    """

    if verbose:
        print(f"\n  {'─'*54}")
        print(f"  NFA Simulation  |  Input: \"{input_string}\"")
        print(f"  {'─'*54}")

    current_states = {automaton["start"]}
    transitions    = automaton["transitions"]

    if verbose:
        print(f"  Start: {_fmt_states(current_states)}")

    # ── Empty string ──────────────────────────────────────────────────────
    if input_string == "":
        if verbose:
            print(f"  (empty string — no transitions taken)")
        accepted = bool(current_states & automaton["final"])
        if verbose:
            _print_result(accepted)
        return accepted

    # ── Process symbols ───────────────────────────────────────────────────
    for symbol in input_string:

        if symbol not in automaton["alphabet"]:
            if verbose:
                print(f"  ✖  Symbol '{symbol}' is NOT in the alphabet "
                      f"{sorted(automaton['alphabet'])}")
                print(f"\n  Invalid symbol '{symbol}' → Rejected ❌")
            return False

        next_states = set()
        for state in current_states:
            key = (state, symbol)
            if key in transitions:
                next_states |= transitions[key]

        if verbose:
            print(f"  {_fmt_states(current_states)} --{symbol}--> {_fmt_states(next_states)}")

        current_states = next_states

        if not current_states:
            if verbose:
                print(f"  Active state set collapsed to ∅ — no path forward.")
                print(f"\n  Rejected ❌")
            return False

    # ── Final verdict ─────────────────────────────────────────────────────
    accepted     = bool(current_states & automaton["final"])
    intersection = current_states & automaton["final"]
    if verbose:
        print(f"\n  Active states at end : {_fmt_states(current_states)}")
        print(f"  Accept states (F)    : {_fmt_states(automaton['final'])}")
        print(f"  Intersection         : {_fmt_states(intersection)}")
        _print_result(accepted)
    return accepted


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 ── UNIFIED RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(problem_name, input_string, verbose=True):
    """
    Detects DFA or NFA and dispatches to the correct simulator.

    Parameters
    ----------
    problem_name : str
    input_string : str
    verbose      : bool — passed through to the simulator

    Returns
    -------
    bool — True if accepted
    """
    automaton = get_automaton(problem_name)
    if automaton["type"] == "DFA":
        return simulate_dfa(automaton, input_string, verbose=verbose)
    elif automaton["type"] == "NFA":
        return simulate_nfa(automaton, input_string, verbose=verbose)
    else:
        raise ValueError(f"  Unknown automaton type: '{automaton['type']}'")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 ── FORMAL DEFINITION DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def get_formal_definition(automaton):
    """
    Prints and returns the formal 5-tuple definition of the automaton.

    Formal notation:  M = (Q, Σ, δ, q₀, F)
    ─────────────────────────────────────────
      Q  — finite set of states
      Σ  — input alphabet
      δ  — transition function
      q₀ — start state
      F  — set of accept (final) states

    Returns
    -------
    dict with keys: Q, Sigma, q0, F, delta
    """

    Q     = sorted(automaton["states"])
    Sigma = sorted(automaton["alphabet"])
    q0    = automaton["start"]
    F     = sorted(automaton["final"])
    delta = automaton["transitions"]

    print(f"\n  {'═'*54}")
    print(f"  FORMAL DEFINITION  ({automaton['type']})")
    print(f"  {'═'*54}")
    print(f"  M = (Q, Σ, δ, q₀, F)  where:\n")
    print(f"  Q  (all states)      : {{ {', '.join(Q)} }}")
    print(f"  Σ  (alphabet)        : {{ {', '.join(Sigma)} }}")
    print(f"  q₀ (start state)     : {q0}")
    print(f"  F  (accept states)   : {{ {', '.join(F)} }}")
    print(f"\n  δ  (transition function):")
    for (state, sym), dest in sorted(delta.items()):
        if isinstance(dest, set):
            dest_str = "{ " + ", ".join(sorted(dest)) + " }"
        else:
            dest_str = dest
        print(f"       δ({state}, {sym})  =  {dest_str}")
    print(f"  {'─'*54}")

    return {"Q": Q, "Sigma": Sigma, "q0": q0, "F": F, "delta": delta}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 ── TRANSITION TABLE PRINTER
# ─────────────────────────────────────────────────────────────────────────────

def print_transition_table(automaton):
    """
    Prints the transition function (δ) as a readable table.

    Column markers:
      →   start state
      *   accept / final state

    Parameters
    ----------
    automaton : dict
    """

    states  = sorted(automaton["states"])
    symbols = sorted(automaton["alphabet"])
    final   = automaton["final"]
    start   = automaton["start"]
    trans   = automaton["transitions"]

    state_w = max(len(s) for s in states) + 6
    sym_w   = max(max(len(s) for s in symbols), 4) + 4

    header_state = "State".center(state_w)
    header_syms  = "".join(sym.center(sym_w) for sym in symbols)
    divider      = "─" * (state_w + 3 + sym_w * len(symbols))

    print(f"\n  {'═'*54}")
    print(f"  TRANSITION TABLE  ({automaton['type']})")
    print(f"  {'═'*54}")
    print(f"  Legend :  →  = start state     *  = accept state\n")
    print(f"  {header_state} │ {header_syms}")
    print(f"  {divider}")

    for state in states:
        marker = ""
        if state == start: marker += "→"
        if state in final: marker += "*"
        label = f"{marker}{state}".ljust(state_w)

        row = ""
        for sym in symbols:
            key = (state, sym)
            if key in trans:
                dest = trans[key]
                if isinstance(dest, set):
                    cell = "{" + ",".join(sorted(dest)) + "}"
                else:
                    cell = dest
            else:
                cell = "—"
            row += cell.center(sym_w)

        print(f"  {label} │ {row}")

    print(f"  {divider}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 ── JFLAP DRAWING GUIDE
# ─────────────────────────────────────────────────────────────────────────────

def print_jflap_steps(automaton, problem_label=""):
    """
    Prints a complete, beginner-friendly step-by-step guide for drawing
    this automaton inside JFLAP (Java Formal Languages and Automata Package).

    Parameters
    ----------
    automaton     : dict
    problem_label : str  — optional display name for the problem
    """

    states  = sorted(automaton["states"])
    final   = automaton["final"]
    start   = automaton["start"]
    trans   = automaton["transitions"]
    symbols = sorted(automaton["alphabet"])
    title   = f"JFLAP GUIDE — {problem_label}" if problem_label else "JFLAP GUIDE"

    print(f"\n  {'═'*60}")
    print(f"  {title}")
    print(f"  Automaton type : {automaton['type']}")
    print(f"  {'═'*60}")

    # Step 0 — Open JFLAP
    print(f"\n  STEP 0  —  Open JFLAP")
    print(f"  ┌─────────────────────────────────────────────────────┐")
    print(f"  │  1. Launch JFLAP  (double-click JFLAP.jar)         │")
    print(f"  │  2. Click 'Finite Automaton' from the opening menu  │")
    if automaton["type"] == "NFA":
        print(f"  │     JFLAP handles NFA automatically when you       │")
        print(f"  │     draw non-deterministic transitions              │")
    print(f"  └─────────────────────────────────────────────────────┘")

    # Step 1 — Create states
    print(f"\n  STEP 1  —  Create States  (total: {len(states)})")
    print(f"  Select the circle/state tool, then click on the canvas")
    print(f"  to place one circle for EACH state listed below:\n")
    for state in states:
        parts = []
        if state == start: parts.append("START  → right-click → set as Initial")
        if state in final: parts.append("ACCEPT → right-click → set as Final  (double-ring)")
        note = "   ← " + " | ".join(parts) if parts else ""
        print(f"    •  {state}{note}")

    # Step 2 — Mark start state
    print(f"\n  STEP 2  —  Mark the Start State")
    print(f"  • Right-click on state '{start}'")
    print(f"  • Choose 'Initial'")
    print(f"  • JFLAP draws a small arrow pointing into this state")

    # Step 3 — Mark accept states
    print(f"\n  STEP 3  —  Mark Accept / Final State(s)")
    for fs in sorted(final):
        print(f"  • Right-click on state '{fs}'  → choose 'Final'")
        print(f"    The state circle gets a double-outline to indicate acceptance")

    # Step 4 — Draw transitions (group by source→dest to merge labels)
    print(f"\n  STEP 4  —  Draw Transitions  (total arrows: {len(trans)})")
    print(f"  Use the arrow/transition tool:")
    print(f"  Click a source state, drag to destination, type the label.\n")

    grouped = {}
    for (src, sym), dest in sorted(trans.items()):
        if isinstance(dest, set):
            for d in sorted(dest):
                grouped.setdefault((src, d), []).append(sym)
        else:
            grouped.setdefault((src, dest), []).append(sym)

    for (src, dst), syms in sorted(grouped.items()):
        label = ", ".join(sorted(syms))
        arrow = "self-loop" if src == dst else f"→  {dst}"
        print(f"    From {src}  on [{label}]  {arrow}")

    print(f"\n  Tip: If two states both have arrows to each other,")
    print(f"  JFLAP automatically curves them in opposite directions.")

    # Step 5 — Verify in JFLAP
    print(f"\n  STEP 5  —  Test Your Diagram Inside JFLAP")
    print(f"  • Single string : Menu → Input → Step by State")
    print(f"  • Many strings  : Menu → Input → Multiple Run")
    print(f"\n  Alphabet for this automaton : {{ {', '.join(symbols)} }}")

    # Accepted / rejected hints
    tc = None
    for key, val in TEST_CASES.items():
        # Match by alphabet overlap (rough heuristic)
        a = get_automaton(key)
        if a["alphabet"] == automaton["alphabet"] and a["start"] == automaton["start"]:
            tc = val
            break

    print(f"\n  STEP 6  —  Quick Sanity Checks (use these in JFLAP)")
    for key, data in TEST_CASES.items():
        a2 = get_automaton(key)
        if (a2["alphabet"] == automaton["alphabet"] and
                a2["states"]   == automaton["states"] and
                a2["start"]    == automaton["start"]):
            print(f"  Accepted strings  : {', '.join(repr(s) for s in data['accepted'][:3])}")
            print(f"  Rejected strings  : {', '.join(repr(s) for s in data['rejected'][:3])}")
            break

    print(f"  {'─'*60}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 ── STATE EXPLANATIONS (VIVA HELPER)
# ─────────────────────────────────────────────────────────────────────────────

STATE_EXPLANATIONS = {

    "ends_with_01": {
        "_intro": (
            "DFA for strings over {0,1} that END with '01'.\n"
            "  The automaton remembers only the last 1–2 relevant symbols."
        ),
        "q0": (
            "INITIAL state.\n"
            "  Meaning : No useful suffix seen yet.\n"
            "  Reached : At the start, or after reading '1' from q0 or q2.\n"
            "  Accept? : No"
        ),
        "q1": (
            "Meaning : The LAST symbol read was '0'.\n"
            "  Reached : After reading '0' from q0, q1, or q2.\n"
            "  Accept? : No  (need '1' next to complete '01')"
        ),
        "q2": (
            "ACCEPT state.\n"
            "  Meaning : The last TWO symbols were '0' then '1'.\n"
            "            The string currently ends with '01'.\n"
            "  Reached : After reading '1' from q1.\n"
            "  Accept? : YES ✅"
        ),
    },

    "contains_aba": {
        "_intro": (
            "NFA for strings over {a,b} that CONTAIN 'aba'.\n"
            "  Nondeterminism lets the automaton guess where 'aba' starts."
        ),
        "q0": (
            "INITIAL state.\n"
            "  Meaning : 'aba' not found yet; no active match in progress.\n"
            "  Accept? : No"
        ),
        "q1": (
            "Meaning : Matched the FIRST 'a' of the target 'aba'.\n"
            "  Reached : From q0 on reading 'a' (one of two nondeterministic branches).\n"
            "  Accept? : No"
        ),
        "q2": (
            "Meaning : Matched 'ab' — first two characters of 'aba'.\n"
            "  Reached : From q1 on reading 'b'.\n"
            "  Accept? : No"
        ),
        "q3": (
            "ACCEPT state (trap / sink).\n"
            "  Meaning : 'aba' has been found as a substring.\n"
            "            Once here, all future input keeps it here.\n"
            "  Reached : From q2 on reading 'a'.\n"
            "  Accept? : YES ✅"
        ),
    },

    "div_by_3": {
        "_intro": (
            "DFA for binary strings whose integer value is divisible by 3.\n"
            "  States track remainder = (current_value) mod 3.\n"
            "  Reading bit b transforms remainder r into (2r + b) mod 3."
        ),
        "q0": (
            "INITIAL & ACCEPT state.\n"
            "  Meaning : Current binary value ≡ 0  (mod 3)  — divisible by 3.\n"
            "  Accept? : YES ✅  (empty string = value 0, which is divisible by 3)"
        ),
        "q1": (
            "Meaning : Current binary value ≡ 1  (mod 3).\n"
            "  Accept? : No"
        ),
        "q2": (
            "Meaning : Current binary value ≡ 2  (mod 3).\n"
            "  Accept? : No"
        ),
    },

    "even_a_even_b": {
        "_intro": (
            "DFA for strings over {a,b} with EVEN count of a's AND EVEN count of b's.\n"
            "  Each state encodes a parity pair  (parity-of-a, parity-of-b).\n"
            "  Reading 'a' flips a-parity; reading 'b' flips b-parity."
        ),
        "q0": (
            "INITIAL & ACCEPT state.\n"
            "  Meaning : count(a) is EVEN  and  count(b) is EVEN.\n"
            "  Accept? : YES ✅"
        ),
        "q1": (
            "Meaning : count(a) is ODD   and  count(b) is EVEN.\n"
            "  Accept? : No"
        ),
        "q2": (
            "Meaning : count(a) is EVEN  and  count(b) is ODD.\n"
            "  Accept? : No"
        ),
        "q3": (
            "Meaning : count(a) is ODD   and  count(b) is ODD.\n"
            "  Accept? : No"
        ),
    },
}


def explain_states(problem_name):
    """
    Prints a viva-style explanation of every state for the given problem.

    Parameters
    ----------
    problem_name : str
    """

    explanations = STATE_EXPLANATIONS.get(problem_name)
    if not explanations:
        print(f"  No state explanations available for '{problem_name}'.")
        return

    automaton = get_automaton(problem_name)
    states    = sorted(automaton["states"])

    print(f"\n  {'═'*60}")
    print(f"  STATE EXPLANATIONS  —  {problem_name}")
    print(f"  (Use these during your viva / oral exam)")
    print(f"  {'═'*60}")

    if "_intro" in explanations:
        print(f"\n  Overview:")
        for line in explanations["_intro"].split("\n"):
            print(f"    {line}")

    print(f"\n  {'─'*60}")

    for state in states:
        expl = explanations.get(state, "No explanation available.")
        marker = ""
        if state == automaton["start"]: marker += " [START]"
        if state in automaton["final"]: marker += " [ACCEPT]"
        print(f"\n  State: {state}{marker}")
        for line in expl.split("\n"):
            print(f"    {line}")

    print(f"\n  {'─'*60}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 ── TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

# At least 3 accepted and 3 rejected strings per problem (5 each here).

TEST_CASES = {
    "ends_with_01": {
        "description": "Strings over {0,1} ending with '01'",
        "accepted"   : ["01", "001", "101", "1101", "0101"],
        "rejected"   : ["0",  "10",  "00",  "11",   "110" ],
    },
    "contains_aba": {
        "description": "Strings over {a,b} containing 'aba' as a substring",
        "accepted"   : ["aba", "aaba", "abab", "bbaba", "babab"],
        "rejected"   : ["",   "ab",   "ba",   "bb",    "aab"  ],
    },
    "div_by_3": {
        "description": "Binary strings whose value is divisible by 3",
        #                value :  0     3     6      9      12
        "accepted"   : ["0", "11", "110", "1001", "1100"],
        #                value :  1     2     4      7      10
        "rejected"   : ["1", "10", "100", "111",  "1010"],
    },
    "even_a_even_b": {
        "description": "Strings over {a,b} with even count of a's AND b's",
        "accepted"   : ["",   "aa",  "bb",   "aabb", "abba"],
        "rejected"   : ["a",  "b",   "ab",   "aab",  "abb" ],
    },
}


def run_all_tests(verbose=False):
    """
    Runs all predefined test cases for every problem.

    Parameters
    ----------
    verbose : bool
        True  → print step-by-step transitions per string
        False → print only PASS/FAIL summary (cleaner output)
    """

    total_passed = 0
    total_failed = 0
    total_count  = 0

    print(f"\n  {'█'*62}")
    print(f"  {'RUNNING ALL TEST CASES':^62}")
    print(f"  {'█'*62}")

    for problem, data in TEST_CASES.items():
        automaton = get_automaton(problem)
        print(f"\n  ┌─ Problem : {problem}")
        print(f"  │  Desc    : {data['description']}")
        print(f"  │  Type    : {automaton['type']}")
        print(f"  │  {'─'*52}")

        p = f = 0
        all_cases = (
            [(s, True)  for s in data["accepted"]] +
            [(s, False) for s in data["rejected"]]
        )

        for string, expected in all_cases:
            label = f'"{string}"' if string != "" else '"" (empty)'

            if verbose:
                print(f"\n  │  ── Testing {label}  "
                      f"(expected: {'ACCEPT' if expected else 'REJECT'}) ──")
                if automaton["type"] == "DFA":
                    result = simulate_dfa(automaton, string, verbose=True)
                else:
                    result = simulate_nfa(automaton, string, verbose=True)
            else:
                result = _silent_simulate(automaton, string)

            ok     = result == expected
            status = "PASS ✅" if ok else "FAIL ❌"
            got    = "ACCEPT" if result else "REJECT"
            exp    = "ACCEPT" if expected else "REJECT"

            if verbose:
                print(f"  │  [{status}]  expected={exp}   got={got}")
            else:
                print(f"  │  [{status}]  {label:<20}  expected={exp:<7}  got={got}")

            if ok: p += 1
            else:  f += 1

        total_passed += p
        total_failed += f
        total_count  += p + f
        print(f"  └─ {p}/{p+f} passed")

    print(f"\n  {'─'*62}")
    suffix = "🎉 All tests passed!" if total_failed == 0 else f"⚠ {total_failed} test(s) FAILED"
    print(f"  TOTAL: {total_passed}/{total_count} passed   {suffix}")
    print(f"  {'─'*62}\n")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 ── INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_states(state_set):
    """Formats a set of states as a readable string. Returns ∅ if empty."""
    if not state_set:
        return "∅"
    return "{ " + ", ".join(sorted(state_set)) + " }"


def _print_result(accepted):
    """Prints the final Accepted / Rejected result banner."""
    if accepted:
        print(f"\n  ╔════════════════════════════════╗")
        print(f"  ║   Result :   Accepted  ✅       ║")
        print(f"  ╚════════════════════════════════╝")
    else:
        print(f"\n  ╔════════════════════════════════╗")
        print(f"  ║   Result :   Rejected  ❌       ║")
        print(f"  ╚════════════════════════════════╝")


def _silent_simulate(automaton, input_string):
    """
    Runs the simulator suppressing all output.
    Used by run_all_tests(verbose=False) for clean PASS/FAIL lines.
    """
    import io, sys
    buf     = io.StringIO()
    old_out = sys.stdout
    sys.stdout = buf
    try:
        if automaton["type"] == "DFA":
            result = simulate_dfa(automaton, input_string, verbose=True)
        else:
            result = simulate_nfa(automaton, input_string, verbose=True)
    finally:
        sys.stdout = old_out
    return result


def _get_input(prompt, valid_options=None):
    """
    Safe input helper — loops until a valid response is entered.

    Parameters
    ----------
    prompt        : str       — displayed to the user
    valid_options : set|None  — if given, only these values accepted
                                (comparison is case-insensitive / upper)

    Returns
    -------
    str — validated, stripped, upper-cased input
    """
    while True:
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Interrupted — exiting.")
            raise SystemExit(0)

        if not raw and valid_options is not None:
            print(f"  ⚠  Please enter one of: {', '.join(sorted(valid_options))}")
            continue

        val = raw.upper()

        if valid_options is not None and val not in valid_options:
            print(f"  ⚠  '{raw}' is not valid. "
                  f"Please choose from: {', '.join(sorted(valid_options))}")
            continue

        return val


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11 ── MAIN CLI MENU
# ─────────────────────────────────────────────────────────────────────────────

# Maps menu number → (problem_key, display_label)
PROBLEM_MENU = {
    "1": ("ends_with_01",  "Strings ending with '01'          (DFA)"),
    "2": ("contains_aba",  "Strings containing 'aba'          (NFA)"),
    "3": ("div_by_3",      "Binary numbers divisible by 3     (DFA)"),
    "4": ("even_a_even_b", "Even number of a's and b's        (DFA)"),
}

# Accept both letter (A–G) and number (1–7) for the sub-menu
SUB_MENU_MAP = {
    "A": "A", "1": "A",   # Formal definition
    "B": "B", "2": "B",   # Transition table
    "C": "C", "3": "C",   # Simulate a string
    "D": "D", "4": "D",   # JFLAP guide
    "E": "E", "5": "E",   # Explain states
    "F": "F", "6": "F",   # All of the above
    "G": "G", "7": "G",   # Back
}

MAIN_VALID   = {"1", "2", "3", "4", "5", "6"}
SUB_VALID    = set(SUB_MENU_MAP.keys())


def _print_banner():
    print(f"\n  {'█'*62}")
    print(f"  {'AUTOMATA SIMULATOR TOOL  v2.0':^62}")
    print(f"  {'Theory of Computation — Academic Project':^62}")
    print(f"  {'Pure Python · No External Libraries':^62}")
    print(f"  {'█'*62}")


def _print_main_menu():
    print(f"\n  {'─'*62}")
    print(f"  MAIN MENU  —  Select a Problem")
    print(f"  {'─'*62}")
    for key, (_, label) in PROBLEM_MENU.items():
        print(f"  {key}.  {label}")
    print(f"  {'─'*62}")
    print(f"  5.  Run ALL predefined test cases")
    print(f"  6.  Exit")
    print(f"  {'─'*62}")


def _print_sub_menu(problem_label, automaton_type, alphabet):
    print(f"\n  Problem   : {problem_label}")
    print(f"  Type      : {automaton_type}")
    print(f"  Alphabet  : {{ {', '.join(sorted(alphabet))} }}")
    print(f"\n  {'─'*62}")
    print(f"  WHAT WOULD YOU LIKE TO DO?  (enter letter OR number)")
    print(f"  {'─'*62}")
    print(f"  A / 1.  Formal Definition  (Q, Σ, δ, q₀, F)")
    print(f"  B / 2.  Transition Table")
    print(f"  C / 3.  Simulate a String  (step-by-step)")
    print(f"  D / 4.  JFLAP Drawing Guide")
    print(f"  E / 5.  Explain States     (viva / oral exam helper)")
    print(f"  F / 6.  All of the Above   (full academic report)")
    print(f"  G / 7.  Back to Main Menu")
    print(f"  {'─'*62}")


def main():
    """
    Entry point — interactive CLI for the Automata Simulator.
    All input is validated; no crashes on bad input.
    """

    _print_banner()

    while True:

        # ── MAIN MENU ─────────────────────────────────────────────────────
        _print_main_menu()
        choice = _get_input("  Enter choice (1–6): ", valid_options=MAIN_VALID)

        # Option 5 — Run all tests ─────────────────────────────────────────
        if choice == "5":
            confirm = _get_input(
                "\n  Are you sure you want to run ALL test cases? (y/n): ",
                valid_options={"Y", "N"}
            )
            if confirm == "N":
                print("  Cancelled — returning to main menu.")
                continue

            v_ans = _get_input(
                "  Show verbose step-by-step transitions? (y/n): ",
                valid_options={"Y", "N"}
            )
            run_all_tests(verbose=(v_ans == "Y"))
            continue

        # Option 6 — Exit ──────────────────────────────────────────────────
        if choice == "6":
            print("\n  Goodbye! 👋\n")
            break

        # Problem chosen (1–4) ─────────────────────────────────────────────
        problem_name, problem_label = PROBLEM_MENU[choice]
        automaton = get_automaton(problem_name)

        # ── SUB-MENU (loop stays here until user picks G/7 — Back) ───────
        while True:
            _print_sub_menu(problem_label, automaton["type"], automaton["alphabet"])

            raw_sub = _get_input(
                "  Enter choice (A–G  or  1–7): ",
                valid_options=SUB_VALID
            )
            sub = SUB_MENU_MAP[raw_sub]   # normalise to canonical letter

            # Back ─────────────────────────────────────────────────────────
            if sub == "G":
                break

            # A: Formal definition ─────────────────────────────────────────
            if sub in ("A", "F"):
                get_formal_definition(automaton)

            # B: Transition table ──────────────────────────────────────────
            if sub in ("B", "F"):
                print_transition_table(automaton)

            # C: Simulate a string ─────────────────────────────────────────
            if sub in ("C", "F"):
                while True:
                    # Use plain input() here so empty string (Enter) is allowed
                    try:
                        user_str = input(
                            f"\n  Enter string to test\n"
                            f"  (alphabet: {sorted(automaton['alphabet'])} — "
                            f"press Enter for empty string): "
                        ).strip()
                    except (EOFError, KeyboardInterrupt):
                        print("\n  Interrupted.")
                        break

                    # Pre-screen for invalid symbols and warn clearly
                    bad = [ch for ch in user_str if ch not in automaton["alphabet"]]
                    if bad:
                        bad_unique = sorted(set(bad))
                        print(f"\n  ⚠  The following symbol(s) are NOT in the alphabet "
                              f"{sorted(automaton['alphabet'])} :")
                        for bc in bad_unique:
                            print(f"     Invalid symbol '{bc}' → Rejected ❌")
                        print(f"  Please re-enter using only valid symbols.\n")
                    else:
                        run_simulation(problem_name, user_str, verbose=True)

                    again = _get_input(
                        "\n  Simulate another string for this problem? (y/n): ",
                        valid_options={"Y", "N"}
                    )
                    if again == "N":
                        break

            # D: JFLAP guide ───────────────────────────────────────────────
            if sub in ("D", "F"):
                print_jflap_steps(automaton, problem_label)

            # E: Explain states ────────────────────────────────────────────
            if sub in ("E", "F"):
                explain_states(problem_name)

            # After a single sub-option: ask to stay or go back
            if sub != "F":
                stay = _get_input(
                    "\n  Return to sub-menu for this problem? (y/n): ",
                    valid_options={"Y", "N"}
                )
                if stay == "N":
                    break
            else:
                # "All of the above" — pause, then loop back to sub-menu
                input("\n  Press Enter to return to sub-menu...")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()