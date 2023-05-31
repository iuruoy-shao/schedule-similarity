# Schedule Similarity
[![Site][Streamlit]][site-url]

## Requirements
If interested in running this repository locally, install requirements via:

```
pip install -r requirements.txt
```

## Overview
This repository is the source code for the Streamlit web app [Schedule Similarity](https://iuruoy-shao-schedule-similarity-main-sz6k3f.streamlit.app/). Created using the [Streamlit API](https://streamlit.io/), student class schedule data for the 2023-24 school year is stored and analysis is done to allow students to compare their schedules with their peers, search for students in a given class, and view whom has the highest classes in common with them.

## Functionality
### The Sidebar

**Use abbreviations** 
* Toggles whether abbreviations are used for class names (ex: "APPC" in place for "AP Physics C")
* This will apply site-wide
* A list of abbreviations is found in [text_replacement.json](text_replacement.json)

**Add your own schedule**
* Temporarily adds your own schedule to the dataset side-wide
* Will disappear upon site reload
* Selection options will appear for P0 through P8, but only if such a class for that period is already in the database
* Requires unique name entry

### Search & Filter
**Compare Students**
* Users can select between 1 to all students and view their schedules
* With multiple selections, the classes shared by all selected students are highlighted
* The number of shared classes is displayed

**Standard Filter**
* Select at least 1 class, displays all students who are in all selected classes
* Does not distinguish between class periods
* Classes matching selection(s) highlighted

**Filter by Period**
* Filters all students which have periods matching inputs
* To deselect a period, select the period number (ex: '1')

### Matrix
Displays how many classes each student shares with every other, colored for clarity.

**Options**
* Group students by period – select which column to apply row sort with, which effectively groups students by that period (column)
* Show full name – shows students' full names, loses organized structure
* View mode – toggle off for ability to sort columns by descending (to view students with most shared classes)

### Data
* The entire dataset is shown, with column headers 0-8 representing P0 through P8.
* A caption compare the number of students in each lunch period and the respective percentages

## Future Plans
1. Login or authorization system
2. Store data in SQL server
3. Expand to different grades/schools

[Streamlit]: https://img.shields.io/badge/Streamlit-View%20Site-000000?style=flat-square&logo=streamlit&logoColor=#FF4B4B
[site-url]: https://iuruoy-shao-schedule-similarity-main-sz6k3f.streamlit.app/