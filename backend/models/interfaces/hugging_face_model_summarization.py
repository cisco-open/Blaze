
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


""" 
====================================================
Hugging Face Model Summary 
====================================================
This module extends the ModelSummary interface to load Hugging Face models.

"""

from os.path import exists
import pandas as pd
from tqdm.auto import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, SummarizationPipeline
from transformers.pipelines.base import KeyDataset

from backend.models.interfaces.model_summarization import ModelSummarization


class HuggingFaceModelSummarization(ModelSummarization):
    """
    A Superclass used to build HuggingFace models for summarization


    Attributes
    ----------
    _info : dictionnary
        A dictionnary containing the name, class name, description, paper link 
        and GitHub repo link of the model
    _max_length : int
        The maximum length parameter of the model
    _truncation : boolean
        Whether or not to truncate input sequences
    _model : AutoModelForSeq2SeqLM
        A HuggingFace model for summarization
    _tokenizer : AutoTokenizer
        A HuggingFace tokenizer 
    _pipe : SummarizationPipeline
        A HuggingFace pipeline for summarization

    Methods
    -------
    _summarize_dataset(self, dataset, column):
        Summarizes a dataset and appends to it a column with the summarized text.

    _summarize_text(self, text_to_summarize):
        Summarizes a piece of text and returns it.

    """

    def __init__(self, model_name, max_length, model_max_length, truncation, model_info, verbose=True):

        self._info = model_info
        self._max_length = max_length
        self._truncation = truncation

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' model...')

        self._model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            max_length=max_length)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' tokenizer...')

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            max_length=max_length,
            model_max_length=model_max_length,
            truncation=truncation)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' pipe...')

        self._pipe = SummarizationPipeline(
            model=self._model,
            tokenizer=self._tokenizer)

        if verbose == True:

            print('\n> Finished loading ' + self._info['name'] + ' class.\n')

    def _summarize_dataset(self, dataset):
        """ 
        Method that takes in a HuggingFace dataset and the name of the column of
        the dataset that contains the text to summarize. It calls the 
        summarization pipeline attribute and runs it on the whole dataset. It 
        saves the results in a list and adds this list to the dataset object and
        returns it.

        Parameters
        ----------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize
        column : str
            The name of the column ofthe dataset with the text to summarize

        Returns
        -------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize with the summarized text column
        """

        # Path where the summarization results are stored
        results_file_path = 'aski/results/' + \
            self._info['name'] + '_' + dataset._dataset_name + '.csv'

        # To store the summarization results (will later be added to the dataset)
        summarization_outputs = []

        # If we already ran the model for this dataset, read the saved results
        if exists(results_file_path):

            # Read the first column of the csv file which contains the summaries
            df = pd.read_csv(results_file_path)
            summarization_outputs = df[df.columns[0]]

            # Add the column to the dataset object to be able to compute metrics
            dataset._dataset[dataset._split] = dataset._dataset[dataset._split].add_column(
                name=('result_' + self._info['class_name']),
                column=summarization_outputs)
        else:
            for output in tqdm(self._pipe(KeyDataset(dataset._dataset[dataset._split], dataset._document_column))):

                answer = output[0]['summary_text']
                summarization_outputs.append(answer)

            # Save the results to a pandas dataframe and dump it to csv
            df = pd.DataFrame(summarization_outputs)
            df.to_csv(results_file_path, index=False)

            # Add the column to the dataset object to be able to compute metrics
            dataset._dataset[dataset._split] = dataset._dataset[dataset._split].add_column(
                name=('result' + self._info['class_name']),
                column=summarization_outputs)

        return dataset

    def _summarize_text(self, text_to_summarize):
        """ 
        Method that takes in a piece of text and summarizes it by calling the 
        tokenizer and model attributes and finally returns it.

        Parameters
        ----------
        text_to_summarize : str
            The piece of text to summarize

        Returns
        -------
        summary_text : List of str
            The summarized text as a list of strings
        """

        inputs = self._tokenizer(
            [text_to_summarize],
            return_tensors="pt",
            max_length=self._max_length,
            truncation=self._truncation)

        summary_ids = self._model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=self._max_length)

        summary_text = self._tokenizer.batch_decode(
            summary_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False)

        return summary_text
