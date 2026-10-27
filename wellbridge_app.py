# WellBridge — deployable Gradio app
# Do not put API keys directly in this file. Configure OPENAI_API_KEY
# through your hosting provider's private environment-variable settings.

import os
from datetime import date, datetime

import gradio as gr
import requests
import folium
from openai import OpenAI

_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=_api_key) if _api_key else None

import gradio as gr
from datetime import date, datetime

# WellBridge visual theme


wellbridge_theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="slate",
    neutral_hue="slate",
    font=["Arial", "Helvetica", "sans-serif"]
).set(
    body_background_fill="#F5F7F4",
    block_background_fill="#FFFFFF",
    block_border_color="#E1E7E0",
    block_radius="12px",
    button_primary_background_fill="#2F6045",
    button_primary_background_fill_hover="#244D38",
    button_primary_text_color="#FFFFFF"
)



wellbridge_css = """
/* Overall page */
.gradio-container,
.gradio-container .main {
    background: #F7FAF7 !important;
    color: #254B38 !important;
}

/* Headings */
.gradio-container h1,
.gradio-container h2,
.gradio-container h3 {
    color: #254B38 !important;
}

/* Form labels: remove bright green backgrounds */
.gradio-container label,
.gradio-container label span,
.gradio-container [data-testid="block-label"] {
    background: transparent !important;
    color: #718B76 !important;
    border: none !important;
    box-shadow: none !important;
}

/* Dropdown and date-picker outer containers */
.gradio-container [data-testid="dropdown"],
.gradio-container [data-testid="datepicker"],
.gradio-container .wrap:has(input),
.gradio-container .input-container {
    background: #FFFFFF !important;
    border-color: #D5E3D6 !important;
    box-shadow: none !important;
}

/* Dropdown selection field */
.gradio-container [role="combobox"],
.gradio-container [role="listbox"],
.gradio-container input,
.gradio-container textarea {
    background: #FFFFFF !important;
    color: #254B38 !important;
    border-color: #D5E3D6 !important;
    box-shadow: none !important;
}

/* Calendar button and other form buttons */
.gradio-container button:not([role="tab"]):not(.primary) {
    background: #EDF5ED !important;
    color: #356B50 !important;
    border-color: #D5E3D6 !important;
}

/* Table headings and cells */
.gradio-container th {
    background: #E7F0E6 !important;
    color: #355C43 !important;
    border-color: #D5E3D6 !important;
}

.gradio-container td {
    background: #FFFFFF !important;
    color: #254B38 !important;
    border-color: #E1EAE1 !important;
}

/* Tabs */
.gradio-container button[role="tab"] {
    color: #254B38 !important;
    background: #EDF5ED !important;
    border-color: #D5E3D6 !important;
}

.gradio-container button[role="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    background: #477A59 !important;
}

/* Primary action buttons */
.gradio-container button.primary {
    background: #477A59 !important;
    color: #FFFFFF !important;
}

/* Placeholder text */
.gradio-container input::placeholder,
.gradio-container textarea::placeholder {
    color: #9AA99B !important;
    opacity: 1 !important;
}

/* Footer */
footer {
    display: none !important;
}


/* Fix dark backgrounds surrounding form components */
.gradio-container [data-testid="block"],
.gradio-container [data-testid="form"],
.gradio-container .form,
.gradio-container .wrap,
.gradio-container .container {
    background-color: #FFFFFF !important;
    border-color: #E1EAE1 !important;
    box-shadow: none !important;
}

/* Keep the overall page a very light sage */
.gradio-container,
.gradio-container .main,
.gradio-container .contain {
    background-color: #F7FAF7 !important;
}

/* Make the WellBridge introduction readable */
.gradio-container .prose,
.gradio-container .prose p,
.gradio-container .prose h1,
.gradio-container .prose h2,
.gradio-container .prose h3 {
    color: #254B38 !important;
}

/* Softer sage labels without bright green boxes */
.gradio-container label span,
.gradio-container [data-testid="block-label"] {
    background-color: transparent !important;
    color: #718B76 !important;
    border: none !important;
    box-shadow: none !important;
}
#care-search-results,
#care-search-results .prose,
#care-search-results .prose p,
#care-search-results .prose h2,
#care-search-results .prose h3,
#care-search-results .prose li,
#care-search-results .prose strong {
    color: #24352A !important;
    background-color: transparent !important;
}

#care-search-results .prose {
    opacity: 1 !important;
}

/* Preventive Care Education text colors */
.gradio-container .prose,
.gradio-container .prose p,
.gradio-container .prose li,
.gradio-container .prose strong,
.gradio-container .prose em {
    color: #254B38 !important;
}

.gradio-container .prose ul,
.gradio-container .prose ol {
    color: #254B38 !important;
}


/* Fix visibility of checkbox selection indicators */
.gradio-container input[type="checkbox"] {
    appearance: auto !important;
    -webkit-appearance: auto !important;
    opacity: 1 !important;
    visibility: visible !important;
    position: static !important;
    width: 16px !important;
    height: 16px !important;
    accent-color: #2F6045 !important;
    cursor: pointer !important;
}


/* Clean, consistent form styling */
.gradio-container input,
.gradio-container textarea,
.gradio-container select {
    background-color: #ffffff !important;
    color: #263b35 !important;
    border-color: #d5e1da !important;
}

/* Softer labels */
.gradio-container label {
    color: #42574d !important;
}

/* Cleaner tables */
.gradio-container table {
    background-color: #ffffff !important;
    color: #263b35 !important;
    border-color: #e0e8e2 !important;
}

/* Subtle borders and rounded controls */
.gradio-container input,
.gradio-container textarea,
.gradio-container select {
    border-radius: 8px !important;
}
"""

tasks = []
next_id = 1


def get_task_rows():
    return [
        [
            task["ID"],
            task.get("Name", ""),
            task["Type of care"],
            task["Due date"],
            task["Notes"],
            task["Status"]
        ]
        for task in tasks
    ]


def get_dashboard():
    total = len(tasks)
    completed = sum(t["Status"] == "Completed" for t in tasks)

    upcoming = sum(
        t["Status"] == "Upcoming"
        and bool(t["Due date"])
        and t["Due date"] >= date.today().isoformat()
        for t in tasks
    )

    overdue = sum(
        t["Status"] == "Upcoming"
        and bool(t["Due date"])
        and t["Due date"] < date.today().isoformat()
        for t in tasks
    )

    progress = round(completed / total * 100) if total else 0

    upcoming_tasks = [
        t for t in tasks
        if t["Status"] == "Upcoming"
    ]
    upcoming_tasks.sort(key=lambda t: t["Due date"])

    if upcoming_tasks:
        upcoming_text = "\n".join(
            f"- **{t['Type of care']}** — {t['Due date']}"
            for t in upcoming_tasks[:5]
        )
    else:
        upcoming_text = "No upcoming tasks yet. Add one in My Care Tracker!"

    summary = f"""
## Your Health Overview

| Metric | Count |
|---|---:|
| Total tasks | {total} |
| Upcoming tasks | {upcoming} |
| Overdue tasks | {overdue} |
| Completed tasks | {completed} |

### Completion progress: {progress}%

{progress_bar(progress)}

### Upcoming Care

{upcoming_text}
"""
    return summary

def answer_guide(question):
    if not question or not question.strip():
        return "Please enter a question so I can help."
    if client is None:
        return "The AI guide is not configured yet. Please try again later."

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions="""
            You are WellBridge Guide, a friendly assistant for a
            preventive-care and healthcare-resource app.

            Help users with:
            - Preventive care and routine checkups
            - Vaccination questions
            - Dental health
            - Preparing for medical appointments
            - Understanding healthcare costs and insurance
            - Finding affordable healthcare resources
            - Navigating the WellBridge app

            Provide clear, supportive, easy-to-understand information.

            Important safety rules:
            - Provide general health education, not diagnoses.
            - Do not prescribe medication or recommend changing
              prescribed treatment.
            - Explain when users should consult a qualified
              healthcare professional.
            - For potentially life-threatening symptoms, advise
              contacting emergency services immediately.
            - Never claim to know a user's medical history.
            - Do not invent clinic locations, phone numbers,
              costs, eligibility, or opening hours.
            - Remind users to verify healthcare information
              with qualified professionals when appropriate.
            - Do not request unnecessary sensitive health data.
            """,
            input=question
        )

        return response.output_text

    except Exception as e:
            print("WellBridge AI error:", repr(e))
            return f"Error: {type(e).__name__}: {e}"

def progress_bar(percent):
    filled = round(percent / 10)
    return f"`{'█' * filled}{'░' * (10 - filled)}` {percent}%"


def refresh_views(message):
    return get_task_rows(), get_dashboard(), message


def add_task(family_name, care_type, due_date, notes):
    global next_id



    if not family_name or not family_name.strip():
        return (
            get_task_rows(),
            get_dashboard(),
            "Please enter a name."
        )

    family_name = family_name.strip()

    if isinstance(due_date, (datetime, date)):
        due_date = due_date.date().isoformat() if isinstance(
            due_date, datetime
        ) else due_date.isoformat()
    else:
        due_date = str(due_date)[:10]

    tasks.append({
        "ID": next_id,
        "Name": family_name,
        "Type of care": care_type,
        "Due date": due_date,
        "Notes": notes.strip() if notes else "None",
        "Status": "Upcoming"
    })
    next_id += 1

    return refresh_views(
        f"Task for {family_name} added successfully!"
    )


def complete_task(task_id):
    if not task_id or not str(task_id).strip().isdigit():
        return get_task_rows(), get_dashboard(), "Enter a valid task ID."

    chosen_id = int(task_id)

    for task in tasks:
        if task["ID"] == chosen_id:
            if task["Status"] == "Completed":
                return get_task_rows(), get_dashboard(), "Already completed."

            task["Status"] = "Completed"
            return refresh_views(f"Task {chosen_id} marked completed!")

    return get_task_rows(), get_dashboard(), "Task ID not found."


def clear_tasks():
    global next_id
    tasks.clear()
    next_id = 1
    return get_task_rows(), get_dashboard(), "Demo tasks cleared."


def search_care(location, service):
    import requests

    city = location.strip() if location and location.strip() else ""

    if not city:
        return (
            "## Find care\nPlease enter a city to search.",
            "<p>Enter a city to display healthcare facilities on the map.</p>"
        )

    city_sql = city.replace("'", "''")

    headers = {"User-Agent": "WellBridge/1.0"}

    results = f"## Healthcare facilities near {city}\n\n"
    facilities = []
    source_used = None

    # Primary source: broader CDPHE health-facilities dataset
    new_url = (
        "https://services3.arcgis.com/66aUo8zsujfVXRIT/"
        "arcgis/rest/services/CDPHE_Health_Facilities/"
        "FeatureServer/0/query"
    )

    new_params = {
        "where": f"Address_Full LIKE '%{city_sql}%'",
        "outFields": (
            "Facility_Name,Address_Full,Operating_Status,"
            "CDPHE_HFEMS_Licensed,Date_Data_Updated"
        ),
"returnGeometry": "true",
"outSR": 4326,
"resultRecordCount": 100,
"f": "json"
    }

    try:
        response = requests.get(
            new_url, params=new_params, headers=headers, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise ValueError("CDPHE query failed")

        facilities = data.get("features", [])
        source_used = "CDPHE"

    except (requests.RequestException, ValueError, TypeError):
        facilities = []

    # Fallback: original community health center dataset
    if not facilities:
        old_url = (
            "https://www.cohealthmaps.dphe.state.co.us/arcgis/rest/"
            "services/OPEN_DATA/"
            "cdphe_cdhs_fqhc_mental_health_facilities/"
            "MapServer/1/query"
        )

        old_params = {
            "where": (
                f"City LIKE '%{city_sql}%' AND State = 'CO' "
                "AND Type_ = 'Clinic Site'"
            ),
            "outFields": (
                "Site_Name,Address,City,State,Zip_Code,Phone,Type_"
            ),
"returnGeometry": "true",
"outSR": 4326,
            "f": "json"
        }

        try:
            response = requests.get(
                old_url, params=old_params, headers=headers, timeout=20
            )
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                raise ValueError("Original dataset query failed")

            facilities = data.get("features", [])
            source_used = "Original Colorado directory"

        except (requests.RequestException, ValueError, TypeError):
            results += (
                "We couldn't retrieve healthcare records right now. "
                "Please try again later.\n\n"
                "[Search the HRSA Health Center Finder]"
                "(https://findahealthcenter.hrsa.gov/)"
            )


    print("Facilities found:", len(facilities))

    if facilities:
        results += f"**Source:** {source_used}\n\n"

        for item in facilities:
            details = item.get("attributes", {})

            name = (
                details.get("Facility_Name")
                or details.get("Site_Name")
                or "Healthcare facility"
            )

            address = (
                details.get("Address_Full")
                or details.get("Address")
                or "Address unavailable"
            )

            phone = details.get("Phone") or "Not listed"
            status = details.get("Operating_Status") or "Not listed"

            results += (
                f"### {name}\n"
                f"- **Address:** {address}\n"
                f"- **Phone:** {phone}\n"
                f"- **Operating status:** {status}\n\n"
            )
    else:
        results += (
            "No matching facilities were found. Try another city or use "
            "[the HRSA Health Center Finder](https://findahealthcenter.hrsa.gov/)."
        )

    map_html = create_care_map(facilities, city)
    return results, map_html


def create_care_map(facilities, city):
    import folium

    # Default map center: Colorado
    map_center = [39.5501, -105.7821]
    care_map = folium.Map(
        location=map_center,
        zoom_start=7,
        tiles="OpenStreetMap"
    )

    locations_added = 0
    print("Facilities passed to map:", len(facilities))


    for item in facilities:
        geometry = item.get("geometry")
        if not geometry:
            continue

        latitude = geometry.get("y")
        longitude = geometry.get("x")

        if latitude is None or longitude is None:
            continue

        details = item.get("attributes", {})

        name = (
            details.get("Facility_Name")
            or details.get("Site_Name")
            or "Healthcare facility"
        )

        address = (
            details.get("Address_Full")
            or details.get("Address")
            or "Address unavailable"
        )

        phone = details.get("Phone") or "Not listed"
        status = details.get("Operating_Status") or "Not listed"
        license_info = (
            details.get("CDPHE_HFEMS_Licensed")
            or "Not listed"
        )

        popup_html = f"""
        <div style="width: 230px; font-family: Arial, sans-serif;">
            <h4>{name}</h4>
            <p><b>Address:</b> {address}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Operating status:</b> {status}</p>
            <p><b>License information:</b> {license_info}</p>
        </div>
        """

        folium.Marker(
            location=[latitude, longitude],
            tooltip=name,
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="green", icon="plus-sign")
        ).add_to(care_map)

        locations_added += 1


    print("Map markers added:", locations_added, "out of", len(facilities))

    if locations_added == 0:
        return (
            "<p>No map coordinates were available for these results. "
            "Try another city or consult the facility directory.</p>"
        )

    return care_map._repr_html_()


    if service and service != "All services":
        results += (
            f"**Selected service:** {service}\n\n"
            "The directory doesn't reliably identify every service "
            "offered by each facility, so results have not been "
            "filtered by service.\n\n"
        )

    if not facilities:
        return (
            results
            + "No matching records were found in these datasets. "
            "This doesn't mean the city has no healthcare facilities.\n\n"
            "[Search the HRSA Health Center Finder]"
            "(https://findahealthcenter.hrsa.gov/)"
        )

    results += f"*Source: {source_used}*\n\n"

    for item in facilities[:10]:
        details = item.get("attributes", {})

        if source_used == "CDPHE":
            name = details.get("Facility_Name") or "Name unavailable"
            address = details.get("Address_Full") or "Address unavailable"
            status = details.get("Operating_Status")
            licensed = details.get("CDPHE_HFEMS_Licensed")
            updated = details.get("Date_Data_Updated")

            results += f"### {name}\n\n"
            results += f"**Address:** {address}\n\n"

            if status:
                results += f"**Operating status:** {status}\n\n"

            if licensed is not None:
                results += f"**License record:** {licensed}\n\n"

            if updated:
                results += f"**Data updated:** {updated}\n\n"

        else:
            name = details.get("Site_Name") or "Name unavailable"
            address = details.get("Address") or "Address unavailable"
            clinic_city = details.get("City") or city
            state = details.get("State") or "CO"
            zip_code = details.get("Zip_Code") or ""
            phone = details.get("Phone") or "Phone unavailable"

            results += (
                f"### {name}\n\n"
                f"**Address:** {address}, {clinic_city}, "
                f"{state} {zip_code}\n\n"
                f"**Phone:** {phone}\n\n"
            )

        results += "---\n\n"

    results += (
        "**Before visiting:** Verify the facility's current operating "
        "status, services, hours, costs, and contact details. "
        "A license record alone doesn't guarantee a facility is open.\n\n"
        "[Find additional health centers through HRSA]"
        "(https://findahealthcenter.hrsa.gov/)"
    )

    return results

def add_planner_topics(selected_topics, due_date):
    global next_id

    if not selected_topics:
        return (
            "Select at least one topic first.",
            get_task_rows(),
            get_dashboard()
        )

    topic_mapping = {
        "Routine physical or wellness visit": "Annual physical",
        "Vaccination questions": "Vaccination",
        "Dental checkup": "Dental checkup",
        "Vision checkup": "Other",
        "Sleep and daily habits": "Other",
        "Mental well-being": "Other",
        "Preventive screenings and family health history": "Preventive screening",
        "Questions about healthcare costs or access": "Other"
    }

    added_count = 0

    for topic in selected_topics:
        tasks.append({
            "ID": next_id,
            "Type of care": topic_mapping.get(topic, "Other"),
            "Due date": due_date or "",
            "Notes": f"Added from Preventive Care Planner: {topic}",
            "Status": "Upcoming"
        })
        next_id += 1
        added_count += 1

    return (
        f"Added {added_count} topic(s) to My Care Tracker. "
        "You can set due dates in your tracker.",
        get_task_rows(),
        get_dashboard()
    )




with gr.Blocks(
    title="WellBridge",
    theme=wellbridge_theme,
    css=wellbridge_css
) as app:
    gr.Markdown("#  WellBridge")
    gr.Markdown("### Preventive Care, Connected.")
    gr.Markdown(
        "Your health. Your community. Your future."
    )

    with gr.Tab("Dashboard"):
        dashboard = gr.Markdown(get_dashboard())

    with gr.Tab("My Care"):
        gr.Markdown("## Add a preventive-care task")

        family_name = gr.Textbox(
          label= "Name",
          placeholder= "Enter family members name"
    )
        care_type = gr.Dropdown(
            choices=[
                "Vaccination",
                "Dental checkup",
                "Annual physical",
                "Preventive screening",
                "Other"
            ],
            label="Type of care",
            value="Vaccination"
        )

        due_date = gr.DateTime(
            label="Due date",
            include_time=False,
            type="string"
        )

        notes = gr.Textbox(
            label="Notes (optional)",
            placeholder="Example: Find a nearby clinic"
        )

        add_button = gr.Button("Add to My Care List", variant="primary")
        message = gr.Textbox(label="Message", interactive=False)

        task_table = gr.Dataframe(
            headers=["ID", "Name", "Type of care", "Due date", "Notes", "Status"],
            datatype=["number", "str", "str", "str", "str", "str"],
            value=get_task_rows(),
            interactive=False
        )

        add_button.click(
            fn=add_task,
            inputs=[family_name, care_type, due_date, notes],
            outputs=[task_table, dashboard, message]
        )

        gr.Markdown("## Mark a task completed")

        task_id = gr.Textbox(
            label="Task ID",
            placeholder="Enter the ID from the first column"
        )

        complete_button = gr.Button("Mark as completed")
        complete_message = gr.Textbox(
            label="Update message",
            interactive=False
        )

        complete_button.click(
            fn=complete_task,
            inputs=task_id,
            outputs=[task_table, dashboard, complete_message]
        )


        gr.Markdown("""
        ---
        ## Plan Your Preventive Care

        Select topics you'd like to discuss with a healthcare
        professional, then add them to your My Care list.
        """)

        planner_topics = gr.CheckboxGroup(
            choices=[
                "Routine physical or wellness visit",
                "Vaccination questions",
                "Dental checkup",
                "Vision checkup",
                "Sleep and daily habits",
                "Mental well-being",
                "Preventive screenings and family health history",
                "Questions about healthcare costs or access"
            ],
            label="Topics to review"
        )
        planner_due_date = gr.DateTime(
            label="Due Date (optional)",
            include_time=False,
            type="string"
        )

        add_to_tracker_button = gr.Button(
            "Add Selected Topics to My Care",
            variant="primary"
        )

        tracker_message = gr.Markdown()

        add_to_tracker_button.click(
            fn=add_planner_topics,
            inputs=[planner_topics, planner_due_date],
            outputs=[tracker_message, task_table, dashboard]
        )




    with gr.Tab("Find Affordable Care"):
        gr.Markdown(
            "## Find healthcare resources\n"
            "Search for care by Colorado city and service type."
        )

        with gr.Row():
            location_search = gr.Textbox(
                label="City",
                placeholder="Example: Denver or Thornton"
            )

            service_search = gr.Dropdown(
                choices=[
                    "All services",
                    "Primary care",
                    "Vaccinations",
                    "Dental care"
                ],
                value="All services",
                label="Type of service"
            )
        search_button = gr.Button(
            "Find Care",
            variant="primary"
        )


        search_results = gr.Markdown(
            "Enter a city or choose a service, then select Find Care.",
            elem_id="care-search-results",
            elem_classes=["care-results"]
        )

        care_map = gr.HTML(
            value=(
                "<div style='padding:24px; text-align:center; "
                "border:1px solid #dce5df; border-radius:12px;'>"
                "<h3>Explore Healthcare Facilities</h3>"
                "<p>Search for a city to view facility locations on the map.</p>"
                "</div>"
            ),
            label="Healthcare facility map"
        )

        search_button.click(
            fn=search_care,
            inputs=[location_search, service_search],
            outputs=[search_results, care_map]
        )



        with gr.Accordion("About these data sources", open=False):
            gr.Markdown("""
            **Where WellBridge gets its information**

            - **Colorado clinic records:** Colorado Department of Public Health and Environment public mapping data.
            - **Health center directory:** [HRSA Find a Health Center](https://findahealthcenter.hrsa.gov/).

            **Please note:** Public listings may be outdated or incomplete.
            Contact a healthcare facility to confirm its services, hours,
            eligibility requirements, and costs before visiting.

            WellBridge is an educational prototype, not a medical service.
            """)


        gr.Markdown("""
        ---

        ### Need help finding affordable care?

        - **Community health centers:** Ask about services and
          fees based on your income.
        - **Local public health departments:** Check for vaccination
          services and other community health programs.
        - **Low-cost dental programs:** Ask about reduced-cost
          appointments or community dental clinics.
        - **Health insurance assistance:** Ask a qualified enrollment
          assister about coverage options.

        **Helpful tip:** Before visiting, contact the organization
        to confirm services, eligibility, costs, and appointment
        availability.
        """)


        gr.Markdown(
            "*Resources are provided for informational purposes. "
            "Contact each organization to confirm services, eligibility, "
            "availability, and costs.*"
        )

    with gr.Tab("Learn & Get Help"):
        gr.Markdown("""
        ## Preventive Care Education

        Learn how routine care, early detection, and reliable health
        information can support long-term health. This section provides
        general education, not personalized medical advice.



        ---

        ### 1. Vaccinations

        Vaccines help the immune system recognize certain infections and
        reduce the risk of serious illness. Recommended vaccines can vary
        based on age, medical history, previous vaccinations, and other
        factors.

        **What you can do:**
        - Keep a record of vaccinations you have received.
        - Ask a healthcare professional which vaccines are recommended
          for you.
        - Check with your healthcare provider or local public health
          department if you need help accessing vaccination services.

        ---

        ### 2. Routine Checkups and Physicals

        Routine checkups give healthcare professionals an opportunity
        to review general health, discuss concerns, and identify
        preventive care that may be appropriate.

        **What you can do:**
        - Ask how often routine visits are recommended for your age.
        - Prepare questions or concerns before an appointment.
        - Ask about recommended screenings and follow-up care.
        - Keep track of appointments and any next steps.

        ---

        ### 3. Dental Health

        Oral health is an important part of overall health. Regular
        dental visits can help identify cavities, gum problems, and
        other concerns before they become more difficult to manage.

        **What you can do:**
        - Brush twice a day with fluoride toothpaste.
        - Clean between your teeth daily.
        - Ask a dental professional how often you should receive
          checkups based on your needs.
        - Ask about lower-cost dental services if cost is a barrier.

        ---

        ### 4. Preventive Screenings

        Screening tests can help identify certain health conditions
        before symptoms appear. The appropriate screenings depend on
        factors such as age, personal history, and individual risk.

        **What you can do:**
        - Ask a healthcare professional which screenings are
          appropriate for you.
        - Find out what a recommended screening involves.
        - Ask when you should follow up about results.

        Not every screening is recommended for every person.
        A healthcare professional can help explain the benefits,
        limitations, and appropriate timing.

        ---

        ### 5. Finding Affordable Healthcare

        Cost, transportation, insurance, and appointment availability
        can make healthcare difficult to access. Asking for assistance
        is a useful first step.

        **Places to explore:**
        - Community health centers that offer services based on income.
        - Local public health departments.
        - Community dental clinics and other low-cost care programs.
        - Healthcare organizations with financial assistance programs.

        Eligibility and services vary, so contact each organization
        to confirm what it offers.

        ---

        ### 6. Preparing for an Appointment

        Preparing questions ahead of time can help you make better
        use of an appointment.

        **Before your visit:**
        - Write down questions you want to ask.
        - Bring any information the clinic requests.
        - Ask the provider to explain unfamiliar medical terms.
        - Before leaving, make sure you understand the next steps
          and how to follow up.

        ---

        ### 7. Evaluating Health Information

        Online health information can be helpful, but not every source
        is reliable.

        **Look for information from:**
        - Government public health agencies.
        - Hospitals and established healthcare organizations.
        - Recognized medical and public health institutions.

        Check when information was published and whether it cites
        credible evidence. Discuss personal medical questions with
        a qualified healthcare professional.

        ---

        ### Why Preventive Care Matters

        Preventive care can support early identification of health
        concerns, help people understand their health, and provide
        opportunities to discuss risk reduction with healthcare
        professionals. Access to these services is not equal for
        everyone, which makes accessible education and community
        outreach important.

        **WellBridge's goal:** Help people organize preventive care,
        learn about their options, and explore healthcare resources.

        *Educational information only. WellBridge does not diagnose
        conditions or replace advice from a qualified healthcare
        professional.*
        """)


        gr.Markdown("""
        ---

        ## Insurance & Costs

        Understanding healthcare costs can help you prepare before
        scheduling an appointment. Coverage and out-of-pocket costs
        depend on your insurance plan, provider, and service.

        ### Common Insurance Terms

        **Premium:** The amount you pay to maintain your insurance,
        often monthly.

        **Deductible:** The amount you pay for covered services before
        your plan begins paying for certain costs.

        **Copay:** A fixed amount you may pay for a covered service.

        **Coinsurance:** The percentage of a covered cost you pay after
        meeting your deductible, when applicable.

        **Out-of-pocket maximum:** The limit on what you pay for covered,
        in-network services during a plan year. Premiums and some other
        expenses generally do not count toward this limit.

        ---

        ### Before You Schedule Care

        - Ask the clinic whether it accepts your insurance plan.
        - Contact your insurer to confirm coverage for the specific service.
        - Ask the clinic about the estimated cost if you pay out of pocket.
        - Ask whether financial assistance or sliding-scale fees are available.
        - Check whether referrals or prior authorization are required.

        **Important:** A clinic accepting your insurance does not guarantee
        that every service is covered or that the clinic is in-network for
        your specific plan. Confirm details with both the insurer and clinic.

        *This information is educational. Actual coverage and costs vary
        by plan and individual circumstances.*
        """)





        gr.Markdown("""
        <div style="height: 40px;"></div>
)

        ## Meet WellBridge Guide

        Your friendly guide to preventive care and healthcare resources.

        Ask a general question about preventive care, preparing for
        an appointment, or using WellBridge. This demo provides
        educational guidance, not medical diagnoses.
        """)

        guide_question = gr.Textbox(
            label="What would you like help with?",
            placeholder="Example: How can I prepare for a checkup?",
            lines=3
        )

        guide_button = gr.Button(
            "Get Guidance",
            variant="primary"
        )



        guide_response = gr.Markdown(
            "Your guidance will appear here."
        )

        guide_button.click(
            fn=answer_guide,
            inputs=guide_question,
            outputs=guide_response

        )

    with gr.Tab("Community Impact"):
        gr.Markdown("""
        ## Community Impact
        ### Inspired by The Health Access Initiative

        Healthcare access should not depend on where you live
        or what resources you have

        The Health Access Initiative is a student-led outreach initiative
        focused on improving healthcare access for underserved communities,
        locally and globally.

        Through education, community outreach, and service, we can help
        make reliable health information and resources easier to access.

        ---

        *Donation requirements and volunteer opportunities should be
        confirmed directly with the organizations involved.*
        """)


        gr.Markdown("### Find a Way to Make an Impact")

        impact_type = gr.Dropdown(
            choices=[
                "First-aid supply drive",
                "Community care packages",
                "Health education",
                "Healthcare volunteering"
            ],
            value="First-aid supply drive",
            label="What are you interested in?"
        )

        impact_button = gr.Button(
            "Explore This Opportunity",
            variant="primary"
        )

        impact_result = gr.Markdown(
            "Choose an option to see suggested next steps."
        )

        def suggest_impact(activity):
            suggestions = {
                "First-aid supply drive": """
                **Start a supply drive**

                1. Get approval from your school or organization.
                2. Confirm which unopened supplies a recipient accepts.
                3. Set collection dates and explain what can be donated.
                4. Arrange delivery with the receiving organization.
                """,
                "Community care packages": """
                **Organize care packages**

                1. Partner with a community nonprofit.
                2. Ask what items recipients need.
                3. Follow its packaging and safety guidelines.
                4. Coordinate a confirmed donation or distribution.
                """,
                "Health education": """
                **Share reliable health information**

                1. Choose a preventive-care topic.
                2. Use trusted public health sources.
                3. Create an accessible flyer or presentation.
                4. Have an appropriate organization review it.
                """,
                "Healthcare volunteering": """
                **Explore volunteering**

                1. Research established hospitals and nonprofits.
                2. Check age requirements and application procedures.
                3. Ask about orientation and supervision.
                4. Confirm the role and schedule with the organization.
                """
            }

            return suggestions.get(
                activity,
                "Please select an opportunity above."
            )

        impact_button.click(
            fn=suggest_impact,
            inputs=impact_type,
            outputs=impact_result
        )







gr.Markdown(
    "**Privacy & Safety:** WellBridge is an educational prototype. "
    "Tasks are temporary and may not persist after the app session ends. "
    "Do not enter sensitive personal or medical information. "
    "WellBridge does not provide diagnoses or replace professional "
    "medical advice."
)

app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", "7860")))

