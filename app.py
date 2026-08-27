from sys import prefix

import streamlit as st
from datetime import date
import json
import os
import re
import copy
import html
import base64
from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

def load_css():
    css_file = Path(__file__).parent / "style.css"

    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# =========================================================
# APP SETTINGS
# =========================================================

st.set_page_config(
    page_title="Bhu Bharathi Files",
    page_icon="📁",
    layout="wide"
)


DATA_FILE = "bhu_bharathi_data.json"

PDF_FOLDER = "BHU_BHARATHI_PDF_FILES"

# Logo is loaded from the same folder as this Python file.
# Supports the normal LOGO.png name and common Windows-renamed variants.
APP_FOLDER = Path(__file__).parent
LOGO_PATH = None
for _logo_name in ("LOGO.png", "logo.png", "LOGO(1).png"):
    _candidate = APP_FOLDER / _logo_name
    if _candidate.exists():
        LOGO_PATH = _candidate
        break


os.makedirs(
    PDF_FOLDER,
    exist_ok=True
)


# =========================================================
# COMPACT DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 0.35rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.30rem;
    }

    hr {
        margin-top: 0.55rem;
        margin-bottom: 0.55rem;
    }

    .app-title {
        text-align: left;
        font-size: 30px;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
    }

    .app-subtitle {
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        color: #bae6fd;
        margin-top: 4px;
    }

    .app-header {
        background: linear-gradient(135deg, #020617, #0b1736, #1e3a8a);
        border: 1px solid #26364d;
        border-radius: 20px;
        padding: 25px 30px;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px rgba(0,0,0,.30);
    }

    .deed-title {
        text-align: center;
        font-size: 27px;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 12px;
        color: #ffffff;
    }

    .section-title {
        text-align: left;
        font-size: 18px;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 12px;
        padding: 12px 16px;
        color: #2563eb;
        background: #ffffff;
        border-left: 5px solid #38bdf8;
        border-radius: 10px;
        box-shadow: 0 5px 16px rgba(0,0,0,.20);
    }

    .family-title {
        text-align: left;
        font-size: 16px;
        font-weight: 750;
        margin-top: 14px;
        margin-bottom: 8px;
        padding: 8px 12px;
        color: #7dd3fc;
        border-left: 3px solid #38bdf8;
        background: rgba(30,58,138,.18);
        border-radius: 7px;
    }

    .dashboard-card {
        background: linear-gradient(145deg, #111c2f, #0d1728);
        border: 1px solid #26364d;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 7px 20px rgba(0,0,0,.25);
    }

    .dashboard-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 650;
    }

    .dashboard-value {
        color: #7dd3fc;
        font-size: 28px;
        font-weight: 850;
        margin-top: 4px;
    }

    .dashboard-note {
        color: #cbd5e1;
        font-size: 12px;
        margin-top: 3px;
    }

    .sheet-wrapper {
        display: flex;
        justify-content: flex-start;
        margin-top: 1px;
        margin-bottom: 4px;
    }

    .sheet-box {
        display: inline-block;
        border: 1.5px solid #777;
        border-radius: 9px;
        padding: 3px 11px;
        text-align: center;
    }

    .sheet-label {
        font-size: 9px;
        font-weight: 650;
        line-height: 10px;
    }

    .sheet-number {
        font-size: 17px;
        font-weight: 850;
        line-height: 19px;
    }

    .search-sheet {
        border: 1px solid #777;
        border-radius: 9px;
        padding: 7px 11px;
        font-size: 17px;
        font-weight: 800;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EMPTY FILE
# =========================================================

def empty_file():

    return {

        "saved": False,

        "document_type": "SALE",

        "entry_date": str(
            date.today()
        ),

        "first_ppb": "",

        "first_name": "",

        "first_age": 0,

        "first_dod": "",

        "successor_count": 1,

        "first_relation": "S/o",

        "first_relation_name": "",

        "first_aadhaar": "",

        "first_house": "",

        "first_location": "",

        "first_state": "Telangana",

        "first_district": "",

        "first_mandal": "",

        "first_village": "",

        "first_pin": "",

        "first_cell": "",


        "first_family_relation":
        "SELECT RELATION",

        "first_family_other": "",

        "first_family_name": "",

        "first_family_father_name": "",

        "first_family_gender": "SELECT GENDER",

        "first_family_caste": "SELECT CASTE",

        "first_family_birth_year": 0,

        "first_family_age": 0,

        "first_family_board_resolution_date": "",

        "first_family_aadhaar": "",

        "first_family_house": "",

        "first_family_location": "",

        "first_family_village": "",

        "first_family_mandal": "",

        "first_family_district": "",

        "first_family_state": "Telangana",

        "first_family_pin": "",

        "first_family_cell": "",


        "transaction_number": "",

        "second_ppb": "",
         
        "second_caste": "SELECT CASTE",

        "second_gender": "SELECT GENDER",

        "second_name": "",

        "second_age": 0,

        "second_relation": "S/o",

        "second_relation_name": "",

        "second_aadhaar": "",

        "second_house": "",

        "second_location": "",

        "second_state": "Telangana",

        "second_district": "",

        "second_mandal": "",

        "second_village": "",

        "second_pin": "",

        "second_cell": "",

        "second_cin": "",

        "second_gstin": "",

        "second_pan": "",

        "second_incorporation_date": "",


        "second_family_relation":
        "SELECT RELATION",

        "second_family_other": "",

        "second_family_name": "",

        "second_family_father_name": "",

        "second_family_gender": "SELECT GENDER",

        "second_family_caste": "SELECT CASTE",

        "second_family_birth_year": 0,

        "second_family_age": 0,

        "second_family_board_resolution_date": "",

        "second_family_aadhaar": "",

        "second_family_house": "",

        "second_family_location": "",

        "second_family_village": "",

        "second_family_mandal": "",

        "second_family_district": "",

        "second_family_state": "Telangana",

        "second_family_pin": "",

        "second_family_cell": "",


        "surveys": [

            {

                "id": 1,

                "survey_number": "",

                "extent": "",

                "north": "",

                "south": "",

                "east": "",

                "west": ""

            }

        ],


        "challan_amount": 0.0,


        "payments": [

            {

                "id": 1,

                "amount": 0.0

            }

        ],


        "slot_date": str(
            date.today()
        ),

        "booking_status":
        "STATUS PENDING",

        "notes": ""

    }


# =========================================================
# DATABASE
# =========================================================

def load_database():

    if not os.path.exists(
        DATA_FILE
    ):

        return {}


    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            database = json.load(
                file
            )


        if isinstance(
            database,
            dict
        ):

            return database


    except Exception:

        return {}


    return {}


def save_database():

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            st.session_state.database,
            file,
            indent=4
        )


# =========================================================
# DATABASE MEMORY
# =========================================================

if "database" not in st.session_state:

    st.session_state.database = (
        load_database()
    )


default_file = empty_file()


for old_data in (
    st.session_state.database.values()
):

    for field, value in (
        default_file.items()
    ):

        if field not in old_data:

            old_data[field] = (
                copy.deepcopy(
                    value
                )
            )


save_database()


# =========================================================
# SHEET NUMBER
# =========================================================

def sheet_value(
    sheet
):

    try:

        return int(
            str(
                sheet
            ).replace(
                "NS-",
                ""
            )
        )

    except Exception:

        return 0


def format_sheet(
    number
):

    return (
        "NS-"
        +
        str(
            number
        ).zfill(4)
    )


def next_sheet():

    if not (
        st.session_state.database
    ):

        return "NS-0001"


    used_numbers = [

        sheet_value(
            item
        )

        for item in
        st.session_state.database.keys()

    ]


    return format_sheet(
        max(
            used_numbers
        )
        +
        1
    )


# =========================================================
# CURRENT SHEET / DIRECT SHEET URL
# =========================================================

# A saved sheet opened in a new tab uses a URL like ?sheet=NS-0001.
# A new empty sheet opened in another tab uses ?new_sheet=1.
new_sheet_request = str(st.query_params.get("new_sheet", "")).strip()
if new_sheet_request == "1":
    # This code runs only in the newly opened tab.
    # Reload the shared database so we use the latest sheet number.
    st.session_state.database = load_database()
    new_sheet_name = next_sheet()
    if new_sheet_name not in st.session_state.database:
        st.session_state.database[new_sheet_name] = empty_file()
        save_database()
    st.session_state.current_sheet = new_sheet_name
    # Change the URL to the real sheet so refreshing does not create another one.
    st.query_params.clear()
    st.query_params["sheet"] = new_sheet_name

requested_sheet = st.query_params.get("sheet", "")
if isinstance(requested_sheet, list):
    requested_sheet = requested_sheet[0] if requested_sheet else ""
requested_sheet = str(requested_sheet).strip().upper()

if (
    requested_sheet
    and requested_sheet in st.session_state.database
    and st.session_state.database[requested_sheet].get("saved", False)
):
    st.session_state.current_sheet = requested_sheet
elif "current_sheet" not in st.session_state:
    st.session_state.current_sheet = next_sheet()

if st.session_state.current_sheet not in st.session_state.database:
    st.session_state.database[st.session_state.current_sheet] = empty_file()
    save_database()


# =========================================================
# HELPERS
# =========================================================

def safe_date(
    value
):

    try:

        return date.fromisoformat(
            str(
                value
            )
        )

    except Exception:

        return date.today()


def document_names(
    document_type
):

    if document_type == "SALE":

        return (
            "SALE DEED DOCUMENT",
            "SELLER",
            "BUYER"
        )


    if document_type == "GIFT":

        return (
            "GIFT DEED DOCUMENT",
            "DONOR",
            "DONEE"
        )


    if document_type == "MORTGAGE":

        return (
            "MORTGAGE DEED DOCUMENT",
            "MORTGAGOR",
            "BANK"
        )


    return (
        "SUCCESSION DEED DOCUMENT",
        "PREDECESSOR",
        "SUCCESSOR"
    )


# =========================================================
# EXTENT
# =========================================================

def clean_extent(
    extent
):

    extent = re.sub(
        r"[^0-9.]",
        "",
        str(
            extent
        )
    )


    if extent.count(
        "."
    ) > 1:

        first, *remaining = (
            extent.split(
                "."
            )
        )


        extent = (
            first
            +
            "."
            +
            "".join(
                remaining
            )
        )


    if "." in extent:

        acres, decimal = (
            extent.split(
                ".",
                1
            )
        )


        extent = (
            acres
            +
            "."
            +
            decimal[:4]
        )


    return extent


def extent_guntas(
    extent
):

    extent = clean_extent(
        extent
    )


    if extent == "":

        return 0


    try:

        if "." in extent:

            acres_text, decimal = (
                extent.split(
                    ".",
                    1
                )
            )

        else:

            acres_text = extent

            decimal = ""


        acres = int(
            acres_text
            if acres_text
            else 0
        )


        decimal = decimal.ljust(
            4,
            "0"
        )


        guntas = int(
            decimal[:2]
        )


        if guntas > 39:

            return None


        return (
            acres * 40
            +
            guntas
        )


    except Exception:

        return None


def total_extent(
    surveys
):

    total = 0

    invalid = False


    for survey in surveys:

        converted = (
            extent_guntas(
                survey.get(
                    "extent",
                    ""
                )
            )
        )


        if converted is None:

            invalid = True

        else:

            total += converted


    acres = total // 40

    guntas = total % 40


    return (
        f"{acres}."
        f"{guntas:02d}"
        "00",
        invalid
    )


# =========================================================
# SAVE CURRENT SCREEN
# =========================================================

def collect_data():

    sheet = (
        st.session_state.current_sheet
    )


    data = (
        st.session_state.database[
            sheet
        ]
    )


    fields = [

        "document_type",

        "first_ppb",

        "first_name",

        "first_age",

        "first_dod",

        "first_relation",

        "first_relation_name",

        "first_aadhaar",

        "first_house",

        "first_location",

        "first_state",

        "first_district",

        "first_mandal",

        "first_village",

        "first_pin",

        "first_cell",

        "first_family_relation",

        "first_family_other",

        "first_family_name",

        "first_family_father_name",

        "first_family_gender",

        "first_family_caste",

        "first_family_birth_year",

        "first_family_age",

        "first_family_board_resolution_date",

        "first_family_aadhaar",

        "first_family_house",

        "first_family_location",

        "first_family_village",

        "first_family_mandal",

        "first_family_district",

        "first_family_state",

        "first_family_pin",

        "first_family_cell",

        "transaction_number",

        "second_ppb",

        "second_caste",

        "second_gender",

        "second_name",

        "second_age",

        "second_relation",

        "second_relation_name",

        "second_aadhaar",

        "second_house",

        "second_location",

        "second_state",

        "second_district",

        "second_mandal",

        "second_village",

        "second_pin",

        "second_cell",

        "second_cin",

        "second_gstin",

        "second_pan",

        "second_incorporation_date",

        "second_family_relation",

        "second_family_other",

        "second_family_name",

        "second_family_father_name",

        "second_family_gender",

        "second_family_caste",

        "second_family_birth_year",

        "second_family_age",

        "second_family_board_resolution_date",

        "second_family_aadhaar",

        "second_family_house",

        "second_family_location",

        "second_family_village",

        "second_family_mandal",

        "second_family_district",

        "second_family_state",

        "second_family_pin",

        "second_family_cell",

        "challan_amount",

        "booking_status",

        "notes"

    ]


    for field in fields:

        widget_key = (
            f"{sheet}_{field}"
        )


        if widget_key in (
            st.session_state
        ):

            data[field] = (
                st.session_state[
                    widget_key
                ]
            )


    # Save dynamically added SUCCESSION successors.
    successor_count_key = f"{sheet}_successor_count"
    if successor_count_key in st.session_state:
        data["successor_count"] = st.session_state[successor_count_key]

    successor_prefix = f"{sheet}_successor_"
    for widget_key, widget_value in st.session_state.items():
        if widget_key.startswith(successor_prefix):
            data[widget_key[len(f"{sheet}_"):]] = widget_value

    dod_key = (
        f"{sheet}_first_dod"
    )

    if dod_key in (
        st.session_state
    ):

        data["first_dod"] = str(
            st.session_state[
                dod_key
            ]
        )


    entry_key = (
        f"{sheet}_entry_date"
    )


    if entry_key in (
        st.session_state
    ):

        data["entry_date"] = str(
            st.session_state[
                entry_key
            ]
        )


    slot_key = (
        f"{sheet}_slot_date"
    )


    if slot_key in (
        st.session_state
    ):

        data["slot_date"] = str(
            st.session_state[
                slot_key
            ]
        )


    for survey in (
        data["surveys"]
    ):

        survey_id = (
            survey["id"]
        )


        for field in [

            "survey_number",

            "extent",

            "north",

            "south",

            "east",

            "west"

        ]:

            key = (

                f"{sheet}_"

                f"survey_"

                f"{survey_id}_"

                f"{field}"

            )


            if key in (
                st.session_state
            ):

                value = (
                    st.session_state[
                        key
                    ]
                )


                if field == "extent":

                    value = (
                        clean_extent(
                            value
                        )
                    )


                survey[field] = value


    for payment in (
        data["payments"]
    ):

        payment_id = (
            payment["id"]
        )


        key = (

            f"{sheet}_"

            f"payment_"

            f"{payment_id}"

        )


        if key in (
            st.session_state
        ):

            payment["amount"] = (
                st.session_state[
                    key
                ]
            )


    # Save SUCCESSION successor-wise land allocations.
    if data.get("document_type") == "SUCCESSION":
        successor_count = int(data.get("successor_count", 1) or 1)
        successor_lands = data.setdefault("successor_lands", {})
        for successor_number in range(1, successor_count + 1):
            land_key = f"successor_{successor_number}"
            allocations = successor_lands.setdefault(land_key, [])
            for allocation in allocations:
                allocation_id = allocation.get("id")
                for field in ["survey_number", "extent", "north", "south", "east", "west"]:
                    widget_key = f"{sheet}_{land_key}_land_{allocation_id}_{field}"
                    if widget_key in st.session_state:
                        value = st.session_state[widget_key]
                        if field == "extent":
                            value = clean_extent(value)
                        allocation[field] = value

    save_database()


# =========================================================
# CLEAR SHEET WIDGETS
# =========================================================

def clear_widgets(
    sheet
):

    remove_keys = [

        key

        for key in
        list(
            st.session_state.keys()
        )

        if str(
            key
        ).startswith(
            f"{sheet}_"
        )

    ]


    for key in remove_keys:

        del st.session_state[
            key
        ]


# =========================================================
# SEARCH
# =========================================================

def search_files(
    text
):

    text = (
        str(
            text
        )
        .strip()
        .lower()
    )


    if text == "":

        return []


    fields = [

        "first_name",

        "first_aadhaar",

        "first_cell",

        "first_family_name",

        "first_family_father_name",

        "first_family_aadhaar",

        "first_family_cell",

        "second_name",

        "second_aadhaar",

        "second_cell",

        "second_cin",

        "second_gstin",

        "second_pan",

        "second_family_name",

        "second_family_father_name",

        "second_family_aadhaar",

        "second_family_cell"

    ]


    found = []


    for sheet, data in (
        st.session_state.database.items()
    ):

        if not data.get(
            "saved",
            False
        ):

            continue


        searchable = [

            str(
                sheet
            ).lower()

        ]


        for field in fields:

            searchable.append(

                str(
                    data.get(
                        field,
                        ""
                    )
                ).lower()

            )


        if any(

            text in value

            for value in searchable

        ):

            found.append(
                sheet
            )


    return sorted(
        found,
        key=sheet_value
    )


def open_sheet(
    new_sheet
):

    old_sheet = (
        st.session_state.current_sheet
    )


    collect_data()


    clear_widgets(
        old_sheet
    )


    st.session_state.current_sheet = (
        new_sheet
    )


# =========================================================
# PDF
# =========================================================

def pdf_text(
    value
):

    return html.escape(
        str(
            value
            if value is not None
            else ""
        )
    )


def create_pdf(
    sheet,
    data
):

    output = BytesIO()


    document = SimpleDocTemplate(

        output,

        pagesize=landscape(
            A4
        ),

        leftMargin=22,

        rightMargin=22,

        topMargin=20,

        bottomMargin=20

    )


    styles = (
        getSampleStyleSheet()
    )


    title_style = (
        styles["Title"]
    )


    title_style.alignment = (
        TA_CENTER
    )


    heading_style = (
        styles["Heading2"]
    )


    heading_style.alignment = (
        TA_CENTER
    )


    story = []


    deed_heading, first_name, second_name = (

        document_names(

            data.get(

                "document_type",

                "SALE"

            )

        )

    )


    story.append(

        Paragraph(

            "BHU BHARATHI LAND FILES",

            title_style

        )

    )


    story.append(

        Paragraph(

            pdf_text(
                deed_heading
            ),

            heading_style

        )

    )


    story.append(

        Spacer(
            1,
            8
        )

    )


    main_rows = [

        [

            "Sheet Number",

            pdf_text(
                sheet
            ),

            "Document Type",

            pdf_text(

                data.get(

                    "document_type",

                    ""

                )

            ),

            "Entry Date",

            pdf_text(

                data.get(

                    "entry_date",

                    ""

                )

            )

        ]

    ]


    main_table = Table(

        main_rows,

        colWidths=[

            85,

            100,

            90,

            100,

            75,

            100

        ]

    )


    main_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0, 0),

                    (-1, -1),

                    0.5,

                    colors.grey

                ),

                (

                    "BACKGROUND",

                    (0, 0),

                    (0, -1),

                    colors.lightgrey

                ),

                (

                    "BACKGROUND",

                    (2, 0),

                    (2, -1),

                    colors.lightgrey

                ),

                (

                    "BACKGROUND",

                    (4, 0),

                    (4, -1),

                    colors.lightgrey

                )

            ]

        )

    )


    story.append(
        main_table
    )


    story.append(

        Spacer(
            1,
            10
        )

    )


    first_address = ", ".join(

        [

            str(data.get("first_house", "")),

            str(data.get("first_location", "")),

            str(data.get("first_village", "")),

            str(data.get("first_mandal", "")),

            str(data.get("first_district", "")),

            str(data.get("first_state", "")),

            str(data.get("first_pin", ""))

        ]

    )


    second_address = ", ".join(

        [

            str(data.get("second_house", "")),

            str(data.get("second_location", "")),

            str(data.get("second_village", "")),

            str(data.get("second_mandal", "")),

            str(data.get("second_district", "")),

            str(data.get("second_state", "")),

            str(data.get("second_pin", ""))

        ]

    )


    if data.get("document_type") == "MORTGAGE":

        auth_address = ", ".join(

            [

                str(data.get("second_family_house", "")),

                str(data.get("second_family_location", "")),

                str(data.get("second_family_village", "")),

                str(data.get("second_family_mandal", "")),

                str(data.get("second_family_district", "")),

                str(data.get("second_family_state", "")),

                str(data.get("second_family_pin", ""))

            ]

        )


        person_rows = [

            [

                f"{first_name} DETAILS",

                "",

                "BANK DETAILS",

                ""

            ],

            [

                "PPB No.",

                pdf_text(data.get("first_ppb", "")),

                "TXN No.",

                pdf_text(data.get("transaction_number", ""))

            ],

            [

                "Name",

                pdf_text(data.get("first_name", "")),

                "Bank Name",

                pdf_text(data.get("second_name", ""))

            ],

            [

                "Age",

                pdf_text(data.get("first_age", "")),

                "CIN/Firm No.",

                pdf_text(data.get("second_cin", ""))

            ],

            [

                "S/D/W/o",

                pdf_text(data.get("first_relation", "")),

                "GSTIN No.",

                pdf_text(data.get("second_gstin", ""))

            ],

            [

                "Relation Name",

                pdf_text(data.get("first_relation_name", "")),

                "PAN No.",

                pdf_text(data.get("second_pan", ""))

            ],

            [

                "Aadhaar",

                pdf_text(data.get("first_aadhaar", "")),

                "Incorp. Date",

                pdf_text(data.get("second_incorporation_date", ""))

            ],

            [

                "Cell",

                pdf_text(data.get("first_cell", "")),

                "Bank Cell",

                pdf_text(data.get("second_cell", ""))

            ],

            [

                "Address",

                pdf_text(first_address),

                "Bank Address",

                pdf_text(second_address)

            ],

            [

                "",

                "",

                "BANK AUTHORISED PERSON",

                ""

            ],

            [

                "",

                "",

                "Aadhaar No.",

                pdf_text(data.get("second_family_aadhaar", ""))

            ],

            [

                "",

                "",

                "Name",

                pdf_text(data.get("second_family_name", ""))

            ],

            [

                "",

                "",

                "Father Name",

                pdf_text(data.get("second_family_father_name", ""))

            ],

            [

                "",

                "",

                "Gender",

                pdf_text(

                    data.get("second_family_gender", "")

                    if data.get("second_family_gender") != "SELECT GENDER"

                    else ""

                )

            ],

            [

                "",

                "",

                "Caste",

                pdf_text(

                    data.get("second_family_caste", "")

                    if data.get("second_family_caste") != "SELECT CASTE"

                    else ""

                )

            ],

            [

                "",

                "",

                "Age",

                pdf_text(data.get("second_family_age", "") or data.get("second_auto_age", ""))

            ],

            [

                "",

                "",

                "Board Res. Date",

                pdf_text(data.get("second_family_board_resolution_date", ""))

            ],

            [

                "",

                "",

                "Cell No.",

                pdf_text(data.get("second_family_cell", ""))

            ],

            [

                "",

                "",

                "Address",

                pdf_text(auth_address)

            ]

        ]

    else:

        person_rows = [

            [

                f"{first_name} DETAILS",

                "",

                f"{second_name} DETAILS",

                ""

            ],

            [

                "PPB No.",

                pdf_text(data.get("first_ppb", "")),

                "TXN No.",

                pdf_text(data.get("transaction_number", ""))

            ],

            [

                "Name",

                pdf_text(data.get("first_name", "")),

                "PPB No.",

                pdf_text(data.get("second_ppb", ""))

            ],

            [

                "Age",

                pdf_text(data.get("first_age", "")),

                "Name",

                pdf_text(data.get("second_name", ""))

            ],

            [

                "S/D/W/o",

                pdf_text(data.get("first_relation", "")),

                "Age",

                pdf_text(data.get("second_age", ""))

            ],

            [

                "Relation Name",

                pdf_text(data.get("first_relation_name", "")),

                "S/D/W/o",

                pdf_text(data.get("second_relation", ""))

            ],

            [

                "Aadhaar",

                pdf_text(data.get("first_aadhaar", "")),

                "Relation Name",

                pdf_text(data.get("second_relation_name", ""))

            ],

            [

                "Cell",

                pdf_text(data.get("first_cell", "")),

                "Gender",

                pdf_text(

                    data.get("second_gender", "")

                    if data.get("second_gender") != "SELECT GENDER"

                    else ""

                )

            ],

            [

                "Address",

                pdf_text(first_address),

                "Caste",

                pdf_text(

                    data.get("second_caste", "")

                    if data.get("second_caste") != "SELECT CASTE"

                    else ""

                )

            ],

            [

                "",

                "",

                "Aadhaar",

                pdf_text(data.get("second_aadhaar", ""))

            ],

            [

                "",

                "",

                "Cell",

                pdf_text(data.get("second_cell", ""))

            ],

            [

                "",

                "",

                "Address",

                pdf_text(second_address)

            ]

        ]


    person_table = Table(

        person_rows,

        colWidths=[

            100,

            275,

            100,

            275

        ]

    )


    person_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0, 0),

                    (-1, -1),

                    0.5,

                    colors.grey

                ),

                (

                    "SPAN",

                    (0, 0),

                    (1, 0)

                ),

                (

                    "SPAN",

                    (2, 0),

                    (3, 0)

                ),

                (

                    "BACKGROUND",

                    (0, 0),

                    (1, 0),

                    colors.lightgrey

                ),

                (

                    "BACKGROUND",

                    (2, 0),

                    (3, 0),

                    colors.lightgrey

                ),

                (

                    "ALIGN",

                    (0, 0),

                    (-1, 0),

                    "CENTER"

                ),

                (

                    "VALIGN",

                    (0, 0),

                    (-1, -1),

                    "TOP"

                )

            ]

        )

    )


    if data.get("document_type") == "MORTGAGE":

        person_table.setStyle(

            TableStyle(

                [

                    (

                        "SPAN",

                        (2, 9),

                        (3, 9)

                    ),

                    (

                        "BACKGROUND",

                        (2, 9),

                        (3, 9),

                        colors.lightgrey

                    ),

                    (

                        "ALIGN",

                        (2, 9),

                        (3, 9),

                        "CENTER"

                    )

                ]

            )

        )


    story.append(
        person_table
    )


    story.append(

        Spacer(
            1,
            10
        )

    )


    land_rows = [

        [

            "Survey No.",

            "Extent",

            "North",

            "South",

            "East",

            "West"

        ]

    ]


    for survey in (

        data.get(

            "surveys",

            []

        )

    ):

        land_rows.append(

            [

                pdf_text(

                    survey.get(

                        "survey_number",

                        ""

                    )

                ),

                pdf_text(

                    survey.get(

                        "extent",

                        ""

                    )

                ),

                pdf_text(

                    survey.get(

                        "north",

                        ""

                    )

                ),

                pdf_text(

                    survey.get(

                        "south",

                        ""

                    )

                ),

                pdf_text(

                    survey.get(

                        "east",

                        ""

                    )

                ),

                pdf_text(

                    survey.get(

                        "west",

                        ""

                    )

                )

            ]

        )


    land_table = Table(

        land_rows,

        repeatRows=1,

        colWidths=[

            100,

            80,

            140,

            140,

            140,

            140

        ]

    )


    land_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0, 0),

                    (-1, -1),

                    0.5,

                    colors.grey

                ),

                (

                    "BACKGROUND",

                    (0, 0),

                    (-1, 0),

                    colors.lightgrey

                )

            ]

        )

    )


    story.append(
        land_table
    )


    calculated_extent, unused = (

        total_extent(

            data.get(

                "surveys",

                []

            )

        )

    )


    story.append(

        Spacer(
            1,
            6
        )

    )


    story.append(

        Paragraph(

            f"<b>TOTAL EXTENT: "

            f"{pdf_text(calculated_extent)}"

            f"</b>",

            styles["Normal"]

        )

    )


    total_paid = sum(

        float(

            payment.get(

                "amount",

                0

            )

        )

        for payment in

        data.get(

            "payments",

            []

        )

    )


    challan = float(

        data.get(

            "challan_amount",

            0

        )

    )


    payment_rows = [

        [

            "Challan Rs.",

            challan,

            "Total Paid",

            total_paid,

            "Balance",

            challan - total_paid

        ],

        [

            "Slot Date",

            pdf_text(

                data.get(

                    "slot_date",

                    ""

                )

            ),

            "Booking Status",

            pdf_text(

                data.get(

                    "booking_status",

                    ""

                )

            ),

            "Notes",

            pdf_text(

                data.get(

                    "notes",

                    ""

                )

            )

        ]

    ]


    payment_table = Table(

        payment_rows,

        colWidths=[

            90,

            120,

            90,

            120,

            90,

            240

        ]

    )


    payment_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0, 0),

                    (-1, -1),

                    0.5,

                    colors.grey

                ),

                (

                    "BACKGROUND",

                    (0, 0),

                    (0, -1),

                    colors.lightgrey

                ),

                (

                    "BACKGROUND",

                    (2, 0),

                    (2, -1),

                    colors.lightgrey

                ),

                (

                    "BACKGROUND",

                    (4, 0),

                    (4, -1),

                    colors.lightgrey

                )

            ]

        )

    )


    story.append(

        Spacer(
            1,
            10
        )

    )


    story.append(
        payment_table
    )


    document.build(
        story
    )


    pdf_bytes = (
        output.getvalue()
    )


    output.close()


    return pdf_bytes


# =========================================================
# TITLE
# =========================================================

header_logo_col, header_text_col = st.columns([1, 6])

with header_logo_col:
    if LOGO_PATH:
        st.image(str(LOGO_PATH), width=110)
    else:
        st.markdown("<div style='font-size:42px; padding-top:10px;'>🏛️</div>", unsafe_allow_html=True)

with header_text_col:
    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-title">SLOT BOOKING DETAILS</div>
            <div class="app-subtitle">
                Digital Land Document Management System
                &nbsp;•&nbsp; Current File: {st.session_state.current_sheet}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CURRENT DATA
# =========================================================

sheet = (
    st.session_state.current_sheet
)



data = (
    st.session_state.database[
        sheet
    ]
)

# =========================================================
# PROFESSIONAL SIDEBAR + NAVIGATION
# =========================================================

saved_files = [
    item for item in st.session_state.database.values()
    if item.get("saved", False)
]

pending_files = sum(
    1 for item in saved_files
    if item.get("booking_status", "STATUS PENDING") == "STATUS PENDING"
)

completed_files = sum(
    1 for item in saved_files
    if item.get("booking_status", "STATUS PENDING") == "REG. COMPLETED"
)

with st.sidebar:
    if LOGO_PATH:
        st.image(str(LOGO_PATH), width=160)
    else:
        st.markdown(
            """
            <div style="text-align:center; padding:8px 0 18px;">
                <div style="font-size:30px;">🏛️</div>
                <div style="font-size:20px; font-weight:850; color:#ffffff;">
                    N-SMART
                </div>
                <div style="font-size:11px; color:#7dd3fc; margin-top:3px;">
                    ONLINE SERVICES
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    navigation = st.radio(
        "NAVIGATION",
        ["📄 Document Entry", "📊 Dashboard"],
        key="main_navigation"
    )

    st.divider()

    st.markdown(
        f"""
        <div style="padding:8px 4px;">
            <div style="font-size:11px;color:#94a3b8;font-weight:700;">
                CURRENT SHEET
            </div>
            <div style="font-size:24px;color:#7dd3fc;font-weight:850;">
                {sheet}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Opens a brand-new empty sheet in a separate browser tab.
    # The current sheet and its current data remain untouched.
    st.markdown(
        """
        <a href="./?new_sheet=1" target="_blank" rel="noopener noreferrer"
           style="display:block; text-align:center; padding:0.55rem 0.8rem;
                  border-radius:0.5rem; text-decoration:none; font-weight:700;
                  background:#1f77b4; color:white; margin-bottom:0.5rem;">
            ➕ NEW EMPTY SHEET ↗
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="margin-top:18px;padding:14px;border:1px solid #26364d;
                    border-radius:12px;background:#111c2f;">
            <div style="font-size:11px;color:#94a3b8;">FILES</div>
            <div style="font-size:22px;font-weight:850;color:#7dd3fc;">
                {len(saved_files)}
            </div>
            <div style="font-size:11px;color:#94a3b8;margin-top:8px;">
                Pending: <b style="color:#fbbf24;">{pending_files}</b>
                &nbsp;&nbsp; Completed:
                <b style="color:#86efac;">{completed_files}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# DASHBOARD VIEW
# =========================================================

if navigation == "📊 Dashboard":
    st.markdown(
        """
        <div class="app-header">
            <div class="app-title">🏛️ BHU BHARATHI</div>
            <div class="app-subtitle">Land Document Management Dashboard</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📊 SYSTEM OVERVIEW</div>',
        unsafe_allow_html=True
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.markdown(
            f'''<div class="dashboard-card">
                <div class="dashboard-label">TOTAL SAVED FILES</div>
                <div class="dashboard-value">{len(saved_files)}</div>
                <div class="dashboard-note">All registered sheets</div>
            </div>''',
            unsafe_allow_html=True
        )

    with metric_2:
        st.markdown(
            f'''<div class="dashboard-card">
                <div class="dashboard-label">PENDING</div>
                <div class="dashboard-value">{pending_files}</div>
                <div class="dashboard-note">Registration pending</div>
            </div>''',
            unsafe_allow_html=True
        )

    with metric_3:
        st.markdown(
            f'''<div class="dashboard-card">
                <div class="dashboard-label">COMPLETED</div>
                <div class="dashboard-value">{completed_files}</div>
                <div class="dashboard-note">Registration completed</div>
            </div>''',
            unsafe_allow_html=True
        )

    with metric_4:
        total_files = len(st.session_state.database)
        st.markdown(
            f'''<div class="dashboard-card">
                <div class="dashboard-label">TOTAL SHEETS</div>
                <div class="dashboard-value">{total_files}</div>
                <div class="dashboard-note">Saved + active sheets</div>
            </div>''',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">📁 SAVED SHEETS</div>',
        unsafe_allow_html=True
    )

    saved_sheet_items = sorted(
        [(name, item) for name, item in st.session_state.database.items()
         if item.get("saved", False)],
        key=lambda item: sheet_value(item[0])
    )

    if saved_sheet_items:
        for row_start in range(0, len(saved_sheet_items), 4):
            row_items = saved_sheet_items[row_start:row_start + 4]
            card_columns = st.columns(4)
            for card_index, card_column in enumerate(card_columns):
                with card_column:
                    if card_index < len(row_items):
                        saved_sheet_name, saved_sheet_data = row_items[card_index]
                        document_type = saved_sheet_data.get("document_type", "SALE")
                        primary_name = saved_sheet_data.get("first_name", "") or "—"
                        st.markdown(
                            f"""
                            <a href="?sheet={saved_sheet_name}" target="_blank"
                               style="text-decoration:none; display:block;">
                              <div style="min-height:145px; padding:16px; border:1px solid #26364d;
                                          border-radius:14px; background:#111c2f; margin-bottom:12px; cursor:pointer;">
                                <div style="font-size:28px;">📄</div>
                                <div style="font-size:20px; font-weight:850; color:#7dd3fc; margin-top:5px;">{saved_sheet_name}</div>
                                <div style="font-size:11px; color:#94a3b8; margin-top:5px;">{document_type}</div>
                                <div style="font-size:12px; color:#ffffff; margin-top:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{primary_name}</div>
                                <div style="font-size:11px; color:#86efac; margin-top:10px; font-weight:700;">OPEN ↗</div>
                              </div>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
    else:
        st.info("No saved sheets yet. Saved files will appear here.")

    st.stop()

# =========================================================
# SHEET NUMBER — TOP LEFT WITHOUT RECTANGLE
# =========================================================

st.markdown(
    f"""
<div style="text-align: left; margin-top: 2px; margin-bottom: 6px;">
<div style="font-size: 10px; font-weight: 600;">SHEET NO.</div>
<div style="font-size: 18px; font-weight: 800;">{sheet}</div>
</div>
""",
    unsafe_allow_html=True
)


type_column, date_column, search_column = (

    st.columns(

        [

            1,

            1,

            1.6

        ]

    )

)


document_types = [

    "SALE",

    "GIFT",

    "MORTGAGE",

    "SUCCESSION"

]


saved_type = (

    data.get(

        "document_type",

        "SALE"

    )

)


if saved_type not in (
    document_types
):

    saved_type = "SALE"


with type_column:

    selected_document = (

        st.selectbox(

            "📜 DOCUMENT TYPE",

            document_types,

            index=(

                document_types.index(

                    saved_type

                )

            ),

            key=(

                f"{sheet}_"

                "document_type"

            )

        )

    )


with date_column:

    st.date_input(

        "📅 ENTRY DATE",

        value=(

            safe_date(

                data.get(

                    "entry_date",

                    str(

                        date.today()

                    )

                )

            )

        ),

        key=(

            f"{sheet}_"

            "entry_date"

        ),

        format="DD/MM/YYYY"

    )


with search_column:

    search_text = (

        st.text_input(

            "🔎 SEARCH SAVED FILE",

            placeholder=(

                "Name, cell, Aadhaar "

                "or NS-0001"

            ),

            key="main_search"

        )

    )


# =========================================================
# SEARCH RESULTS
# =========================================================

results = search_files(
    search_text
)


if search_text.strip():

    if not results:

        st.warning(
            "No saved sheet found."
        )

    else:

        for result in results:

            result_box, result_button = (

                st.columns(

                    [

                        5,

                        1

                    ]

                )

            )


            with result_box:

                st.markdown(

                    f"""

                    <div class="search-sheet">

                    📄 {result}

                    </div>

                    """,

                    unsafe_allow_html=True

                )


            with result_button:

                # Opens the selected saved sheet in a new browser tab.
                st.markdown(
                    f"""<a href="?sheet={result}" target="_blank"
                    style="display:block; text-align:center; padding:0.55rem 0.7rem;
                    border-radius:8px; background:#1d4ed8; color:white;
                    text-decoration:none; font-weight:700;">📂 OPEN ↗</a>""",
                    unsafe_allow_html=True
                )


# =========================================================
# DEED HEADING
# =========================================================

deed_heading, first_title, second_title = (

    document_names(

        selected_document

    )

)


st.markdown(

    f"""

    <div class="deed-title">

    {deed_heading}

    </div>

    """,

    unsafe_allow_html=True

)


# =========================================================
# REUSABLE PERSON FORM
# =========================================================

def person_form(

    prefix,

    person_title,

    include_transaction=False,

    ppb_optional=False,

    show_caste_gender=False,

    is_bank=False

):


    if is_bank:

        st.markdown(

            """

            <div class="section-title">

            BANK DETAILS

            </div>

            """,

            unsafe_allow_html=True

        )


        name_col, txn_col = st.columns(2)


        with name_col:

            st.text_input(

                "BANK NAME",

                value=data.get(f"{prefix}_name", ""),

                key=f"{sheet}_{prefix}_name"

            )


        with txn_col:

            st.text_input(

                "TXN No.",

                value=data.get("transaction_number", ""),

                key=f"{sheet}_transaction_number"

            )


        cin_col, gstin_col = st.columns(2)


        with cin_col:

            st.text_input(

                "CIN/FIRM/SOCIETY/TRUST NO.",

                value=data.get(f"{prefix}_cin", ""),

                key=f"{sheet}_{prefix}_cin"

            )


        with gstin_col:

            st.text_input(

                "GSTIN NO.",

                value=data.get(f"{prefix}_gstin", ""),

                key=f"{sheet}_{prefix}_gstin"

            )


        pan_col, inc_col = st.columns(2)


        with pan_col:

            st.text_input(

                "PAN NO.",

                value=data.get(f"{prefix}_pan", ""),

                max_chars=10,

                key=f"{sheet}_{prefix}_pan"

            )


        with inc_col:

            st.text_input(

                "DATE OF INCORPORATION",

                value=data.get(f"{prefix}_incorporation_date", ""),

                placeholder="DD-MM-YYYY",

                key=f"{sheet}_{prefix}_incorporation_date"

            )


        # =====================================================
        # BANK ADDRESS HEADER
        # =====================================================
        st.markdown(

            """

            <div class="section-title">

            BANK ADDRESS

            </div>

            """,

            unsafe_allow_html=True

        )


        house_col, location_col = st.columns(2)


        with house_col:

            st.text_input(

                "Bank Branch H.No. / Bldg.",

                value=data.get(f"{prefix}_house", ""),

                key=f"{sheet}_{prefix}_house"

            )


        with location_col:

            st.text_input(

                "Location / Street",

                value=data.get(f"{prefix}_location", ""),

                key=f"{sheet}_{prefix}_location"

            )


        village_col, mandal_col = st.columns(2)


        with village_col:

            st.text_input(

                "Village / City",

                value=data.get(f"{prefix}_village", ""),

                key=f"{sheet}_{prefix}_village"

            )


        with mandal_col:

            st.text_input(

                "Mandal",

                value=data.get(f"{prefix}_mandal", ""),

                key=f"{sheet}_{prefix}_mandal"

            )


        district_col, state_col = st.columns(2)


        with district_col:

            st.text_input(

                "District",

                value=data.get(f"{prefix}_district", ""),

                key=f"{sheet}_{prefix}_district"

            )


        with state_col:

            st.text_input(

                "State",

                value=data.get(f"{prefix}_state", "Telangana"),

                key=f"{sheet}_{prefix}_state"

            )


        pin_col, cell_col = st.columns(2)


        with pin_col:

            st.text_input(

                "PIN No.",

                value=data.get(f"{prefix}_pin", ""),

                max_chars=6,

                key=f"{sheet}_{prefix}_pin"

            )


        with cell_col:

            st.text_input(

                "Bank Cell / Phone No.",

                value=data.get(f"{prefix}_cell", ""),

                max_chars=10,

                key=f"{sheet}_{prefix}_cell"

            )


        # =====================================================
        # BANK AUTHORISED PERSON DETAILS
        # =====================================================
        st.markdown(

            """

            <div class="family-title">

            BANK AUTHORISED PERSON DETAILS

            </div>

            """,

            unsafe_allow_html=True

        )


        aadhaar_col, name_col = st.columns(2)


        with aadhaar_col:

            st.text_input(

                "Aadhaar No.",

                value=data.get(f"{prefix}_family_aadhaar", ""),

                max_chars=12,

                key=f"{sheet}_{prefix}_family_aadhaar"

            )


        with name_col:

            st.text_input(

                "Name",

                value=data.get(f"{prefix}_family_name", ""),

                key=f"{sheet}_{prefix}_family_name"

            )


        father_col, gender_col = st.columns(2)


        with father_col:

            st.text_input(

                "Father Name",

                value=data.get(f"{prefix}_family_father_name", ""),

                key=f"{sheet}_{prefix}_family_father_name"

            )


        gender_options = [

            "SELECT GENDER",

            "MALE",

            "FEMALE",

            "OTHER"

        ]


        caste_options = [

            "SELECT CASTE",

            "GENERAL(OC)",

            "SC",

            "ST",

            "BC-A",

            "BC-B",

            "BC-C",

            "BC-D",

            "BC-E",

            "MINORITY",

            "OTHERS"

        ]


        saved_gender = data.get(f"{prefix}_family_gender", "SELECT GENDER")

        saved_caste = data.get(f"{prefix}_family_caste", "SELECT CASTE")


        if saved_gender not in gender_options:

            saved_gender = "SELECT GENDER"


        if saved_caste not in caste_options:

            saved_caste = "SELECT CASTE"


        with gender_col:

            st.selectbox(

                "Gender",

                gender_options,

                index=gender_options.index(saved_gender),

                key=f"{sheet}_{prefix}_family_gender"

            )


        caste_col, res_col = st.columns(2)


        with caste_col:

            st.selectbox(

                "Caste",

                caste_options,

                index=caste_options.index(saved_caste),

                key=f"{sheet}_{prefix}_family_caste"

            )


        with res_col:

            st.text_input(

                "Date of Board Resolution",

                value=data.get(f"{prefix}_family_board_resolution_date", ""),

                placeholder="DD-MM-YYYY",

                key=f"{sheet}_{prefix}_family_board_resolution_date"

            )


        current_year = date.today().year


        birth_col, age_col = st.columns(2)


        with birth_col:

            birth_year = st.number_input(

                "Birth Year",

                min_value=0,

                max_value=current_year,

                value=int(data.get(f"{prefix}_family_birth_year", 0)),

                key=f"{sheet}_{prefix}_family_birth_year"

            )


        with age_col:

            if birth_year > 0:

                calculated_age = current_year - birth_year

                st.number_input(

                    "Age",

                    value=calculated_age,

                    disabled=True,

                    key=f"{sheet}_{prefix}_auto_age"

                )

            else:

                st.number_input(

                    "Age",

                    min_value=0,

                    max_value=120,

                    value=int(data.get(f"{prefix}_family_age", 0)),

                    key=f"{sheet}_{prefix}_family_age"

                )


        auth_house_col, auth_street_col = st.columns(2)


        with auth_house_col:

            st.text_input(

                "H.No. / Bldg.",

                value=data.get(f"{prefix}_family_house", ""),

                key=f"{sheet}_{prefix}_family_house"

            )


        with auth_street_col:

            st.text_input(

                "Street / Location",

                value=data.get(f"{prefix}_family_location", ""),

                key=f"{sheet}_{prefix}_family_location"

            )


        auth_village_col, auth_mandal_col = st.columns(2)


        with auth_village_col:

            st.text_input(

                "Village / City",

                value=data.get(f"{prefix}_family_village", ""),

                key=f"{sheet}_{prefix}_family_village"

            )


        with auth_mandal_col:

            st.text_input(

                "Mandal",

                value=data.get(f"{prefix}_family_mandal", ""),

                key=f"{sheet}_{prefix}_family_mandal"

            )


        auth_district_col, auth_state_col = st.columns(2)


        with auth_district_col:

            st.text_input(

                "District",

                value=data.get(f"{prefix}_family_district", ""),

                key=f"{sheet}_{prefix}_family_district"

            )


        with auth_state_col:

            st.text_input(

                "State",

                value=data.get(f"{prefix}_family_state", "Telangana"),

                key=f"{sheet}_{prefix}_family_state"

            )


        auth_pin_col, auth_cell_col = st.columns(2)


        with auth_pin_col:

            st.text_input(

                "PIN No.",

                value=data.get(f"{prefix}_family_pin", ""),

                max_chars=6,

                key=f"{sheet}_{prefix}_family_pin"

            )


        with auth_cell_col:

            st.text_input(

                "Cell No.",

                value=data.get(f"{prefix}_family_cell", ""),

                max_chars=10,

                key=f"{sheet}_{prefix}_family_cell"

            )


        return


    # =====================================================
    # NORMAL PERSON FORM (FOR SELLER/BUYER/DONOR/DONEE ETC.)
    # =====================================================

    st.markdown(

        f"""

        <div class="section-title">

        {person_title} DETAILS

        </div>

        """,

        unsafe_allow_html=True

    )



    # =====================================================
    # NAME + AGE / DOD
    # =====================================================

    if (
        selected_document == "SUCCESSION"
        and prefix == "first"
    ):

        # SUCCESSION — PREDECESSOR
        st.text_input("PPB No.", value=data.get("first_ppb", ""), key=f"{sheet}_first_ppb")

        name_column, age_column, dod_column = st.columns(3)
        with name_column:
            st.text_input("Predecessor Name", value=data.get("first_name", ""), key=f"{sheet}_first_name")
        with age_column:

            if birth_year > 0:

                calculated_age = max(
                    0,
                    current_year - int(birth_year)
                )

                data[
                    f"{prefix}_family_age"
                ] = calculated_age

                st.text_input(
                    "Age",
                    value=f"{calculated_age} years",
                    disabled=True,
                    key=(
                        f"{sheet}_"
                        f"{prefix}_family_age_display"
                    )
                )


            else:

                st.number_input(

                    "Age",

                    min_value=0,

                    max_value=120,

                    value=int(

                        data.get(

                            f"{prefix}_family_age",

                            0

                        )

                    ),

                    key=(

                        f"{sheet}_"

                        f"{prefix}_family_age"

                    )

                )

        family_aadhaar, family_cell = (

            st.columns(2)

        )


        with family_aadhaar:

            st.text_input(

                "Family Aadhaar No.",

                value=(

                    data.get(

                        f"{prefix}_family_aadhaar",

                        ""

                    )

                ),

                max_chars=12,

                key=(

                    f"{sheet}_"

                    f"{prefix}_family_aadhaar"

                )

            )


        with family_cell:

            st.text_input(

                "Family Cell No.",

                value=(

                    data.get(

                        f"{prefix}_family_cell",

                        ""

                    )

                ),

                max_chars=10,

                key=(

                    f"{sheet}_"

                    f"{prefix}_family_cell"

                )

            )


# =========================================================
# SUCCESSION — SUCCESSOR COUNT
# =========================================================
if selected_document == "SUCCESSION":
    successor_count_key = f"{sheet}_successor_count"
    if successor_count_key not in st.session_state:
        st.session_state[successor_count_key] = max(1, int(data.get("successor_count", 1)))

# =========================================================
# PERSON SPLIT VIEW
# =========================================================

first_column, second_column = (

    st.columns(

        2,

        gap="medium"

    )

)


with first_column:

    person_form(

        "first",

        first_title

    )


with second_column:

    person_form(

        "second",

        second_title,

        include_transaction=True,

        ppb_optional=True,

        show_caste_gender=(

            selected_document in [

                "SALE",

                "GIFT"

            ]

        ),

        is_bank=(

            selected_document == "MORTGAGE"

        )

    )


# =========================================================
# SUCCESSION — SUCCESSOR-WISE LAND DETAILS
# =========================================================
def render_successor_land(successor_number):
    """Render land details directly under one successor and return total guntas."""
    land_key = f"successor_{successor_number}"
    successor_lands = data.setdefault("successor_lands", {})
    allocations = successor_lands.setdefault(land_key, [])

    with st.container(border=True):
        st.markdown(f"#### 🌾 LAND DETAILS — SUCCESSOR {successor_number}")

        top_left, top_right = st.columns([3, 1])
        with top_left:
            if st.button("➕ ADD SURVEY", key=f"{sheet}_{land_key}_add_land", use_container_width=True):
                collect_data()
                existing_ids = [item.get("id", 0) for item in allocations]
                new_id = max(existing_ids) + 1 if existing_ids else 1
                allocations.append({"id": new_id, "survey_number": "", "extent": "", "north": "", "south": "", "east": "", "west": ""})
                save_database()
                st.rerun()
        with top_right:
            st.caption("Add land for this successor")

        total_guntas = 0
        for allocation in allocations.copy():
            allocation_id = allocation.get("id")
            with st.container(border=True):
                survey_col, extent_col, delete_col = st.columns([1.5, 1.1, 0.45])
                with survey_col:
                    st.text_input("Survey No.", value=allocation.get("survey_number", ""), key=f"{sheet}_{land_key}_land_{allocation_id}_survey_number")
                with extent_col:
                    allocation_extent = st.text_input("Extent", value=allocation.get("extent", ""), placeholder="1.1500", key=f"{sheet}_{land_key}_land_{allocation_id}_extent")
                with delete_col:
                    st.caption("Delete")
                    if st.button("🗑️", key=f"{sheet}_{land_key}_delete_land_{allocation_id}", use_container_width=True):
                        collect_data()
                        successor_lands[land_key] = [item for item in allocations if item.get("id") != allocation_id]
                        save_database()
                        st.rerun()

                north_col, south_col, east_col, west_col = st.columns(4)
                with north_col:
                    st.text_input("North", value=allocation.get("north", ""), key=f"{sheet}_{land_key}_land_{allocation_id}_north")
                with south_col:
                    st.text_input("South", value=allocation.get("south", ""), key=f"{sheet}_{land_key}_land_{allocation_id}_south")
                with east_col:
                    st.text_input("East", value=allocation.get("east", ""), key=f"{sheet}_{land_key}_land_{allocation_id}_east")
                with west_col:
                    st.text_input("West", value=allocation.get("west", ""), key=f"{sheet}_{land_key}_land_{allocation_id}_west")

                cleaned_extent = clean_extent(allocation_extent)
                converted_extent = extent_guntas(cleaned_extent)
                if allocation_extent and converted_extent is None:
                    st.error("Invalid extent. Example: 1.1500 (guntas 00–39).")
                elif converted_extent is not None:
                    total_guntas += converted_extent

        total_acres = total_guntas // 40
        remaining_guntas = total_guntas % 40
        total_extent = f"{total_acres}.{remaining_guntas:02d}00"
        total_col, _ = st.columns([1.2, 2.8])
        total_widget_key = f"{sheet}_{land_key}_total_extent"
        # This is a calculated field, so refresh its widget value on every rerun.
        # Otherwise Streamlit keeps the old disabled value (often 0.0000).
        st.session_state[total_widget_key] = total_extent
        with total_col:
            st.text_input("TOTAL EXTENT", value=total_extent, disabled=True, key=total_widget_key)

    return total_guntas


# =========================================================
# SUCCESSION — ADDITIONAL SUCCESSORS + LINKED LAND
# =========================================================
def delete_successor(successor_number, successor_count):
    delete_prefix = f"{sheet}_successor_{successor_number}_"
    for key in list(st.session_state.keys()):
        if key.startswith(delete_prefix):
            del st.session_state[key]

    for current_number in range(successor_number + 1, successor_count + 1):
        old_prefix = f"{sheet}_successor_{current_number}_"
        new_prefix = f"{sheet}_successor_{current_number - 1}_"
        for key in list(st.session_state.keys()):
            if key.startswith(old_prefix):
                st.session_state[new_prefix + key[len(old_prefix):]] = st.session_state.pop(key)

    for key in list(data.keys()):
        if key.startswith(f"successor_{successor_number}_"):
            del data[key]

    for current_number in range(successor_number + 1, successor_count + 1):
        old_prefix = f"successor_{current_number}_"
        new_prefix = f"successor_{current_number - 1}_"
        for key in list(data.keys()):
            if key.startswith(old_prefix):
                data[new_prefix + key[len(old_prefix):]] = data.pop(key)

    successor_lands = data.setdefault("successor_lands", {})
    successor_lands.pop(f"successor_{successor_number}", None)
    for current_number in range(successor_number + 1, successor_count + 1):
        old_land_key = f"successor_{current_number}"
        new_land_key = f"successor_{current_number - 1}"
        if old_land_key in successor_lands:
            successor_lands[new_land_key] = successor_lands.pop(old_land_key)

    new_count = max(1, successor_count - 1)
    st.session_state[f"{sheet}_successor_count"] = new_count
    data["successor_count"] = new_count


if selected_document == "SUCCESSION":
    successor_count = st.session_state.get(f"{sheet}_successor_count", 1)
    all_successor_total_guntas = 0

    # Successor 1 is the main right-side person. Its land stays directly with the succession section.
    all_successor_total_guntas += render_successor_land(1)

    # Additional successors are compact: two successor cards per row.
    successor_numbers = list(range(2, successor_count + 1))
    for row_start in range(0, len(successor_numbers), 2):
        row_numbers = successor_numbers[row_start:row_start + 2]
        row_columns = st.columns(len(row_numbers), gap="small")
        for successor_number, successor_column in zip(row_numbers, row_columns):
            with successor_column:
                with st.container(border=True):
                    title_col, delete_col = st.columns([5, 1])
                    with title_col:
                        st.markdown(
                            f"<div style='font-size:0.95rem;font-weight:750;margin:0 0 0.15rem 0;'>SUCCESSOR {successor_number}</div>",
                            unsafe_allow_html=True
                        )
                    with delete_col:
                        if st.button("🗑️", key=f"{sheet}_delete_successor_{successor_number}", help="Delete successor and linked land"):
                            delete_successor(successor_number, successor_count)
                            st.rerun()
                    person_form(f"successor_{successor_number}", "SUCCESSOR", ppb_optional=True)
                    all_successor_total_guntas += render_successor_land(successor_number)

    add_col, _ = st.columns([0.9, 3.1], gap="small")
    with add_col:
        if st.button("➕ ADD SUCCESSOR", key=f"{sheet}_add_successor", use_container_width=False):
            st.session_state[f"{sheet}_successor_count"] += 1
            st.rerun()

    all_acres = all_successor_total_guntas // 40
    all_remaining_guntas = all_successor_total_guntas % 40
    all_successors_extent = f"{all_acres}.{all_remaining_guntas:02d}00"
    st.markdown("#### 🌾 TOTAL EXTENT — ALL SUCCESSORS")
    total_all_col, _ = st.columns([0.9, 3.1], gap="small")
    all_total_widget_key = f"{sheet}_all_successors_total_extent"
    st.session_state[all_total_widget_key] = all_successors_extent
    with total_all_col:
        st.text_input("TOTAL EXTENT", value=all_successors_extent, disabled=True, key=all_total_widget_key)
st.divider()


# =========================================================
# LAND AND PAYMENT SPLIT VIEW
# =========================================================

if selected_document == "SUCCESSION":
    payment_column = st.container()
else:
    land_column, payment_column = st.columns(2, gap="medium")


# =========================================================
# LAND DETAILS
# =========================================================

if selected_document != "SUCCESSION":
    with land_column:

        st.markdown(

            """

            <div class="section-title land-details-title">

            🌾 LAND DETAILS

            </div>

            """,

            unsafe_allow_html=True

        )


        if st.button(

            "➕ ADD NEW SURVEY NO.",

            use_container_width=True,

            key=(

                f"{sheet}_"

                "add_survey"

            )

        ):

            collect_data()


            existing_ids = [

                survey["id"]

                for survey in

                data["surveys"]

            ]


            new_id = (

                max(
                    existing_ids
                )
                +
                1

                if existing_ids

                else 1

            )


            data["surveys"].append(

                {

                    "id": new_id,

                    "survey_number": "",

                    "extent": "",

                    "north": "",

                    "south": "",

                    "east": "",

                    "west": ""

                }

            )


            save_database()


            st.rerun()


        live_total_guntas = 0

        invalid_extent = False


        for survey in (
            data["surveys"].copy()
        ):

            survey_id = (
                survey["id"]
            )


            with st.container(
                border=True
            ):

                survey_column, extent_column, delete_column = (

                    st.columns(

                        [

                            2,

                            1.4,

                            0.6

                        ]

                    )

                )


                with survey_column:

                    st.text_input(

                        "Survey No.",

                        value=(

                            survey.get(

                                "survey_number",

                                ""

                            )

                        ),

                        key=(

                            f"{sheet}_"

                            f"survey_"

                            f"{survey_id}_"

                            "survey_number"

                        )

                    )


                with extent_column:

                    extent_value = (

                        st.text_input(

                            "Extent",

                            value=(

                                survey.get(

                                    "extent",

                                    ""

                                )

                            ),

                            placeholder=(

                                "Example: 1.1500"

                            ),

                            max_chars=20,

                            key=(

                                f"{sheet}_"

                                f"survey_"

                                f"{survey_id}_"

                                "extent"

                            )

                        )

                    )


                with delete_column:

                    st.caption(
                        "DELETE"
                    )


                    if st.button(

                        "🗑️",

                        key=(

                            f"{sheet}_"

                            f"delete_survey_"

                            f"{survey_id}"

                        ),

                        use_container_width=True

                    ):

                        collect_data()


                        data["surveys"] = [

                            item

                            for item in

                            data["surveys"]

                            if item["id"]

                            != survey_id

                        ]


                        save_database()


                        st.rerun()


                north_column, south_column = (

                    st.columns(2)

                )


                with north_column:

                    st.text_input(

                        "North",

                        value=(

                            survey.get(

                                "north",

                                ""

                            )

                        ),

                        key=(

                            f"{sheet}_"

                            f"survey_"

                            f"{survey_id}_"

                            "north"

                        )

                    )


                with south_column:

                    st.text_input(

                        "South",

                        value=(

                            survey.get(

                                "south",

                                ""

                            )

                        ),

                        key=(

                            f"{sheet}_"

                            f"survey_"

                            f"{survey_id}_"

                            "south"

                        )

                    )


                east_column, west_column = (

                    st.columns(2)

                )


                with east_column:

                    st.text_input(

                        "East",

                        value=(

                            survey.get(

                                "east",

                                ""

                            )

                        ),

                        key=(

                            f"{sheet}_"

                            f"survey_"

                            f"{survey_id}_"

                            "east"

                        )

                    )


                with west_column:

                    st.text_input(

                        "West",

                        value=(

                            survey.get(

                                "west",

                                ""

                            )

                        ),

                        key=(

                            f"{sheet}_"

                            f"survey_"

                            f"{survey_id}_"

                            "west"

                        )

                    )


                cleaned_live_extent = (

                    clean_extent(

                        extent_value

                    )

                )


                if (
                    extent_value

                    !=

                    cleaned_live_extent
                ):

                    st.warning(

                        "Extent allows numbers, "

                        "one decimal point and "

                        "a maximum of four digits "

                        "after the decimal."

                    )


                converted_extent = (

                    extent_guntas(

                        cleaned_live_extent

                    )

                )


                if converted_extent is None:

                    invalid_extent = True


                    st.error(

                        "Invalid extent. Use a "

                        "format such as 1.1500. "

                        "The first two digits "

                        "after the decimal are "

                        "guntas and must be "

                        "between 00 and 39."

                    )


                else:

                    live_total_guntas += (

                        converted_extent

                    )


        total_acres = (

            live_total_guntas

            // 40

        )


        remaining_guntas = (

            live_total_guntas

            % 40

        )


        live_total_extent = (

            f"{total_acres}."

            f"{remaining_guntas:02d}"

            "00"

        )

    total_extent_box = st.container(border=True)

    with total_extent_box:
        st.markdown("#### TOTAL EXTENT")

        st.markdown(
            f"## {live_total_extent}"
        )


# =========================================================
# PAYMENT DETAILS
# =========================================================

with payment_column:

    st.markdown(

        """

        <div class="section-title payment-details-title">

        💰 PAYMENT DETAILS

        </div>

        """,

        unsafe_allow_html=True

    )


    challan_amount = (

        st.number_input(

            "Challan Rs.",

            min_value=0.0,

            value=float(

                data.get(

                    "challan_amount",

                    0

                )

            ),

            step=100.0,

            key=(

                f"{sheet}_"

                "challan_amount"

            )

        )

    )


    if st.button(

        "➕ ADD ANOTHER PAYMENT",

        use_container_width=False,

        key=(

            f"{sheet}_"

            "add_payment"

        )

    ):

        collect_data()


        existing_payment_ids = [

            payment["id"]

            for payment in

            data["payments"]

        ]


        new_payment_id = (

            max(
                existing_payment_ids
            )
            +
            1

            if existing_payment_ids

            else 1

        )


        data["payments"].append(

            {

                "id":
                new_payment_id,

                "amount":
                0.0

            }

        )


        save_database()


        st.rerun()


    payment_values = []


    for payment in (
        data["payments"].copy()
    ):

        payment_id = (
            payment["id"]
        )


        amount_column, delete_column = (

            st.columns(

                [

                    4,

                    1

                ]

            )

        )


        with amount_column:

            amount = (

                st.number_input(

                    f"Amount Paid "
                    f"{payment_id}",

                    min_value=0.0,

                    value=float(

                        payment.get(

                            "amount",

                            0

                        )

                    ),

                    step=100.0,

                    key=(

                        f"{sheet}_"

                        f"payment_"

                        f"{payment_id}"

                    )

                )

            )


        with delete_column:

            st.caption(
                "DELETE"
            )


            if st.button(

                "🗑️",

                key=(

                    f"{sheet}_"

                    f"delete_payment_"

                    f"{payment_id}"

                ),

                use_container_width=True

            ):

                collect_data()


                data["payments"] = [

                    item

                    for item in

                    data["payments"]

                    if item["id"]

                    != payment_id

                ]


                save_database()


                st.rerun()


        payment_values.append(
            amount
        )


    total_paid = sum(
        payment_values
    )


    total_column, balance_column = (

        st.columns(2)

    )


    with total_column:

        st.number_input(

            "Total Amount Paid",

            value=float(
                total_paid
            ),

            disabled=True,

            key=(

                f"{sheet}_"

                "total_paid_display"

            )

        )


    with balance_column:

        balance = (

            challan_amount

            -

            total_paid

        )


        st.number_input(

            "Balance Amount",

            value=float(
                balance
            ),

            disabled=True,

            key=(

                f"{sheet}_"

                "balance_display"

            )

        )


    date_slot_column, status_column = (

        st.columns(2)

    )


    with date_slot_column:

        st.date_input(

            "Date of Slot Booked",

            value=(

                safe_date(

                    data.get(

                        "slot_date",

                        str(

                            date.today()

                        )

                    )

                )

            ),

            key=(

                f"{sheet}_"

                "slot_date"

            )

        )


    status_options = [

        "STATUS PENDING",

        "REG. COMPLETED"

    ]


    saved_status = (

        data.get(

            "booking_status",

            "STATUS PENDING"

        )

    )


    if saved_status not in (
        status_options
    ):

        saved_status = (
            "STATUS PENDING"
        )


    with status_column:

        st.selectbox(

            "Booking Status",

            status_options,

            index=(

                status_options.index(

                    saved_status

                )

            ),

            key=(

                f"{sheet}_"

                "booking_status"

            )

        )


    st.text_area(

        "Notes",

        value=(

            data.get(

                "notes",

                ""

            )

        ),

        height=70,

        key=(

            f"{sheet}_"

            "notes"

        )

    )


st.divider()


# =========================================================
# FINAL ACTIONS
# =========================================================

st.markdown(
    '<div class="section-title">💾 SAVE & DOCUMENT ACTIONS</div>',
    unsafe_allow_html=True
)

# =========================================================
# SAVE FILE
# =========================================================

if st.button(

    "💾 SAVE FILE",

    type="primary",

    use_container_width=True,

    key=(

        f"{sheet}_"

        "save_file"

    )

):

    collect_data()


    data = (

        st.session_state.database[

            sheet

        ]

    )


    calculated_extent, invalid = (

        total_extent(

            data["surveys"]

        )

    )


    if invalid:

        st.error(

            "The file was not saved. "

            "Correct the invalid "

            "extent first."

        )


    else:

        data["saved"] = True


        save_database()


        pdf_bytes = (

            create_pdf(

                sheet,

                data

            )

        )


        pdf_path = (

            os.path.join(

                PDF_FOLDER,

                f"{sheet}.pdf"

            )

        )


        with open(

            pdf_path,

            "wb"

        ) as pdf_file:

            pdf_file.write(

                pdf_bytes

            )


        st.session_state[

            "saved_pdf"

        ] = pdf_bytes


        st.session_state[

            "saved_sheet"

        ] = sheet


        st.session_state[

            "show_saved_options"

        ] = True


        st.success(

            f"{sheet} saved successfully."

        )


# =========================================================
# PDF, PRINT AND NEXT SHEET
# =========================================================

if st.session_state.get(

    "show_saved_options",

    False

):

    saved_sheet = (

        st.session_state.get(

            "saved_sheet",

            ""

        )

    )


    saved_pdf = (

        st.session_state.get(

            "saved_pdf",

            b""

        )

    )


    download_column, print_column, next_column = (

        st.columns(3)

    )


    with download_column:

        st.download_button(

            "📄 DOWNLOAD PDF",

            data=saved_pdf,

            file_name=(

                f"{saved_sheet}.pdf"

            ),

            mime=(

                "application/pdf"

            ),

            use_container_width=True

        )


    with print_column:

        st.download_button(

            "🖨️ DOWNLOAD PDF FOR PRINTING",

            data=saved_pdf,

            file_name=f"{saved_sheet}_PRINT.pdf",

            mime="application/pdf",

            use_container_width=True

        )


    with next_column:

        # Open the next empty sheet in a completely separate browser tab.
        # The current saved sheet and its session data are left untouched.
        st.markdown(
            """
            <a href="./?new_sheet=1"
               target="_blank"
               rel="noopener noreferrer"
               style="
                    display:block;
                    width:100%;
                    box-sizing:border-box;
                    text-align:center;
                    padding:0.62rem 0.8rem;
                    border-radius:0.55rem;
                    text-decoration:none;
                    font-weight:700;
                    background:#2563eb;
                    color:white;
                    border:1px solid rgba(255,255,255,0.15);
                ">
                ➡️ OPEN NEXT EMPTY SHEET ↗
            </a>
            """,
            unsafe_allow_html=True
        )