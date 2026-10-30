# Introduction

<h3 align="center">Cost Benefit Calculator</h3>

<p align="center">
  Description
</p>

<p align="center">
  You will need to have Dokcer installed on your system
  <br>
  Windows : <a href="https://docs.docker.com/desktop/install/windows-install/"><strong>Installation Guide</strong></a>
  <br>
  Ubuntu : <a href="https://docs.docker.com/engine/install/ubuntu/"><strong>Installation Guide</strong></a>
  <br>
  Linux : <a href="https://docs.docker.com/desktop/install/mac-install/"><strong>Installation Guide</strong></a>
</p>

## Installation

- Create a Folder in your System
- Clone / Download the Git Code into the folder
- Execute the following command 
```console
$ docker compose up
```
- Done

<p align="center">
After a successful service initiation the Webservice API documentation is available here:
http://localhost:8687/documentation
</p>

## Initial Configuration of the Web Service
Some initial actions must be taken for the Web Service to become fully installed. Those actions include "**Initializing Database**" and "**Initializing Models**". Those actions can be performed through the following procedure.

> **Note:** The administration endpoints are protected with HTTP Basic authentication. Set the environment variables `API_ADMIN_USERNAME` and `API_ADMIN_PASSWORD` (e.g. in the `.env` file next to `docker-compose.yml`) before starting the service. If they are not set, the administration endpoints are disabled.

- Go to http://localhost:8687/documentation
- Expand the "**/administration/create_db_tables**" (under the "**Administration**" Header) press the "**Try it out**" on the right side and then the "**Execute**" Button. 
- Expand the "**/administration/create_input_models**" (under the "**Administration**" Header) press the "**Try it out**" on the right side and then the "**Execute**" Button. 

## Add User Data in the Webservice
In order to receive the **Calculation Results** , we are going to have to provide User Input Data to the WebService. 
And those input data will be fed to the Models to produce the desired calculations.
This can be achieved by using the "**/user_data**" Endpoint , under the "**User Data Crops**" and "**User Data Livestock**" Header respectively, and fill in each form with the appropriate user data.

<b>Example for Crops : </b>

- Go to http://localhost:8687/documentation
- Expand the "**/user_data/crops**" (under the "**User Data Crops**" Header).
- Press the "**Try it out**" on the right side.
- Fill in the JSON Form with the appropriate values.
- Provide a Custom "user_id" so that all data are attached to a specific id.
- Press the "**Execute**" Button.

## Getting the Results 
If all the available User Data have been added in the Web Service we can then proceed in getting the calculation results from the Models.

- Go to http://localhost:8687/documentation
- Expand the "**/totals**" (under the "**Totals**" Header).
- Press the "**Try it out**" on the right side.
- In "**cfilter**" provide the Crop Name or the Animal Name you are interested in. (Eg. "Vegetables (Potato)")
- In "**dat_name**" provide the DAT Name you are interested in. (Eg. "gaiasense")
  - **Important**: If you want to know which DATs are available for the specific Cultivation Type you will have to use the "**/dat_tree**" endpoint under the "**dat_tree**" header. And you will receive a JSON with all the DATs in a Tree Format. Select the name you want and fill it in the form here.
- Provide your custom "**user_id**" that you used to add all the data.
- Press the "**Execute**" Button.