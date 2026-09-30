# ================================================================
# EDUTEXT MAIN APPLICATION
# ================================================================
#
# EduText is an educational quiz and learning platform.
#
# This application provides:
#
#   1. Student landing page
#   2. Subject selection
#   3. Question selection
#   4. Randomized quizzes
#   5. Answer checking
#   6. Hints
#   7. Explanations
#   8. Question history
#   9. Student analytics
#  10. Administrator analytics
#  11. SQLite database storage
#  12. SMS webhook support
#  13. PRIVATE ADMIN DASHBOARD
#  14. ADMIN LOGIN / LOGOUT
#
# ================================================================


# ================================================================
# IMPORTS
# ================================================================

import os
import random
import sqlite3

from datetime import datetime

from functools import wraps

from flask import (
    Flask,
    request,
    jsonify,
    render_template_string,
    session,
    redirect,
    url_for
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from subjects import (
    get_all_subjects,
    get_subject
)


# ================================================================
# APPLICATION CONFIGURATION
# ================================================================

DATABASE_NAME = "edutext_analytics.db"

HOST = "0.0.0.0"

PORT = int(
    os.getenv(
        "PORT",
        "5000"
    )
)


# ================================================================
# FLASK APPLICATION
# ================================================================

app = Flask(__name__)


# ================================================================
# SECURITY CONFIGURATION
# ================================================================

app.secret_key = os.getenv(
    "EDUTEXT_SECRET_KEY",
    os.urandom(32)
)


# ================================================================
# ADMIN USERNAME
# ================================================================

ADMIN_USERNAME = os.getenv(
    "EDUTEXT_ADMIN_USERNAME",
    "Keh Austine"
)


# ================================================================
# ADMIN PASSWORD
# ================================================================

ADMIN_PASSWORD = "Egr58MFe"

ADMIN_PASSWORD_HASH = generate_password_hash(
    ADMIN_PASSWORD
)


# ================================================================
# ADMIN AUTHENTICATION DECORATOR
# ================================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(
        *args,
        **kwargs
    ):

        if not session.get(
            "admin_authenticated"
        ):

            return redirect(
                url_for(
                    "admin_login"
                )
            )

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# ================================================================
# DATABASE CLASS
# ================================================================

class Database:

    def __init__(
        self,
        database_name
    ):

        self.database_name = (
            database_name
        )

        self.initialize()


    def connection(self):

        return sqlite3.connect(
            self.database_name,
            timeout=10,
            check_same_thread=False
        )


    def initialize(self):

        with self.connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_sessions (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    phone_number TEXT NOT NULL,

                    subject TEXT NOT NULL,

                    score INTEGER NOT NULL,

                    total_questions INTEGER NOT NULL,

                    accuracy_percentage REAL NOT NULL,

                    completion_time TIMESTAMP NOT NULL

                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS engagement_events (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    phone_number TEXT NOT NULL,

                    event_type TEXT NOT NULL,

                    question_id INTEGER,

                    timestamp TIMESTAMP NOT NULL

                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_question_history (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    phone_number TEXT NOT NULL,

                    subject TEXT NOT NULL,

                    question_id INTEGER NOT NULL,

                    answered_at TIMESTAMP NOT NULL,

                    UNIQUE (
                        phone_number,
                        subject,
                        question_id
                    )

                )
            """)

            conn.commit()


# ================================================================
# CREATE DATABASE INSTANCE
# ================================================================

database = Database(
    DATABASE_NAME
)


# ================================================================
# QUESTION HISTORY
# ================================================================

def get_attempted_question_ids(
    phone_number,
    subject_name
):

    with database.connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT question_id

            FROM student_question_history

            WHERE phone_number = ?

            AND subject = ?
        """, (
            phone_number,
            subject_name
        ))

        rows = cursor.fetchall()

    return {
        row[0]
        for row in rows
    }


# ================================================================
# GET UNUSED QUESTIONS
# ================================================================

def get_unused_questions(
    phone_number,
    subject
):

    attempted_ids = get_attempted_question_ids(
        phone_number,
        subject["name"]
    )

    return [
        question
        for question in subject["questions"]
        if question["id"]
        not in attempted_ids
    ]


# ================================================================
# RECORD QUESTION ATTEMPT
# ================================================================

def record_question_attempt(
    phone_number,
    subject_name,
    question_id
):

    with database.connection() as conn:

        conn.execute("""
            INSERT OR IGNORE INTO
            student_question_history
            (
                phone_number,
                subject,
                question_id,
                answered_at
            )

            VALUES (?, ?, ?, ?)
        """, (
            phone_number,
            subject_name,
            question_id,
            datetime.now()
        ))

        conn.commit()


# ================================================================
# ANALYTICS
# ================================================================

def log_event(
    phone_number,
    event_type,
    question_id=None
):

    with database.connection() as conn:

        conn.execute("""
            INSERT INTO engagement_events
            (
                phone_number,
                event_type,
                question_id,
                timestamp
            )

            VALUES (?, ?, ?, ?)
        """, (
            phone_number,
            event_type,
            question_id,
            datetime.now()
        ))

        conn.commit()


# ================================================================
# LOG COMPLETED SESSION
# ================================================================

def log_completed_session(
    phone_number,
    subject,
    score,
    total
):

    percentage = (
        (score / total) * 100
        if total > 0
        else 0
    )

    with database.connection() as conn:

        conn.execute("""
            INSERT INTO student_sessions
            (
                phone_number,
                subject,
                score,
                total_questions,
                accuracy_percentage,
                completion_time
            )

            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            phone_number,
            subject,
            score,
            total,
            percentage,
            datetime.now()
        ))

        conn.commit()


# ================================================================
# ANALYTICS REPORT
# ================================================================

def analytics_report():

    with database.connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(DISTINCT phone_number)

            FROM engagement_events
        """)

        students = (
            cursor.fetchone()[0]
            or 0
        )

        cursor.execute("""
            SELECT COUNT(*)

            FROM student_sessions
        """)

        quizzes = (
            cursor.fetchone()[0]
            or 0
        )

        cursor.execute("""
            SELECT AVG(accuracy_percentage)

            FROM student_sessions
        """)

        accuracy = (
            cursor.fetchone()[0]
            or 0
        )

        cursor.execute("""
            SELECT COUNT(*)

            FROM engagement_events

            WHERE event_type = 'HINT_CLICKED'
        """)

        hints = (
            cursor.fetchone()[0]
            or 0
        )

        cursor.execute("""
            SELECT COUNT(*)

            FROM student_question_history
        """)

        questions = (
            cursor.fetchone()[0]
            or 0
        )

    return {

        "students":
            students,

        "quizzes":
            quizzes,

        "accuracy":
            round(
                accuracy,
                1
            ),

        "hints":
            hints,

        "questions":
            questions

    }


# ================================================================
# QUIZ SESSIONS
# ================================================================

SESSIONS = {}


# ================================================================
# CREATE SESSION
# ================================================================

def create_session(phone):

    SESSIONS[phone] = {

        "step":
            "SUBJECT",

        "subject_key":
            None,

        "questions":
            [],

        "current":
            0,

        "score":
            0,

        "incorrect":
            0,

        "skipped":
            0,

        "answered":
            False,

        "selected":
            None,

        "correct":
            None,

        "hint":
            False

    }


# ================================================================
# GET SESSION
# ================================================================

def get_session(phone):

    if phone not in SESSIONS:

        create_session(
            phone
        )

    return SESSIONS[phone]


# ================================================================
# PROCESS QUIZ INPUT
# ================================================================

def process_input(
    phone,
    text
):

    text = (
        text
        .strip()
        .upper()
    )

    if (
        phone not in SESSIONS
        or text == "START"
    ):

        create_session(
            phone
        )

        log_event(
            phone,
            "SESSION_INITIATED"
        )

        return subject_response()


    session_data = get_session(
        phone
    )


    if session_data["step"] == "SUBJECT":

        subject = get_subject(
            text
        )

        if subject is None:

            return subject_response(
                "Invalid subject selection."
            )

        session_data["subject_key"] = text

        unused = get_unused_questions(
            phone,
            subject
        )

        if not unused:

            return {

                "type":
                    "empty",

                "subject":
                    subject["name"]

            }

        session_data["step"] = "LIMIT"

        return {

            "type":
                "limit",

            "subject":
                subject["name"],

            "maximum":
                len(unused)

        }


    if session_data["step"] == "LIMIT":

        if not text.isdigit():

            subject = get_subject(
                session_data["subject_key"]
            )

            unused = get_unused_questions(
                phone,
                subject
            )

            return {

                "type":
                    "limit",

                "subject":
                    subject["name"],

                "maximum":
                    len(unused),

                "error":
                    "Please enter a valid number."

            }


        amount = int(text)

        subject = get_subject(
            session_data["subject_key"]
        )

        unused = get_unused_questions(
            phone,
            subject
        )

        if (
            amount < 1
            or amount > len(unused)
        ):

            return {

                "type":
                    "limit",

                "subject":
                    subject["name"],

                "maximum":
                    len(unused),

                "error":
                    (
                        "Choose a number between 1 and "
                        f"{len(unused)}."
                    )

            }


        session_data["questions"] = random.sample(
            unused,
            amount
        )

        session_data["current"] = 0

        session_data["score"] = 0

        session_data["incorrect"] = 0

        session_data["skipped"] = 0

        session_data["answered"] = False

        session_data["selected"] = None

        session_data["correct"] = None

        session_data["hint"] = False

        session_data["step"] = "QUIZ"

        log_event(
            phone,
            "QUIZ_STARTED"
        )

        return question_response(
            session_data
        )


    if session_data["step"] == "QUIZ":

        question = session_data["questions"][
            session_data["current"]
        ]

        subject = get_subject(
            session_data["subject_key"]
        )

        subject_name = subject["name"]


        if text == "HINT":

            session_data["hint"] = not session_data["hint"]

            if session_data["hint"]:

                log_event(
                    phone,
                    "HINT_CLICKED",
                    question["id"]
                )

            return question_response(
                session_data
            )


        if text == "NEXT":

            if not session_data["answered"]:

                return question_response(
                    session_data,
                    "Answer or skip the question first."
                )

            session_data["current"] += 1

            session_data["answered"] = False

            session_data["selected"] = None

            session_data["correct"] = None

            session_data["hint"] = False

            if (
                session_data["current"]
                >= len(
                    session_data["questions"]
                )
            ):

                total = len(
                    session_data["questions"]
                )

                log_completed_session(
                    phone,
                    subject_name,
                    session_data["score"],
                    total
                )

                session_data["step"] = "COMPLETE"

                percentage = round(
                    (
                        session_data["score"]
                        / total
                    ) * 100
                )

                return {

                    "type":
                        "complete",

                    "score":
                        session_data["score"],

                    "incorrect":
                        session_data["incorrect"],

                    "skipped":
                        session_data["skipped"],

                    "total":
                        total,

                    "percentage":
                        percentage

                }

            return question_response(
                session_data
            )


        if session_data["answered"]:

            return question_response(
                session_data,
                "This question has already been answered. "
                "Select Next Question."
            )


        if text == "SKIP":

            session_data["skipped"] += 1

            session_data["answered"] = True

            session_data["selected"] = "SKIP"

            session_data["correct"] = None

            record_question_attempt(
                phone,
                subject_name,
                question["id"]
            )

            log_event(
                phone,
                "QUESTION_SKIPPED",
                question["id"]
            )

            return question_response(
                session_data
            )


        if text in question["options"]:

            record_question_attempt(
                phone,
                subject_name,
                question["id"]
            )

            session_data["selected"] = text

            session_data["answered"] = True

            if text == question["answer"]:

                session_data["score"] += 1

                session_data["correct"] = True

                log_event(
                    phone,
                    "ANSWER_CORRECT",
                    question["id"]
                )

            else:

                session_data["incorrect"] += 1

                session_data["correct"] = False

                log_event(
                    phone,
                    "ANSWER_INCORRECT",
                    question["id"]
                )

            return question_response(
                session_data
            )


        return question_response(
            session_data,
            "Invalid answer. Choose A, B, C or D."
        )


    if session_data["step"] == "COMPLETE":

        total = len(
            session_data["questions"]
        )

        percentage = round(
            (
                session_data["score"]
                / total
            ) * 100
        )

        return {

            "type":
                "complete",

            "score":
                session_data["score"],

            "incorrect":
                session_data["incorrect"],

            "skipped":
                session_data["skipped"],

            "total":
                total,

            "percentage":
                percentage

        }


# ================================================================
# SUBJECT RESPONSE
# ================================================================

def subject_response(
    error=None
):

    return {

        "type":
            "subject",

        "subjects":
            get_all_subjects(),

        "error":
            error

    }


# ================================================================
# QUESTION RESPONSE
# ================================================================

def question_response(
    session_data,
    error=None
):

    question = session_data["questions"][
        session_data["current"]
    ]

    return {

        "type":
            "question",

        "question":
            question,

        "current":
            session_data["current"],

        "total":
            len(
                session_data["questions"]
            ),

        "selected":
            session_data["selected"],

        "correct":
            session_data["correct"],

        "answered":
            session_data["answered"],

        "hint":
            session_data["hint"],

        "error":
            error

    }


# ================================================================
# BASE HTML
# ================================================================

BASE_HTML = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>{{ title }}</title>


    <style>

        * {
            box-sizing: border-box;
        }


        html {
            scroll-behavior: smooth;
        }


        body {

            margin: 0;

            background:
                #0f172a;

            color:
                #f8fafc;

            font-family:
                Arial,
                Helvetica,
                sans-serif;

        }


        .app {

            width: 100%;

            max-width: 680px;

            margin: auto;

            padding:
                25px 18px 60px;

        }


        .logo {

            display: flex;

            align-items: center;

            gap: 9px;

            color:
                #38bdf8;

            font-weight:
                900;

            font-size:
                18px;

            letter-spacing:
                1px;

            margin-bottom:
                25px;

        }


        .logo-mark {

            width:
                30px;

            height:
                30px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                9px;

            background:
                linear-gradient(
                    135deg,
                    #38bdf8,
                    #2563eb
                );

            color:
                #082f49;

            font-size:
                14px;

        }


        h1 {

            line-height:
                1.3;

        }


        .muted {

            color:
                #94a3b8;

            line-height:
                1.6;

        }


        .error {

            background:
                #7f1d1d;

            border:
                1px solid #ef4444;

            padding:
                14px;

            border-radius:
                12px;

            margin:
                15px 0;

            line-height:
                1.5;

        }


        .subject {

            display:
                flex;

            align-items:
                center;

            gap:
                15px;

            background:
                #1e293b;

            color:
                white;

            text-decoration:
                none;

            padding:
                18px;

            margin:
                12px 0;

            border:
                1px solid #334155;

            border-radius:
                15px;

            transition:
                0.2s ease;

        }


        .subject:hover {

            border-color:
                #38bdf8;

            transform:
                translateY(-2px);

        }


        .number {

            width:
                40px;

            height:
                40px;

            border-radius:
                10px;

            background:
                #2563eb;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-weight:
                800;

        }


        .slider-card {

            background:
                #1e293b;

            border:
                1px solid #334155;

            padding:
                25px;

            border-radius:
                18px;

            margin-top:
                25px;

        }


        .slider-value {

            text-align:
                center;

            font-size:
                60px;

            color:
                #38bdf8;

            font-weight:
                900;

            margin:
                20px;

        }


        input[type=range] {

            width:
                100%;

            accent-color:
                #2563eb;

        }


        .range-labels {

            display:
                flex;

            justify-content:
                space-between;

            color:
                #64748b;

            margin-top:
                8px;

        }


        .button {

            display:
                block;

            width:
                100%;

            padding:
                15px;

            margin-top:
                20px;

            background:
                #2563eb;

            color:
                white;

            text-align:
                center;

            text-decoration:
                none;

            border-radius:
                13px;

            font-weight:
                700;

            border:
                none;

            cursor:
                pointer;

            transition:
                0.2s ease;

        }


        .button:hover {

            background:
                #1d4ed8;

            transform:
                translateY(-1px);

        }


        .question {

            font-size:
                23px;

            line-height:
                1.5;

            margin-top:
                25px;

        }


        .progress {

            height:
                7px;

            background:
                #334155;

            border-radius:
                10px;

            overflow:
                hidden;

        }


        .progress-fill {

            height:
                100%;

            background:
                #38bdf8;

        }


        .progress-text {

            color:
                #94a3b8;

            font-size:
                13px;

            margin-bottom:
                8px;

        }


        .option {

            display:
                flex;

            align-items:
                center;

            gap:
                13px;

            background:
                #1e293b;

            color:
                white;

            text-decoration:
                none;

            padding:
                16px;

            margin:
                12px 0;

            border:
                1px solid #334155;

            border-radius:
                14px;

            line-height:
                1.5;

            transition:
                0.2s ease;

        }


        .option:hover {

            border-color:
                #38bdf8;

        }


        .letter {

            width:
                38px;

            height:
                38px;

            min-width:
                38px;

            background:
                #334155;

            border-radius:
                10px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-weight:
                800;

        }


        .correct {

            background:
                #166534;

            border-color:
                #4ade80;

        }


        .wrong {

            background:
                #991b1b;

            border-color:
                #f87171;

        }


        .hint {

            background:
                #3f3215;

            border:
                1px solid #7c5d18;

            color:
                #fcd34d;

            padding:
                15px;

            border-radius:
                14px;

            margin:
                20px 0;

            line-height:
                1.5;

        }


        .hint-button {

            display:
                block;

            text-align:
                center;

            color:
                #38bdf8;

            text-decoration:
                none;

            margin:
                20px 0;

            font-weight:
                700;

        }


        .explanation {

            background:
                #1e293b;

            border:
                1px solid #334155;

            padding:
                18px;

            border-radius:
                15px;

            margin-top:
                20px;

            line-height:
                1.6;

        }


        .score {

            font-size:
                70px;

            font-weight:
                900;

            text-align:
                center;

            color:
                #38bdf8;

            margin:
                30px 0;

        }


        .stats {

            display:
                grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap:
                10px;

        }


        .stat {

            padding:
                15px;

            border-radius:
                12px;

            text-align:
                center;

        }


        .stat strong {

            display:
                block;

            font-size:
                25px;

            margin-top:
                8px;

        }


        .stat-correct {

            background:
                #166534;

        }


        .stat-wrong {

            background:
                #991b1b;

        }


        .stat-skip {

            background:
                #475569;

        }


        .home-page {

            width:
                100%;

            padding-bottom:
                30px;

        }


        .hero-card {

            position:
                relative;

            overflow:
                hidden;

            background:
                linear-gradient(
                    135deg,
                    #172554 0%,
                    #1e3a8a 45%,
                    #0f172a 100%
                );

            border:
                1px solid #2563eb;

            border-radius:
                26px;

            padding:
                38px 30px;

            margin-bottom:
                38px;

            box-shadow:
                0 20px 50px
                rgba(0, 0, 0, 0.25);

        }


        .hero-card::before {

            content:
                "";

            position:
                absolute;

            width:
                220px;

            height:
                220px;

            border-radius:
                50%;

            background:
                rgba(
                    56,
                    189,
                    248,
                    0.10
                );

            top:
                -90px;

            right:
                -60px;

        }


        .hero-card::after {

            content:
                "";

            position:
                absolute;

            width:
                150px;

            height:
                150px;

            border-radius:
                50%;

            background:
                rgba(
                    99,
                    102,
                    241,
                    0.10
                );

            bottom:
                -70px;

            left:
                -50px;

        }


        .hero-badge {

            display:
                inline-flex;

            align-items:
                center;

            padding:
                7px 12px;

            border-radius:
                999px;

            background:
                rgba(
                    56,
                    189,
                    248,
                    0.12
                );

            border:
                1px solid
                rgba(
                    56,
                    189,
                    248,
                    0.30
                );

            color:
                #7dd3fc;

            font-size:
                11px;

            font-weight:
                800;

            letter-spacing:
                1px;

            position:
                relative;

            z-index:
                2;

        }


        .hero-title {

            position:
                relative;

            z-index:
                2;

            font-size:
                42px;

            line-height:
                1.15;

            margin:
                20px 0 15px;

            max-width:
                480px;

            font-weight:
                900;

            letter-spacing:
                -1.5px;

        }


        .hero-title span {

            color:
                #38bdf8;

        }


        .hero-description {

            position:
                relative;

            z-index:
                2;

            max-width:
                500px;

            color:
                #cbd5e1;

            line-height:
                1.7;

            margin-bottom:
                28px;

            font-size:
                15px;

        }


        .hero-actions {

            position:
                relative;

            z-index:
                2;

            display:
                flex;

            gap:
                12px;

            flex-wrap:
                wrap;

        }


        .primary-home-button,
        .secondary-home-button {

            display:
                inline-flex;

            align-items:
                center;

            justify-content:
                center;

            gap:
                9px;

            padding:
                14px 18px;

            border-radius:
                13px;

            text-decoration:
                none;

            font-weight:
                800;

            font-size:
                14px;

            transition:
                transform 0.2s ease,
                background 0.2s ease,
                border-color 0.2s ease;

        }


        .primary-home-button {

            background:
                #38bdf8;

            color:
                #082f49;

            box-shadow:
                0 8px 20px
                rgba(
                    56,
                    189,
                    248,
                    0.25
                );

        }


        .primary-home-button:hover {

            transform:
                translateY(-2px);

            background:
                #7dd3fc;

        }


        .secondary-home-button {

            background:
                rgba(
                    15,
                    23,
                    42,
                    0.65
                );

            border:
                1px solid #475569;

            color:
                #f8fafc;

        }


        .secondary-home-button:hover {

            transform:
                translateY(-2px);

            border-color:
                #38bdf8;

        }


        .button-icon {

            font-size:
                13px;

        }


        .section-heading {

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

            margin-bottom:
                15px;

        }


        .section-heading h2 {

            margin:
                0;

            font-size:
                21px;

            letter-spacing:
                -0.3px;

        }


        .section-heading p {

            margin:
                5px 0 0;

            color:
                #64748b;

            font-size:
                13px;

        }


        .feature-grid {

            display:
                grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap:
                14px;

            margin-bottom:
                38px;

        }


        .feature-card {

            display:
                flex;

            gap:
                15px;

            text-decoration:
                none;

            color:
                white;

            background:
                #1e293b;

            border:
                1px solid #334155;

            border-radius:
                18px;

            padding:
                19px;

            min-height:
                175px;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;

        }


        .feature-card:hover {

            transform:
                translateY(-3px);

            border-color:
                #38bdf8;

            box-shadow:
                0 12px 30px
                rgba(
                    0,
                    0,
                    0,
                    0.18
                );

        }


        .feature-icon {

            width:
                45px;

            height:
                45px;

            min-width:
                45px;

            border-radius:
                13px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-size:
                21px;

            font-weight:
                900;

        }


        .blue-icon {

            color:
                #38bdf8;

            background:
                rgba(
                    14,
                    165,
                    233,
                    0.12
                );

            border:
                1px solid
                rgba(
                    56,
                    189,
                    248,
                    0.2
                );

        }


        .purple-icon {

            color:
                #c4b5fd;

            background:
                rgba(
                    139,
                    92,
                    246,
                    0.12
                );

            border:
                1px solid
                rgba(
                    167,
                    139,
                    250,
                    0.2
                );

        }


        .feature-content {

            flex:
                1;

        }


        .feature-content h3 {

            margin:
                2px 0 8px;

            font-size:
                16px;

        }


        .feature-content p {

            margin:
                0;

            color:
                #94a3b8;

            font-size:
                13px;

            line-height:
                1.55;

        }


        .feature-link {

            margin-top:
                17px;

            color:
                #38bdf8;

            font-size:
                12px;

            font-weight:
                800;

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

        }


        .feature-link span {

            font-size:
                17px;

        }


        .purple-link {

            color:
                #a78bfa;

        }


        .subject-heading {

            margin-bottom:
                15px;

        }


        .subject-preview-grid {

            display:
                grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap:
                12px;

            margin-bottom:
                25px;

        }


        .preview-subject {

            display:
                flex;

            align-items:
                center;

            gap:
                13px;

            padding:
                15px;

            background:
                #1e293b;

            border:
                1px solid #334155;

            border-radius:
                15px;

        }


        .preview-number {

            width:
                40px;

            height:
                40px;

            min-width:
                40px;

            border-radius:
                11px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            background:
                rgba(
                    37,
                    99,
                    235,
                    0.18
                );

            color:
                #60a5fa;

            font-size:
                12px;

            font-weight:
                900;

        }


        .math-number {

            background:
                rgba(
                    139,
                    92,
                    246,
                    0.18
                );

            color:
                #c4b5fd;

        }


        .preview-subject strong {

            display:
                block;

            font-size:
                13px;

            margin-bottom:
                4px;

        }


        .preview-subject small {

            display:
                block;

            color:
                #64748b;

            font-size:
                11px;

            line-height:
                1.4;

        }


        .info-banner {

            display:
                flex;

            align-items:
                flex-start;

            gap:
                13px;

            padding:
                17px;

            border-radius:
                16px;

            background:
                linear-gradient(
                    135deg,
                    #132e25,
                    #14251f
                );

            border:
                1px solid #285c4a;

            margin-top:
                10px;

        }


        .info-symbol {

            width:
                34px;

            height:
                34px;

            min-width:
                34px;

            border-radius:
                10px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            background:
                rgba(
                    74,
                    222,
                    128,
                    0.12
                );

            color:
                #4ade80;

            font-weight:
                900;

        }


        .info-banner strong {

            display:
                block;

            font-size:
                13px;

            color:
                #bbf7d0;

            margin-bottom:
                5px;

        }


        .info-banner p {

            margin:
                0;

            color:
                #86a99a;

            font-size:
                12px;

            line-height:
                1.5;

        }


        .home-footer {

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

            gap:
                10px;

            padding-top:
                28px;

            margin-top:
                28px;

            border-top:
                1px solid #1e293b;

            color:
                #475569;

            font-size:
                11px;

        }


        .home-footer span:first-child {

            color:
                #64748b;

            font-weight:
                800;

        }


        /* ========================================================
           ADMIN DASHBOARD
           ======================================================== */

        .admin-header {

            background:
                linear-gradient(
                    135deg,
                    #172554,
                    #1e293b
                );

            border:
                1px solid #334155;

            border-radius:
                22px;

            padding:
                25px;

            margin-bottom:
                25px;

        }


        .admin-header-label {

            display:
                inline-block;

            color:
                #38bdf8;

            font-size:
                11px;

            font-weight:
                900;

            letter-spacing:
                1.2px;

            margin-bottom:
                10px;

        }


        .admin-header h1 {

            margin:
                0 0 8px;

            font-size:
                28px;

        }


        .admin-header p {

            margin:
                0;

            color:
                #94a3b8;

            line-height:
                1.6;

            font-size:
                13px;

        }


        .analytics-grid {

            display:
                grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap:
                14px;

            margin-bottom:
                20px;

        }


        .analytics-card {

            position:
                relative;

            overflow:
                hidden;

            min-height:
                150px;

            padding:
                20px;

            border-radius:
                18px;

            background:
                #1e293b;

            border:
                1px solid #334155;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;

        }


        .analytics-card:hover {

            transform:
                translateY(-3px);

            border-color:
                #475569;

        }


        .analytics-card::after {

            content:
                "";

            position:
                absolute;

            width:
                90px;

            height:
                90px;

            border-radius:
                50%;

            right:
                -35px;

            bottom:
                -35px;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.025
                );

        }


        .analytics-top {

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

            margin-bottom:
                15px;

        }


        .analytics-icon {

            width:
                42px;

            height:
                42px;

            border-radius:
                12px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-size:
                18px;

            font-weight:
                900;

        }


        .students-icon {

            color:
                #38bdf8;

            background:
                rgba(
                    56,
                    189,
                    248,
                    0.12
                );

        }


        .accuracy-icon {

            color:
                #4ade80;

            background:
                rgba(
                    74,
                    222,
                    128,
                    0.12
                );

        }


        .questions-icon {

            color:
                #a78bfa;

            background:
                rgba(
                    167,
                    139,
                    250,
                    0.12
                );

        }


        .quiz-icon {

            color:
                #fbbf24;

            background:
                rgba(
                    251,
                    191,
                    36,
                    0.12
                );

        }


        .hints-icon {

            color:
                #fb7185;

            background:
                rgba(
                    251,
                    113,
                    133,
                    0.12
                );

        }


        .analytics-label {

            color:
                #94a3b8;

            font-size:
                12px;

            font-weight:
                700;

            margin-bottom:
                7px;

        }


        .analytics-value {

            font-size:
                31px;

            line-height:
                1;

            font-weight:
                900;

            letter-spacing:
                -1px;

        }


        .analytics-description {

            color:
                #64748b;

            font-size:
                11px;

            margin-top:
                9px;

        }


        .analytics-card.featured {

            grid-column:
                span 2;

            background:
                linear-gradient(
                    135deg,
                    #172554,
                    #172033
                );

            border-color:
                #1d4ed8;

        }


        .featured-row {

            display:
                flex;

            align-items:
                center;

            justify-content:
                space-between;

            gap:
                20px;

        }


        .featured-info {

            flex:
                1;

        }


        .accuracy-large {

            font-size:
                44px;

            font-weight:
                900;

        }


        .accuracy-bar {

            height:
                8px;

            width:
                100%;

            background:
                #334155;

            border-radius:
                999px;

            overflow:
                hidden;

            margin-top:
                13px;

        }


        .accuracy-bar-fill {

            height:
                100%;

            background:
                linear-gradient(
                    90deg,
                    #22c55e,
                    #4ade80
                );

            border-radius:
                999px;

        }


        .admin-info-panel {

            background:
                #111c31;

            border:
                1px solid #26364d;

            border-radius:
                18px;

            padding:
                19px;

            margin-top:
                15px;

            margin-bottom:
                15px;

        }


        .admin-info-title {

            font-size:
                13px;

            font-weight:
                800;

            margin-bottom:
                6px;

        }


        .admin-info-text {

            color:
                #64748b;

            font-size:
                12px;

            line-height:
                1.6;

        }


        .admin-back {

            margin-top:
                18px;

        }


        /* ========================================================
           ADMIN LOGIN
           ======================================================== */

        .login-card {

            background:
                #1e293b;

            border:
                1px solid #334155;

            border-radius:
                18px;

            padding:
                25px;

        }


        .login-label {

            display:
                block;

            margin-bottom:
                8px;

            color:
                #94a3b8;

            font-size:
                13px;

            font-weight:
                700;

        }


        .login-input {

            width:
                100%;

            padding:
                14px;

            border-radius:
                10px;

            border:
                1px solid #475569;

            background:
                #0f172a;

            color:
                white;

            margin-bottom:
                18px;

            font-size:
                15px;

            outline:
                none;

        }


        .login-input:focus {

            border-color:
                #38bdf8;

        }


        /* ========================================================
           PASSWORD SHOW / HIDE EYE ICON
           ======================================================== */

        .password-wrapper {

            position:
                relative;

            width:
                100%;

        }


        .password-wrapper .password-input {

            padding-right:
                52px;

        }


        .password-toggle {

            position:
                absolute;

            right:
                10px;

            top:
                50%;

            transform:
                translateY(-50%);

            width:
                38px;

            height:
                38px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border:
                none;

            background:
                transparent;

            color:
                #94a3b8;

            cursor:
                pointer;

            border-radius:
                8px;

            padding:
                0;

            transition:
                0.2s ease;

        }


        .password-toggle:hover {

            background:
                #334155;

            color:
                #38bdf8;

        }


        .password-toggle:focus {

            outline:
                2px solid #38bdf8;

            outline-offset:
                2px;

        }


        .password-toggle svg {

            width:
                21px;

            height:
                21px;

        }


        .security-message {

            background:
                #132e25;

            border:
                1px solid #285c4a;

            color:
                #86efac;

            padding:
                14px;

            border-radius:
                12px;

            margin-bottom:
                18px;

            font-size:
                12px;

            line-height:
                1.5;

        }


        .logout-button {

            display:
                inline-block;

            margin-top:
                15px;

            color:
                #f87171;

            text-decoration:
                none;

            font-size:
                12px;

            font-weight:
                800;

        }


        @media(max-width: 600px) {

            .app {

                padding:
                    20px 15px 50px;

            }


            .hero-card {

                padding:
                    30px 21px;

                border-radius:
                    22px;

            }


            .hero-title {

                font-size:
                    34px;

            }


            .hero-description {

                font-size:
                    14px;

            }


            .hero-actions {

                flex-direction:
                    column;

            }


            .primary-home-button,
            .secondary-home-button {

                width:
                    100%;

            }


            .feature-grid {

                grid-template-columns:
                    1fr;

            }


            .subject-preview-grid {

                grid-template-columns:
                    1fr;

            }


            .analytics-grid {

                grid-template-columns:
                    1fr;

            }


            .analytics-card.featured {

                grid-column:
                    span 1;

            }


            .featured-row {

                align-items:
                    flex-start;

                flex-direction:
                    column;

            }


            .home-footer {

                flex-direction:
                    column;

                align-items:
                    flex-start;

            }

        }


        @media(max-width: 500px) {

            .stats {

                grid-template-columns:
                    1fr;

            }


            .question {

                font-size:
                    20px;

            }

        }


        @media(max-width: 380px) {

            .hero-title {

                font-size:
                    30px;

            }


            .hero-card {

                padding:
                    25px 17px;

            }


            .analytics-value {

                font-size:
                    27px;

            }

        }

    </style>

</head>


<body>


<div class="app">


    <div class="logo">

        <div class="logo-mark">
            E
        </div>

        EduText

    </div>


    {{ content|safe }}


</div>


</body>

</html>
"""


# ================================================================
# TEST / QUIZ ROUTE
# ================================================================

@app.route(
    "/test",
    methods=["GET"]
)
def test():

    phone = request.args.get(
        "from",
        "+237699999999"
    )

    text = request.args.get(
        "text"
    )

    if text is None:

        text = "START"

    result = process_input(
        phone,
        text
    )

    result_type = result["type"]


    if result_type == "subject":

        subjects_html = ""

        for key, subject in (
            result["subjects"].items()
        ):

            subjects_html += f"""

                <a
                    class="subject"
                    href="/test?from={phone}&text={key}"
                >

                    <div class="number">
                        {key}
                    </div>

                    <div>

                        <strong>
                            {subject["name"]}
                        </strong>

                    </div>

                </a>

            """

        error_html = ""

        if result.get("error"):

            error_html = f"""

                <div class="error">
                    {result["error"]}
                </div>

            """

        return render_template_string(

            BASE_HTML,

            title="Choose Subject",

            content=f"""

                <h1>
                    Choose Subject
                </h1>

                <p class="muted">
                    Select the subject you want to study.
                </p>

                {error_html}

                {subjects_html}

            """

        )


    if result_type == "empty":

        return render_template_string(

            BASE_HTML,

            title="No Questions",

            content=f"""

                <h1>
                    No New Questions
                </h1>

                <p class="muted">

                    You have already attempted all available
                    questions in {result["subject"]}.

                </p>

                <a
                    class="button"
                    href="/test?from={phone}&text=START"
                >
                    Choose Another Subject
                </a>

            """

        )


    if result_type == "limit":

        maximum = result["maximum"]

        error_html = ""

        if result.get("error"):

            error_html = f"""

                <div class="error">
                    {result["error"]}
                </div>

            """

        return render_template_string(

            BASE_HTML,

            title="Choose Questions",

            content=f"""

                <h1>
                    {result["subject"]}
                </h1>

                <p class="muted">

                    Select how many questions you want to solve.

                </p>

                {error_html}

                <div class="slider-card">

                    <div
                        class="slider-value"
                        id="sliderValue"
                    >
                        1
                    </div>

                    <input
                        id="slider"
                        type="range"
                        min="1"
                        max="{maximum}"
                        value="1"
                    >

                    <div class="range-labels">

                        <span>
                            1
                        </span>

                        <span>
                            {maximum}
                        </span>

                    </div>

                    <a
                        id="startQuiz"
                        class="button"
                        href="/test?from={phone}&text=1"
                    >
                        Start Quiz
                    </a>

                </div>

                <script>

                    const slider =
                        document.getElementById(
                            "slider"
                        );

                    const display =
                        document.getElementById(
                            "sliderValue"
                        );

                    const start =
                        document.getElementById(
                            "startQuiz"
                        );

                    const phone =
                        {phone!r};

                    function update() {{

                        const value =
                            slider.value;

                        display.textContent =
                            value;

                        start.href =
                            "/test?from="
                            +
                            encodeURIComponent(phone)
                            +
                            "&text="
                            +
                            encodeURIComponent(value);

                    }}

                    slider.addEventListener(
                        "input",
                        update
                    );

                    update();

                </script>

            """

        )


    if result_type == "complete":

        return render_template_string(

            BASE_HTML,

            title="Quiz Complete",

            content=f"""

                <h1>
                    Quiz Complete
                </h1>

                <div class="score">
                    {result["percentage"]}%
                </div>

                <div class="stats">

                    <div class="stat stat-correct">

                        Correct

                        <strong>
                            {result["score"]}
                        </strong>

                    </div>

                    <div class="stat stat-wrong">

                        Incorrect

                        <strong>
                            {result["incorrect"]}
                        </strong>

                    </div>

                    <div class="stat stat-skip">

                        Skipped

                        <strong>
                            {result["skipped"]}
                        </strong>

                    </div>

                </div>

                <a
                    class="button"
                    href="/test?from={phone}&text=START"
                >
                    Start New Session
                </a>

            """

        )


    question = result["question"]

    current = result["current"]

    total = result["total"]

    selected = result["selected"]

    correct = result["correct"]

    progress = int(
        (
            (current + 1)
            / total
        )
        * 100
    )

    error_html = ""

    if result.get("error"):

        error_html = f"""

            <div class="error">
                {result["error"]}
            </div>

        """

    options_html = ""

    for key, value in (
        question["options"].items()
    ):

        css = "option"

        if selected:

            if key == selected:

                if correct:

                    css += " correct"

                elif correct is False:

                    css += " wrong"

            elif key == question["answer"]:

                css += " correct"

        href = ""

        if not selected:

            href = (
                f"/test?from={phone}"
                f"&text={key}"
            )

        options_html += f"""

            <a
                class="{css}"
                href="{href}"
                {
                    "onclick='return false;'"
                    if selected
                    else ""
                }
            >

                <span class="letter">
                    {key}
                </span>

                <span>
                    {value}
                </span>

            </a>

        """

    hint_html = ""

    if result["hint"]:

        hint_html = f"""

            <div class="hint">

                <strong>
                    Hint
                </strong>

                <br>

                {question["hint"]}

            </div>

        """

    hint_text = (
        "Hide Hint"
        if result["hint"]
        else "Show Hint"
    )

    hint_html += f"""

        <a
            class="hint-button"
            href="/test?from={phone}&text=HINT"
        >
            {hint_text}
        </a>

    """

    explanation_html = ""

    if selected:

        if selected == "SKIP":

            title = "Question Skipped"

        elif correct:

            title = "Correct"

        else:

            title = "Incorrect"

        explanation_html = f"""

            <div class="explanation">

                <h3>
                    {title}
                </h3>

                <p>
                    {question["explanation"]}
                </p>

                <p>

                    <strong>
                        Correct answer:
                    </strong>

                    {question["answer"]}

                </p>

            </div>

        """

    if selected:

        action_html = f"""

            <a
                class="button"
                href="/test?from={phone}&text=NEXT"
            >
                Next Question
            </a>

        """

    else:

        action_html = f"""

            <a
                class="button"
                href="/test?from={phone}&text=SKIP"
            >
                Skip Question
            </a>

        """

    return render_template_string(

        BASE_HTML,

        title="Quiz",

        content=f"""

            {error_html}

            <div class="progress-text">

                Question
                {current + 1}
                of
                {total}

            </div>

            <div class="progress">

                <div
                    class="progress-fill"
                    style="width:{progress}%"
                ></div>

            </div>

            <div class="question">

                {question["question_text"]}

            </div>

            {hint_html}

            <div>

                {options_html}

            </div>

            {explanation_html}

            {action_html}

        """

    )


# ================================================================
# HOME / LANDING PAGE
# ================================================================

@app.route("/")
def home():

    return render_template_string(

        BASE_HTML,

        title="EduText | Learning Platform",

        content="""

        <div class="home-page">

            <div class="hero-card">

                <div class="hero-badge">

                    SMART LEARNING PLATFORM

                </div>

                <h1 class="hero-title">

                    Learn.
                    <span>
                        Practice.
                    </span>
                    Improve.

                </h1>

                <p class="hero-description">

                    Welcome to EduText, your interactive learning
                    platform for practicing questions, testing your
                    knowledge and improving your accuracy.

                </p>

                <div class="hero-actions">

                    <a
                        class="primary-home-button"
                        href="/test"
                    >

                        <span class="button-icon">
                            ▶
                        </span>

                        Start Learning

                    </a>

                    <a
                        class="secondary-home-button"
                        href="/admin/login"
                    >

                        <span class="button-icon">
                            ◈
                        </span>

                        Admin Login

                    </a>

                </div>

            </div>


            <div class="section-heading">

                <div>

                    <h2>
                        What can you do?
                    </h2>

                    <p>
                        Choose an option below to get started.
                    </p>

                </div>

            </div>


            <div class="feature-grid">

                <a
                    href="/test"
                    class="feature-card"
                >

                    <div class="feature-icon blue-icon">

                        ?

                    </div>

                    <div class="feature-content">

                        <h3>
                            Practice Questions
                        </h3>

                        <p>

                            Test yourself with questions from
                            your available subjects.

                        </p>

                        <div class="feature-link">

                            Start Practice

                            <span>
                                →
                            </span>

                        </div>

                    </div>

                </a>


                <a
                    href="/admin/login"
                    class="feature-card"
                >

                    <div class="feature-icon purple-icon">

                        ↗

                    </div>

                    <div class="feature-content">

                        <h3>
                            Learning Analytics
                        </h3>

                        <p>

                            Administrator access to student
                            activity, accuracy and performance.

                        </p>

                        <div class="feature-link purple-link">

                            Admin Login

                            <span>
                                →
                            </span>

                        </div>

                    </div>

                </a>

            </div>


            <div class="section-heading subject-heading">

                <div>

                    <h2>
                        Available Subjects
                    </h2>

                    <p>

                        Select a subject when you start your quiz.

                    </p>

                </div>

            </div>


            <div class="subject-preview-grid">

                <div class="preview-subject">

                    <div class="preview-number">

                        01

                    </div>

                    <div>

                        <strong>
                            Computer Science
                        </strong>

                        <small>

                            Practice computer science questions

                        </small>

                    </div>

                </div>


                <div class="preview-subject">

                    <div class="preview-number math-number">

                        02

                    </div>

                    <div>

                        <strong>
                            Mathematics
                        </strong>

                        <small>

                            Practice mathematics questions

                        </small>

                    </div>

                </div>

            </div>


            <div class="info-banner">

                <div class="info-symbol">

                    ✓

                </div>

                <div>

                    <strong>

                        Learn at your own pace

                    </strong>

                    <p>

                        Choose the number of questions you want
                        to attempt and track your performance
                        after completing the quiz.

                    </p>

                </div>

            </div>


            <div class="home-footer">

                <span>
                    EduText
                </span>

                <span>
                    Smart learning made simple.
                </span>

            </div>


        </div>

        """

    )


# ================================================================
# ADMIN LOGIN
# ================================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    error = None


    # ------------------------------------------------------------
    # If already logged in, go directly to dashboard.
    # ------------------------------------------------------------

    if session.get(
        "admin_authenticated"
    ):

        return redirect(
            url_for(
                "admin"
            )
        )


    # ------------------------------------------------------------
    # Process login form.
    # ------------------------------------------------------------

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        # --------------------------------------------------------
        # Check credentials.
        # --------------------------------------------------------

        if (

            username == ADMIN_USERNAME

            and ADMIN_PASSWORD_HASH

            and check_password_hash(
                ADMIN_PASSWORD_HASH,
                password
            )

        ):

            session.clear()

            session["admin_authenticated"] = True

            session["admin_username"] = (
                ADMIN_USERNAME
            )

            return redirect(
                url_for(
                    "admin"
                )
            )


        error = (
            "Invalid administrator username or password."
        )


    error_html = ""


    if error:

        error_html = f"""

            <div class="error">

                {error}

            </div>

        """


    return render_template_string(

        BASE_HTML,

        title="EduText | Admin Login",

        content=f"""

        <div class="admin-header">


            <div class="admin-header-label">

                PRIVATE ADMINISTRATION

            </div>


            <h1>

                Admin Login

            </h1>


            <p>

                The EduText analytics dashboard is private.
                Sign in with your administrator credentials
                to continue.

            </p>


        </div>


        {error_html}


        <div class="security-message">

            🔒 This area is restricted to authorized
            EduText administrators.

        </div>


        <form
            method="POST"
            class="login-card"
        >


            <label class="login-label">

                Username

            </label>


            <input
                class="login-input"
                type="text"
                name="username"
                autocomplete="username"
                required
            >


            <label class="login-label">

                Password

            </label>


            <!-- =================================================
                 PASSWORD FIELD WITH EYE ICON
                 ================================================= -->

            <div class="password-wrapper">

                <input
                    id="adminPassword"
                    class="login-input password-input"
                    type="password"
                    name="password"
                    autocomplete="current-password"
                    required
                >


                <button
                    type="button"
                    class="password-toggle"
                    id="passwordToggle"
                    aria-label="Show password"
                    title="Show password"
                >

                    <!-- CLOSED EYE -->
                    <svg
                        id="eyeClosed"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >

                        <path
                            d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        />

                        <circle
                            cx="12"
                            cy="12"
                            r="3"
                        />

                    </svg>


                    <!-- OPEN EYE -->
                    <svg
                        id="eyeOpen"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        style="display:none;"
                    >

                        <path
                            d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        />

                        <circle
                            cx="12"
                            cy="12"
                            r="3"
                        />

                        <line
                            x1="4"
                            y1="4"
                            x2="20"
                            y2="20"
                        />

                    </svg>

                </button>

            </div>


            <button
                type="submit"
                class="button"
            >

                Sign In

            </button>


        </form>


        <a
            class="button admin-back"
            href="/"
        >

            ← Back to EduText

        </a>


        <!-- =====================================================
             PASSWORD SHOW / HIDE SCRIPT
             ===================================================== -->

        <script>

            const passwordInput =
                document.getElementById(
                    "adminPassword"
                );


            const passwordToggle =
                document.getElementById(
                    "passwordToggle"
                );


            const eyeClosed =
                document.getElementById(
                    "eyeClosed"
                );


            const eyeOpen =
                document.getElementById(
                    "eyeOpen"
                );


            passwordToggle.addEventListener(
                "click",
                function() {{

                    if (
                        passwordInput.type === "password"
                    ) {{

                        passwordInput.type = "text";

                        eyeClosed.style.display =
                            "none";

                        eyeOpen.style.display =
                            "block";

                        passwordToggle.setAttribute(
                            "aria-label",
                            "Hide password"
                        );

                        passwordToggle.setAttribute(
                            "title",
                            "Hide password"
                        );

                    }} else {{

                        passwordInput.type = "password";

                        eyeClosed.style.display =
                            "block";

                        eyeOpen.style.display =
                            "none";

                        passwordToggle.setAttribute(
                            "aria-label",
                            "Show password"
                        );

                        passwordToggle.setAttribute(
                            "title",
                            "Show password"
                        );

                    }}

                }}

            );

        </script>

        """

    )


# ================================================================
# ADMIN LOGOUT
# ================================================================

@app.route(
    "/admin/logout"
)
def admin_logout():

    session.clear()

    return redirect(
        url_for(
            "home"
        )
    )


# ================================================================
# ADMIN DASHBOARD
# ================================================================

@app.route("/admin")
@admin_required
def admin():

    report = analytics_report()


    accuracy_width = min(
        max(
            float(
                report["accuracy"]
            ),
            0
        ),
        100
    )


    accuracy_color = (

        "#ef4444"

        if float(
            report["accuracy"]
        ) < 50

        else "#4ade80"

    )


    return render_template_string(

        BASE_HTML,

        title="EduText | Analytics",

        content=f"""

        <div class="admin-header">


            <div class="admin-header-label">

                EDUTEXT ADMINISTRATION

            </div>


            <h1>

                Analytics Dashboard

            </h1>


            <p>

                Monitor student participation, question attempts
                and overall learning performance.

            </p>


            <div style="
                margin-top:18px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:10px;
                flex-wrap:wrap;
            ">


                <span style="
                    color:#64748b;
                    font-size:12px;
                ">

                    🔒 Logged in as administrator

                </span>


                <a
                    href="/admin/logout"
                    class="logout-button"
                >

                    Logout

                </a>


            </div>


        </div>


        <div class="analytics-grid">


            <div class="analytics-card">


                <div class="analytics-top">


                    <div class="analytics-icon students-icon">

                        👥

                    </div>


                </div>


                <div class="analytics-label">

                    STUDENTS LOGGED IN

                </div>


                <div class="analytics-value">

                    {report["students"]}

                </div>


                <div class="analytics-description">

                    Unique students who have interacted
                    with the platform.

                </div>


            </div>


            <div class="analytics-card">


                <div class="analytics-top">


                    <div class="analytics-icon questions-icon">

                        ?

                    </div>


                </div>


                <div class="analytics-label">

                    QUESTIONS ATTEMPTED

                </div>


                <div class="analytics-value">

                    {report["questions"]}

                </div>


                <div class="analytics-description">

                    Total unique question attempts recorded.

                </div>


            </div>


            <div class="analytics-card">


                <div class="analytics-top">


                    <div class="analytics-icon quiz-icon">

                        ✓

                    </div>


                </div>


                <div class="analytics-label">

                    COMPLETED QUIZZES

                </div>


                <div class="analytics-value">

                    {report["quizzes"]}

                </div>


                <div class="analytics-description">

                    Quiz sessions completed by students.

                </div>


            </div>


            <div class="analytics-card">


                <div class="analytics-top">


                    <div class="analytics-icon hints-icon">

                        ?

                    </div>


                </div>


                <div class="analytics-label">

                    HINTS REQUESTED

                </div>


                <div class="analytics-value">

                    {report["hints"]}

                </div>


                <div class="analytics-description">

                    Number of times students requested hints.

                </div>


            </div>


            <div class="analytics-card featured">


                <div class="featured-row">


                    <div class="featured-info">


                        <div class="analytics-label">

                            AVERAGE ACCURACY

                        </div>


                        <div
                            class="accuracy-large"
                            style="color:{accuracy_color};"
                        >

                            {report["accuracy"]}%

                        </div>


                        <div class="analytics-description">

                            Average score across completed quiz
                            sessions.

                        </div>


                        <div class="accuracy-bar">


                            <div
                                class="accuracy-bar-fill"
                                style="width:{accuracy_width}%"
                            ></div>


                        </div>


                    </div>


                    <div class="analytics-icon accuracy-icon">

                        %

                    </div>


                </div>


            </div>


        </div>


        <div class="admin-info-panel">


            <div class="admin-info-title">

                Dashboard Overview

            </div>


            <div class="admin-info-text">

                These statistics are generated automatically from
                the EduText SQLite database. Student activity,
                completed quizzes, question attempts and hint
                requests are recorded as students use the platform.

            </div>


        </div>


        <a
            class="button admin-back"
            href="/"
        >

            ← Back to EduText

        </a>

        """

    )


# ================================================================
# SMS WEBHOOK
# ================================================================

@app.route(
    "/sms/incoming",
    methods=["POST"]
)
def incoming_sms():

    phone = request.form.get(
        "from"
    )

    text = request.form.get(
        "text",
        ""
    )

    if not phone:

        return jsonify({

            "status":
                "error",

            "message":
                "Missing phone number"

        }), 400


    result = process_input(
        phone,
        text
    )


    return jsonify({

        "status":
            "success",

        "response":
            result

    })


# ================================================================
# APPLICATION START
# ================================================================

if __name__ == "__main__":

    print(
        "=" * 60
    )

    print(
        "EduText Quiz Platform"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Open in your browser:"
    )

    print(
        "http://127.0.0.1:5000/"
    )

    print()

    print(
        "Quiz simulator:"
    )

    print(
        "http://127.0.0.1:5000/test"
    )

    print()

    print(
        "Admin Login:"
    )

    print(
        "http://127.0.0.1:5000/admin/login"
    )

    print()

    print(
        "Admin Dashboard:"
    )

    print(
        "http://127.0.0.1:5000/admin"
    )

    print()

    print(
        "Database:"
    )

    print(
        DATABASE_NAME
    )

    print()

    print(
        "=" * 60
    )

    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )
