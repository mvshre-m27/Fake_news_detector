#importing libraries
import gradio as gr
from analyzer import analyze_news
from clickbait import clickbait_score
def analyze(headline, body):

    if not headline or not headline.strip():
        return (
            "<div class='empty-result'>Enter a headline to begin analysis.</div>",
            "",
            "",
            ""
        )

    if not body or not body.strip():
        return (
            "<div class='empty-result'>Enter the article body to begin analysis.</div>",
            "",
            "",
            ""
        )

    result = analyze_news(headline, body)


    if result["prediction"] == 0:

        prediction_html = f"""
        <div class="main-result fake-result">

            <div class="result-kicker">MODEL PREDICTION</div>

            <div class="prediction-row">
                <div>
                    <div class="prediction-status">
                        <span class="dot fake-dot"></span>
                        Likely Fake
                    </div>

                    <div class="prediction-number">
                        {result["fake_probability"]:.2f}%
                    </div>

                    <div class="prediction-caption">
                        fake probability
                    </div>
                </div>

                <div class="secondary-prob">
                    {result["real_probability"]:.2f}%<br>
                    <span>real</span>
                </div>
            </div>

            <div class="bar">
                <div class="bar-fill fake-fill"
                     style="width:{result["fake_probability"]}%">
                </div>
            </div>

            <p class="description">
                The model detected patterns that are more
                associated with fake news in the training dataset.
            </p>

        </div>
        """

    else:

        prediction_html = f"""
        <div class="main-result real-result">

            <div class="result-kicker">MODEL PREDICTION</div>

            <div class="prediction-row">
                <div>
                    <div class="prediction-status">
                        <span class="dot real-dot"></span>
                        Likely Real
                    </div>

                    <div class="prediction-number">
                        {result["real_probability"]:.2f}%
                    </div>

                    <div class="prediction-caption">
                        real probability
                    </div>
                </div>

                <div class="secondary-prob">
                    {result["fake_probability"]:.2f}%<br>
                    <span>fake</span>
                </div>
            </div>

            <div class="bar">
                <div class="bar-fill real-fill"
                     style="width:{result["real_probability"]}%">
                </div>
            </div>

            <p class="description">
                The model detected patterns that are more
                associated with real news in the training dataset.
            </p>

        </div>
        """

    discrepancy = result["discrepancy_score"]
    match = result["hybrid_match"]

    if discrepancy < 30:
        status = "High consistency"
        status_class = "good"
        dot_class = "real-dot"
        message = (
            "The headline is strongly aligned with the "
            "information in the article body."
        )

    elif discrepancy < 60:
        status = "Moderate discrepancy"
        status_class = "warning"
        dot_class = "warning-dot"
        message = (
            "The headline and article body show some differences."
        )

    else:
        status = "High discrepancy"
        status_class = "danger"
        dot_class = "fake-dot"
        message = (
            "The headline may not accurately represent "
            "the article body."
        )

    consistency_html = f"""
    <div class="main-result">

        <div class="result-kicker">HEADLINE–BODY CONSISTENCY</div>

        <div class="prediction-status">
            <span class="dot {dot_class}"></span>
            {status}
        </div>

        <div class="match-number">
            {match:.2f}%
        </div>

        <div class="prediction-caption">
            headline–body match
        </div>

        <div class="bar">
            <div class="bar-fill match-fill"
                 style="width:{match}%">
            </div>
        </div>

        <div class="three-metrics">

            <div>
                <span>TF-IDF</span>
                <strong>
                    {result["lexical_similarity"]:.2f}%
                </strong>
            </div>

            <div>
                <span>Semantic</span>
                <strong>
                    {result["semantic_similarity"]:.2f}%
                </strong>
            </div>

            <div>
                <span>Discrepancy</span>
                <strong class="{status_class}-text">
                    {discrepancy:.2f}%
                </strong>
            </div>

        </div>

        <p class="description">
            {message}
        </p>

    </div>
    """
#clickbait score

    score, level, reasons = clickbait_score(headline)

    if score >= 60:
        click_class = "danger"
        click_dot = "fake-dot"
    elif score >= 30:
        click_class = "warning"
        click_dot = "warning-dot"
    else:
        click_class = "good"
        click_dot = "real-dot"

    if reasons:
        reasons_html = ""

        for reason in reasons:
            reasons_html += f"""
            <div class="reason">
                {reason}
            </div>
            """

    else:
        reasons_html = """
        <div class="no-warning">
            ✓ No major clickbait indicators detected.
        </div>
        """

    clickbait_html = f"""
    <div class="small-card">

        <div class="card-heading">
            <span class="card-icon">01</span>
            Clickbait analysis
        </div>

        <div class="clickbait-row">

            <div>
                <div class="prediction-status small-status">
                    <span class="dot {click_dot}"></span>
                    {level.title()}
                </div>

                <div class="description">
                    Based on headline wording and formatting.
                </div>
            </div>

            <div class="click-number">
                {score}<span>/100</span>
            </div>

        </div>

        <div class="bar">
            <div class="bar-fill click-fill"
                 style="width:{score}%">
            </div>
        </div>

        <div class="reasons">
            {reasons_html}
        </div>

    </div>
    """

#overall assessment with statistics

    if discrepancy >= 60 and score >= 60:

        assessment_class = "assessment-danger"
        assessment_title = "Review recommended"
        assessment_message = (
            "The headline shows both high headline–body "
            "discrepancy and strong clickbait indicators."
        )

    elif discrepancy >= 60:

        assessment_class = "assessment-warning"
        assessment_title = "Headline requires review"
        assessment_message = (
            "The headline does not closely match the "
            "information presented in the article body."
        )

    elif score >= 60:

        assessment_class = "assessment-warning"
        assessment_title = "Strong clickbait indicators"
        assessment_message = (
            "The headline contains patterns commonly "
            "associated with sensational content."
        )

    else:

        assessment_class = "assessment-good"
        assessment_title = "No major warning detected"
        assessment_message = (
            "No major headline–body discrepancy or "
            "clickbait indicators were detected."
        )

    assessment_html = f"""

    <div class="assessment {assessment_class}">

        <div class="assessment-kicker">
            OVERALL ASSESSMENT
        </div>

        <div class="assessment-title">
            {assessment_title}
        </div>

        <div class="assessment-message">
            {assessment_message}
        </div>

    </div>

    <div class="stats-grid">

        <div class="stat-card">
            <span>HEADLINE</span>
            <strong>{result["title_words"]}</strong>
            <small>words</small>
        </div>

        <div class="stat-card">
            <span>ARTICLE</span>
            <strong>{result["body_words"]}</strong>
            <small>words</small>
        </div>

        <div class="stat-card">
            <span>LENGTH RATIO</span>
            <strong>{result["length_ratio"]:.3f}</strong>
            <small>headline / body</small>
        </div>

        <div class="stat-card">
            <span>QUESTIONS</span>
            <strong>{result["question_marks"]}</strong>
            <small>in headline</small>
        </div>

        <div class="stat-card">
            <span>EXCLAMATIONS</span>
            <strong>{result["exclamation_marks"]}</strong>
            <small>in headline</small>
        </div>

    </div>

    """

    return (
        prediction_html,
        consistency_html,
        clickbait_html,
        assessment_html
    )

def clear_all():

    return (
        "",
        "",
        "",
        "",
        "",
    )

#css

css = """

/* ============================================================
   PAGE
   ============================================================ */

body {
    background: #f6f7fb !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: auto !important;
    padding: 0 35px 40px 35px !important;
    font-family: Arial, Helvetica, sans-serif !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.brand {
    padding: 30px 5px 22px 5px;
    border-bottom: 1px solid #e5e7eb;
}

.brand-name {
    font-size: 25px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.8px;
}

.brand-name span {
    color: #4f46e5;
}

.brand-subtitle {
    margin-top: 5px;
    font-size: 13px;
    color: #6b7280;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 55px 10px 45px 10px;
}

.hero h1 {
    font-size: 48px;
    line-height: 1.1;
    color: #111827;
    margin: 0 0 15px 0;
    font-weight: 800;
    letter-spacing: -2px;
}

.hero p {
    max-width: 700px;
    margin: auto;
    color: #6b7280;
    font-size: 16px;
    line-height: 1.7;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #6b7280;
    margin-bottom: 14px;
}


/* ============================================================
   INPUT
   ============================================================ */

.input-panel {
    background: #ffffff;
    border: 1px solid #e1e5ec;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 10px 35px rgba(15, 23, 42, 0.06);
}

.input-panel-title {
    font-size: 18px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 22px;
}

.input-panel-subtitle {
    font-size: 13px;
    color: #9ca3af;
    margin-top: -15px;
    margin-bottom: 20px;
}


/* ============================================================
   TEXTBOX
   ============================================================ */

textarea,
input {
    background: #fafbfc !important;
    border: 1px solid #d9dee8 !important;
    border-radius: 11px !important;
    font-size: 14px !important;
    color: #111827 !important;
}

textarea {
    line-height: 1.6 !important;
}

textarea:focus,
input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.10) !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.analyze-btn {
    height: 50px !important;
    border-radius: 11px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    background: #4f46e5 !important;
    border: none !important;
}

.clear-btn {
    height: 50px !important;
    border-radius: 11px !important;
    font-size: 15px !important;
}


/* ============================================================
   RESULT CARDS
   ============================================================ */

.main-result {
    background: #ffffff;
    border: 1px solid #e1e5ec;
    border-radius: 18px;
    padding: 27px;
    margin-bottom: 17px;
    box-shadow: 0 10px 35px rgba(15, 23, 42, 0.05);
}

.real-result {
    border-top: 4px solid #10b981;
}

.fake-result {
    border-top: 4px solid #ef4444;
}

.result-kicker {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
    color: #9ca3af;
    margin-bottom: 14px;
}

.prediction-status {
    font-size: 21px;
    font-weight: 800;
    color: #111827;
    display: flex;
    align-items: center;
    gap: 9px;
    text-transform: capitalize;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

.real-dot {
    background: #10b981;
}

.fake-dot {
    background: #ef4444;
}

.warning-dot {
    background: #f59e0b;
}

.prediction-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}

.prediction-number {
    font-size: 43px;
    line-height: 1;
    font-weight: 800;
    color: #111827;
    margin-top: 15px;
    letter-spacing: -1px;
}

.prediction-caption {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 5px;
}

.secondary-prob {
    text-align: right;
    font-size: 18px;
    font-weight: 700;
    color: #9ca3af;
    line-height: 1.2;
}

.secondary-prob span {
    font-size: 11px;
    font-weight: 500;
}


/* ============================================================
   PROGRESS
   ============================================================ */

.bar {
    width: 100%;
    height: 8px;
    background: #edf0f4;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 19px;
}

.bar-fill {
    height: 100%;
    border-radius: 20px;
}

.real-fill {
    background: #10b981;
}

.fake-fill {
    background: #ef4444;
}

.match-fill {
    background: #6366f1;
}

.click-fill {
    background: #f59e0b;
}


/* ============================================================
   DESCRIPTION
   ============================================================ */

.description {
    color: #6b7280;
    font-size: 13px;
    line-height: 1.6;
    margin: 15px 0 0 0;
}


/* ============================================================
   MATCH
   ============================================================ */

.match-number {
    font-size: 43px;
    font-weight: 800;
    color: #111827;
    line-height: 1;
    margin-top: 16px;
    letter-spacing: -1px;
}


/* ============================================================
   THREE METRICS
   ============================================================ */

.three-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 20px;
}

.three-metrics div {
    background: #f8f9fb;
    border-radius: 10px;
    padding: 13px;
}

.three-metrics span {
    display: block;
    font-size: 10px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: .5px;
}

.three-metrics strong {
    display: block;
    margin-top: 5px;
    font-size: 15px;
    color: #111827;
}

.danger-text {
    color: #ef4444 !important;
}

.warning-text {
    color: #d97706 !important;
}

.good-text {
    color: #059669 !important;
}


/* ============================================================
   SMALL CARD
   ============================================================ */

.small-card {
    background: #ffffff;
    border: 1px solid #e1e5ec;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 10px 35px rgba(15, 23, 42, 0.04);
    min-height: 190px;
}

.card-heading {
    font-size: 16px;
    font-weight: 800;
    color: #111827;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 22px;
}

.card-icon {
    width: 26px;
    height: 26px;
    border-radius: 7px;
    background: #eef2ff;
    color: #4f46e5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 800;
}

.clickbait-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.small-status {
    font-size: 17px;
}

.click-number {
    font-size: 35px;
    font-weight: 800;
    color: #111827;
}

.click-number span {
    font-size: 12px;
    color: #9ca3af;
    font-weight: 500;
}

.reason {
    padding: 7px 0;
    font-size: 12px;
    color: #6b7280;
}

.no-warning {
    margin-top: 17px;
    color: #059669;
    font-size: 12px;
}


/* ============================================================
   ASSESSMENT
   ============================================================ */

.assessment {
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
}

.assessment-good {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
}

.assessment-warning {
    background: #fffbeb;
    border: 1px solid #fde68a;
}

.assessment-danger {
    background: #fef2f2;
    border: 1px solid #fecaca;
}

.assessment-kicker {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #9ca3af;
    margin-bottom: 7px;
}

.assessment-title {
    font-size: 18px;
    font-weight: 800;
    color: #111827;
}

.assessment-message {
    font-size: 13px;
    color: #6b7280;
    margin-top: 5px;
    line-height: 1.6;
}


/* ============================================================
   STATISTICS
   ============================================================ */

.stats-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
}

.stat-card {
    background: #ffffff;
    border: 1px solid #e1e5ec;
    border-radius: 13px;
    padding: 16px 10px;
    text-align: center;
}

.stat-card span {
    display: block;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .7px;
    color: #9ca3af;
}

.stat-card strong {
    display: block;
    font-size: 21px;
    margin-top: 7px;
    color: #111827;
}

.stat-card small {
    display: block;
    font-size: 9px;
    color: #9ca3af;
    margin-top: 3px;
}


/* ============================================================
   EXAMPLES
   ============================================================ */

.example-title {
    margin-top: 45px;
    margin-bottom: 14px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #6b7280;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    border-top: 1px solid #e5e7eb;
    margin-top: 50px;
    padding: 25px 5px;
    text-align: center;
    color: #9ca3af;
    font-size: 11px;
    line-height: 1.7;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-result {
    background: #ffffff;
    border: 1px dashed #d1d5db;
    border-radius: 18px;
    padding: 40px 25px;
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 850px) {

    .gradio-container {
        padding: 0 18px 30px 18px !important;
    }

    .hero h1 {
        font-size: 35px;
    }

    .three-metrics {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

}

"""


with gr.Blocks(
    title="NewsLens — AI News Intelligence",
    css=css
) as app:

#header

    gr.HTML("""
    <div class="brand">

        <div class="brand-name">
            News<span>Lens</span>
        </div>

        <div class="brand-subtitle">
            AI-powered news intelligence & headline analysis
        </div>

    </div>
    """)

  #hero

    gr.HTML("""
    <div class="hero">

        <h1>Analyze before you believe.</h1>

        <p>
            Examine the relationship between a news headline
            and its article using machine learning, lexical
            similarity, semantic analysis and clickbait detection.
        </p>

    </div>
    """)


    with gr.Row(equal_height=True):

      
        with gr.Column(scale=1):

            gr.HTML("""
            <div class="section-title">
                NEWS INPUT
            </div>
            """)

            gr.HTML("""
            <div class="input-panel-title">
                Analyze an article
            </div>

            <div class="input-panel-subtitle">
                Enter a headline and paste the article body.
            </div>
            """)

            headline = gr.Textbox(
                label="News headline",
                placeholder="Enter the news headline...",
                lines=2
            )

            body = gr.Textbox(
                label="Article body",
                placeholder="Paste the complete article body...",
                lines=13
            )

            with gr.Row():

                analyze_button = gr.Button(
                    "Analyze article",
                    variant="primary",
                    elem_classes="analyze-btn"
                )

                clear_button = gr.Button(
                    "Clear",
                    elem_classes="clear-btn"
                )

       

        with gr.Column(scale=1):

            gr.HTML("""
            <div class="section-title">
                AI ANALYSIS
            </div>
            """)

            prediction_output = gr.HTML(
                value="""
                <div class="empty-result">
                    Analysis results will appear here.
                </div>
                """
            )

            consistency_output = gr.HTML()

   
    gr.HTML("""
    <div class="section-title" style="margin-top:35px;">
        ANALYSIS BREAKDOWN
    </div>
    """)

    with gr.Row():

        with gr.Column():

            clickbait_output = gr.HTML()

        with gr.Column():

            assessment_output = gr.HTML()

   #example

    gr.HTML("""
    <div class="example-title">
        TRY A SAMPLE
    </div>
    """)

    gr.Examples(
        examples=[
            [
                "Virat Kohli Scores Historic Triple Century as India Crush Australia",
                """The match focused on India's bowling performance
                and a strong opening partnership from the opposition.
                The Indian team made several changes to its bowling
                attack and struggled to create regular opportunities.
                The captain praised the bowlers for their discipline.
                No triple century was scored during the game."""
            ],

            [
                "🔥 YOU WON'T BELIEVE WHAT HAPPENED TO INDIA'S STAR BATTER!",
                """India's star batter scored 78 runs during the match
                before being dismissed while attempting to accelerate
                the scoring rate. The innings helped India build a
                competitive total, although the team eventually fell
                short of its target."""
            ]
        ],
        inputs=[
            headline,
            body
        ]
    )

 #footer

    gr.HTML("""
    <div class="footer">

        <strong>NewsLens</strong> · Hybrid Fake News & Clickbait Analyzer

        <br><br>

        NewsLens provides analytical predictions based on
        patterns learned from the training dataset.
        It does not independently verify facts or guarantee
        that an article is true or false.

    </div>
    """)

   #events

    analyze_button.click(
        fn=analyze,
        inputs=[headline, body],
        outputs=[
            prediction_output,
            consistency_output,
            clickbait_output,
            assessment_output
        ]
    )

    clear_button.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            headline,
            body,
            prediction_output,
            consistency_output,
            clickbait_output,
            assessment_output
        ]
    )

app.launch()