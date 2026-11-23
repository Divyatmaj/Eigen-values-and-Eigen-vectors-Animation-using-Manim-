"""
EigenValues-and-EigenVectors.py - Eigenvalues & Eigenvectors (M3, Linear Algebra)

An educational Manim video for first-year engineering students.

Render the whole video (1080p, 30 fps):
    manim -qh --fps 30 EigenValues-and-EigenVectors.py FullVideo

Render one part on its own for testing (480p, fast):
    manim -ql EigenValues-and-EigenVectors.py Part05Sweep

Manim also writes FullVideo.srt next to the MP4. It holds every narration
line with its start and end time, so the voice-over can be recorded and
lined up against it.

Requires Manim Community Edition v0.18 or later and a LaTeX installation.
"""

from manim import *
import numpy as np


# ============================================================================
# 1. CONSTANTS - student details, colours and the running example
# ============================================================================

STUDENT_NAME = "Divyatmaj Tamhankar"
URN = "E25B070629"
BATCH = "Neumann"
LAB = "Memory"

# Fixed colour code, used the same way in every part of the video.
COL_A = TEAL      # the matrix A
COL_V = YELLOW    # an input vector v
COL_AV = RED      # its image A v
COL_E1 = GREEN    # eigenpair 1: lambda = 3, v1 = (1, 1)
COL_E2 = ORANGE   # eigenpair 2: lambda = 1, v2 = (1, -1)

config.background_color = "#0e1116"   # dark background

# Running example used everywhere in the video.
A = np.array([[2.0, 1.0],
              [1.0, 2.0]])
LAM1, LAM2 = 3, 1
V1 = np.array([1.0, 1.0])
V2 = np.array([1.0, -1.0])

# ---- Check every number that appears on screen before anything is drawn ----
assert np.allclose(A @ V1, [3, 3]) and np.allclose(A @ V1, LAM1 * V1)  # A(1,1) = (3,3)
assert np.allclose(A @ V2, [1, -1]) and np.allclose(A @ V2, LAM2 * V2)  # A(1,-1) = (1,-1)
assert np.isclose(np.linalg.det(A), 3)                    # det A = 4 - 1 = 3
assert np.isclose(np.trace(A), 4)                         # tr A = 2 + 2 = 4
assert np.allclose(sorted(np.linalg.eigvals(A)), [1, 3])  # roots of l^2 - 4l + 3
assert np.isclose(LAM1 * LAM2, np.linalg.det(A))          # product of eigenvalues = det
assert np.isclose(LAM1 + LAM2, np.trace(A))               # sum of eigenvalues = trace
assert np.allclose(A @ [1, 0], [2, 1])                    # first column of A
assert np.allclose(0.5 * V1 + 0.5 * V2, [1, 0])           # (1,0) = v1/2 + v2/2
assert np.allclose(LAM1 * 0.5 * V1 + LAM2 * 0.5 * V2, [2, 1])
assert np.isclose(abs(np.linalg.det(np.column_stack([V1, V2]))), 2)          # area 2
assert np.isclose(abs(np.linalg.det(np.column_stack([A @ V1, A @ V2]))), 6)  # area 6

# LaTeX for the matrix, reused in several parts.
A_TEX = r"\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}"


def fmt(x):
    """Format a number for LaTeX: 2.0 -> '2', 1.5 -> '1.5', -1.0 -> '-1'."""
    x = float(x)
    return str(int(x)) if x.is_integer() else f"{x:g}"


def tex_vec(*entries):
    """LaTeX for a column vector, e.g. tex_vec(1, -1) -> (1 over -1)."""
    return r"\begin{pmatrix}" + r"\\".join(fmt(e) for e in entries) + r"\end{pmatrix}"


# ============================================================================
# 2. NARRATION - the voice-over script, split into one entry per say() call
# ============================================================================

NARRATION = {
    "opening": [
        f"Hi, I'm {STUDENT_NAME or '[name]'}, URN {URN or '[URN]'}, from batch {BATCH}. "
        "This video is about "
        "eigenvalues and eigenvectors: the directions a matrix cannot turn.",
    ],
    "hook": [
        "Here is a grid with six arrows. Watch what happens when we multiply every "
        "point by one matrix.",
        "Almost every arrow gets knocked off its line and turns somewhere new.",
        "But two did not turn: one became three times longer, and the other did not "
        "move at all.",
        "Which directions does a matrix leave alone, and how can we find them without "
        "guessing?",
    ],
    "definition": [
        "These special directions are called eigenvectors. Let A be a square matrix.",
        "A nonzero vector v is an eigenvector of A if A v equals lambda v, a scalar "
        "multiple of v. The scalar lambda is the eigenvalue: it tells us how much v "
        "is stretched.",
        "v must be nonzero, because A times zero is zero for every lambda, which "
        "tells us nothing.",
        "If lambda is bigger than one, v stretches. Between zero and one, it shrinks. "
        "If lambda is negative, it flips backwards. In every case it stays on its "
        "own line.",
        "By the end of this video, you will be able to explain what A v equals lambda "
        "v means geometrically, and compute the eigenvalues and eigenvectors of a two "
        "by two matrix by hand.",
    ],
    "tests": [
        "Our example matrix is A equals two, one, one, two. Yellow is v, and red is A v.",
        "Take v equals one, zero. A v is two, one, the first column of A. It has left "
        "the dashed line through v, so this is not an eigenvector.",
        "Now v equals one, one. A v is three, three: exactly three times v, on the "
        "same line. That is an eigenvector with eigenvalue three.",
        "And v equals one, minus one gives one, minus one: v itself. That is an "
        "eigenvector with eigenvalue one.",
    ],
    "sweep": [
        "Now sweep v around a circle. Usually the two arrows point in different "
        "directions, but at forty-five degrees they line up, and A v equals three v.",
        "They line up again at one hundred thirty-five degrees, where A v equals v.",
        "The red tip traces an ellipse whose axes lie along exactly these two "
        "directions.",
    ],
    "grid": [
        "On the whole grid, A stretches the line y equals x by three, leaves y equals "
        "minus x fixed, and rotates every other line.",
    ],
    "derivation": [
        "Guessing won't always work, so here is a method. Start from A v equals lambda v.",
        "Write lambda v as lambda I v and move it across,",
        "then factor out v: A minus lambda I, times v, equals zero.",
        "If A minus lambda I were invertible, multiplying by its inverse would force "
        "v to be zero, which is a contradiction.",
        "So its determinant must be zero. This is the characteristic equation.",
    ],
    "solve": [
        "For our matrix, subtract lambda down the diagonal: two minus lambda, one, "
        "one, two minus lambda.",
        "The determinant is two minus lambda squared, minus one times one.",
        "That expands to lambda squared minus four lambda plus three, which factors "
        "as lambda minus one, times lambda minus three.",
        "So the eigenvalues are three and one.",
    ],
    "eigenvectors": [
        "For lambda equals three, A minus three I is minus one, one, one, minus one.",
        "Both rows say minus x plus y equals zero, so y equals x, and we choose v one "
        "equals one, one.",
        "For lambda equals one, A minus I is all ones, so x plus y equals zero, and "
        "v two equals one, minus one.",
        "The rows repeat because the determinant is zero; that dependence is what "
        "allows a whole line of solutions.",
        "Check by substitution: A v one is three, three, which is three v one, and "
        "A v two is one, minus one, which is v two.",
    ],
    "area": [
        "What do these numbers mean? The parallelogram built from v one and v two "
        "has area two.",
        "Apply A: along v one everything stretches by three, and along v two nothing "
        "changes. The area grows from two to six.",
        "That factor of three is the determinant of A, and it equals the product of "
        "the eigenvalues, three times one.",
        "The trace, four, equals their sum, three plus one.",
    ],
    "basis": [
        "Any vector can be built from eigenvectors. One, zero is one half v one plus "
        "one half v two.",
        "So A times one, zero is three halves v one plus one half v two, which is two, "
        "one: the first column of A, as we saw earlier.",
        "In the eigenvector basis, a matrix is just scaling along each axis.",
    ],
    "recap": [
        "To recap.",
        "One: an eigenvector is a nonzero direction that A only stretches, shrinks or "
        "flips, so A v equals lambda v.",
        "Two: eigenvalues solve the determinant of A minus lambda I equals zero, and "
        "eigenvectors solve A minus lambda I, times v, equals zero.",
        "Three: in the eigenvector basis, A is pure scaling, here by three along y "
        "equals x and by one along y equals minus x.",
    ],
    "closing": [
        "Thanks for watching. The references, credits and AI disclosure are on screen now.",
    ],
}


# ============================================================================
# 3. BASE SCENE - narration timing and drawing helpers shared by every part
# ============================================================================

class EigenBase(Scene):
    """Holds the helpers and one method per part of the video.

    FullVideo calls every part in order; the PartNN classes at the bottom of
    the file each call a single part so it can be rendered alone.
    """

    # ------------------------------------------------------------ narration
    def setup(self):
        self._line_end = 0.0   # scene time at which the current narration line ends

    def say(self, text):
        """Start a narration line.

        It is added as a subtitle (Manim writes all subtitles to an .srt file),
        lasting words / 2.5 + 0.6 seconds, i.e. about 150 words a minute.
        Animations played after say() run while the line is being spoken.
        """
        self.finish()                                   # never overlap two lines
        duration = len(text.split()) / 2.5 + 0.6
        self.add_subcaption(text, duration=duration)
        self._line_end = self.renderer.time + duration

    def finish(self):
        """Wait until the current narration line has finished."""
        remaining = self._line_end - self.renderer.time
        if remaining > 0.01:
            self.wait(remaining)

    def clear_screen(self):
        """End a part: let narration finish, stop updaters, fade everything out."""
        self.finish()
        for mob in self.mobjects:
            mob.clear_updaters()
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.8)

    # ------------------------------------------------------------ drawing
    def make_plane(self, opacity=0.55, **kwargs):
        """A NumberPlane with one screen unit per grid unit (unless resized)."""
        return NumberPlane(
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1.5,
                "stroke_opacity": opacity,
            },
            axis_config={"stroke_opacity": 0.9},
            **kwargs,
        )

    def axis_labels(self, plane):
        """Labels x and y at the ends of a plane's axes."""
        x_lab = MathTex("x", font_size=36).next_to(plane.x_axis.get_right(), UL, buff=0.15)
        y_lab = MathTex("y", font_size=36).next_to(plane.y_axis.get_top(), DR, buff=0.15)
        return VGroup(x_lab, y_lab)

    def arrow(self, start, end, color, width=6):
        """A straight arrow between two screen points, with a fixed-size tip."""
        return Arrow(
            start, end, buff=0, color=color, stroke_width=width,
            max_tip_length_to_length_ratio=0.25,
            max_stroke_width_to_length_ratio=12,
        )

    def matrix_badge(self):
        """'A = (2 1; 1 2)' in teal, pinned to the top-left corner."""
        badge = MathTex(r"A = " + A_TEX, color=COL_A, font_size=40)
        badge.to_corner(UL, buff=0.3)
        badge.add_background_rectangle(opacity=0.85, buff=0.15)
        return badge

    def label(self, tex, color=WHITE, size=36):
        """A MathTex label with a dark background so it reads over the grid."""
        lab = MathTex(tex, color=color, font_size=size)
        lab.add_background_rectangle(opacity=0.8, buff=0.08)
        return lab

    # ====================================================================
    # PART 1 - opening frame
    # ====================================================================
    def part01_opening(self):
        title = Text("Eigenvalues & Eigenvectors", font_size=54, weight=BOLD)
        subtitle = Text("The directions a matrix cannot turn", font_size=36, color=COL_A)
        details = VGroup(
            Text(f"Name: {STUDENT_NAME}   |   URN: {URN}", font_size=30, color=GRAY_A),
            Text(f"Batch: {BATCH}   |   Lab: {LAB}", font_size=30, color=GRAY_A),
        ).arrange(DOWN, buff=0.2)
        group = VGroup(title, subtitle, details).arrange(DOWN, buff=0.5)
        details.shift(DOWN * 0.6)

        self.say(NARRATION["opening"][0])
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(FadeIn(details))
        self.clear_screen()

    # ====================================================================
    # PART 2 - hook: six arrows, one matrix, two directions that do not turn
    # ====================================================================
    def part02_hook(self):
        lines = NARRATION["hook"]

        # A faint static grid stays behind as a reference; the brighter
        # foreground grid is the one that A transforms.
        bg = self.make_plane(opacity=0.2)
        fg = self.make_plane(opacity=0.6)
        labels = self.axis_labels(bg)
        badge = self.matrix_badge()

        inputs = [(1, 0), (0, 1), (1, 1), (-1, 1), (-1, 0.5), (0.5, -1)]
        arrows = VGroup(*[
            self.arrow(ORIGIN, bg.c2p(*v), COL_V) for v in inputs
        ])

        self.say(lines[0])
        self.add(bg)
        self.play(Create(fg), FadeIn(labels), run_time=2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                  FadeIn(badge))

        # Faint copies of the inputs stay behind so we can compare.
        ghosts = arrows.copy().set_opacity(0.3)
        self.add(ghosts, arrows)

        # Apply A to the grid; each arrow turns into its image A v (red).
        self.say(lines[1])
        fg.prepare_for_nonlinear_transform()
        images = [self.arrow(ORIGIN, bg.c2p(*(A @ np.array(v))), COL_AV) for v in inputs]
        self.play(
            ApplyMatrix(A, fg),
            *[Transform(a, img) for a, img in zip(arrows, images)],
            run_time=3,
        )

        # Highlight the two arrows that stayed on their own lines.
        # (1,1) -> (3,3) is green, (-1,1) -> (-1,1) is orange.
        self.say(lines[2])
        span1 = DashedLine(bg.c2p(-4, -4), bg.c2p(4, 4), color=COL_E1, dash_length=0.15)
        span2 = DashedLine(bg.c2p(4, -4), bg.c2p(-4, 4), color=COL_E2, dash_length=0.15)
        others = [arrows[i] for i in (0, 1, 4, 5)] + [ghosts[i] for i in (0, 1, 4, 5)]
        self.play(
            arrows[2].animate.set_color(COL_E1),
            arrows[3].animate.set_color(COL_E2),
            ghosts[2].animate.set_color(COL_E1),
            *[m.animate.set_opacity(0.15) for m in others],
            fg.animate.set_stroke(opacity=0.25),
            Create(span1), Create(span2),
            run_time=1.5,
        )
        times3 = self.label(r"\times 3", COL_E1).next_to(bg.c2p(3, 3), RIGHT, buff=0.15)
        times1 = self.label(r"\times 1", COL_E2).next_to(bg.c2p(-1, 1), LEFT, buff=0.15)
        self.play(Write(times3), Write(times1))

        self.say(lines[3])
        question = Text("Which directions does a matrix leave alone?", font_size=40)
        question.to_edge(DOWN, buff=0.4).add_background_rectangle(opacity=0.9, buff=0.2)
        self.play(FadeIn(question, shift=UP * 0.2))
        self.clear_screen()

    # ====================================================================
    # PART 3 - definition, why v != 0, what lambda does, learning objective
    # ====================================================================
    def part03_definition(self):
        lines = NARRATION["definition"]

        heading = Text("Eigenvectors and eigenvalues", font_size=44, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        s1 = Tex(r"Let $A$ be a square ($n \times n$) matrix.", font_size=40)
        s2 = Tex(r"A vector $\mathbf{v} \neq \mathbf{0}$ is an \emph{eigenvector} of $A$ if",
                 font_size=40)
        key = MathTex("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", font_size=72)
        key[0].set_color(COL_A)
        key[1].set_color(COL_V)
        key[4].set_color(COL_V)
        box = SurroundingRectangle(key, color=COL_A, buff=0.25, corner_radius=0.1)
        s3 = Tex(r"for some scalar $\lambda$, the \emph{eigenvalue}.", font_size=40)
        block = VGroup(s1, s2, VGroup(key, box), s3).arrange(DOWN, buff=0.4)
        block.next_to(heading, DOWN, buff=0.5)

        self.say(lines[0])
        self.play(FadeIn(heading))
        self.play(Write(s1))

        self.say(lines[1])
        self.play(Write(s2))
        self.play(Write(key), run_time=1.5)
        self.play(Create(box))
        self.play(Write(s3))

        # Why v = 0 is excluded.
        self.say(lines[2])
        why = MathTex(r"\text{Why } \mathbf{v} \neq \mathbf{0}?\quad",
                      r"A\mathbf{0} = \lambda \mathbf{0} \text{ for every } \lambda",
                      font_size=38, color=GRAY_A)
        why.next_to(block, DOWN, buff=0.5)
        self.play(FadeIn(why))
        self.finish()

        # Three number-line panels: stretch, shrink, flip.
        self.say(lines[3])
        self.play(FadeOut(s1, s2, s3, why), VGroup(key, box).animate.next_to(heading, DOWN, buff=0.5))
        panels = VGroup(*[
            self._lambda_panel(lam, word) for lam, word in
            [(2, "stretch"), (0.5, "shrink"), (-1, "flip")]
        ]).arrange(RIGHT, buff=0.3).shift(DOWN * 0.9)
        for panel in panels:
            frame, line, v_arr, lv_arr, text = panel
            self.play(Create(frame), Create(line), GrowArrow(v_arr), FadeIn(text), run_time=0.8)
            self.play(TransformFromCopy(v_arr, lv_arr), run_time=1)
        self.finish()
        self.play(FadeOut(panels))

        # Learning objective in a frame.
        self.say(lines[4])
        obj_title = Text("By the end of this video you will be able to:", font_size=34)
        obj1 = Tex(r"1.\ explain what $A\mathbf{v} = \lambda\mathbf{v}$ means geometrically;",
                   font_size=38)
        obj2 = Tex(r"2.\ compute the eigenvalues and eigenvectors of a $2 \times 2$ matrix by hand.",
                   font_size=38)
        objective = VGroup(obj_title, obj1, obj2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        objective.next_to(box, DOWN, buff=0.7)
        frame = SurroundingRectangle(objective, color=COL_A, buff=0.35, corner_radius=0.1)
        self.play(Create(frame), FadeIn(obj_title))
        self.play(Write(obj1))
        self.play(Write(obj2))
        self.clear_screen()

    def _lambda_panel(self, lam, word):
        """One small panel: v (yellow) above a number line, lambda v (red) below."""
        line = NumberLine(x_range=[-2.5, 2.5, 1], length=3.6, include_tip=False)
        v_arr = self.arrow(line.n2p(0), line.n2p(1), COL_V, width=5).shift(UP * 0.35)
        lv_arr = self.arrow(line.n2p(0), line.n2p(lam), COL_AV, width=5).shift(DOWN * 0.35)
        cond = {2: r"\lambda > 1", 0.5: r"0 < \lambda < 1", -1: r"\lambda < 0"}[lam]
        text = VGroup(
            MathTex(cond, font_size=38),
            Text(f"{word}  (e.g. λ = {fmt(lam)})", font_size=26),
        ).arrange(DOWN, buff=0.15).next_to(line, DOWN, buff=0.7)
        content = VGroup(line, v_arr, lv_arr, text)
        frame = SurroundingRectangle(content, color=GRAY_B, buff=0.3, corner_radius=0.1)
        return VGroup(frame, line, v_arr, lv_arr, text)

    # ====================================================================
    # PART 4 - test three vectors on a static grid
    # ====================================================================
    def part04_tests(self):
        lines = NARRATION["tests"]
        plane = self.make_plane()
        labels = self.axis_labels(plane)
        badge = self.matrix_badge()

        # Legend: yellow is v, red is A v.
        legend = VGroup(
            VGroup(self.arrow(ORIGIN, RIGHT * 0.8, COL_V, 5), MathTex(r"\mathbf{v}", font_size=36)),
            VGroup(self.arrow(ORIGIN, RIGHT * 0.8, COL_AV, 5), MathTex(r"A\mathbf{v}", font_size=36)),
        )
        for item in legend:
            item.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4)
        legend.add_background_rectangle(opacity=0.85, buff=0.15)

        self.say(lines[0])
        self.play(Create(plane), FadeIn(labels), run_time=1.5)
        self.play(FadeIn(badge), FadeIn(legend))

        # (input v, where to put the v label, where to put the Av label, verdict, colour)
        tests = [
            ((1, 0), DOWN, RIGHT,
             r"left the line: \emph{not} an eigenvector", COL_AV),
            ((1, 1), DR, RIGHT,
             r"$A\mathbf{v} = 3\mathbf{v}$: eigenvector, $\lambda = 3$", COL_E1),
            ((1, -1), DL, RIGHT,
             r"$A\mathbf{v} = 1\mathbf{v}$: eigenvector, $\lambda = 1$", COL_E2),
        ]
        previous = VGroup()
        for i, (v, v_dir, av_dir, verdict_tex, verdict_col) in enumerate(tests):
            self.say(lines[i + 1])
            if len(previous):
                self.play(FadeOut(previous), run_time=0.6)
            v = np.array(v, dtype=float)
            av = A @ v

            # Dashed span line through v: the line v must stay on to be an eigenvector.
            reach = min(7 / abs(v[0]) if v[0] else np.inf, 4 / abs(v[1]) if v[1] else np.inf)
            span = DashedLine(plane.c2p(*(-reach * v)), plane.c2p(*(reach * v)),
                              color=COL_V, dash_length=0.15, stroke_opacity=0.7)

            # v is drawn wider than A v so the two can both be seen when they coincide.
            v_arr = self.arrow(ORIGIN, plane.c2p(*v), COL_V, width=10)
            v_lab = self.label(r"\mathbf{v} = " + tex_vec(*v), COL_V, 34)
            v_lab.next_to(plane.c2p(*v), v_dir, buff=0.15)
            self.play(Create(span), GrowArrow(v_arr), FadeIn(v_lab))

            av_arr = self.arrow(ORIGIN, plane.c2p(*av), COL_AV, width=5)
            av_lab = self.label(r"A\mathbf{v} = " + tex_vec(*av), COL_AV, 34)
            av_lab.next_to(plane.c2p(*av), av_dir, buff=0.15)
            self.play(TransformFromCopy(v_arr, av_arr), run_time=1.5)
            self.play(FadeIn(av_lab))

            verdict = Tex(verdict_tex, font_size=36, color=verdict_col)
            verdict.add_background_rectangle(opacity=0.9, buff=0.2)
            verdict.to_corner(DR, buff=0.4)
            self.play(FadeIn(verdict, shift=UP * 0.2))
            previous = VGroup(span, v_arr, v_lab, av_arr, av_lab, verdict)
        self.clear_screen()

    # ====================================================================
    # PART 5 - sweep v around a circle; A v traces an ellipse
    # ====================================================================
    def part05_sweep(self):
        lines = NARRATION["sweep"]
        plane = self.make_plane(opacity=0.4)
        labels = self.axis_labels(plane)
        badge = self.matrix_badge()
        R = 1.3                                   # radius of the circle v moves on
        theta = ValueTracker(0)                   # angle of v, in degrees

        def v_now():
            t = theta.get_value() * DEGREES
            return R * np.array([np.cos(t), np.sin(t)])

        def av_now():
            return A @ v_now()

        def parallel():
            """True when v and A v lie on one line (normalised cross product ~ 0)."""
            v, av = v_now(), av_now()
            cross = v[0] * av[1] - v[1] * av[0]
            return abs(cross) / (np.linalg.norm(v) * np.linalg.norm(av)) < 0.02

        # The span line of v turns green and thick whenever A v lies on it.
        span = always_redraw(lambda: Line(
            plane.c2p(*(-5 * v_now() / R)), plane.c2p(*(5 * v_now() / R)),
            color=COL_E1 if parallel() else GRAY,
            stroke_width=8 if parallel() else 2,
            stroke_opacity=1 if parallel() else 0.6,
        ))
        v_arr = always_redraw(lambda: self.arrow(ORIGIN, plane.c2p(*v_now()), COL_V, width=8))
        av_arr = always_redraw(lambda: self.arrow(ORIGIN, plane.c2p(*av_now()), COL_AV, width=5))
        v_lab = always_redraw(lambda: MathTex(r"\mathbf{v}", color=COL_V, font_size=36)
                              .move_to(plane.c2p(*(v_now() * 0.55)) + 0.35 * rotate_vector(
                                  normalize(np.append(v_now(), 0)), PI / 2)))
        av_lab = always_redraw(lambda: MathTex(r"A\mathbf{v}", color=COL_AV, font_size=36)
                               .next_to(plane.c2p(*av_now()),
                                        normalize(np.append(av_now(), 0)), buff=0.15))
        circle = Circle(radius=R, color=COL_V, stroke_opacity=0.35).move_to(plane.c2p(0, 0))
        trace = TracedPath(lambda: plane.c2p(*av_now()), stroke_color=COL_AV,
                           stroke_width=3, stroke_opacity=0.8)

        self.say(lines[0])
        self.play(Create(plane), FadeIn(labels), FadeIn(badge), run_time=1.5)
        self.play(Create(circle), FadeIn(span, v_arr, av_arr, v_lab, av_lab))
        self.add(trace)
        self.play(theta.animate.set_value(45), run_time=4, rate_func=linear)
        lab45 = self.label(r"A\mathbf{v} = 3\mathbf{v}", COL_E1).next_to(
            plane.c2p(*av_now()), RIGHT, buff=0.3).shift(DOWN * 0.7)
        self.play(Write(lab45))

        self.say(lines[1])
        self.play(FadeOut(lab45), theta.animate.set_value(135), run_time=4, rate_func=linear)
        lab135 = self.label(r"A\mathbf{v} = 1\mathbf{v}", COL_E2).next_to(
            plane.c2p(*av_now()), LEFT, buff=0.7).shift(DOWN * 0.45)
        self.play(Write(lab135))

        self.say(lines[2])
        self.play(FadeOut(lab135), theta.animate.set_value(360), run_time=7, rate_func=linear)
        # The ellipse's axes lie along the two eigen-directions.
        ax1 = DashedLine(plane.c2p(-4, -4), plane.c2p(4, 4), color=COL_E1, dash_length=0.15)
        ax2 = DashedLine(plane.c2p(3, -3), plane.c2p(-3, 3), color=COL_E2, dash_length=0.15)
        self.play(Create(ax1), Create(ax2))
        self.clear_screen()

    # ====================================================================
    # PART 6 - A acting on the whole grid
    # ====================================================================
    def part06_grid(self):
        bg = self.make_plane(opacity=0.15)
        fg = self.make_plane(opacity=0.55)
        labels = self.axis_labels(bg)
        badge = self.matrix_badge()
        diag = Line(bg.c2p(-4, -4), bg.c2p(4, 4), color=COL_E1, stroke_width=6)     # y = x
        anti = Line(bg.c2p(-4, 4), bg.c2p(4, -4), color=COL_E2, stroke_width=6)     # y = -x
        x_copy = Line(bg.c2p(-7, 0), bg.c2p(7, 0), color=COL_V, stroke_width=5)     # x-axis

        self.say(NARRATION["grid"][0])
        self.add(bg)
        self.play(Create(fg), FadeIn(labels), FadeIn(badge), run_time=1.2)
        self.play(Create(diag), Create(anti), Create(x_copy))
        moving = VGroup(fg, diag, anti, x_copy)
        moving.save_state()
        fg.prepare_for_nonlinear_transform()
        self.play(ApplyMatrix(A, moving), run_time=4)

        lab1 = Tex(r"$y = x$: $\times 3$", color=COL_E1, font_size=38)
        lab1.add_background_rectangle(opacity=0.85, buff=0.1).move_to(bg.c2p(1.6, 3.2))
        lab2 = Tex(r"$y = -x$: $\times 1$", color=COL_E2, font_size=38)
        lab2.add_background_rectangle(opacity=0.85, buff=0.1).move_to(bg.c2p(-4.0, 2.4))
        lab3 = Tex(r"$x$-axis: rotated", color=COL_V, font_size=34)
        lab3.add_background_rectangle(opacity=0.85, buff=0.1).move_to(bg.c2p(5.2, 1.8))
        self.play(FadeIn(lab1), FadeIn(lab2), FadeIn(lab3))
        self.clear_screen()

    # ====================================================================
    # PART 7 - deriving the characteristic equation
    # ====================================================================
    def part07_derivation(self):
        lines = NARRATION["derivation"]
        size = 52

        # Each line is split into pieces so TransformMatchingTex can move
        # matching pieces (A, v, lambda, =) from one line to the next.
        l1 = MathTex("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", font_size=size)
        l2 = MathTex("A", r"\mathbf{v}", "-", r"\lambda", "I", r"\mathbf{v}", "=",
                     r"\mathbf{0}", font_size=size)
        l3 = MathTex("(", "A", "-", r"\lambda", "I", ")", r"\mathbf{v}", "=",
                     r"\mathbf{0}", font_size=size)
        for line in (l1, l2, l3):
            for piece in line:
                if piece.get_tex_string() == "A":
                    piece.set_color(COL_A)
                if piece.get_tex_string() == r"\mathbf{v}":
                    piece.set_color(COL_V)

        # Stack the lines with their "=" signs in one column.
        l1.move_to(UP * 2.9)
        l2.next_to(l1, DOWN, buff=0.45)
        l3.next_to(l2, DOWN, buff=0.45)
        eq_x = -1.0
        for line in (l1, l2, l3):
            eq = [p for p in line if p.get_tex_string() == "="][0]
            line.shift(RIGHT * (eq_x - eq.get_center()[0]))

        note2 = Tex(r"($\lambda\mathbf{v} = \lambda I\mathbf{v}$)", font_size=36, color=GRAY_B)
        note2.next_to(l2, RIGHT, buff=0.6).set_x(4.6)
        note3 = Text("(factor out v)", font_size=28, color=GRAY_B)
        note3.next_to(l3, RIGHT, buff=0.6).set_x(4.6)

        self.say(lines[0])
        self.play(Write(l1))

        self.say(lines[1])
        self.play(TransformMatchingTex(l1.copy(), l2), run_time=1.5)
        self.play(FadeIn(note2))

        self.say(lines[2])
        self.play(TransformMatchingTex(l2.copy(), l3), run_time=1.5)
        self.play(FadeIn(note3))

        # Proof by contradiction, in red.
        self.say(lines[3])
        c1 = MathTex(r"\text{If } (A - \lambda I)^{-1} \text{ existed: }\ "
                     r"\mathbf{v} = (A - \lambda I)^{-1}\mathbf{0} = \mathbf{0}",
                     font_size=40, color=RED)
        c2 = MathTex(r"\Rightarrow\ \text{contradiction, since } \mathbf{v} \neq \mathbf{0}",
                     font_size=40, color=RED)
        contra = VGroup(c1, c2).arrange(DOWN, buff=0.25).next_to(l3, DOWN, buff=0.6).set_x(0)
        self.play(Write(c1), run_time=2)
        self.play(Write(c2), run_time=1.5)

        self.say(lines[4])
        final = MathTex(r"\det(A - \lambda I) = 0", font_size=60)
        final[0][4].set_color(COL_A)          # the "A" inside det(A - lambda I)
        final_box = SurroundingRectangle(final, color=COL_A, buff=0.25, corner_radius=0.1)
        caption = Text("characteristic equation", font_size=30, color=COL_A)
        result = VGroup(VGroup(final, final_box), caption).arrange(RIGHT, buff=0.5)
        result.next_to(contra, DOWN, buff=0.6).set_x(0)
        self.play(Write(final))
        self.play(Create(final_box), FadeIn(caption))
        self.clear_screen()

    # ====================================================================
    # PART 8 - solving the characteristic equation for our matrix
    # ====================================================================
    def part08_solve(self):
        lines = NARRATION["solve"]
        size = 42

        top = MathTex(r"A - \lambda I = \begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix}",
                      font_size=46)
        top[0][0].set_color(COL_A)
        top.to_edge(UP, buff=0.5)

        # Rows of the computation; each is (left side, right side) so the
        # "=" signs can be lined up in one column.
        rows_tex = [
            (r"\det(A - \lambda I)", r"(2-\lambda)(2-\lambda) - (1)(1)"),
            ("", r"\lambda^2 - 4\lambda + 4 - 1"),
            ("", r"\lambda^2 - 4\lambda + 3"),
            ("", r"(\lambda - 1)(\lambda - 3) = 0"),
        ]
        rows = VGroup()
        for lhs, rhs in rows_tex:
            parts = [lhs, "=", rhs] if lhs else ["=", rhs]
            rows.add(MathTex(*parts, font_size=size))
        rows.arrange(DOWN, buff=0.4).next_to(top, DOWN, buff=0.6)
        eq_x = -1.4
        for row in rows:
            eq = row[1] if len(row) == 3 else row[0]
            row.shift(RIGHT * (eq_x - eq.get_left()[0]))

        r1 = MathTex(r"\lambda_1 = 3", color=COL_E1, font_size=54)
        r2 = MathTex(r"\lambda_2 = 1", color=COL_E2, font_size=54)
        results = VGroup(r1, r2).arrange(RIGHT, buff=2.0).next_to(rows, DOWN, buff=0.6).set_x(0)

        self.say(lines[0])
        self.play(Write(top), run_time=2)

        self.say(lines[1])
        self.play(Write(rows[0]), run_time=2)

        self.say(lines[2])
        self.play(Write(rows[1]))
        self.play(Write(rows[2]))
        self.play(Write(rows[3]))

        self.say(lines[3])
        self.play(FadeIn(r1, shift=UP * 0.2), FadeIn(r2, shift=UP * 0.2))
        self.play(Circumscribe(results, color=WHITE))
        self.clear_screen()

    # ====================================================================
    # PART 9 - eigenvectors from (A - lambda I) v = 0, then check
    # ====================================================================
    def part09_eigenvectors(self):
        lines = NARRATION["eigenvectors"]
        left = self._eigen_column(3, [[-1, 1], [1, -1]], r"-x + y = 0 \;\Rightarrow\; y = x",
                                  r"\mathbf{v}_1", (1, 1), COL_E1)
        right = self._eigen_column(1, [[1, 1], [1, 1]], r"x + y = 0 \;\Rightarrow\; y = -x",
                                   r"\mathbf{v}_2", (1, -1), COL_E2)
        left.move_to(LEFT * 3.5).to_edge(UP, buff=0.35)
        right.move_to(RIGHT * 3.5).to_edge(UP, buff=0.35)
        divider = DashedLine(UP * 3.7, DOWN * 3.2, color=GRAY_C)

        # Left column: lambda = 3.
        self.say(lines[0])
        self.play(Create(divider), FadeIn(left[0]))
        self.play(Write(left[1]))

        self.say(lines[1])
        self.play(Write(left[2]))
        self.play(Write(left[3]))
        self.play(Write(left[4]))

        # Right column: lambda = 1.
        self.say(lines[2])
        self.play(FadeIn(right[0]))
        self.play(Write(right[1]))
        self.play(Write(right[2]), Write(right[3]))
        self.play(Write(right[4]))

        # Repeated rows: the determinant is zero, so the rows are dependent.
        self.say(lines[3])
        boxes = VGroup()
        for col in (left, right):
            matrix = col[1][1]
            for row in matrix.get_rows():
                boxes.add(SurroundingRectangle(row, color=YELLOW_B, buff=0.08))
        note = Text("rows repeat  →  det = 0  →  a whole line of solutions",
                    font_size=28, color=YELLOW_B).to_edge(DOWN, buff=0.3)
        note.add_background_rectangle(opacity=0.9, buff=0.1)
        self.play(Create(boxes), FadeIn(note))
        self.finish()

        # Check by substitution.
        self.say(lines[4])
        self.play(FadeOut(left[1:4], right[1:4], boxes, note, divider))
        # Move each eigenvector up under its header to make room for the check.
        self.play(left[4].animate.next_to(left[0], DOWN, buff=0.3),
                  right[4].animate.next_to(right[0], DOWN, buff=0.3))
        chk1 = MathTex(
            r"A\mathbf{v}_1 = " + A_TEX + tex_vec(1, 1)
            + r" = \begin{pmatrix} 2+1 \\ 1+2 \end{pmatrix} = " + tex_vec(3, 3)
            + r" = 3\mathbf{v}_1 \;\checkmark", font_size=40, color=COL_E1)
        chk2 = MathTex(
            r"A\mathbf{v}_2 = " + A_TEX + tex_vec(1, -1)
            + r" = \begin{pmatrix} 2-1 \\ 1-2 \end{pmatrix} = " + tex_vec(1, -1)
            + r" = 1\,\mathbf{v}_2 \;\checkmark", font_size=40, color=COL_E2)
        checks = VGroup(chk1, chk2).arrange(DOWN, buff=0.5).shift(DOWN * 1.2)
        self.play(Write(chk1), run_time=2.5)
        self.play(Write(chk2), run_time=2.5)
        self.clear_screen()

    def _eigen_column(self, lam, m, eq_tex, name, vec, color):
        """One column of part 9: header, A - lam I, the matrix equation, the
        reduced equation and the chosen eigenvector."""
        header = MathTex(r"\lambda = " + str(lam), color=color, font_size=46)
        mat = IntegerMatrix(m).scale(0.8)
        row1 = VGroup(MathTex(r"A - " + ("I" if lam == 1 else f"{lam}I") + " =", font_size=40), mat)
        row1.arrange(RIGHT, buff=0.2)
        row1[0][0][0].set_color(COL_A)
        row2 = VGroup(IntegerMatrix(m).scale(0.8),
                      MathTex(r"\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}",
                              font_size=40)).arrange(RIGHT, buff=0.1)
        row3 = MathTex(eq_tex, font_size=40)
        row4 = MathTex(name + " = " + tex_vec(*vec), color=color, font_size=44)
        return VGroup(header, row1, row2, row3, row4).arrange(DOWN, buff=0.35)

    # ====================================================================
    # PART 10 - area: det = product of eigenvalues, trace = sum
    # ====================================================================
    def part10_area(self):
        lines = NARRATION["area"]
        plane = self.make_plane(opacity=0.45, x_range=[-2, 5, 1], y_range=[-2, 4, 1],
                                x_length=7, y_length=6)
        plane.shift(np.array([-4.8, -0.8, 0]) - plane.c2p(0, 0))   # origin at (-4.8, -0.8)
        labels = self.axis_labels(plane)
        O = plane.c2p(0, 0)

        def parallelogram(a, b):
            return Polygon(O, plane.c2p(*a), plane.c2p(*(a + b)), plane.c2p(*b),
                           color=BLUE_B, fill_color=BLUE, fill_opacity=0.35, stroke_width=3)

        poly = parallelogram(V1, V2)
        a1 = self.arrow(O, plane.c2p(*V1), COL_E1)
        a2 = self.arrow(O, plane.c2p(*V2), COL_E2)
        l1 = self.label(r"\mathbf{v}_1", COL_E1).next_to(plane.c2p(*V1), UL, buff=0.1)
        l2 = self.label(r"\mathbf{v}_2", COL_E2).next_to(plane.c2p(*V2), DL, buff=0.1)
        area = self.label(r"\text{Area} = 2", size=34).move_to(plane.c2p(1, 0))

        self.say(lines[0])
        self.play(Create(plane), FadeIn(labels), run_time=1.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2))
        self.play(FadeIn(poly), FadeIn(area))

        self.say(lines[1])
        poly2 = parallelogram(A @ V1, A @ V2)
        b1 = self.arrow(O, plane.c2p(*(A @ V1)), COL_E1)
        b2 = self.arrow(O, plane.c2p(*(A @ V2)), COL_E2)
        m1 = self.label(r"A\mathbf{v}_1 = 3\mathbf{v}_1", COL_E1).next_to(plane.c2p(3, 3), RIGHT, buff=0.1)
        m2 = self.label(r"A\mathbf{v}_2 = \mathbf{v}_2", COL_E2).next_to(plane.c2p(1, -1), DR, buff=0.1)
        area2 = self.label(r"\text{Area} = 6", size=34).move_to(plane.c2p(2, 1))
        self.play(Transform(poly, poly2), Transform(a1, b1), Transform(a2, b2),
                  FadeOut(l1, l2, area), run_time=3)
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(area2))

        # Info panel on the right.
        self.say(lines[2])
        i1 = MathTex(r"\text{New area} = 6 = 3 \times 2", font_size=38)
        i2 = MathTex(r"\det A = 4 - 1 = 3", font_size=38)
        i3 = MathTex(r"= \lambda_1 \lambda_2 = 3 \times 1", font_size=38)
        i4 = MathTex(r"\operatorname{tr} A = 2 + 2 = 4", font_size=38)
        i5 = MathTex(r"= \lambda_1 + \lambda_2 = 3 + 1", font_size=38)
        info = VGroup(i1, i2, i3, i4, i5).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        i3.shift(RIGHT * 0.9)
        i5.shift(RIGHT * 0.9)
        info.move_to(RIGHT * 3.9 + UP * 0.2)
        panel = SurroundingRectangle(info, color=COL_A, buff=0.3, corner_radius=0.1)
        panel.set_fill(config.background_color, opacity=0.9)
        self.play(FadeIn(panel), Write(i1))
        self.play(Write(i2))
        self.play(Write(i3))

        self.say(lines[3])
        self.play(Write(i4))
        self.play(Write(i5))
        self.clear_screen()

    # ====================================================================
    # PART 11 - any vector in the eigenvector basis
    # ====================================================================
    def part11_basis(self):
        lines = NARRATION["basis"]
        # Zoomed plane: 1 grid unit = 2 screen units, grid lines every 0.5.
        plane = self.make_plane(opacity=0.45, x_range=[-1, 2.5, 0.5], y_range=[-1.5, 2, 0.5],
                                x_length=7, y_length=7)
        plane.shift(np.array([-4.3, -0.8, 0]) - plane.c2p(0, 0))
        labels = self.axis_labels(plane)
        O = plane.c2p(0, 0)
        half1, half2 = 0.5 * V1, 0.5 * V2

        e = self.arrow(O, plane.c2p(1, 0), COL_V, width=8)
        e_lab = self.label(r"\begin{pmatrix}1\\0\end{pmatrix}", COL_V, 34).next_to(
            plane.c2p(1, 0), DOWN, buff=0.2)
        g = self.arrow(O, plane.c2p(*half1), COL_E1)                       # (1/2) v1
        o = self.arrow(plane.c2p(*half1), plane.c2p(*(half1 + half2)), COL_E2)   # (1/2) v2, tip to tail
        g_lab = self.label(r"\tfrac12\mathbf{v}_1", COL_E1).next_to(plane.c2p(*(half1 / 2)), UL, buff=0.1)
        o_lab = self.label(r"\tfrac12\mathbf{v}_2", COL_E2).next_to(plane.c2p(0.75, 0.25), UR, buff=0.1)
        decomp = MathTex(r"\begin{pmatrix}1\\0\end{pmatrix} = \tfrac12\mathbf{v}_1 + \tfrac12\mathbf{v}_2",
                         font_size=40)
        decomp.move_to(RIGHT * 4.2 + UP * 2.6)

        self.say(lines[0])
        self.play(Create(plane), FadeIn(labels), run_time=1.5)
        self.play(GrowArrow(e), FadeIn(e_lab))
        self.play(GrowArrow(g), FadeIn(g_lab))
        self.play(GrowArrow(o), FadeIn(o_lab))
        self.play(Write(decomp))

        # Apply A: the green part triples, the orange part stays the same length.
        self.say(lines[1])
        big1 = LAM1 * half1
        g2 = self.arrow(O, plane.c2p(*big1), COL_E1)
        o2 = self.arrow(plane.c2p(*big1), plane.c2p(*(big1 + LAM2 * half2)), COL_E2)
        g2_lab = self.label(r"3 \cdot \tfrac12\mathbf{v}_1", COL_E1).next_to(plane.c2p(0.75, 0.75), UL, buff=0.1)
        o2_lab = self.label(r"1 \cdot \tfrac12\mathbf{v}_2", COL_E2).next_to(plane.c2p(1.75, 1.25), UR, buff=0.1)
        self.play(e.animate.set_opacity(0.3), FadeOut(g_lab, o_lab))
        self.play(Transform(g, g2), Transform(o, o2), run_time=2.5)
        self.play(FadeIn(g2_lab), FadeIn(o2_lab))
        red = self.arrow(O, plane.c2p(2, 1), COL_AV)
        red_lab = self.label(r"\begin{pmatrix}2\\1\end{pmatrix}", COL_AV, 34).next_to(
            plane.c2p(2, 1), DR, buff=0.15)
        self.play(GrowArrow(red), FadeIn(red_lab))

        eq1 = MathTex(r"A\begin{pmatrix}1\\0\end{pmatrix} = 3 \cdot \tfrac12\mathbf{v}_1 + 1 \cdot \tfrac12\mathbf{v}_2",
                      font_size=40)
        eq2 = MathTex(r"= \begin{pmatrix}1.5\\1.5\end{pmatrix} + \begin{pmatrix}0.5\\-0.5\end{pmatrix}",
                      font_size=40)
        eq3 = MathTex(r"= \begin{pmatrix}2\\1\end{pmatrix}", font_size=40, color=COL_AV)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        eq2.shift(RIGHT * 1.0)
        eq3.shift(RIGHT * 1.0)
        eqs.next_to(decomp, DOWN, buff=0.6).set_x(4.0)
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.play(Write(eq3))

        self.say(lines[2])
        caption = Tex(r"In the eigenvector basis, $A$ is just scaling: $\times 3$ and $\times 1$",
                      font_size=38)
        caption.to_edge(DOWN, buff=0.35).add_background_rectangle(opacity=0.9, buff=0.15)
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.clear_screen()

    # ====================================================================
    # PART 12 - three takeaways
    # ====================================================================
    def part12_recap(self):
        lines = NARRATION["recap"]
        title = Text("Three takeaways", font_size=48, weight=BOLD).to_edge(UP, buff=0.6)
        items = VGroup(
            VGroup(Tex(r"(1) An eigenvector is a nonzero direction $A$ only stretches,", font_size=38),
                   Tex(r"shrinks or flips: $A\mathbf{v} = \lambda\mathbf{v}$.", font_size=38)),
            VGroup(Tex(r"(2) Eigenvalues solve $\det(A - \lambda I) = 0$;", font_size=38),
                   Tex(r"each eigenvector solves $(A - \lambda I)\mathbf{v} = \mathbf{0}$.", font_size=38)),
            VGroup(Tex(r"(3) In the eigenvector basis, $A$ is pure scaling", font_size=38),
                   Tex(r"($\times 3$ along $y = x$, $\times 1$ along $y = -x$).", font_size=38)),
        )
        for item in items:
            item.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            item[1].shift(RIGHT * 0.65)          # indent the second line
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(title, DOWN, buff=0.7)

        self.say(lines[0])
        self.play(Write(title))
        for i, item in enumerate(items):
            self.say(lines[i + 1])
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=1.2)
        self.clear_screen()

    # ====================================================================
    # PART 13 - closing frame: references, credits, AI disclosure
    # ====================================================================
    def part13_closing(self):
        def heading(text):
            return Text(text, font_size=32, weight=BOLD, color=COL_A)

        def body(text):
            return Text(text, font_size=24)

        refs = VGroup(
            heading("References"),
            body("• G. Strang, Introduction to Linear Algebra, 5th ed., Ch. 6"),
            body("• 3Blue1Brown, Essence of Linear Algebra, Ch. 14 (visual-style inspiration)"),
            body("• Manim Community Edition"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        music = VGroup(heading("Music"), body("none")).arrange(RIGHT, buff=0.3)
        disclosure = VGroup(
            heading("AI disclosure"),
            body("\u201cAnimation code and narration draft prepared with help from"),
            body("an AI assistant; all mathematics checked by hand by the student;"),
            body("voice-over recorded by the student.\u201d"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        credits = VGroup(refs, music, disclosure).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        credits.to_edge(UP, buff=0.35)

        details = VGroup(
            Text(f"Name: {STUDENT_NAME}   |   URN: {URN}", font_size=26, color=GRAY_A),
            Text(f"Batch: {BATCH}   |   Lab: {LAB}", font_size=26, color=GRAY_A),
        ).arrange(DOWN, buff=0.12)
        thanks = Text("Thanks for watching!", font_size=44, weight=BOLD)
        end = VGroup(details, thanks).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.35)

        self.say(NARRATION["closing"][0])
        self.play(FadeIn(refs, shift=UP * 0.2))
        self.play(FadeIn(music), FadeIn(disclosure, shift=UP * 0.2))
        self.play(FadeIn(end))
        self.finish()
        self.wait(3)                                   # hold the final frame for 3 s
        self.play(FadeOut(*self.mobjects), run_time=1.5)


# ============================================================================
# 4. SCENES - the full video, and one scene per part for testing
# ============================================================================

PARTS = [
    "part01_opening", "part02_hook", "part03_definition", "part04_tests",
    "part05_sweep", "part06_grid", "part07_derivation", "part08_solve",
    "part09_eigenvectors", "part10_area", "part11_basis", "part12_recap",
    "part13_closing",
]


class FullVideo(EigenBase):
    """The complete video: every part, in order."""

    def construct(self):
        for name in PARTS:
            getattr(self, name)()


class Part01Opening(EigenBase):
    def construct(self): self.part01_opening()


class Part02Hook(EigenBase):
    def construct(self): self.part02_hook()


class Part03Definition(EigenBase):
    def construct(self): self.part03_definition()


class Part04Tests(EigenBase):
    def construct(self): self.part04_tests()


class Part05Sweep(EigenBase):
    def construct(self): self.part05_sweep()


class Part06Grid(EigenBase):
    def construct(self): self.part06_grid()


class Part07Derivation(EigenBase):
    def construct(self): self.part07_derivation()


class Part08Solve(EigenBase):
    def construct(self): self.part08_solve()


class Part09Eigenvectors(EigenBase):
    def construct(self): self.part09_eigenvectors()


class Part10Area(EigenBase):
    def construct(self): self.part10_area()


class Part11Basis(EigenBase):
    def construct(self): self.part11_basis()


class Part12Recap(EigenBase):
    def construct(self): self.part12_recap()


class Part13Closing(EigenBase):
    def construct(self): self.part13_closing()