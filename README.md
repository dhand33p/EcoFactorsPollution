# DSCI510 Final Project - Economic Power and its effects on CO2 and Pollution around the globe

### How does economic power influence CO2 emissions and the effects around the globe?
Project Description: Understanding the effects(if any) of economic status and its effects on countries. Specifically, this project aims to find insights regarding GDP Per Capita, CO2 emissions, and how pollution is affected as a result of these factors. 

### To run this code
For the data visualization notebook: Cell->Run All.
Click run all, and all visualizations and analyses will be shown.

For the data collection notebook: Cell->Run All. 
Click run all and some examples of different data frames will be generated through the web scraping and data cleaning process. 

### Dependances needed
pandas
numpy
requests
beautifulsoup4
re
matplotlib
plotly

### Data Collection
For this final project, I created a CSV after web scraping three websites. Specifically, I used requests and beautifulsoup to parse through the content and cleaned up the data using regex and other techniques(more detail in the project report). Each website pertained to different data, specifically about the growth of domestic product per capita(how much a person makes), carbon dioxide emissions, and pollution levels for each respective country. After collecting all this data, I joined the three datasets and created one CSV regarding each country's data. After joining, the result was 97 different countries.

Problems: Cleaning the data provided was challenging; however, by using regex expressions to filter through the collected data, I could extract the necessary information. 


### Data Visualizations

I decided to analyze the relationship and correlation using the Pearson correlation coeffecient. For my visuals, I included an interactive pie chart that depicts the top 20 global leaders in C02 Emissions. After, I compare the pollution score and CO2 emissions of the top 5 CO2 emissions in the world to find insights regardings their respective pollution and emissions. Finally, I decided to create a scatterplot that analyzed the Real GDP Per capita and pollution of the countries. 

Problems: I originally wanted the scatterplot to be interactive and allow the user to hover over each data point to see the specific country. However, I could not do this. Instead, I visualized the pollution through the size of points. 

Findings: Through this analysis, some insightful trends were found. By understanding the global leaders of CO2 emissions, those countries are not significantly affected by their CO2 emissions in regard to pollution. Also, the Pearson coefficient showed a slight -0.322 between GDP and pollution level. This does support the fact that a country’s pollution level is effected by its economic status(countries with higher GDP had lower pollution levels). This person coefficient and scatterplot allow us to provide evidence that the global leaders in CO2 are affecting other developing countries in regard to pollution besides themselves. 

### Future Work
I would want to add more data regarding each country, specifically, looking at the number of metropolitan areas in each country and analyzing the overall health of individuals(effects of pollution on population). Through this data, I would possibly want to predict for the upcoming years how each country would be effected(collect data from the previous years) in regards to overall health and pollution. 