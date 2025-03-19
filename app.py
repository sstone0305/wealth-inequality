import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import os

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for deployment

# Define the CSV file path
DATA_FILE = "user_data.csv"

# 📌 Load existing data from CSV on startup
if os.path.exists(DATA_FILE):
    user_data = pd.read_csv(DATA_FILE)
    user_data.columns = user_data.columns.str.strip()  # Remove accidental spaces from column names
    if user_data.empty or not all(col in user_data.columns for col in ["Age", "Income", "Racial_Broad", "Racial_Specific", "Gender", "Continent", "Country"]):
        user_data = pd.DataFrame(columns=["Age", "Income", "Racial_Broad", "Racial_Specific", "Gender", "Continent", "Country"])
else:
    user_data = pd.DataFrame(columns=["Age", "Income", "Racial_Broad", "Racial_Specific", "Gender", "Continent", "Country"])


# Persistent dataset to store user submissions
user_data = pd.DataFrame(columns=["Age", "Income", "Racial_Broad", "Racial_Specific", "Gender", "Continent", "Country"])

# Full list of 195 countries categorized by continent
country_list = {
    "North America": ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", 
                      "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", 
                      "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", 
                      "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"],
    
    "South America": ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", 
                      "Peru", "Suriname", "Uruguay", "Venezuela"],
    
    "Europe": ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina",
               "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia",
               "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Latvia", "Liechtenstein",
               "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
               "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia",
               "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City"],
    
    "Asia": ["Afghanistan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "India", "Indonesia",
             "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia",
             "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines",
             "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand",
             "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"],
    
    "Africa": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
               "Central African Republic", "Chad", "Comoros", "Democratic Republic of the Congo", "Djibouti",
               "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
               "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
               "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Republic of the Congo",
               "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
               "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
    
    "Oceania": ["Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau",
                "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]
}


# Hardcoded racial categories with specific racial identities
racial_categories = {
    "White": ["German", "Irish", "Italian", "French", "Polish", "British", "Dutch", "Russian", "Greek", "Hungarian",
              "Norwegian", "Swedish", "Finnish", "Danish", "Portuguese", "Spanish", "Austrian", "Swiss", "Czech",
              "Slovak", "Lithuanian", "Latvian", "Estonian", "Belarusian", "Ukrainian", "Other White"],
    "Black": ["Nigerian", "Ethiopian", "Ghanaian", "Jamaican", "Haitian", "South African", "Somali", "Afro-Latino",
              "African American", "Kenyan", "Sudanese", "Congolese", "Zimbabwean", "Rwandan", "Tanzanian",
              "Senegalese", "Malian", "Cameroonian", "Other Black"],
    "Asian": ["Chinese", "Indian", "Filipino", "Vietnamese", "Korean", "Japanese", "Pakistani", "Bangladeshi", "Thai",
              "Indonesian", "Malaysian", "Sri Lankan", "Nepalese", "Mongolian", "Burmese", "Kazakh", "Uzbek", "Tajik",
              "Turkmen", "Kyrgyz", "Maldivian", "Bhutanese", "Other Asian"],
    "Latino": ["Mexican", "Puerto Rican", "Cuban", "Dominican", "Colombian", "Argentinian", "Peruvian", "Chilean",
               "Venezuelan", "Ecuadorian", "Bolivian", "Paraguayan", "Uruguayan", "Salvadoran", "Honduran", "Guatemalan",
               "Costa Rican", "Panamanian", "Nicaraguan", "Brazilian", "Other Latino"],
    "Indigenous": ["Native American", "First Nations (Canada)", "Mayan", "Quechua", "Aymara", "Guarani", "Mapuche",
                   "Inuit", "Apache", "Navajo", "Cherokee", "Sioux", "Chickasaw", "Iroquois", "Zuni", "Seminole",
                   "Ojibwe", "Tlingit", "Other Indigenous"],
    "Other": ["Middle Eastern", "North African", "Mixed", "Pacific Islander", "Jewish", "Other"]
}

# 📌 Default Dropdown Choices
default_continents = list(country_list.keys())
default_genders = ["Male", "Female", "Other"]
default_races = list(racial_categories.keys())

# Layout
app.layout = html.Div([
    html.H1("Income & Demographics Explorer"),

    # 📌 Data Storage
    dcc.Store(id="stored-data", data=user_data.to_dict("records")),

    # 📌 User Input Section
    html.H3("Submit Your Data"),
    
    html.Label("Select Broad Racial Identity:"),
    dcc.Dropdown(id="racial_broad", options=[{"label": k, "value": k} for k in default_races], clearable=True),

    html.Label("Select Specific Racial Identity:"),
    dcc.Dropdown(id="racial_specific", clearable=True),

    html.Label("Select Continent:"),
    dcc.Dropdown(id="continent", options=[{"label": k, "value": k} for k in default_continents], clearable=True),

    html.Label("Select Country:"),
    dcc.Dropdown(id="country", clearable=True),

    html.Label("Select Gender:"),
    dcc.Dropdown(id="gender", options=[{"label": g, "value": g} for g in default_genders], clearable=True),

    html.Label("Enter Age:"),
    dcc.Input(id="age", type="number", min=18, max=80, step=1),

    html.Label("Enter Income ($):"),
    dcc.Input(id="income", type="number", min=0, max=1000000000, step=1000),

    html.Button("Submit Data", id="submit", n_clicks=0),

    # 📌 Default Worldwide Graph
    html.H3("🌍 Global Income Distribution"),
    dcc.Graph(id="global_scatterplot"),

    # 📌 Filters Section
    html.H3("🎯 Filter Data Below to Generate a Custom Graph"),
    
    html.Label("Filter by Continent:"),
    dcc.Dropdown(id="filter_continent", options=[{"label": k, "value": k} for k in default_continents], clearable=True),

    html.Label("Filter by Country:"),
    dcc.Dropdown(id="filter_country", clearable=True),

    html.Label("Filter by Broad Race:"),
    dcc.Dropdown(id="filter_race_broad", options=[{"label": k, "value": k} for k in default_races], clearable=True),

    html.Label("Filter by Specific Race:"),
    dcc.Dropdown(id="filter_race_specific", clearable=True),

    html.Label("Filter by Gender:"),
    dcc.Dropdown(id="filter_gender", options=[{"label": g, "value": g} for g in default_genders], clearable=True),

    html.Label("Filter by Age Range:"),
    dcc.RangeSlider(id="filter_age", min=18, max=80, step=1, value=[18, 80], marks={18: "18", 80: "80"}),

    html.Button("Apply Filters", id="filter_button", n_clicks=0),

    # 📌 Filtered Graph
    html.H3("Filtered Income Distribution"),
    dcc.Graph(id="filtered_scatterplot"),
])

# Callbacks for dependent dropdowns
@app.callback(
    Output("country", "options"),
    Input("continent", "value")
)
def update_country_options(selected_continent):
    return [{"label": c, "value": c} for c in country_list.get(selected_continent, [])]

@app.callback(
    Output("racial_specific", "options"),
    Input("racial_broad", "value")
)
def update_racial_specific_options(selected_race):
    return [{"label": r, "value": r} for r in racial_categories.get(selected_race, [])]

# Store User Data
@app.callback(
    Output("stored-data", "data"),
    Input("submit", "n_clicks"),
    State("stored-data", "data"),
    State("age", "value"),
    State("income", "value"),
    State("racial_broad", "value"),
    State("racial_specific", "value"),
    State("gender", "value"),
    State("continent", "value"),
    State("country", "value"),
    prevent_initial_call=True
)
def store_user_data(n_clicks, stored_data, age, income, racial_broad, racial_specific, gender, continent, country):
    if not all([age, income, racial_broad, racial_specific, gender, continent, country]):
        return dash.no_update  # Prevent errors if fields are missing
    
    # Convert stored_data back into DataFrame
    df = pd.DataFrame(stored_data) if stored_data else pd.DataFrame(columns=["Age", "Income", "Racial_Broad", "Racial_Specific", "Gender", "Continent", "Country"])
    
    # Add new entry
    new_entry = pd.DataFrame([{
        "Age": age, "Income": income, "Racial_Broad": racial_broad, 
        "Racial_Specific": racial_specific, "Gender": gender,
        "Continent": continent, "Country": country
    }])

    # Append new data to DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save to CSV
    df.to_csv(DATA_FILE, index=False)

    # Return updated data to Dash
    return df.to_dict("records")

# Update Scatterplots
@app.callback(
    Output("global_scatterplot", "figure"),
    Input("stored-data", "data")
)
def update_global_scatterplot(stored_data):
    if not stored_data:
        return px.scatter(title="Income Distribution (No Data Yet)")

    # Convert stored_data (dict) back into a DataFrame
    df = pd.DataFrame(stored_data)

    # Debugging: Print available columns
    print("Columns in DataFrame:", df.columns)

    # Check if 'Age' exists before applying numeric conversion
    if "Age" in df.columns and "Income" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
        df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
    else:
        print("⚠️ Warning: 'Age' or 'Income' not found in dataset.")

    if df.empty or "Age" not in df.columns or "Income" not in df.columns:
        return px.scatter(title="Income Distribution (No Data Yet)")

    return px.scatter(
        df, x="Age", y="Income", color="Racial_Broad",
        title="🌍 Global Income Distribution",
        labels={"Age": "Age", "Income": "Income ($)", "Racial_Broad": "Broad Race Category"},
        hover_data=["Racial_Specific", "Gender", "Continent", "Country"]
    )

if __name__ == "__main__":
    app.run(debug=True)