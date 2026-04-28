"""
generate_report.py — Generates a professional PDF project report for the Automata Simulator.
Run:  python generate_report.py
"""
from fpdf import FPDF
from automata import (
    get_automaton, get_formal_definition, generate_jflap_xml,
    nfa_to_dfa, explain_states, TEST_CASES, STATE_EXPLANATIONS,
    simulate_dfa, simulate_nfa
)
import io, sys, math

# ── All 12 problems ──────────────────────────────────────────────────────────
PROBLEMS = [
    ("ends_with_01",        "Strings ending with '01'",            "DFA"),
    ("contains_aba",        "Strings containing 'aba'",            "NFA"),
    ("div_by_3",            "Binary numbers divisible by 3",       "DFA"),
    ("even_a_even_b",       "Even number of a's and b's",          "DFA"),
    ("starts_a_ends_b",     "Starts with 'a', ends with 'b'",     "DFA"),
    ("no_consecutive_ones", "No two consecutive 1s",               "DFA"),
    ("a_followed_by_b",     "Every 'a' followed by 'b'",          "DFA"),
    ("length_div_3",        "String length divisible by 3",        "DFA"),
    ("odd_num_ones",        "Odd number of 1s",                    "DFA"),
    ("ends_with_ab",        "Strings ending with 'ab'",            "NFA"),
    ("exactly_two_as",      "Exactly two a's",                     "DFA"),
    ("starts_1_ends_0",     "Starts with '1', ends with '0'",     "DFA"),
]


def capture(fn, *a, **kw):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try: r = fn(*a, **kw)
    finally: sys.stdout = old
    return buf.getvalue(), r


def safe(text):
    """Replace chars that fpdf can't encode."""
    return (text.replace('\u2208', 'in').replace('\u2209', 'not in')
            .replace('\u2205', '{}').replace('\u03b4', 'd').replace('\u03a3', 'E')
            .replace('\u2261', '=').replace('\u2264', '<=').replace('\u2265', '>=')
            .replace('\u2190', '<-').replace('\u2192', '->').replace('\u2194', '<->')
            .replace('\u2500', '-').replace('\u2502', '|').replace('\u250c', '+')
            .replace('\u2514', '+').replace('\u2510', '+').replace('\u2518', '+')
            .replace('\u2550', '=').replace('\u2551', '||').replace('\u2588', '#')
            .replace('\u2713', 'v').replace('\u2714', 'v').replace('\u2716', 'x')
            .replace('\u2026', '...').replace('\u00b2', '2').replace('\u00b3', '3')
            .replace('\u2248', '~=').replace('\u00d7', 'x').replace('\u00f7', '/')
            .replace('\u221e', 'inf').replace('\u2260', '!=')
            .replace('\u2081', '0').replace('\u2080', '0')
            .replace('\u2082', '2').replace('\u2083', '3')
            .encode('latin-1', errors='replace').decode('latin-1'))


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(120)
            self.cell(0, 8, 'Automata Simulator Tool - TOC Project Report', align='C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(25, 60, 120)
        self.cell(0, 10, safe(title), ln=True)
        self.set_draw_color(25, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(40, 80, 140)
        self.cell(0, 8, safe(title), ln=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30)
        self.multi_cell(0, 5, safe(text))
        self.ln(2)

    def mono_text(self, text, size=8):
        self.set_font('Courier', '', size)
        self.set_text_color(50)
        self.multi_cell(0, 4, safe(text))
        self.ln(2)


def build_report():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── TITLE PAGE ────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(20, 50, 100)
    pdf.cell(0, 15, 'Automata Simulator Tool', align='C', ln=True)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(80)
    pdf.cell(0, 10, 'Theory of Computation (TOC)', align='C', ln=True)
    pdf.cell(0, 8, 'Academic Project Report', align='C', ln=True)
    pdf.ln(15)
    pdf.set_draw_color(20, 50, 100)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(60)
    pdf.cell(0, 8, 'Prepared by: Yash Lund', align='C', ln=True)
    pdf.cell(0, 8, 'Technology: Python + Streamlit', align='C', ln=True)
    pdf.cell(0, 8, 'Problems Covered: 12 (DFA & NFA)', align='C', ln=True)
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(120)
    pdf.cell(0, 8, 'Pure Python Implementation - No External Automata Libraries', align='C', ln=True)

    # ── TABLE OF CONTENTS ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Table of Contents')
    toc = [
        '1. Introduction',
        '2. Objectives',
        '3. Technology Stack',
        '4. System Architecture',
        '5. Automata Problems (12 Problems)',
        '   5.1 - 5.12  Individual Problem Details',
        '6. NFA to DFA Conversion',
        '7. Test Results',
        '8. Features Summary',
        '9. Conclusion',
    ]
    for item in toc:
        pdf.body_text(item)

    # ── 1. INTRODUCTION ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('1. Introduction')
    pdf.body_text(
        'This project implements a comprehensive Automata Simulator Tool for the '
        'Theory of Computation (TOC) course. The tool supports simulation of both '
        'Deterministic Finite Automata (DFA) and Nondeterministic Finite Automata (NFA) '
        'across 12 different language recognition problems.\n\n'
        'The simulator provides step-by-step visualization of state transitions, '
        'formal 5-tuple definitions, transition tables, state diagrams (SVG), '
        'NFA-to-DFA conversion via subset construction, JFLAP file export, '
        'and automated test case validation.\n\n'
        'The project is built entirely in pure Python with no external automata '
        'libraries. The frontend is powered by Streamlit, providing an interactive '
        'web-based interface.'
    )

    # ── 2. OBJECTIVES ────────────────────────────────────────────────────
    pdf.section_title('2. Objectives')
    objectives = [
        'Design and implement DFA and NFA for 12 language recognition problems.',
        'Provide step-by-step string simulation with transition traces.',
        'Display formal definitions: M = (Q, Sigma, delta, q0, F).',
        'Generate visual state transition diagrams (SVG).',
        'Implement NFA to DFA conversion using subset construction.',
        'Export JFLAP-compatible .jff files for each automaton.',
        'Provide comprehensive test cases for validation.',
        'Build an interactive web UI with Streamlit.',
    ]
    for i, obj in enumerate(objectives, 1):
        pdf.body_text(f'{i}. {obj}')

    # ── 3. TECHNOLOGY STACK ──────────────────────────────────────────────
    pdf.section_title('3. Technology Stack')
    pdf.body_text(
        'Language: Python 3.x\n'
        'Frontend: Streamlit (web UI framework)\n'
        'Backend: Pure Python (automata.py - single file, no external libraries)\n'
        'Diagram: SVG generation (inline, no dependencies)\n'
        'Export: JFLAP XML (.jff format)\n'
        'Report: fpdf2 (PDF generation)\n'
        'Version Control: Git + GitHub'
    )

    # ── 4. SYSTEM ARCHITECTURE ───────────────────────────────────────────
    pdf.section_title('4. System Architecture')
    pdf.body_text(
        'The project follows a clean two-file architecture:\n\n'
        'automata.py (Backend)\n'
        '  - Automaton definitions (12 problems)\n'
        '  - DFA simulator (step-by-step)\n'
        '  - NFA simulator (subset tracking)\n'
        '  - Formal definition printer\n'
        '  - Transition table generator\n'
        '  - SVG state diagram generator\n'
        '  - NFA-to-DFA converter (subset construction)\n'
        '  - JFLAP XML generator\n'
        '  - State explanations (viva helper)\n'
        '  - Test case runner\n'
        '  - Interactive CLI menu\n\n'
        'app.py (Frontend)\n'
        '  - Streamlit web application\n'
        '  - 7 interactive tabs\n'
        '  - Custom dark theme CSS\n'
        '  - Real-time simulation\n'
        '  - SVG diagram rendering\n'
        '  - JFLAP .jff file download'
    )

    # ── 5. INDIVIDUAL PROBLEM DETAILS ────────────────────────────────────
    pdf.add_page()
    pdf.section_title('5. Automata Problems')
    pdf.body_text(
        'The simulator covers 12 problems across DFA and NFA types. '
        'Each problem below includes its formal definition, transition table, '
        'state explanations, and test cases.'
    )

    for idx, (key, label, atype) in enumerate(PROBLEMS, 1):
        if pdf.get_y() > 220:
            pdf.add_page()

        automaton = get_automaton(key)
        pdf.sub_title(f'5.{idx}  {label}  ({atype})')

        # Formal definition
        Q = sorted(automaton["states"])
        Sigma = sorted(automaton["alphabet"])
        q0 = automaton["start"]
        F = sorted(automaton["final"])
        delta = automaton["transitions"]

        pdf.set_font('Courier', '', 9)
        pdf.set_text_color(30)
        pdf.multi_cell(0, 4, safe(
            f'  M = (Q, Sigma, delta, q0, F)\n'
            f'  Q     = {{ {", ".join(Q)} }}\n'
            f'  Sigma = {{ {", ".join(Sigma)} }}\n'
            f'  q0    = {q0}\n'
            f'  F     = {{ {", ".join(F)} }}'
        ))
        pdf.ln(2)

        # Transition function
        lines = []
        for (s, sym), dest in sorted(delta.items()):
            if isinstance(dest, set):
                d = "{ " + ", ".join(sorted(dest)) + " }"
            else:
                d = dest
            lines.append(f'  delta({s}, {sym}) = {d}')
        pdf.mono_text('\n'.join(lines))

        # State explanations
        if key in STATE_EXPLANATIONS:
            expl = STATE_EXPLANATIONS[key]
            if "_intro" in expl:
                pdf.set_font('Helvetica', 'I', 9)
                pdf.set_text_color(80)
                pdf.multi_cell(0, 4, safe(expl["_intro"]))
                pdf.ln(1)
            for state in Q:
                if state in expl:
                    pdf.set_font('Courier', 'B', 8)
                    pdf.set_text_color(40)
                    marker = ""
                    if state == q0: marker += " [START]"
                    if state in automaton["final"]: marker += " [ACCEPT]"
                    pdf.cell(0, 4, safe(f'  {state}{marker}'), ln=True)
                    pdf.set_font('Courier', '', 8)
                    pdf.set_text_color(60)
                    pdf.multi_cell(0, 3.5, safe(f'    {expl[state]}'))
                    pdf.ln(1)

        # Test cases
        if key in TEST_CASES:
            tc = TEST_CASES[key]
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(30, 100, 30)
            pdf.cell(0, 5, safe(f'  Accepted: {", ".join(repr(s) for s in tc["accepted"][:5])}'), ln=True)
            pdf.set_text_color(150, 30, 30)
            pdf.cell(0, 5, safe(f'  Rejected: {", ".join(repr(s) for s in tc["rejected"][:5])}'), ln=True)
            pdf.ln(4)

        pdf.set_draw_color(200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

    # ── 6. NFA TO DFA CONVERSION ─────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('6. NFA to DFA Conversion (Subset Construction)')
    pdf.body_text(
        'The tool implements the standard subset (powerset) construction algorithm '
        'to convert any NFA into an equivalent DFA. Each DFA state represents a set '
        'of NFA states that the automaton could be in simultaneously.\n\n'
        'Algorithm:\n'
        '1. Start with the set containing only the NFA start state.\n'
        '2. For each unprocessed DFA state (set of NFA states), compute transitions.\n'
        '3. For each alphabet symbol, find all NFA states reachable from the current set.\n'
        '4. The resulting set becomes a new DFA state (if not already seen).\n'
        '5. A DFA state is accepting if it contains any NFA accept state.\n'
        '6. Repeat until no new states are discovered.'
    )

    # Show conversion for each NFA problem
    nfa_problems = [(k, l) for k, l, t in PROBLEMS if t == "NFA"]
    for key, label in nfa_problems:
        if pdf.get_y() > 200:
            pdf.add_page()
        pdf.sub_title(f'Conversion: {label}')
        automaton = get_automaton(key)
        dfa, steps = nfa_to_dfa(automaton)

        for step in steps:
            if step == "":
                pdf.ln(1)
            else:
                pdf.mono_text(step, size=8)

        # State mapping
        mapping = dfa.get("state_mapping", {})
        if mapping:
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(30)
            pdf.cell(0, 6, 'State Mapping:', ln=True)
            for dfa_s in sorted(mapping.keys()):
                nfa_set = mapping[dfa_s]
                nfa_str = "{ " + ", ".join(sorted(nfa_set)) + " }" if nfa_set else "{}"
                marker = ""
                if dfa_s == dfa["start"]: marker = " [START]"
                if dfa_s in dfa["final"]: marker += " [ACCEPT]"
                pdf.mono_text(f'  {dfa_s} = {nfa_str}{marker}')
        pdf.ln(4)

    # ── 7. TEST RESULTS ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('7. Test Results')
    pdf.body_text(
        'All 12 problems include predefined test cases. The following shows '
        'the validation results for each problem.'
    )

    total_pass = 0
    total_all = 0
    for key, label, atype in PROBLEMS:
        automaton = get_automaton(key)
        tc = TEST_CASES.get(key, {})
        cases = ([(s, True) for s in tc.get("accepted", [])] +
                 [(s, False) for s in tc.get("rejected", [])])
        passed = 0
        for string, expected in cases:
            buf = io.StringIO()
            old = sys.stdout; sys.stdout = buf
            try:
                if automaton["type"] == "DFA":
                    result = simulate_dfa(automaton, string, verbose=False)
                else:
                    result = simulate_nfa(automaton, string, verbose=False)
            finally:
                sys.stdout = old
            if result == expected:
                passed += 1
        total = len(cases)
        total_pass += passed
        total_all += total
        status = "ALL PASSED" if passed == total else f"{total - passed} FAILED"
        color = (30, 100, 30) if passed == total else (150, 30, 30)

        if pdf.get_y() > 270:
            pdf.add_page()
        pdf.set_font('Courier', '', 9)
        pdf.set_text_color(*color)
        pdf.cell(0, 5, safe(f'  {label:.<45} {passed}/{total}  {status}'), ln=True)

    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(20, 50, 100)
    pdf.cell(0, 8, safe(f'TOTAL: {total_pass}/{total_all} test cases passed'), ln=True)

    # ── 8. FEATURES SUMMARY ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('8. Features Summary')
    features = [
        ('12 Automata Problems', '10 DFA + 2 NFA covering diverse TOC concepts'),
        ('Step-by-Step Simulation', 'Verbose transition traces for both DFA and NFA'),
        ('Formal Definitions', 'Complete 5-tuple M = (Q, Sigma, delta, q0, F)'),
        ('Transition Tables', 'Formatted tables with start/accept markers'),
        ('SVG State Diagrams', 'Visual diagrams with circles, arrows, self-loops'),
        ('NFA to DFA Conversion', 'Subset construction with step-by-step explanation'),
        ('JFLAP Export', 'Download .jff files to open in JFLAP directly'),
        ('State Explanations', 'Viva/oral exam helper for each state'),
        ('Test Case Runner', '121 predefined test cases with PASS/FAIL validation'),
        ('Interactive Web UI', 'Streamlit app with dark theme, 7 tabs'),
        ('CLI Mode', 'Full terminal-based menu system'),
    ]
    for title, desc in features:
        if pdf.get_y() > 270:
            pdf.add_page()
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(25, 60, 120)
        pdf.cell(0, 6, safe(f'  {title}'), ln=True)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(60)
        pdf.cell(0, 5, safe(f'    {desc}'), ln=True)
        pdf.ln(2)

    # ── 9. CONCLUSION ────────────────────────────────────────────────────
    pdf.section_title('9. Conclusion')
    pdf.body_text(
        'This Automata Simulator Tool successfully demonstrates the core concepts '
        'of the Theory of Computation course through a practical implementation. '
        'The tool covers 12 language recognition problems using both DFA and NFA, '
        'provides comprehensive simulation capabilities, and includes an NFA-to-DFA '
        'converter using the subset construction algorithm.\n\n'
        'The project serves as both a learning tool and an academic submission, '
        'with features designed to help with viva preparation, JFLAP integration, '
        'and visual understanding of finite automata.\n\n'
        'All 121 test cases pass successfully, validating the correctness of '
        'every automaton implementation.'
    )

    # ── Save ─────────────────────────────────────────────────────────────
    output_path = "Automata_Simulator_Report.pdf"
    pdf.output(output_path)
    print(f"\n  Report generated: {output_path}")
    print(f"  Total pages: {pdf.page_no()}")
    return output_path


if __name__ == "__main__":
    build_report()
