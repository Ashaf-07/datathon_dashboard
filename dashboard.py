# This is our full dashboard script. Save this as 'dashboard.py'
import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import warnings

# --- 0. Ignore "noise" warnings ---
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- 1. Load Our Pre-Prepared Data "Snippets" ---
# This makes our app incredibly fast and memory-safe
try:
    df_bar = pd.read_csv('viz_data_bar_chart.csv')
    df_structural_top10 = pd.read_csv('viz_data_structural_top10.csv')
    df_resource_top10 = pd.read_csv('viz_data_resource_top10.csv')
    df_scatter = pd.read_csv('viz_data_scatter.csv')
    df_donut = pd.read_csv('viz_data_donut.csv')
except FileNotFoundError as e:
    print(f"--- ERROR: A data snippet is missing! ---")
    print(f"Did you run the 'FINAL PREP' cell (Cell 23) first?")
    print(f"Missing file: {e}")
    exit()

# --- 2. Create the Figures (Our Visualizations) ---

# --- Figure 1: The "Driver" Bar Chart (Slide 4) ---
# This is our "Problem Decomposition" and "Don't Waste Money" chart
fig_bar_chart = px.bar(
    df_bar, 
    x='Problem', 
    y='Importance (%)', 
    title='Figure 1: Root Drivers of the G8-to-G9 Bottleneck',
    text='Importance (%)',
    color='Problem',
    color_discrete_map={ # Color-code our findings
        '1. Structural Failure': '#1f77b4',
        '2. Resource Failure': '#ff7f0e',
        '3. Unexplained "Chaos"': '#7f7f7f',
        '4. General Infrastructure': '#d62728'
    }
)
fig_bar_chart.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
fig_bar_chart.update_layout(
    yaxis_title="Problem Importance (out of 100%)",
    showlegend=False
)

# --- Figure 2: The "Red Zone" Scatter Plot (Slide 3) ---
# This is our "Heuristic Model" justification
fig_scatter = px.scatter(
    df_scatter, 
    x='ptr_2024', 
    y='sqcr_2024', 
    # Color the dots based on their "Red Zone" status
    color=df_scatter['is_red_zone_2024'].map({1: 'Red Zone (194k Schools)', 0: 'OK (1.2M Schools)'}),
    title='Figure 2: Identifying "Red Zone" Schools (100k Sample)',
    labels={'ptr_2024': 'Pupil-Teacher Ratio (PTR)', 'sqcr_2024': 'Student-per-Quality-Classroom (SQCR)'}
)
# Add our "Frank Judge-approved" threshold lines
fig_scatter.add_vline(x=48.50, line_dash="dash", line_color="red", annotation_text="PTR = 48.5")
fig_scatter.add_hline(y=57.00, line_dash="dash", line_color="red", annotation_text="SQCR = 57.0")

# --- Figure 3: The "79% Validation" Donut Chart (Slide 3) ---
# This is our "Killer" 79% validation
fig_donut = px.pie(
    df_donut, 
    names='Failure Type', 
    values='Count', 
    title='Figure 3: 79% of "Red Zone" Schools are CHRONIC Failures',
    hole=0.4 # This makes it a donut chart
)
fig_donut.update_traces(textinfo='percent+label', pull=[0.05, 0]) # Pull out the "Chronic" slice

# --- 3. Build the App Layout (Our 6-Slide Story) ---
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server # This line is needed for deployment

# This is our "single page" website
app.layout = html.Div(className='container', style={'maxWidth': '1200px'}, children=[
    
    # --- SLIDE 1: EXECUTIVE SUMMARY ---
    html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '5px'}, children=[
        html.H1("Datathon: Solving India's 'Education Bottleneck'"),
        html.H3("A Two-Problem, Two-Solution Framework"),
        html.Hr(),
        html.P("Our analysis of the G8-to-G9 (Upper Primary to Secondary) transition proves this is not one problem, but two distinct, solvable problems. We present a data-driven, granular, and validated 5-year plan."),
        html.P("This dashboard walks you through our findings, from the core drivers to our final, costed policy recommendations.")
    ]),
    
    # --- SLIDE 4: THE "WHY" ---
    html.Div(style={'marginTop': '30px'}, children=[
        html.H2("Our Core Finding: What *Really* Drives the Bottleneck?"),
        html.P("Our models proved that for this *specific* G8-to-G9 problem, 'Structural' and 'Resource' failures are the dominant drivers. General infrastructure, while important, is not the bottleneck. Our two interventions address a combined, data-proven 79.4% of the *entire* policy-addressable problem."),
        dcc.Graph(figure=fig_bar_chart)
    ]),
    html.Hr(),

    # --- SLIDE 2: STRUCTURAL FIX ---
    html.Div(style={'marginTop': '30px'}, children=[
        html.H2("Problem 1: The 'Structural' Failure (434,013 Schools)"),
        html.P("Over 50% of relevant schools have a 0.0 transition rate. This is a 'forced exit' by design. The solution is a 'Vertical Integration Program' to add Grades 9 and 10 to these schools."),
        html.H4("Top 10 Priority Districts for Structural Intervention:"),
        dash_table.DataTable(
            data=df_structural_top10.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_structural_top10.columns],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_data_conditional=[{ # Make the numbers stand out
                'if': {'column_type': 'numeric'},
                'fontWeight': 'bold'
            }]
        )
    ]),
    html.Hr(),

    # --- SLIDE 3: RESOURCE FIX ---
    html.Div(style={'marginTop': '30px'}, children=[
        html.H2("Problem 2: The 'Resource' Failure (194,066 Schools)"),
        html.P("These are 'Red Zone' schools defined by a high Pupil-Teacher Ratio (>48.5) and high Overcrowding (>57.0). This is not a guess; it's a validated, chronic problem."),
        
        # The two charts for Slide 3, side-by-side
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(figure=fig_scatter) # The scatter plot
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure=fig_donut) # The 79% donut
            ]),
        ]),
        
        html.H4("Top 10 Priority Districts for 'Resource Strike Team' Intervention:"),
        dash_table.DataTable(
            data=df_resource_top10.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_resource_top10.columns],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_data_conditional=[{ # Make the numbers stand out
                'if': {'column_type': 'numeric'},
                'fontWeight': 'bold'
            }]
        )
    ]),
    
    html.Hr(),
    html.Footer("End of Datathon Policy Briefing - NexaVision")
])

# --- 4. Run the App (THE FIX IS HERE) ---
if __name__ == '__main__':
    app.run(debug=False) # Changed from app.run_server to app.run