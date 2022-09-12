"""This defines a list of constants used in the dashboard."""

from enum import Enum, auto
import dash_bootstrap_components as dbc
from dash.dependencies import Input 

import yaml 
import drag.global_obj as g


from drag.design import Node 

ID_CONTENT = "page-content"

RESOURCE_COMPUTES = "computes"
RESOURCE_DATA = "data"
RESOURCE_DESIGN = "design"
RESOURCE_JOBS = "jobs"
RESOURCE_MODELS = "models"

CREAM = "#FFE5B4"

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
FONT_QUICKSAND = "https://fonts.googleapis.com/css?family=Quicksand&display=swap"


class DesignID(Enum):
    """Define IDs of layout props used in design pane."""

    #
    def __str__(self):
        """
        Override the basic Enum __str__.

        The reason for overriding it is that dot(.) is not allowed in IDs of
        Dash components.
        """
        return f"{self.__class__.__name__}-{self._name_}"

    TOAST_MESSAGE = auto()

    DESIGN_INTERFACE = auto()

    BTN_ADD_DATA = auto()
    BTN_ADD_MODEL = auto() 
    BTN_REMOVE_ELMT = auto()
    BTN_CONNECT_NODES = auto()

    BTN_UPLOAD_SCHEMA = auto() 

    INPUT_SELECT_ELEMENT = auto()
    INPUT_DISPLAY_ELEMENT = auto() 

    INPUT_MODEL_DISPLAY_ELEMENT = auto() 
    INPUT_DATA_DISPLAY_ELEMENT = auto() 

    TEXTAREA_MODEL_NODE_DESCRIPTION = auto() 
    TEXTAREA_DATA_NODE_DESCRIPTION = auto() 

    TEXTAREA_NODE_DESCRIPTION = auto()
    TEXTAREA_NODE_DESCRIPTION_OK = auto()

    TOGGLE_DATA_CONSUMER = auto()
    TOGGLE_CUSTOM = auto()
    TOGGLE_BENCHMARK = auto() 
    TOGGLE_COMPARISON = auto() 

    INPUT_DESIGN_TITLE = auto()
    INPUT_YAML_TITLE = auto() 
    NODE_CARD = auto()
    TAB_NODE_MODEL_CONTENT = auto() 
    TAB_NODE_DATA_CONTENT = auto()

    SCHEMA_PANE = auto() 

    INPUT_EDIT_EDGE_LABEL = auto()
    TEXTAREA_EDGE_DESCRIPTION = auto()
    TEXTAREA_EDGE_DESCRIPTION_OK = auto()
    INPUT_EDIT_FUNC_TAGS = auto()
    DROPDOWN_FUNCTAGS = auto()
    INPUT_EDIT_GROUP_BY = auto()
    DROPDOWN_GROUP_BY = auto()

    DOWNLOAD_FILE = auto() 

    BTN_CLEAR_DESIGN = auto()
    UPLOAD_TEMPLATE = auto()
    BTN_BUILD_SCHEMA = auto()

    TABS_DESIGN = auto()
    TAB_NODE_PROPERTY_VALUE = auto()
    TAB_EDGE_PROPERTY_VALUE = auto()

    TAB_NODE_CONTENT = auto()
    TAB_EDGE_CONTENT = auto()

    UPLOAD_ML_CODE = auto()
    LISTGROUP_ML_CODE_FILES = auto()
    LISTGROUP_FUNC_TAGS = auto()

    RADIOITEMS_ROLES_FOR_FUNC_TAGS = auto()

    INPUTGROUP_CHECKBOX_FUNC_TAG = auto()
    INPUTGROUP_INPUT_FUNC_TAG = auto()

    TEXTAREA_SCHEMA_DISPLAY = auto()


class JobID(Enum):
    """Define IDs of layout props used in job pane."""

    #
    def __str__(self):
        """
        Override the basic Enum __str__.

        The reason for overriding it is that dot(.) is not allowed in IDs of
        Dash components.
        """
        return f"{self.__class__.__name__}-{self._name_}"

    DIV_DUMMY = auto()
    TOAST_MESSAGE = auto()

    BTN_BUILD_JOB = auto()
    BTN_START_JOB = auto()

    INPUT_DESIGN_ID = auto()
    INPUT_SCHEMA_VERSION = auto()
    INPUT_CODE_VERSION = auto()

    INPUT_BASE_MODEL_NAME = auto()
    INPUT_BASE_MODEL_VERSION = auto()

    TEXTAREA_HYPERPARAMETERS = auto()

    SELECT_BACKEND = auto()
    INPUT_TIMEOUT = auto()
    SELECT_PRIORITY = auto()

    INPUT_DATASET = auto()
    BTN_ADD_DATASET = auto()
    DIV_DATASET_CONTAINER = auto()

    TEXTAREA_JOB_SPEC = auto()

    BTN_DELETE_DATASET = auto()
    DIV_DATASET = auto()


# TODO: get these directly from files instead of constants (we do this somewhere already!) 
    
supported_models = {
    'search' : {
        'ElasticBERT' : 'This is a sample description for ElasticBERT.', 
        'ColBERT' : 'Woah, this is a short snipped about ColBERT'
    }, 
    'summarization' : {
        'Bart' : 'BART. What an interesting name...', 
        'T5' : 'Here, we briefly cover the T5 model...'
    }, 
}

supported_data = {
    'search' : {
        'Squad' : 'Question-Answering Dataset developed by Stanford. Contains...', 
    }, 
    'summarization' : {
        'CNN Dailymail' : 'A collection of over...'
    }
}


PORTS = [5001, 8051]
ports = PORTS 

def generate_dropdown(choice): 
    if choice == "models": 
        data = supported_models 
    else: 
        data = supported_data 

    dropdown_menu_items = [] 
    dropdown_menu_inputs = [] 

    for task in data: 
        for model in data[task]: 
            dropdown_menu_items.append(dbc.DropdownMenuItem(model, id=f"dropdown_{model}"))
            dropdown_menu_inputs.append(Input(f"dropdown_{model}", "n_clicks"))
        dropdown_menu_items.append(dbc.DropdownMenuItem(divider=True))

    dropdown_menu_items.pop() # Removing that last barrier 

    return dropdown_menu_items, dropdown_menu_inputs

dropdown_models_items, dropdown_models_inputs = generate_dropdown("models")
dropdown_data_items, dropdown_data_inputs = generate_dropdown("data")

master_dict = {} 
for task in supported_models: 
    master_dict.update(supported_models[task])
for task in supported_data: 
    master_dict.update(supported_data[task])




def build_elements(filename, filecontent): 
    print(f"YAML recieived: {filename}")

    with open(f"yaml/{filename}", mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    print(f"Data read: {data}")

    # First, get title 

    title = data['Title']

    # Next, get elements 

    elements_model = []
    elements_data = [] 
    counter = 0 

    flag_list = [False, False, False]
    for func in data['function']: 
        if func == 'custom': 
            flag_list[0] = True 
        if func == 'benchmark': 
            flag_list[1] = True 
        if func == 'comparison': 
            flag_list[2] = True 


    # Models 
    for model in data['models']: 
        #elements_model.append({'data': {'id': f'Model {counter}', 'label': model, 'sort': 'Node'}})
        #counter += 1
        node = g.design.get_new_node('model')
        print(node)
        g.design.update_label(node['data'], model)
        print(node)
        elements_model.append(node)
        
    
    # Datasets 
    for base in data['datasets']: 
        #data_id = f'Data {counter}'
        #elements_data.append({'data': {'id': data_id, 'label': base, 'sort': 'Node'}})
        #counter += 1 

        node = g.design.get_new_node('data')
        g.design.update_label(node['data'], base)

        # Now, for each model, we must create an edge between said model and this dataset 
        for model in elements_model: 
            #model_id = model['data']['id']

            #elements_data.append({'data' : {'source' : model_id, 'target' : data_id, 'sort' : 'Edge', 'label' : f"{model_id}-{data_id}", 'flags':flag_list}})
         
            g.design.link([model['data'], node['data']])

            print(model['data'])
            print(node['data'])

            u = g.design.find_node_by_id(model['data']['id'])
            v = g.design.find_node_by_id(node['data']['id'])

            print(u)
            print(v)
            edge = Node.edge_to_callback(u, v)
            g.design.update_toggle(edge['data'], flag_list[0], flag_list[1], flag_list[2])


    #elements = elements_model + elements_data 
    elements = g.design.get_nodes_edges()
    # Functions 
    print(f"Elements: {elements}\n\n")

    return title, elements


def build_yaml(title, nodes_edges_list): 
   
    func_dict = {}
    models = []
    datasets = []

    for elm in nodes_edges_list: 
        info_dict = elm['data']

        if 'id' in info_dict: 
            # Means it's a node 

            if "Model" in info_dict['id']: 
                m = info_dict['label']
                models.append(m)

                if m in supported_models['search']: 
                    func_dict['task'] = "search" 
                if m in supported_models['summarization']: 
                    func_dict['task'] = "summarization"

            elif "Data" in info_dict['id']: 
                datasets.append(info_dict['label'])



        elif 'source' in info_dict: 
            # Means it's an edge 
            flags = info_dict['flags']

            if flags[0]: 
                func_dict['custom'] = True 
            if flags[1]: 
                func_dict['benchmarking'] = True 
            if flags[2]: 
                func_dict['comparison'] = True 

    yaml = {
        'Title' : title, 
        'function' : func_dict, 
        'models' : models, 
        'datasets' : datasets, 
        'metrics' : {}
    }

    return yaml 