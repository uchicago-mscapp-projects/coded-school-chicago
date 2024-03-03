# Do the financial conditions of an area impact school performance metrics?

Using data from City of Chicago and ZIP Atlas, we examined how the financial conditions of a given area impacts school performance metrics.

The financial conditions of interest were: median household income, poverty rate, and unemployment rate. We defined an area by its zip code and, looking only at High Schools, we examined the data of seven performance areas: 

* student attainment: based on how well the school performed on standardized tests; schools are rated on a scale of ‘far below expectations’ to ‘far above expectations’, which we coded numerically on a scale of 1 - 6.
* culture/climate: based on student and teacher responses to the My Voice, My School ‘5Essentials’ survey; schools are rated on a scale of ‘not yet organized’ to ‘well organized’, which we coded numerically on a scale of 1-5.
* Mobility rate: the percentage of students who experienced at least one transfer in or out of the school, excluding graduates (Illinois Report Card).
* Chronic truancy: a student who is absent from school without valid cause for 5% or more days at any time of the school year (CPS Comprehensive Policy on Attendance).
* 11th grade SAT score: the average SAT score of 11th grade students at the school.
* Drop out rate: the percent of students enrolled in grades 9-12 at any time during a school year who dropped out during that year (CPS Office of Accountability).
Suspension rate: the removal of a student from their regular educational schedule for in-school or out-of-school consequences (CPS Student Code of Conduct).

![image](https://github.com/apichat-klang/Coded-school-Chicago/assets/142816445/2e43c0bd-4a00-4cb0-801b-d716ea6561f5)

# Running our Project: 
In order to view our project:

* Clone this repository
* Set up your local environment by running poetry install, then poetry shell 
* From the command line, run vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py, then vsapp.
* This will open a webpage in your default browser.


