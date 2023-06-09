# BLAZE - Building Language Applications with eaZE 

> [BLAZE Drag-and-Drop - README](drag/README.md) | [BLAZE Conversational AI - README](conv/README.md)

&nbsp;&nbsp;

The goal of BLAZE is to **make the lives of data scientists easier**, filling-in a required niche. 

Natural Language Processing (NLP) pipelines reuse many of the same components arranged in different orders. The purpose each NLP model serves varies from use-case to use-case. However, these NLP models are not standardized in terms of their inputs, outputs, and hardware requirements. As a result, it is very difficult to interchange and combine NLP models, especially without introducing significant amounts of code. This lack of standardization causes NLP pipelines to be very rigid. Their lack of flexibility makes it difficult to compose, modify, and add functionality. 

To solve this problem, Blaze that allows for the modular creation and composition of NLP pipelines. Each component of the NLP Pipeline can be implemented as "building block" (for example, a microservice). These building blocks will have standardized inputs and outputs, and they can easily be assembled in varying orders. The order and choice of these specific blocks result in varying pipelines, built for unique use-cases. 


## Features 

Here's BLAZE's current functionalities:

**Use Case #1 - Developer** 

- **Drag-and-Drop Pipeline Builder** 
  - Visual builder for configuring and deploying pipelines
  - Allows for building from scratch (adding, connecting components)
  - Allows for uploading existing pipelines (visualize "recipes") 
  - Converts custom recipe into downloadable YAML config file 
  - Generates and launches custom NLP pipeline solution 

- **Conversational AI (Webex Bot)** 
  - Interface with BLAZE to specify pipeline components
  - Generate and launch custom NLP pipeline solution 

  &nbsp;&nbsp;

**Use Case #2 - Business** 

- **Visual Dashboard Web App** 
  - Visual representation of generated pipeline
  - Supports semantic search, summarization, file upload, etc. 

- **Conversational AI (Webex Bot)** 
  - Interact with generated pipeline through natural language
  - Can choose knowledge base (ex. upload file, view all files) 
  - Can index model and retrieve results (ex. summarize this doc) 
  - Can retrieve knowledge base, model, and metrics info 

  &nbsp;&nbsp;

**Use Case #3 - Researcher** 

- **Model/Knowledge Base Benchmarking** 
  - Benchmark selected model on selected knowledge base 
  - Gives latency (avg time/question, as well as generates real-time graph)
  - Gives accuracy (num correct, num total, % correct, % progress) 
  - Displays incorrect questions 

- **Model/Knowledge Base Comparison** 
  - Benchmark multiple models on selected knowledge base 
  - Gives latency (avg time/question, as well as generates real-time graph)
  - Gives side-by-side accuracy (num correct, num total, % correct, % progress) 
  - Displays incorrect questions 

- **Model/Knowledge Base Metrics** 
  - Compute and display scientific metrics 
  - Currently Supported Metrics: BertScore, Bleu, Rouge 

  &nbsp;&nbsp;

> GIFS/Screenshots Coming Soon! 

  ![Custom](./docs/images/custom_qna.PNG)

  ![Comparison](./docs/images/model_comparison.png)



> Over the coming weeks, this platform will be further fleshed out with more exciting features 😄. 


&nbsp;&nbsp;

## Install using Pyenv: Local Development

Install Dependencies
For Ubuntu/Debian
`sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl`

For Fedora/CentOS
`sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel`

Install Pyenv
`curl https://pyenv.run | bash`

Install Python version 3.9.16 using below command
`pyenv install -v 3.9.16`

check python version installed in pyenv using command
`pyenv versions`

Create virtual environment with specific version using below command
`pyenv virtualenv 3.9.16 venv`

Activate virtual environment using 
`pyenv local venv` or `pyenv activate <environment_name>`

You can verify this by running the following:
`pyenv which python`

Install packages and modules using 
`pip install -r requirements.txt`

Run the Program with:
`python build.py`

Now, a link should appear (ex. `Dash is running on http://127.0.0.1:5000/`). Run this link in your browser to open the dashboard!

`python run.py yaml/<file-name>.yaml`

&nbsp;&nbsp;

## Install using conda: Local development 

## NOTE: The use of Conda may require the use of Anaconda Commercial Edition to comply with Anaconda's Terms of Service if your use is considered commercial according to Anaconda. More information about Anaconda's Terms of Service and what qualifies as commercial usage can be found here: https://www.anaconda.com/blog/anaconda-commercial-edition-faq/ 

Create your conda environment with

conda env create -f aski_env.yml

Then, activate your conda environment with

conda activate aski

## Using the Conversational AI

Build the conversational model with

`python -m conv build`

(This step may take about 15 minutes without a GPU)

And run the AI in the command line with

`python -m conv converse`

To run the webex bot server, start an ngrok tunnel with

`ngrok http 8080 --region=eu`

It is important that the region is *not* 'us'.

Set the environment variables BOT_ACCESS_TOKEN (received when you register your bot) and WEBHOOK_URL (generated by ngrok) and change to the conv directory. Then run

`python webex_bot_server.py`

***Sources for training data***
- greet: food_ordering/greet/train.txt
- exit: food_ordering/exit/train.txt
- ask_question: manual data entry + mindmeld data augmentation
- get_summary: manual data entry + mindmeld data augmentation
- upload_data: manual data entry + mindmeld data augmentation


## Supported Models, Knowledge Bases

***Installing Elasticsearch***

Navigate to [Elasticsearch Installation](https://www.elastic.co/downloads/past-releases/elasticsearch-7-0-0) and 
follow the instructions according to your specific setup. 

> NOTE: ASKI does **not currently support** Elasticsearch 8 or higher! 

In order to launch elasticsearch, open a new terminal, navigate to the elasticsearch directory, and run either of the following: 

place the elastic folder as same hirerachy as ASKI project folder to start elastic service when running run.py file insted of running it manually using the commands below

- `./bin/elasticsearch` (Linux/Mac)
- `.\bin\elasticsearch.bat` (Windows)

Now, leave this terminal window open! 

&nbsp;&nbsp;

***Installing ColBERT***

Clone the following [GitHub Repo (new-api branch)](https://github.com/stanford-futuredata/ColBERT/tree/new_api) into the `ColBERT` folder. 

> NOTE: There might be some issues with environments, these will be resolved by next commit! 

Once downloading the ColBERT files, make sure to uncomment the three lines near the top 
of the file `ColBERTSearch.py`. More instructions are detailed at the top of this file. 

After this, navigate to the `get_sidebar()` function in `app_elements.py` and make sure to 
toggle the "Disabled" option next to ColBERT. You should be good to go now! 

&nbsp;&nbsp;

***Installing Knowledge Graph***

Stay tuned, support for this is coming soon! 

&nbsp;&nbsp;
