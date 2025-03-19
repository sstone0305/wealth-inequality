import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for deployment

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

# Layout
app.layout = html.Div([
    html.H1("Income & Demographics Explorer"),

     # 📌 Wealth Inequality Section
    html.H3("Understanding Wealth Inequality"),
    html.Div([
        html.P(
            "Wealth inequality refers to the uneven distribution of financial assets, income, and opportunities across "
            "different groups in society. While some level of economic disparity is natural, extreme wealth inequality "
            "has profound implications for social mobility, economic stability, and political influence."
        ),
        html.P(
            "Wealth inequality arises from multiple factors, including income disparities, generational wealth, access to "
            "financial markets, and differences in education quality. The richest 1% of the world owns nearly half of global wealth, "
            "while the bottom 50% collectively own less than 2%. Countries with high levels of inequality often experience lower "
            "social mobility, making it difficult for individuals from lower-income backgrounds to improve their economic standing."
        ),
        html.P(
            "The consequences of extreme wealth inequality include reduced economic growth, increased social unrest, and disproportionate "
            "political influence by the wealthy. Policies such as progressive taxation, universal basic income, and investments in education "
            "and healthcare have been proposed as ways to reduce these disparities."
        ),
        html.P(
            "For further reading, refer to\n"
            "Piketty, T. (2014). 'Capital in the Twenty-First Century.' Harvard University Press\n"
            "Stiglitz, J. (2012). 'The Price of Inequality.' W.W. Norton & Company\n" 
            "Credit Suisse Global Wealth Report (2022)."
        ),
    ], style={"margin-bottom": "30px"}),

    # User Input Section
    html.H3("Submit Your Data"),
    dcc.Store(id="stored-data", data=user_data.to_dict("records")),  

    html.Label("Select Broad Racial Identity:"),
    dcc.Dropdown(id="racial_broad", options=[{"label": k, "value": k} for k in racial_categories.keys()], clearable=True),

    html.Label("Select Specific Racial Identity:"),
    dcc.Dropdown(id="racial_specific", clearable=True),

    html.Label("Select Continent:"),
    dcc.Dropdown(id="continent", options=[{"label": k, "value": k} for k in country_list.keys()], clearable=True),

    html.Label("Select Country:"),
    dcc.Dropdown(id="country", clearable=True),

    html.Label("Select Gender:"),
    dcc.Dropdown(id="gender", options=[{"label": g, "value": g} for g in ["Male", "Female", "Other"]], clearable=True),

    html.Label("Enter Age:"),
    dcc.Input(id="age", type="number", min=18, max=80, step=1),

    html.Label("Enter Income ($):"),
    dcc.Input(id="income", type="number", min=0, max=1000000000, step=1000),

    html.Button("Submit Data", id="submit", n_clicks=0),

    # Income Scatterplot
    html.H3("Income Distribution"),
    dcc.Graph(id="scatterplot"),
])

# Callbacks for dropdown updates
@app.callback(
    Output("country", "options"),
    Input("continent", "value")
)
def update_country_options(selected_continent):
    return [{"label": c, "value": c} for c in country_list[selected_continent]] if selected_continent else []

# Callback to update specific racial identities based on the selected broad race
@app.callback(
    Output("racial_specific", "options"),
    Input("racial_broad", "value")
)
def update_racial_specific_options(selected_race):
    if selected_race and selected_race in racial_categories:
        return [{"label": r, "value": r} for r in racial_categories[selected_race]]
    return []

# Store user data
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
)
def store_user_data(n_clicks, stored_data, age, income, racial_broad, racial_specific, gender, continent, country):
    if n_clicks > 0 and all([age, income, racial_broad, racial_specific, gender, continent, country]):
        stored_data.append({
            "Age": age, "Income": income, "Racial_Broad": racial_broad, "Racial_Specific": racial_specific,
            "Gender": gender, "Continent": continent, "Country": country
        })
    return stored_data


# Scatterplot (Income Distribution)
@app.callback(
    Output("scatterplot", "figure"),
    Input("stored-data", "data")
)
def update_scatterplot(stored_data):
    df = pd.DataFrame(stored_data)
    if df.empty:
        return px.scatter(title="Income Distribution (No Data Yet)")
    return px.scatter(df, x="Age", y="Income", color="Racial_Broad", title="Income Distribution")

if __name__ == "__main__":
    app.run(debug=True)


