import streamlit as st
from datetime import date
import json
import os
import re
import copy
import html
import base64
from io import BytesIO

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
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .deed-title {
        text-align: center;
        font-size: 27px;
        font-weight: 800;
        margin-top: 2px;
        margin-bottom: 8px;
    }

    .section-title {
        text-align: center;
        font-size: 21px;
        font-weight: 750;
        margin-top: 4px;
        margin-bottom: 6px;
    }

    .family-title {
        text-align: center;
        font-size: 17px;
        font-weight: 700;
        margin-top: 7px;
        margin-bottom: 4px;
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

        "first_aadhaar": "[Aadhaar Redacted]",

        "first_name": "",

        "first_relation": "S/o",

        "first_relation_name": "",

        "first_age": 0,

        "first_death_date": "",

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

        "first_family_aadhaar": "[Aadhaar Redacted]",

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

        "second_aadhaar": "[Aadhaar Redacted]",

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

        "second_family_aadhaar": "[Aadhaar Redacted]",

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
# CURRENT SHEET
# =========================================================

if "current_sheet" not in (
    st.session_state
):

    st.session_state.current_sheet = (
        next_sheet()
    )


if (
    st.session_state.current_sheet

    not in

    st.session_state.database
):

    st.session_state.database[
        st.session_state.current_sheet
    ] = empty_file()


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

        "first_death_date",

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

                "Auth. Address",

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

st.markdown(

    """

    <div class="app-title">

    📁 BHU BHARATHI LAND FILES

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

        )

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

                if st.button(

                    "📂 OPEN",

                    key=(

                        f"open_"

                        f"{result}"

                    ),

                    use_container_width=True

                ):

                    open_sheet(
                        result
                    )

                    st.rerun()


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

    is_bank=False,

    is_succession=False

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

                "Bank House No.",

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

                "H.No.",

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


    # Succession specific fields in order: PPB, Aadhaar, Name, Relation, Relation Name, Age, Death Date
    if is_succession and prefix == "first":
        st.text_input(
            "PPB No.",
            value=data.get(f"{prefix}_ppb", ""),
            key=f"{sheet}_{prefix}_ppb"
        )
    
    # Aadhaar, Name, Relation for everyone
    aadhaar_col, name_col = st.columns(2)
    with aadhaar_col:
        st.text_input(
            "Aadhaar No.",
            value=data.get(f"{prefix}_aadhaar", ""),
            max_chars=12,
            key=f"{sheet}_{prefix}_aadhaar"
        )
    with name_col:
        st.text_input(
            f"{person_title.title()} Name",
            value=data.get(f"{prefix}_name", ""),
            key=f"{sheet}_{prefix}_name"
        )

    relation_options = ["S/o", "D/o", "W/o"]
    saved_relation = data.get(f"{prefix}_relation", "S/o")
    if saved_relation not in relation_options: saved_relation = "S/o"

    rel_col, rel_name_col = st.columns([1, 2])
    with rel_col:
        st.selectbox(
            "S/D/W/o",
            relation_options,
            index=relation_options.index(saved_relation),
            key=f"{sheet}_{prefix}_relation"
        )
    with rel_name_col:
        st.text_input(
            "Father / Mother / Spouse",
            value=data.get(f"{prefix}_relation_name", ""),
            key=f"{sheet}_{prefix}_relation_name"
        )

    # Age and Death Date for succession
    if is_succession and prefix == "first":
        age_col, death_col = st.columns(2)
        with age_col:
            st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=int(data.get(f"{prefix}_age", 0)),
                key=f"{sheet}_{prefix}_age"
            )
        with death_col:
            st.text_input(
                "Date of Death",
                value=data.get(f"{prefix}_death_date", ""),
                placeholder="DD-MM-YYYY",
                key=f"{sheet}_{prefix}_death_date"
            )
    else:
        st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=int(data.get(f"{prefix}_age", 0)),
            key=f"{sheet}_{prefix}_age"
        )


    # =====================================================
    # BUYER / DONEE GENDER & CASTE DROPDOWN
    # =====================================================
    if show_caste_gender:

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


        saved_gender = (

            data.get(

                f"{prefix}_gender",

                "SELECT GENDER"

            )

        )


        saved_caste = (

            data.get(

                f"{prefix}_caste",

                "SELECT CASTE"

            )

        )


        if saved_gender not in gender_options:

            saved_gender = "SELECT GENDER"


        if saved_caste not in caste_options:

            saved_caste = "SELECT CASTE"


        gender_col, caste_col = st.columns(2)


        with gender_col:

            st.selectbox(

                f"{person_title} GENDER",

                gender_options,

                index=(

                    gender_options.index(

                        saved_gender

                    )

                ),

                key=(

                    f"{sheet}_"

                    f"{prefix}_gender"

                )

            )


        with caste_col:

            st.selectbox(

                f"{person_title} CASTE",

                caste_options,

                index=(

                    caste_options.index(

                        saved_caste

                    )

                ),

                key=(

                    f"{sheet}_"

                    f"{prefix}_caste"

                )

            )


    house_column, location_column = (

        st.columns(2)

    )


    with house_column:

        st.text_input(

            "H.No.",

            value=(

                data.get(

                    f"{prefix}_house",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_house"

            )

        )


    with location_column:

        st.text_input(

            "Location",

            value=(

                data.get(

                    f"{prefix}_location",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_location"

            )

        )


    state_column, district_column = (

        st.columns(2)

    )


    with state_column:

        st.text_input(

            "State",

            value=(

                data.get(

                    f"{prefix}_state",

                    "Telangana"

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_state"

            )

        )


    with district_column:

        st.text_input(

            "District",

            value=(

                data.get(

                    f"{prefix}_district",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_district"

            )

        )


    mandal_column, village_column = (

        st.columns(2)

    )


    with mandal_column:

        st.text_input(

            "Mandal",

            value=(

                data.get(

                    f"{prefix}_mandal",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_mandal"

            )

        )


    with village_column:

        st.text_input(

            "Village",

            value=(

                data.get(

                    f"{prefix}_village",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_village"

            )

        )


    pin_column, cell_column = (

        st.columns(2)

    )


    with pin_column:

        st.text_input(

            "PIN No.",

            value=(

                data.get(

                    f"{prefix}_pin",

                    ""

                )

            ),

            max_chars=6,

            key=(

                f"{sheet}_"

                f"{prefix}_pin"

            )

        )


    with cell_column:

        st.text_input(

            "Cell No.",

            value=(

                data.get(

                    f"{prefix}_cell",

                    ""

                )

            ),

            max_chars=10,

            key=(

                f"{sheet}_"

                f"{prefix}_cell"

            )

        )


    # =====================================================
    # FAMILY MEMBER
    # =====================================================

    st.markdown(

        f"""

        <div class="family-title">

        {person_title} FAMILY MEMBER

        </div>

        """,

        unsafe_allow_html=True

    )


    family_options = [

        "SELECT RELATION",

        "FATHER",

        "MOTHER",

        "SON",

        "DAUGHTER",

        "WIFE",

        "HUSBAND",

        "OTHERS"

    ]


    family_saved = (

        data.get(

            f"{prefix}_family_relation",

            "SELECT RELATION"

        )

    )


    if family_saved not in (
        family_options
    ):

        family_saved = (
            "SELECT RELATION"
        )


    family_relation = (

        st.selectbox(

            "Family Relation",

            family_options,

            index=(

                family_options.index(

                    family_saved

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_family_relation"

            )

        )

    )


    if family_relation != (
        "SELECT RELATION"
    ):

        if family_relation == (
            "OTHERS"
        ):

            st.text_input(

                "Enter Relation",

                value=(

                    data.get(

                        f"{prefix}_family_other",

                        ""

                    )

                ),

                key=(

                    f"{sheet}_"

                    f"{prefix}_family_other"

                )

            )


        st.text_input(

            "Family Member Name",

            value=(

                data.get(

                    f"{prefix}_family_name",

                    ""

                )

            ),

            key=(

                f"{sheet}_"

                f"{prefix}_family_name"

            )

        )


        current_year = (
            date.today().year
        )


        birth_column, age_column = (

            st.columns(2)

        )


        with birth_column:

            birth_year = (

                st.number_input(

                    "Birth Year",

                    min_value=0,

                    max_value=(
                        current_year
                    ),

                    value=int(

                        data.get(

                            f"{prefix}_family_birth_year",

                            0

                        )

                    ),

                    key=(

                        f"{sheet}_"

                        f"{prefix}_family_birth_year"

                    )

                )

            )


        with age_column:

            if birth_year > 0:

                calculated_age = (

                    current_year

                    -

                    birth_year

                )


                st.number_input(

                    "Age",

                    value=(

                        calculated_age

                    ),

                    disabled=True,

                    key=(

                        f"{sheet}_"

                        f"{prefix}_auto_age"

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

        first_title,
        is_succession=(selected_document == "SUCCESSION")

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


st.divider()


# =========================================================
# LAND AND PAYMENT SPLIT VIEW
# =========================================================

land_column, payment_column = (

    st.columns(

        2,

        gap="medium"

    )

)


# =========================================================
# LAND DETAILS
# =========================================================

with land_column:

    st.markdown(

        """

        <div class="section-title">

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


    st.text_input(

        "TOTAL EXTENT",

        value=(

            live_total_extent

        ),

        disabled=True,

        key=(

            f"{sheet}_"

            "total_extent_display"

        )

    )


# =========================================================
# PAYMENT DETAILS
# =========================================================

with payment_column:

    st.markdown(

        """

        <div class="section-title">

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

        use_container_width=True,

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

        encoded_pdf = (

            base64.b64encode(

                saved_pdf

            ).decode(

                "utf-8"

            )

        )


        st.markdown(

            f"""

            <a

            href="data:application/pdf;base64,{encoded_pdf}"

            target="_blank"

            style="

            display:block;

            border:1px solid #888;

            border-radius:8px;

            padding:0.55rem;

            text-align:center;

            text-decoration:none;

            font-weight:700;

            ">

            🖨️ OPEN PDF TO PRINT

            </a>

            """,

            unsafe_allow_html=True

        )


    with next_column:

        if st.button(

            "➡️ OPEN NEXT EMPTY SHEET",

            type="primary",

            use_container_width=True

        ):

            old_sheet = (

                st.session_state.current_sheet

            )


            clear_widgets(
                old_sheet
            )


            new_sheet = (
                next_sheet()
            )


            st.session_state.database[

                new_sheet

            ] = empty_file()


            save_database()


            st.session_state.current_sheet = (

                new_sheet

            )


            st.session_state[

                "show_saved_options"

            ] = False


            st.session_state[

                "main_search"

            ] = ""


            st.rerun()