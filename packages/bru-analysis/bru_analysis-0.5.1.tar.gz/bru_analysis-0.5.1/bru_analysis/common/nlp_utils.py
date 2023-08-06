import os
import re
import sys
import json
import uuid
import time
import spacy
import logging
import requests
import pandas as pd
import numpy as np
import traceback
from sys import exc_info

pd.options.mode.chained_assignment = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERR_SYS = "System error: "
RETRIES = int(os.environ["RETRIES"])
TOKEN = os.environ["TOKEN"]

logger = logging.getLogger(__name__)


class Features:
    """
    Clase para el procesamiento de texto con spacy
    """

    def __init__(self):
        """
        Inicialización de la clase
        """
        print('\nLoading Spacy es model...')
        nlp_model = spacy.load('es_core_news_md',
                               disable=['ner', 'parser'])  # disabling Named Entity Recognition for speed
        print('Done.\n')
        self.nlp_model = nlp_model

        self.bad_words = ['de', 'que', 'la', 'los', 'el', 'las']

    def pos_tags(self, input_txt):
        """
        Funcion para generar las features de las palabras enviadas con el parametro input_txt
        :param input_txt: String to get the features from.
        :return:dict: keys -> tokens, lemmas and part of speech tags.
        """
        method_name = "pos_tags"
        self.input_txt = input_txt
        words = []
        lemmas = []
        pos_tags = []
        if type(input_txt) != str:
            print('ERROR: Input is not a string.')
            print(f'Class: {self.__str__()}\nMethod: {method_name}')
            logger.info(f"Se produjo error al no llegar datos en {method_name}")
        else:
            bad_words = self.bad_words
            nlp_model = self.nlp_model
            try:
                doc = nlp_model(self.input_txt.lower())
                features = [(token.text.replace('xxhashtagsignxx', '#').replace('xxatsignxx', '@'),
                             token.lemma_.replace('xxhashtagsignxx', '#').replace('xxatsignxx', '@'),
                             token.pos_) for token in doc if token.text not in bad_words and len(token.text) > 1]
                for feat in features:
                    if feat[2] in {'PROPN', 'NOUN', 'VERB', 'ADJ'}:
                        words.append(feat[0])
                        lemmas.append(feat[1])
                        pos_tags.append(feat[2])
                logger.info(f"Se generaron los datos para {method_name}")
            except Exception as e:
                print(e)
                error_1 = sys.exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f'Class: {self.__str__()}\nMethod: {method_name}')
                logger.info(f"Se produjo error al procesar los datos en {method_name}")
                words.clear()
                lemmas.clear()
                pos_tags.clear()
        out_dict = {
            'words': words,
            'lemmas': lemmas,
            'pos_tags': pos_tags
        }
        return out_dict


class CleanText:
    """
    this function clean and prepare text to analysis
    """

    def __init__(self, input_txt, verbose=False):
        """
        This functions validates if the input of the class is a string.

        Parameters
        ----------
        input_txt:
            type: str
            String to clean.
        """
        method_name = "__init__"

        self.bad_words = ["y", "de", "que", "la", "los", "el", "las"]
        with open(BASE_DIR + "/common/stopwords/English.txt", "r") as file:
            self.stopwords = file.read().splitlines()
        self.bad_words.extend(self.stopwords)
        with open(BASE_DIR + "/common/stopwords/Spanish.txt", "r") as file:
            self.stopwords = file.read().splitlines()
        self.bad_words.extend(self.stopwords)

        if type(input_txt) == str:
            self.input_txt = input_txt
        else:
            if verbose:
                print(f'WARNING: Input {input_txt} is not a string. Default set to "".')
                print(f"Class: {self.__str__()}\nMethod: {method_name}")
            self.input_txt = ""

    def process_text(
            self,
            rts=True,
            mentions=True,
            hashtags=True,
            links=True,
            spec_chars=True,
            stop_words=True,
    ):
        """
        This functions cleans the input text.

        Parameters
        ----------
        rts:
            type: bool
            If True the patterns associated with retweets are removed
            from the text, default=False.
        mentions:
            type: bool
            If True the mentions are removed from the text, default=False.
        hashtags:
            type: bool
            If True the hashtags are removed from the text, default=False.
        links:
            type: bool
            If True the patterns associated with links (urls) are removed
            from the text, default=False.
        spec_chars:
            type: bool
            If True all special characters (except accents, # and @) are removed
            from the text, default=False.
        stop_words:
            type: bool
            If True stop_words are removed from the, text, default=True.

        Returns
        -------
        str
        """

        input_txt = self.input_txt.lower()
        if rts:
            rt_pattern = re.compile(r"^(?:RT|rt) \@[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(rt_pattern, "", input_txt)
        if mentions:
            mention_pattern = re.compile(r"\@[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(mention_pattern, "", input_txt)
        else:
            # procect '@' signs of being removed in spec_chars
            input_txt = input_txt.replace("@", "xxatsignxx")
        if hashtags:
            hashtag_pattern = re.compile(r"\#[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(hashtag_pattern, "", input_txt)
        else:
            # procect '#' signs to being removed in spec_chars
            input_txt = input_txt.replace("#", "xxhashtagsignxx")
        if links:
            link_pattern = re.compile(r"\bhttps:.+\b")
            input_txt = re.sub(link_pattern, "", input_txt)
            link_pattern = re.compile(r"\bhttp:.+\b")
            input_txt = re.sub(link_pattern, "", input_txt)
        if spec_chars:
            input_txt = re.sub(r"[^a-zA-Z\u00C0-\u00FF ]", " ", input_txt)

        if stop_words:
            temp_txt = input_txt.split()
            temp_txt = [word for word in temp_txt if word not in self.bad_words]
            output_txt = " ".join(temp_txt)

        output_txt = output_txt.replace("xxatsignxx", "@")
        output_txt = output_txt.replace("xxhashtagsignxx", "#")

        return output_txt


class sendData:
    """
    This class send data to microservices emotion sentiment and pqrs
    """

    def __init__(self, df, url, token):
        """
        Parameters
        ----------
        df : TYPE dataframe
            DESCRIPTION. dataframe to send
        url : TYPE string
            DESCRIPTION. url microservice
        """

        self.df_b2b = df
        self.url = url
        self.token = token

    def batch2batch(self, batch=500, delay_req=0.05, verbose=False):
        """
        This function sends the data in batches to the microservice,
        sends a batch receives the same response batch

        Parameters
        ----------
        batch : TYPE, optional int
            DESCRIPTION. The default is 500. Number of rows to send
        delay_req : TYPE, optional float
            DESCRIPTION. The default is 0.05. delay between request and request in seconds
        verbose : TYPE, optional bool
            DESCRIPTION. The default is False. if you want to see the batches in the terminal

        Returns
        -------
        df_output : TYPE dataframe
            DESCRIPTION. microservice response

        """
        df_b2b = self.df_b2b
        url = self.url
        df_output = pd.DataFrame()
        len_df = len(df_b2b)
        last_index = 0
        seq = np.arange(0, len_df, batch)
        method_name = 'batch2batch'

        for index in seq:
            if index == 0:
                i_1 = index
                i_2 = (index + batch) - 1
                last_index = last_index + batch

            else:
                i_1 = index
                i_2 = (last_index + batch) - 1
                last_index = last_index + batch

            data = df_b2b[i_1:i_2 + 1]
            data["uuid"] = None
            data["uuid"] = data["uuid"].apply(lambda x: f"{uuid.uuid4()}")
            original_id = list(data["uuid"])
            data = data.to_dict(orient='records')
            data = json.dumps(data)
            url_send = f'{url}/?len_df={len_df}&last_index={last_index}'
            requests_id = 1
            try:
                # try to make the request RETRIES times if the identifiers do not correspond
                while requests_id < RETRIES:
                    response = requests.post(url=url_send, data=data, headers={'x-api-key': self.token})
                    time.sleep(delay_req)

                    res_json = response.json()
                    df_response = pd.DataFrame(res_json)
                    validation_ids = original_id == list(df_response["uuid"])

                    if validation_ids:
                        break

                    print('Bad request')
                    requests_id += 1

                df_output = pd.concat([df_output, df_response])
                df_output = df_output.reset_index(drop=True)

                if verbose:
                    print(f'Send batch column: {i_1} to {i_2}')

            except ConnectionError as e_1:
                print(''.center(60, '='))
                print(e_1)
                print(''.center(60, '='))
                error_1 = exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f'\nMethod: {method_name}')
                print(''.center(60, '='))
                traceback.print_exc()
                df_output = pd.DataFrame(columns=df_b2b.columns)

            except Exception as e_2:
                print(''.center(60, '='))
                print(e_2)
                print(''.center(60, '='))
                error_1 = exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f'\nMethod: {method_name}')
                print(''.center(60, '='))
                traceback.print_exc()
                df_output = pd.DataFrame(columns=df_b2b.columns)

        return df_output

    def batch2all(self, batch=500, delay_req=0.05, verbose=False):
        """
        This function sends the data in batches to the microservice,
        sends the data batch by batch,
        when it finishes it receives a single response with all the data sent

        Parameters
        ----------
        batch : TYPE, optional int
            DESCRIPTION. The default is 500. Number of rows to send
        delay_req : TYPE, optional float
            DESCRIPTION. The default is 0.05. delay between request and request in seconds
        verbose : TYPE, optional bool
            DESCRIPTION. The default is False. if you want to see the batches in the terminal

        Returns
        -------
        df_output_all : TYPE dataframe
            DESCRIPTION. microservice response

        """

        df_b2a = self.df_b2b
        url = self.url
        df_output_all = pd.DataFrame()
        len_df = len(df_b2a)
        last_index = 0
        seq = np.arange(0, len_df, batch)
        reg_name = uuid.uuid4()
        method_name = 'batch2all'

        for index in seq:
            if index == 0:
                i_1 = index
                i_2 = (index + batch) - 1
                last_index = last_index + batch

            else:
                i_1 = index
                i_2 = (last_index + batch) - 1
                last_index = last_index + batch

            data = df_b2a[i_1:i_2 + 1]
            data = data.to_dict(orient='records')
            data = json.dumps(data)
            u_id = uuid.uuid4()
            url_send = f'{url}/?len_df={len_df}&last_index={last_index}&u_id={u_id}&reg_name={reg_name}'
            try:
                response = requests.post(url=url_send, data=data, headers={'x-api-key': self.token})
                time.sleep(delay_req)

                res_json = response.json()
                if not response.headers.get('x_status') == 'in_batch':
                    df_output = pd.DataFrame(res_json)
                    df_output = df_output.reset_index(drop=True)
                else:
                    continue

                df_output_all = df_output
                if verbose:
                    print(f'Send batch column: {i_1} to {i_2}')

            except ConnectionError as e_1:
                print(''.center(60, '='))
                print(e_1)
                print(''.center(60, '='))
                error_1 = exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f'\nMethod: {method_name}')
                print(''.center(60, '='))
                traceback.print_exc()
                df_output_all = pd.DataFrame(columns=df_b2a.columns)

            except Exception as e_2:
                print(''.center(60, '='))
                print(e_2)
                print(''.center(60, '='))
                error_1 = exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f'\nMethod: {method_name}')
                print(''.center(60, '='))
                traceback.print_exc()
                df_output_all = pd.DataFrame(columns=df_b2a.columns)

        return df_output_all

# class Features:
#     def __init__(self):
#         """
#         This functions loads the spacy model for spanish.
#
#         """
#
#     def pos_tags(self, input_txt):
#         """
#         This functions get the features of the words in the input_txt parameter.
#
#         Parameters
#         ----------
#         input_txt:
#             type: str
#             String to get the features from.
#
#         Returns
#         -------
#         dict: keys -> tokens, lemmas and part of speech tags.
#         i
#         """
#         method_name = "pos_tags"
#         self.input_txt = input_txt
#         if type(input_txt) != str:
#             print("ERROR: Input is not a string.")
#             print(f"Class: {self.__str__()}\nMethod: {method_name}")
#             self.input_txt = ""
#
#         try:
#             out_dict = send_to_model(
#                 data={"value": input_txt},
#                 ms_models_path=URL_MS_MODELOS + "/models_reg/features/pos_tags",
#             )
#         except Exception as e_1:
#             print(e_1)
#             error_1 = sys.exc_info()[0]
#             print(ERR_SYS + str(error_1))
#             print(f"Class: {self.__str__()}\nMethod: {method_name}")
#             out_dict = {"words": [], "lemmas": [], "pos_tags": []}
#
#         return out_dict
