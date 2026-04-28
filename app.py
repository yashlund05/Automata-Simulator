"""
app.py  —  Streamlit UI for Automata Simulator Tool
Run with:  streamlit run app.py
Requires:  automata.py in the same directory
"""

import io
import sys
import streamlit as st

# ── Import everything from the backend ────────────────────────────────────────
from automata import (
    get_automaton,
    simulate_dfa,
    simulate_nfa,
    get_formal_definition,
    print_transition_table,
    print_jflap_steps,
    generate_jflap_xml,
    generate_svg_diagram,
    nfa_to_dfa,
    explain_states,
    TEST_CASES,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: capture printed output from backend functions into a string
# ─────────────────────────────────────────────────────────────────────────────

def capture(fn, *args, **kwargs):
    """Run fn(*args, **kwargs) and return everything it prints as a string."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        result = fn(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue(), result


# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Automata Simulator — TOC",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS  —  clean monospace-academic look
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* ── Global background ── */
.stApp {
    background: #0d0f14;
    color: #e0e6f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111520 !important;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] * {
    color: #c8d0e0 !important;
}

/* ── Main title ── */
.main-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #4fc3f7 0%, #7c6af7 50%, #f06292 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}
.main-subtitle {
    color: #5a6a8a;
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #4fc3f7;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #1e2a3a;
}

/* ── Code / monospace blocks ── */
.mono-block {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    background: #0a0c12;
    border: 1px solid #1e2535;
    border-left: 3px solid #4fc3f7;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    color: #b0c4de;
    white-space: pre;
    overflow-x: auto;
    line-height: 1.65;
}

/* ── Accept / Reject badges ── */
.badge-accept {
    display: inline-block;
    background: #0d2e1e;
    color: #4caf84;
    border: 1px solid #2e7d52;
    border-radius: 20px;
    padding: 6px 20px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 1px;
}
.badge-reject {
    display: inline-block;
    background: #2e0d10;
    color: #ef5350;
    border: 1px solid #7d2e30;
    border-radius: 20px;
    padding: 6px 20px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 1px;
}

/* ── Transition step lines ── */
.step-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #90caf9;
    padding: 3px 0;
}
.step-arrow {
    color: #7c6af7;
    font-weight: 700;
}

/* ── Info / meta chips ── */
.chip {
    display: inline-block;
    background: #141b2d;
    border: 1px solid #2a3550;
    border-radius: 6px;
    padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #7c6af7;
    margin-right: 8px;
    margin-bottom: 6px;
}
.chip-label {
    color: #5a6a8a;
    font-size: 0.75rem;
    margin-right: 4px;
}

/* ── Test result rows ── */
.test-pass {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #4caf84;
    padding: 2px 0;
}
.test-fail {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #ef5350;
    padding: 2px 0;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #0a0c12 !important;
    border: 1px solid #1e2535 !important;
    color: #e0e6f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 6px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1a2a4a, #0f1a2e) !important;
    color: #4fc3f7 !important;
    border: 1px solid #2a4a6a !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: #4fc3f7 !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #1e3560, #162040) !important;
}
.stSelectbox > div > div {
    background: #0a0c12 !important;
    border: 1px solid #1e2535 !important;
    color: #e0e6f0 !important;
    border-radius: 6px !important;
}
div[data-testid="stDivider"] > hr {
    border-color: #1e2535 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Problem map
# ─────────────────────────────────────────────────────────────────────────────

PROBLEMS = {
    "Strings ending with '01'":           "ends_with_01",
    "Strings containing 'aba'":           "contains_aba",
    "Binary numbers divisible by 3":      "div_by_3",
    "Even number of a's and b's":         "even_a_even_b",
    "Starts with 'a', ends with 'b'":     "starts_a_ends_b",
    "No two consecutive 1s":              "no_consecutive_ones",
    "Every 'a' followed by 'b'":          "a_followed_by_b",
    "String length divisible by 3":       "length_div_3",
    "Odd number of 1s":                   "odd_num_ones",
    "Strings ending with 'ab'":           "ends_with_ab",
    "Exactly two a's":                    "exactly_two_as",
    "Starts with '1', ends with '0'":     "starts_1_ends_0",
}


# ─────────────────────────────────────────────────────────────────────────────
# Simulation helpers  (parse backend output into structured steps)
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation_captured(problem_name, input_string):
    """
    Run the appropriate simulator and return (output_text, accepted_bool).
    """
    automaton = get_automaton(problem_name)
    if automaton["type"] == "DFA":
        text, result = capture(simulate_dfa, automaton, input_string, verbose=True)
    else:
        text, result = capture(simulate_nfa, automaton, input_string, verbose=True)
    return text, result


def parse_transition_lines(raw_text):
    """
    Extract transition lines like 'q0 --a--> q1' or '{q0} --a--> {q1, q2}'
    from the raw simulation output.
    """
    lines = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        if "--" in stripped and "-->" in stripped:
            lines.append(stripped)
    return lines


def run_all_tests_structured():
    """
    Run all test cases and return a list of dicts:
      { problem, string, expected, got, passed }
    """
    results = []
    for problem_key, data in TEST_CASES.items():
        automaton = get_automaton(problem_key)
        cases = (
            [(s, True)  for s in data["accepted"]] +
            [(s, False) for s in data["rejected"]]
        )
        for string, expected in cases:
            _, result = capture(
                simulate_dfa if automaton["type"] == "DFA" else simulate_nfa,
                automaton, string, verbose=True
            )
            results.append({
                "problem" : problem_key,
                "string"  : string,
                "expected": expected,
                "got"     : result,
                "passed"  : result == expected,
            })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — problem selector
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🤖 Automata Simulator")
    st.markdown("<small style='color:#5a6a8a'>Theory of Computation · TOC Project</small>",
                unsafe_allow_html=True)
    st.divider()

    selected_label = st.selectbox(
        "Select a Problem",
        list(PROBLEMS.keys()),
        help="Choose the automaton / language to explore"
    )
    problem_key = PROBLEMS[selected_label]
    automaton   = get_automaton(problem_key)

    st.divider()
    st.markdown(
        f"<span class='chip'><span class='chip-label'>TYPE</span>{automaton['type']}</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span class='chip'><span class='chip-label'>Σ</span>"
        f"{{ {', '.join(sorted(automaton['alphabet']))} }}</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span class='chip'><span class='chip-label'>|Q|</span>{len(automaton['states'])} states</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span class='chip'><span class='chip-label'>q₀</span>{automaton['start']}</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span class='chip'><span class='chip-label'>F</span>"
        f"{{ {', '.join(sorted(automaton['final']))} }}</span>",
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown(
        "<small style='color:#3a4a5a'>Pure Python · No external APIs · "
        "Single file backend</small>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<p class="main-title">Automata Simulator Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Theory of Computation — TOC Academic Project</p>',
            unsafe_allow_html=True)

st.markdown(f"### {selected_label}")
badge_color = "#4fc3f7" if automaton["type"] == "DFA" else "#f06292"
st.markdown(
    f'<span style="display:inline-block;background:#0a0c12;border:1px solid {badge_color};'
    f'border-radius:4px;padding:2px 10px;font-family:JetBrains Mono,monospace;'
    f'font-size:0.8rem;color:{badge_color};">{automaton["type"]}</span>',
    unsafe_allow_html=True
)

st.divider()

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab_def, tab_table, tab_sim, tab_jflap, tab_nfa2dfa, tab_states, tab_tests = st.tabs([
    "📐 Formal Definition",
    "📋 Transition Table",
    "▶  Simulate",
    "🎨 State Diagram",
    "🔄 NFA → DFA",
    "💬 State Explanations",
    "✅ Test Cases",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Formal Definition
# ══════════════════════════════════════════════════════════════════════════════

with tab_def:
    st.markdown('<div class="section-header">Formal Definition  M = (Q, Σ, δ, q₀, F)</div>',
                unsafe_allow_html=True)

    text, _ = capture(get_formal_definition, automaton)

    # ── Structured display ────────────────────────────────────────────────────
    Q     = sorted(automaton["states"])
    Sigma = sorted(automaton["alphabet"])
    q0    = automaton["start"]
    F     = sorted(automaton["final"])
    delta = automaton["transitions"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Q — All States**")
        st.markdown(
            "<div class='mono-block'>{ " + ", ".join(Q) + " }</div>",
            unsafe_allow_html=True
        )
        st.markdown("**Σ — Alphabet**")
        st.markdown(
            "<div class='mono-block'>{ " + ", ".join(Sigma) + " }</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("**q₀ — Start State**")
        st.markdown(
            f"<div class='mono-block'>{q0}</div>",
            unsafe_allow_html=True
        )
        st.markdown("**F — Accept States**")
        st.markdown(
            "<div class='mono-block'>{ " + ", ".join(F) + " }</div>",
            unsafe_allow_html=True
        )

    st.markdown("**δ — Transition Function**")
    delta_lines = []
    for (state, sym), dest in sorted(delta.items()):
        if isinstance(dest, set):
            dest_str = "{ " + ", ".join(sorted(dest)) + " }"
        else:
            dest_str = dest
        delta_lines.append(f"  δ({state}, {sym})  =  {dest_str}")

    st.markdown(
        "<div class='mono-block'>" + "\n".join(delta_lines) + "</div>",
        unsafe_allow_html=True
    )

    with st.expander("📄 Raw backend output"):
        st.code(text, language=None)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Transition Table
# ══════════════════════════════════════════════════════════════════════════════

with tab_table:
    st.markdown('<div class="section-header">Transition Table  δ : Q × Σ → Q</div>',
                unsafe_allow_html=True)

    states  = sorted(automaton["states"])
    symbols = sorted(automaton["alphabet"])
    trans   = automaton["transitions"]
    final   = automaton["final"]
    start   = automaton["start"]

    # Build a pretty HTML table
    th_style = (
        "background:#0a0c12;color:#4fc3f7;font-family:'JetBrains Mono',monospace;"
        "font-size:0.82rem;padding:8px 16px;border:1px solid #1e2535;"
        "text-align:center;letter-spacing:1px;"
    )
    td_style = (
        "background:#0d1018;color:#b0c4de;font-family:'JetBrains Mono',monospace;"
        "font-size:0.82rem;padding:6px 16px;border:1px solid #1a2030;text-align:center;"
    )
    td_state_style = (
        "background:#0a0c12;color:#c8d8f0;font-family:'JetBrains Mono',monospace;"
        "font-size:0.82rem;padding:6px 16px;border:1px solid #1a2030;text-align:left;"
    )

    rows_html = ""
    for state in states:
        marker = ""
        if state == start: marker += "→ "
        if state in final: marker += "* "
        label = f"{marker}{state}"

        color = "#e0e6f0"
        if state in final:   color = "#4caf84"
        if state == start:   color = "#4fc3f7"
        if state == start and state in final: color = "#f06292"

        cells = f"<td style=\"{td_state_style}color:{color};\">{label}</td>"
        for sym in symbols:
            key = (state, sym)
            if key in trans:
                dest = trans[key]
                if isinstance(dest, set):
                    cell_val = "{" + ", ".join(sorted(dest)) + "}"
                else:
                    cell_val = dest
            else:
                cell_val = "—"
            cells += f"<td style=\"{td_style}\">{cell_val}</td>"
        rows_html += f"<tr>{cells}</tr>"

    header_syms = "".join(f"<th style=\"{th_style}\">{s}</th>" for s in symbols)
    table_html = f"""
    <table style="border-collapse:collapse;width:auto;margin-top:0.5rem;">
      <thead>
        <tr>
          <th style="{th_style}text-align:left;">State</th>
          {header_syms}
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#3a4a5a;margin-top:0.5rem;">
      Legend :  → = start state &nbsp;&nbsp; * = accept state
    </p>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    with st.expander("📄 Raw backend output"):
        raw_table, _ = capture(print_transition_table, automaton)
        st.code(raw_table, language=None)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Simulate
# ══════════════════════════════════════════════════════════════════════════════

with tab_sim:
    st.markdown('<div class="section-header">Step-by-Step String Simulation</div>',
                unsafe_allow_html=True)

    alphabet_display = "{ " + ", ".join(sorted(automaton["alphabet"])) + " }"
    st.markdown(
        f"<small style='color:#5a6a8a;font-family:JetBrains Mono,monospace;'>"
        f"Alphabet : {alphabet_display}&nbsp;&nbsp;|&nbsp;&nbsp;"
        f"Type : {automaton['type']}</small>",
        unsafe_allow_html=True
    )

    user_input = st.text_input(
        "Enter input string",
        placeholder="e.g.  " + list(TEST_CASES[problem_key]["accepted"])[0],
        help=f"Use only symbols from {alphabet_display}",
        key=f"sim_input_{problem_key}"
    )

    run_btn = st.button("▶  Run Simulation", key=f"run_{problem_key}")

    if run_btn:
        # Validate symbols
        bad = [ch for ch in user_input if ch not in automaton["alphabet"]]
        if bad:
            bad_unique = sorted(set(bad))
            st.error(
                "**Invalid symbol(s) detected — Rejected ❌**\n\n" +
                "\n".join(f"• Invalid symbol `'{b}'` is not in alphabet {alphabet_display}"
                          for b in bad_unique)
            )
        else:
            raw_output, accepted = run_simulation_captured(problem_key, user_input)
            transition_lines = parse_transition_lines(raw_output)

            st.markdown("**Transition trace:**")

            if not transition_lines:
                st.markdown(
                    "<div class='mono-block'>(empty string — no transitions taken)</div>",
                    unsafe_allow_html=True
                )
            else:
                steps_html = ""
                for line in transition_lines:
                    # Colorize arrows
                    colored = line.replace("-->", '<span class="step-arrow">--></span>')
                    steps_html += f"<div class='step-line'>{colored}</div>"
                st.markdown(
                    f"<div class='mono-block' style='border-left-color:#7c6af7;'>{steps_html}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)
            if accepted:
                st.markdown(
                    "<span class='badge-accept'>✅ &nbsp; Accepted</span>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<span class='badge-reject'>❌ &nbsp; Rejected</span>",
                    unsafe_allow_html=True
                )

            with st.expander("📄 Raw backend output"):
                st.code(raw_output, language=None)

    # ── Quick examples ────────────────────────────────────────────────────────
    st.divider()
    st.markdown("**Quick examples for this problem:**")

    tc = TEST_CASES[problem_key]
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            "<span style='color:#4caf84;font-family:JetBrains Mono,monospace;"
            "font-size:0.8rem;'>✅ Accepted strings</span>",
            unsafe_allow_html=True
        )
        for s in tc["accepted"]:
            label = f'"{s}"' if s else '"" (empty)'
            st.markdown(
                f"<span style='font-family:JetBrains Mono,monospace;font-size:0.82rem;"
                f"color:#2a7a52;'>&nbsp;&nbsp;{label}</span>",
                unsafe_allow_html=True
            )
    with col_b:
        st.markdown(
            "<span style='color:#ef5350;font-family:JetBrains Mono,monospace;"
            "font-size:0.8rem;'>❌ Rejected strings</span>",
            unsafe_allow_html=True
        )
        for s in tc["rejected"]:
            label = f'"{s}"' if s else '"" (empty)'
            st.markdown(
                f"<span style='font-family:JetBrains Mono,monospace;font-size:0.82rem;"
                f"color:#7a2a2e;'>&nbsp;&nbsp;{label}</span>",
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — JFLAP Guide
# ══════════════════════════════════════════════════════════════════════════════

with tab_jflap:
    st.markdown('<div class="section-header">State Transition Diagram</div>',
                unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#5a6a8a;'>Visual state diagram for this automaton — "
        "equivalent to a JFLAP diagram. Download the .jff file to open in JFLAP directly.</small>",
        unsafe_allow_html=True
    )

    # ── Render SVG diagram ────────────────────────────────────────────────
    svg_markup = generate_svg_diagram(automaton)
    st.markdown(
        f"<div style='display:flex;justify-content:center;margin:1.5rem 0;'>{svg_markup}</div>",
        unsafe_allow_html=True
    )

    # ── Legend ─────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='display:flex;gap:24px;justify-content:center;margin:0.5rem 0 1rem;'>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#4caf84;'>"
        "● Double ring = Accept state</span>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#4caf84;'>"
        "→ Green arrow = Start</span>"
        "<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#7c6af7;'>"
        "↺ Purple = Self-loop</span>"
        "</div>",
        unsafe_allow_html=True
    )

    # ── Download JFLAP .jff file ──────────────────────────────────────────
    jff_xml = generate_jflap_xml(automaton)
    st.download_button(
        label="📥  Download JFLAP .jff File",
        data=jff_xml,
        file_name=f"{problem_key}.jff",
        mime="application/xml",
        key=f"jff_{problem_key}",
    )

    # ── Collapsible text guide ────────────────────────────────────────────
    with st.expander("📄 Step-by-step JFLAP construction guide"):
        raw_jflap, _ = capture(print_jflap_steps, automaton, selected_label)
        st.code(raw_jflap, language=None)



# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — NFA → DFA Conversion
# ══════════════════════════════════════════════════════════════════════════════

with tab_nfa2dfa:
    st.markdown('<div class="section-header">NFA → DFA Conversion (Subset Construction)</div>',
                unsafe_allow_html=True)

    if automaton["type"] == "DFA":
        st.info(
            "ℹ️ **This automaton is already a DFA.**\n\n"
            "Select an NFA problem from the sidebar (e.g. *Strings containing 'aba'*, "
            "*Strings ending with 'ab'*) to see the NFA → DFA conversion."
        )
    else:
        st.markdown(
            "<small style='color:#5a6a8a;'>The subset (powerset) construction converts "
            "an NFA into an equivalent DFA. Each DFA state represents a set of NFA states.</small>",
            unsafe_allow_html=True
        )

        converted_dfa, conversion_steps = nfa_to_dfa(automaton)

        # ── Step-by-step explanation ──────────────────────────────────────
        st.markdown("**Step-by-step conversion:**")
        steps_html = ""
        for step in conversion_steps:
            if step == "":
                steps_html += "<br>"
            elif step.startswith("═"):
                steps_html += f"<div style='color:#4caf84;font-weight:700;margin-top:0.5rem;'>{step}</div>"
            elif step.startswith("Step"):
                steps_html += f"<div style='color:#4fc3f7;font-weight:600;'>{step}</div>"
            elif step.startswith("  →"):
                steps_html += f"<div style='color:#4caf84;'>&nbsp;&nbsp;{step[2:]}</div>"
            elif step.startswith("  δ"):
                steps_html += f"<div style='color:#b0c4de;'>&nbsp;&nbsp;{step[2:]}</div>"
            else:
                steps_html += f"<div style='color:#90a0b8;'>{step}</div>"
        st.markdown(
            f"<div class='mono-block' style='border-left-color:#f06292;'>{steps_html}</div>",
            unsafe_allow_html=True
        )

        # ── State mapping table ───────────────────────────────────────────
        st.markdown("**State mapping (DFA state → NFA states):**")
        mapping = converted_dfa.get("state_mapping", {})
        th = ("background:#0a0c12;color:#f06292;font-family:'JetBrains Mono',monospace;"
              "font-size:0.82rem;padding:8px 16px;border:1px solid #1e2535;text-align:center;")
        td = ("background:#0d1018;color:#b0c4de;font-family:'JetBrains Mono',monospace;"
              "font-size:0.82rem;padding:6px 16px;border:1px solid #1a2030;text-align:center;")
        rows = ""
        for dfa_s in sorted(mapping.keys()):
            nfa_set = mapping[dfa_s]
            nfa_str = "{ " + ", ".join(sorted(nfa_set)) + " }" if nfa_set else "∅"
            marker = ""
            if dfa_s == converted_dfa["start"]:
                marker += " → "
            if dfa_s in converted_dfa["final"]:
                marker += " * "
            rows += f"<tr><td style=\"{td}\">{marker}{dfa_s}</td><td style=\"{td}\">{nfa_str}</td></tr>"
        map_html = f"""
        <table style="border-collapse:collapse;margin-top:0.5rem;">
          <thead><tr>
            <th style="{th}">DFA State</th>
            <th style="{th}">NFA States</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <p style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#3a4a5a;margin-top:0.5rem;">
          Legend :  → = start state &nbsp;&nbsp; * = accept state
        </p>
        """
        st.markdown(map_html, unsafe_allow_html=True)

        # ── Converted DFA diagram ─────────────────────────────────────────
        st.markdown("**Equivalent DFA diagram:**")
        dfa_svg = generate_svg_diagram(converted_dfa)
        st.markdown(
            f"<div style='display:flex;justify-content:center;margin:1rem 0;'>{dfa_svg}</div>",
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — State Explanations
# ══════════════════════════════════════════════════════════════════════════════

with tab_states:
    st.markdown('<div class="section-header">State Explanations — Viva Helper</div>',
                unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#5a6a8a;'>Use these explanations during your "
        "viva / oral examination to clearly explain each state.</small>",
        unsafe_allow_html=True
    )

    raw_expl, _ = capture(explain_states, problem_key)
    st.markdown(
        f"<div class='mono-block'>{raw_expl}</div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — Test Cases
# ══════════════════════════════════════════════════════════════════════════════

with tab_tests:
    st.markdown('<div class="section-header">Predefined Test Cases</div>',
                unsafe_allow_html=True)

    scope = st.radio(
        "Scope",
        ["Current problem only", "All problems"],
        horizontal=True,
        key="test_scope"
    )

    run_tests_btn = st.button("✅  Run Test Cases", key="run_tests")

    if run_tests_btn:
        all_results = run_all_tests_structured()

        if scope == "Current problem only":
            results = [r for r in all_results if r["problem"] == problem_key]
            problems_to_show = [problem_key]
        else:
            results = all_results
            problems_to_show = list(TEST_CASES.keys())

        for prob in problems_to_show:
            prob_results = [r for r in results if r["problem"] == prob]
            passed = sum(1 for r in prob_results if r["passed"])
            total  = len(prob_results)

            color = "#4caf84" if passed == total else "#f06292"
            st.markdown(
                f"<div style='margin-top:1rem;padding:6px 12px;border-left:3px solid {color};"
                f"background:#0a0c12;border-radius:0 6px 6px 0;'>"
                f"<span style='font-family:Syne,sans-serif;font-weight:700;color:{color};'>"
                f"{prob}</span>&nbsp;&nbsp;"
                f"<span style='font-family:JetBrains Mono,monospace;font-size:0.8rem;"
                f"color:#5a6a8a;'>{passed}/{total} passed</span></div>",
                unsafe_allow_html=True
            )

            lines_html = ""
            for r in prob_results:
                label   = f'"{r["string"]}"' if r["string"] else '"" (empty)'
                exp_str = "ACCEPT" if r["expected"] else "REJECT"
                got_str = "ACCEPT" if r["got"]      else "REJECT"
                icon    = "✅ PASS" if r["passed"] else "❌ FAIL"
                css     = "test-pass" if r["passed"] else "test-fail"
                lines_html += (
                    f"<div class='{css}'>"
                    f"  [{icon}]  {label:<22}  "
                    f"expected={exp_str:<7}  got={got_str}"
                    f"</div>"
                )

            st.markdown(
                f"<div class='mono-block' style='margin-top:0.25rem;'>{lines_html}</div>",
                unsafe_allow_html=True
            )

        # Summary
        total_pass = sum(1 for r in results if r["passed"])
        total_all  = len(results)
        if total_pass == total_all:
            st.success(f"🎉 All {total_all} test cases passed!")
        else:
            st.warning(f"⚠ {total_pass}/{total_all} passed — "
                       f"{total_all - total_pass} failed")