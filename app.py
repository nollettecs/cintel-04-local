import plotly.express as px
import seaborn as sns
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly
import palmerpenguins
from shiny import reactive, render, req
import shinyswatch

# Theme
shinyswatch.theme.superhero()

# Built-in function to load the penguin dataset
penguins_df = palmerpenguins.load_penguins()

# Title for chart
ui.page_opts(title="Nollettecs Penguins", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):

    # Use the ui.h2() function to add a 2nd level header to the sidebar
    # pass in a string argument (in quotes) to set the header text to "Sidebar"
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize("selected_attribute", "Selected Attribute",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
    
    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 15)

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 0, 100, 30)

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Species",
                            ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie","Gentoo", "Chinstrap"])

    # Use ui.input_checkbox() to create a checkbox to show the sex
    ui.input_checkbox("show_sex", "Show Sex")

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/nollettecs/cintel-02-data", target="_blank")

# Data Content

# Data Table and Data Grid
with ui.layout_columns():
    with ui.accordion(id="acc", open="open"):
        with ui.accordion_panel("Data Table"):
            @render.data_frame
            def penguin_datatable():
                return render.DataTable(filtered_data())

        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def penguin_datagrid():
                return render.DataGrid(filtered_data())

# Display Plotly histogram
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count",
            )
            
            return plotly_hist

# Display Seaborn histogram    
    with ui.nav_panel("Seaborn Histogram"):
        @render.plot
        def seaborn_histogram():
            histplot = sns.histplot(data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count())
            histplot.set_title("Palmer Penguins")
            histplot.set_xlabel("Mass")
            histplot.set_ylabel("Count")
            sns.set_style('darkgrid')
            return histplot

# Display Plotly Scatterplot
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                 color_discrete_map={
                     'Adelie': 'blue',
                     'Chinstrap': 'green',
                     'Gentoo': 'red'},
            )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
