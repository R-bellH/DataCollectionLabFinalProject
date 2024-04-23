# Data Collection Lab Final Project - Adding LinkedIn Companies Badges <br> <small><small><sub>by: Yarden Kamienney, Arbel Hadar and Menachem Franko</sub></small></small>

![diverse company badge](./DataCollectionLab1/data/readmeAdds/diverseCompanyBadge.png)  ![top recuiter badge](./DataCollectionLab1/data/readmeAdds/recuiterBadge.png)

## Project introduction
In response to the evolving needs of both job seekers and companies, we have decided to develop AI-driven solutions for internal LinkedIn company use. We propose the integration of innovative badges on LinkedIn company pages. This solution addresses the current limitations of the platform by providing dynamic indicators of essential features such as diversity metrics and available positions. The necessity for this development arises from the growing demand for more comprehensive insights into potential employers, as well as the lack of uniformity in how companies present themselves on LinkedIn. By introducing badges, we aim to revolutionize the way companies are represented, offering users a more holistic understanding of a company's culture, values, and opportunities. This strategic initiative will benefit both companies and users. Companies showcasing their best qualities publicly will stand out, enabling users to make informed decisions about their professional endeavors, thus enhancing the efficacy and utility of the LinkedIn platform for all stakeholders involved.

## Set up code environment
1. Make sure to have poetry installed on your computer. 
If not, please install by running:
    ```bash
    pip install poetry
    ```
2. Clone this repo.
3. Run from main root:
    ```bash
    poetry install
    ```
Now everything is set and you are ready to run the code.

## Run the code files

### Create Diversity Badge
1. Collect data using gemini API:
    * Get an api key from here: [Get Google API Key](https://aistudio.google.com/app/apikey?hl=he) .
        * instuctions can be found here: [Get Google API Key Instructions](https://ai.google.dev/tutorials/get_started_web) . 
    * Add your personal API key to ataCollectionLab1/code/predCountry/collectCountryDataWithGemini.py
    * Run 
        ```bash
        python DataCollectionLab1/code/predCountry/collectCountryDataWithGemini.py
        ```
        * In case Gemini returns errors, please rerun the file with the rest of the wanted countries. 
        * If wanted more origins, please add them to the list *languages_list* in this python file.
2. Create the diversity badge:
    * Run DataCollectionLab1/code/predCountry/PredCountryModel.ipynb notebook **using the databricks platform**. [Here is a link to this notebook on DataBricks](https://adb-4286500221395801.1.azuredatabricks.net/?o=4286500221395801#notebook/4480858659357171) .
        * To train the model, please change the train_model parameter in the begining of the notebook to be set as True.
        * All the analysis for the diversity badge are at the end of this notebook. 

### Create Top Recuiter Badge
please run DataCollectionLab1/code/createWorkOpportunitiesBadge/createWorkOpportunitiesBadge.ipynb notebook.
* All the analysis for the recuiter badge are at the end of this notebook. 


