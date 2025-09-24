Purpose of Repository: To visualize the changes in EV infrastructure related to EV stations, ports, and current events.

Visualizations:
1. EV Stations and Ports (Observable Notebook): https://observablehq.com/d/da0a460e7816edba
2. EV Car Registration (Altair): See Repository Structure Below.
3. EV Infrastructure Timeline (Timeline.js): https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1seKezAHvGEPBFdXfhAldhfchOZe5HRiBGvh4_kyBd1Q&font=Bitter-Raleway&lang=en&initial_zoom=2&height=650

Repository Structure:

1. `Preprocessing`: contains the raw data, scripts, and polished data used to construct the visualizations in index.html

    * Contents:
        * `preprocessing_notebook.ipynb`: Jupyter notebook used to process the raw data into usable formats for the Observable notebook and EV registration visualization
        * `EV_data_with_Counties_latlongchanges_fixed.csv`: Department of Transportation EV data preprocessed using the generate_county_ids.py script to add FIPs nunbers and county names (used as starting place to format Observable Imports). No OBJECTIDs have been dropped from this file - this is done in the preprocessing_notebook.ipynb.
        * `EV_Registrations.ipynb`: notebook used to generate the car registration interactive altair plot
        * `car_registration.html`: html file after saving the chart from the `EV_Registrations.ipynb` that is embedded on the website
        * `ev_reg_data.csv`: formatted .csv file from `preprocessing_notebook.ipynb` used in the `EV_Registrations.ipynb` (annual number of EV registrations per year for each state)
        * `df_stations_cum.csv`: formatted .csv file from `preprocessing_notebook.ipynb` used in the `EV_Registrations.ipynb` (cummulative number of open charging stations per year/state based on newly opened station counts)
        * `EV_infrastructure_timeline_events.csv`: formatted .csv containing timeline events and their sources (template used on TimelineJS website)

    * `Observable_Imports`: contains the preprocessed data from the preprocessing_notebook.ipynb that was imported into the Observable Notebook 
        * `df_locations.csv`: processed version of the `EV_data_with_Counties_latlongchanges_fixed.csv` dataset, with OBJECTIDS dropped, containing lat/long for each EV stations
        * `df_ports.csv`: processed version of the `EV_data_with_Counties_latlongchanges_fixed.csv` dataset, with OBJECTIDS dropped, containing port charging speed counts and power capacities for each EV station
        * `df_stations.csv`: processed version of the `EV_data_with_Counties_latlongchanges_fixed.csv` dataset, with OBJECTIDS dropped, containing the EV station counts
        * `population.csv`: concatenated population data from the Raw_Data files
        * `state_counties_all.csv`: processed version of the `county_state_ids_important` dataset containing also the states each county is in
        * `state_ids.csv`: formatted county FIPS numbers from the Federal Communications Commission for each state
             * https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt#:~:text=WISCONSIN%0A%20%20%20%20%20%20%2056%20%20%20%20%20%20%20%20WYOMING-,county%2Dlevel,-place%0A%20%20FIPS%20code
        * `USA_Freeway_System.geojson`: raw geojson data containing geometries for major Freeways and Interstates in USA
            * https://hub.arcgis.com/maps/91c6a5f6410b4991ab0db1d7c26daacb/about
        * `counties_edited.json`: edited version of the altair counties data, with the null entries removed and re-grouping of islands into single objects (see A3 repo for further explanation of things fixed)

    * `Raw_Data`: contains the raw data files downloaded directly from the respective sources
        - EV Station Data:
            * `Alternative_Fueling_Stations_Raw_Data.csv`: raw data from the Department of Transportation
                * https://data-usdot.opendata.arcgis.com/datasets/usdot::alternative-fueling-stations/about
            * `county_state_ids_important.csv`: formatted county FIPS numbers from the Federal Communications Commission used to map county names to FIPS
                * https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt#:~:text=WISCONSIN%0A%20%20%20%20%20%20%2056%20%20%20%20%20%20%20%20WYOMING-,county%2Dlevel,-place%0A%20%20FIPS%20code
            * `dropped_ids.csv`: csv containing the OBJECTIDS that were dropped from the raw EV data along with the reasons for their drop

        - Population Data:
            * `POP1990.csv`: population data formated by Duke University Libraries that is sourced from the US Census for years 1990 - 1999
                - https://repository.duke.edu/catalog/27251037-2a3b-462a-971d-4b023121bf7b
            * `POP2000.csv`: population data formated by Duke University Libraries taht is sourced form the US Census for years 2000 - 2010
                * https://repository.duke.edu/catalog/f49b199b-1496-4636-91f3-36226c8e7f80
            * `co-est2020-alldata.csv`: population data directly from the US Census for years 2010 - 2020 (years 2010 and 2020 were ignored since in other datasets)
                * https://www.census.gov/programs-surveys/popest/technical-documentation/research/evaluation-estimates/2020-evaluation-estimates/2010s-counties-total.html >> https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/totals/co-est2020-alldata.csv
            * `co-est2023-alldata.csv`: population data directly from the US Census for years 2020 - 2023
                * https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html#v2023 >> https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/counties/totals/co-est2023-alldata.csv

        - County Boundary/Polygon Data:
            * `generate_county_ids.py`: script used to determine the county name each EV station belonged to
            * `us-couty-boundaries.json`: opendatasoft dataset containing the polygon coordinate boundary paths (lat/long) for every USA county 
                * https://public.opendatasoft.com/explore/dataset/us-county-boundaries/map/?flg=en-us&disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InVzLWNvdW50eS1ib3VuZGFyaWVzIiwib3B0aW9ucyI6eyJmbGciOiJlbi11cyIsImRpc2p1bmN0aXZlLnN0YXRlZnAiOnRydWUsImRpc2p1bmN0aXZlLmNvdW50eWZwIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lbHNhZCI6dHJ1ZSwiZGlzanVuY3RpdmUuc3R1c2FiIjp0cnVlLCJkaXNqdW5jdGl2ZS5zdGF0ZV9uYW1lIjp0cnVlfX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImFsYW5kIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJzdGF0ZWZwIiwibWF4cG9pbnRzIjo1MCwic29ydCI6IiJ9XSwidGltZXNjYWxlIjoiIiwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&location=4,43.35714,-98.87695&basemap=jawg.light
       
       - Car Registration Data:
            * `EV_registration_raw.csv`: car registration data from energy.gov from 2016 to 2022
                * https://afdc.energy.gov/vehicle-registration?year=2016

2. Public
    * index.html: website containing all three visualizations with clickable top navigation bar
    * font_style.tff: font file used for website title

General Preprocessing Steps:

* Dataset used in analysis is from the United States Department of Transportation named "Alternative Fueling Stations" (https://data-usdot.opendata.arcgis.com/datasets/usdot::alternative-fueling-stations/about). Census Population data was aquired from Duke University Libraries and directly from the US Census website, as linked in Section 1.

* The `us-county-boundaries.json` file contains the latitude-longitude polygon coordinates for all US counties, and was used to calculate the predicted county name for each OBJECTID based on their reported latitudes and longitudes. County names were mapped to their ids, or FIPS numbers, using https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt. Object IDs with missing logitude and latitude values were manually looked up to find their county names via their provided addresses. These mapped county names and ids were compiled into the file `EV_data_with_Counties_latlongchanges_fixed`.

* Individual preprocessing datasets were compiled using the preprocessing_notebook.ipynb and saved into the `Observable_Imports` folder (d3 plots) or `Preprocessing` folder (altair plots). These were the datasets used to make the visualizations. View `preprocessing_notebook.ipynb` for a detailed look at how each dataset was processed.
