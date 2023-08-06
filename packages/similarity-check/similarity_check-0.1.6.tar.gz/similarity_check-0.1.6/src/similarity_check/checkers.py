from typing import Union
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download
from gensim.models import KeyedVectors
import gensim.downloader as api
from sentence_transformers import SentenceTransformer, util, InputExample, losses, models
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer
from tqdm import tqdm
from collections import Counter
download('stopwords')

def preprocess(sentence: str, remove_punct: bool, remove_stop_words: bool, stemm: bool, lang: str='en') -> str: 
    if lang.lower() == 'en':
        ps = PorterStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            stop_words = stopwords.words('english')
            return ' '.join([ps.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([ps.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    elif lang.lower() == 'ar':
        st = ISRIStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('arabic')
            return ' '.join([st.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([st.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    else:
        raise Exception('non recognized language please specify either en|ar')
        

def preprocess(sentence: str, remove_punct: bool, remove_stop_words: bool, stemm: bool, lang: str='en') -> str: 
    if lang.lower() == 'en':
        ps = PorterStemmer()
        # remove punctuations
        if remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            stop_words = stopwords.words('english')
            return ' '.join([ps.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([ps.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    elif lang.lower() == 'ar':
        st = ISRIStemmer()
        # remove punctuations
        if remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('arabic')
            return ' '.join([st.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([st.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    else:
        raise Exception('non recognized language please specify either en|ar')

    
class sentence_tranformer_checker():
    def __init__(
        self, 
        targets: Union[list[str], pd.DataFrame], 
        target_group: Union[list[str], pd.DataFrame]=None,
        target_col: str=None, 
        model: SentenceTransformer=None, 
        lang: str='en', 
        only_include: list[str]=None,
        encode_batch = 32,
        encode_target = False,
        remove_punct: bool=True, 
        remove_stop_words: bool=True, 
        stemm: bool=False
    ):    
        """
        parameters:
            source: dataframe or list of input texts to find closest match for.
            target: dataframe or list of targets text to compare with.
            model (optional): a sentence tranformer model object, to use instead of the default one, for more [details](https://www.sbert.net/).
            target_group (optional): goups ids for the target to match only a single target for each group, can either provide list of ids,
            or the column name in the target dataframe.
            source_col (partially optional): the source column name used to match, *must be specified for dataframe matching*.
            target_col (partially optional): the target column name used to match, *must be specified for dataframe matching*.
            only_include (optional): used only for dataframe matching, allow providing a list of column names to only include for the target matches, provide empty list to get only target_col.
            encode_batch (optional): the number of sentences to encode in a batch.
            encode_target: boolean flag to indicate whatever to enocde the targets when initilizing the object (to cache target encoding).
            lang (optional): the languge of the model ('en'|'ar').
            remove_punct: boolean flag to indicate whatever to remove punctuations. 
            remove_stop_words: boolean flag to indicate whatever to remove stop words.
            stemm: boolean flag to indicate whatever to do stemming.
        """

        self.encode_batch = encode_batch
        self.remove_punct = remove_punct
        self.remove_stop_words = remove_stop_words
        self.stemm = stemm
        self.lang = lang 

        if isinstance(targets, pd.DataFrame):
            self.use_frames = True
    
            if target_col not in targets.columns:
                raise KeyError('target_col not found in target DataFrame cloumns')

            if target_group is not None:
                if isinstance(target_group, str):
                    if target_group not in targets.columns:
                        raise KeyError('target_group not found in target DataFrame cloumns')
                    self.group_ids = targets[target_group].tolist()
                else:
                    self.group_ids = target_group
            else:
                self.group_ids = None
                
            if only_include is not None:
                for col_name in only_include:
                    if col_name not in targets.columns:       
                        raise KeyError(f'only_include value:({col_name}) not found not found in target DataFrame cloumns')    
                only_include.insert(0, target_col)
                
                targets = targets.loc[:, only_include]

            self.target_df = targets.reset_index(drop=True)
            self.target_names = [preprocess(sent, self.remove_punct, self.remove_stop_words, self.stemm, self.lang) for sent in targets[target_col].tolist()]
        else:
            if isinstance(target_group, list):
                self.group_ids = target_group
            else:
                if target_group is None:
                    self.group_ids = target_group
                else:
                    raise TypeError('if target are a list entered groups must also be a list')
        
            if not targets:
                raise TypeError('Targets are empty') 

            self.use_frames = False
            self.target_names = [preprocess(sent, self.remove_punct, self.remove_stop_words, self.stemm, self.lang) for sent in targets]

        if pd.isnull(self.target_names).any():
            raise ValueError('Targets contain null values')

        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model...')
            if lang.lower() == 'en':
                self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
                print('done...')
            else:
                self.model = SentenceTransformer('distiluse-base-multilingual-cased-v1', device='cuda')
                print('done...')
        
        if encode_target:  
            print('enocding targets: ')
            self.encoded_targets = self.model.encode(self.target_names, batch_size=self.encode_batch, show_progress_bar=True,  normalize_embeddings=True) # encode the targets


    # used to make sure that if the object targets are updated, the cached targets are deleted
    def __setattr__(self, key, value):
        # self.key = value
        if key == 'target_names' or key == 'target_df':
            if hasattr(self, 'encoded_targets'):
                del self.encoded_targets     
        super().__setattr__(key, value)


    def match(
        self, 
        source: Union[list[str], pd.DataFrame], 
        source_col: str=None, 
        topn: int=1, 
        return_match_idx: bool=False, 
        threshold: float=0.5, 
        batch_size: int=128
    ) -> pd.DataFrame:
        '''
        Main match function. return only the top candidate for every source string.
        parameters:
            source: dataframe or list of input texts to find closest match for.
            source_col (partially optional): the source column name used to match, *must be specified for dataframe matching*.
            topn: number of matches to return.
            threshold: the lowest threeshold to ignore matches below it.
            return_match_idx: return an extra column for each match containing the index of the match within the target_names.
            batch_size: the size of the batch in inputs to match with targets (to limit space usage).
        returns:
            a data frame with 3 columns (source, target, score), and two extra columns for each extra match (target_2, score_2 ...), and an optional extra column for each match containg the match index, if return_match_idxs set to True.
        ''' 
        if isinstance(source, pd.DataFrame) and not hasattr(self, 'target_df'):
            raise TypeError('if target is a dataframe source must also be a dataframe')

        if isinstance(source, list) and hasattr(self, 'target_df'):
            source = pd.DataFrame({source_col: source})

        if isinstance(source, pd.DataFrame):
            self.use_frames = True
    
            if source_col not in source.columns:
                raise KeyError('source_col not found in source DataFrame cloumns')

            self.source_df = source.reset_index(drop=True)
            self.source_names = [preprocess(sent, self.remove_punct, self.remove_stop_words, self.stemm, self.lang) for sent in source[source_col].tolist()]
        else:
            if not source:
                raise TypeError('Inputs are empty')

            self.use_frames = False
            self.source_names = [preprocess(sent, self.remove_punct, self.remove_stop_words, self.stemm, self.lang) for sent in source]

        if not hasattr(self, 'encoded_targets'):
            print('enocding targets: ')
            encoded_targets = self.model.encode(self.target_names, batch_size=self.encode_batch, show_progress_bar=True,  normalize_embeddings=True) # encode the targets
        else:
            encoded_targets = self.encoded_targets

        targets = np.full((len(self.source_names), topn), None)
        top_cosine = np.full((len(self.source_names), topn), None)
        match_idxs = np.full((len(self.source_names), topn), None)

        print('matching prograss:')
        for i in tqdm(range(0, len(self.source_names), batch_size)):
            encoded_inputs = self.model.encode(self.source_names[i:i+batch_size], batch_size=self.encode_batch, normalize_embeddings=True) # encode the inputs

            batch_targets, batch_top_cosine, batch_match_idxs = self.max_cosine_sim(encoded_inputs, encoded_targets , topn, threshold)
            targets[i:i+batch_size, :] = batch_targets
            top_cosine[i:i+batch_size, :] = batch_top_cosine
            match_idxs[i:i+batch_size, :] = batch_match_idxs
        
        match_output = self._make_matchdf(targets, top_cosine, match_idxs, topn, return_match_idx)

        return match_output


    def max_cosine_sim(self, encoded_inputs, encoded_targets,  topn, threshold):
        if len(encoded_inputs.shape) == 1:
            a = a.unsqueeze(0)

        if len(encoded_targets.shape) == 1:
            b = b.unsqueeze(0)

        scores = np.matmul(encoded_inputs, encoded_targets.T)

        if self.group_ids is None:
            max_matches = min((len(self.target_names)-1, topn))
        else:
            max_matches = min((len(self.target_names)-1, topn * Counter(self.group_ids).most_common()[0][1]))
        
        top_sorted_idxs = np.argpartition(scores, -max_matches, axis=1)[:, -max_matches:] 
        
        # resort the result as the partition sort doesn't completly sort the result
        for i, idxs in enumerate(top_sorted_idxs):
            top_sorted_idxs[i, :] = top_sorted_idxs[i, np.argsort(-scores[i, idxs])]

        targets = np.full((encoded_inputs.shape[0], topn), None)
        max_cosines = np.full((encoded_inputs.shape[0], topn), None)
        match_idxs = np.full((encoded_inputs.shape[0], topn), None)
            
        # loop over top results to extract the index, target, and score for each match
        if self.group_ids is not None:
            for i, row in enumerate(top_sorted_idxs):
                column_id = 0
                previous_group_id = float('inf')
                for highest_score_idx in row:
                    if column_id >= topn or scores[i, highest_score_idx] < threshold:
                        break
                    if self.group_ids[highest_score_idx] == previous_group_id:
                        continue
                    match_idxs[i, column_id] = highest_score_idx
                    targets[i, column_id] = self.target_names[highest_score_idx]
                    max_cosines[i, column_id] = scores[i, highest_score_idx]
                    
                    column_id += 1
                    previous_group_id = self.group_ids[highest_score_idx]
        else:
            for i, row in enumerate(top_sorted_idxs):
                column_id = 0
                for highest_score_idx in row:
                    if column_id >= topn or scores[i, highest_score_idx] < threshold:
                        break
                    match_idxs[i, column_id] = highest_score_idx
                    targets[i, column_id] = self.target_names[highest_score_idx]
                    max_cosines[i, column_id] = scores[i, highest_score_idx]
                    
                    column_id += 1
        return targets, max_cosines, match_idxs


    def _make_matchdf(self, targets, top_cosine, match_idxs, topn, return_match_idx)-> pd.DataFrame:
        ''' Build dataframe for result return '''
        if self.use_frames:
            arr_temp = np.full((len(self.source_names), len(self.target_df.columns)+1), None)

            for i, (match_idx, score) in enumerate(zip(match_idxs.T[0], top_cosine.T[0])):
                if match_idx in self.target_df.index:
                     temp = self.target_df.iloc[match_idx].tolist()
                     temp.insert(0, score)
                     arr_temp[i, :] = temp

            cols = self.target_df.columns.tolist() 
            cols.insert(0, 'score_1')
            match_df= pd.DataFrame(arr_temp, columns=cols)

            # concat targets matches into one dataframe
            for match_num in range(1, len(match_idxs.T)):
                arr_temp = np.full((len(self.source_names), len(self.target_df.columns)+1), None)
                for i, (match_idx, score) in enumerate(zip(match_idxs.T[match_num], top_cosine.T[match_num])):
                    if match_idx in self.target_df.index:
                        temp = self.target_df.iloc[match_idx].tolist()
                        temp.insert(0, score)
                        arr_temp[i, :] = temp

                cols = self.target_df.columns.tolist() 
                cols.insert(0, f'score_{match_num+1}')
                df_temp= pd.DataFrame(arr_temp, columns=cols)
                match_df = match_df.merge(df_temp, left_index=True, right_index=True, suffixes=(f'_{match_num}', f'_{match_num+1}'))

            # merge matches with source
            match_df = self.source_df.reset_index(drop=True).merge(match_df, left_index=True, right_index=True, suffixes=(f'_source', f'_target'))
        elif not return_match_idx:
            match_list = []

            for source, top_scores, targets in zip(self.source_names, top_cosine, targets):
                row = []
                row.append(source)
                # loop over results of multi matches
                for top_score, target in zip(top_scores, targets):
                    row.append(top_score)
                    row.append(target)

                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'score', 'prediction']
            
            for i in range(2, topn+1):
                colnames.append(f'score_{i}')
                colnames.append(f'prediction_{i}')
                
            match_df = pd.DataFrame(match_list, columns=colnames)
        else:
            match_list = []
            for source, top_scores, targets, match_idxs in zip(self.source_names, top_cosine, targets, match_idxs):
                row = []
                row.append(source)
                # loop over results of multi matches
                for top_score, target, match_idx in zip(top_scores, targets, match_idxs):
                    row.append(top_score) 
                    row.append(target)
                    row.append(match_idx)
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'score', 'prediction', 'match_idx']
            
            for i in range(2, topn+1):
                colnames.append(f'score_{i}')
                colnames.append(f'prediction_{i}')
                colnames.append(f'match_idx_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)  

        return match_df


class word_mover_distance():
    def __init__(self, source_names, target_names, model):
        if not source_names:
            raise Exception('Inputs are empty')
        
        if not target_names:
            raise Exception('Targets are empty') 
               
        if pd.isnull(source_names).any():
            raise Exception('Inputs contain null values')
        
        if pd.isnull(target_names).any():
            raise Exception('Targets contain null values')
        
        self.source_names = source_names
        self.target_names = target_names
        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model (English model)...')
            self.model = api.load('glove-wiki-gigaword-300')

    def match(self, topn=1, return_match_idx=False):
        '''
        Main match function. return only the top candidate for every source string.
        '''
        self.topn = topn
        self.return_match_idx = return_match_idx
        
        self.top_wmd_distance()

        match_output = self._make_matchdf()

        return match_output


    def clean_data(self, remove_punct=True, remove_stop_words=True, stemm=False, lang='en'): 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def min_wmd_distance(self, input):
        wmd_results = np.array([self.model.wmdistance(input, target) for target in self.target_names])
        
        # get topn results
        wmd_sorted = np.sort(np.unique(wmd_results))
        scores = []
        indexes = []
        for x in wmd_sorted:
            if len(indexes) == self.topn:
                break
            for y in np.where(wmd_results == x)[0]:
                scores.append(float(1 - x)) # convert distance to score
                indexes.append(y)
                if len(indexes) == self.topn:
                    break    
        targets = [self.target_names[idx] for idx in indexes]
        
        # fill empty topn results 
        while len(targets) < self.topn:
            indexes.append(None)
            targets.append(None)
            scores.append(None)
        return targets, scores, indexes
    

    def top_wmd_distance(self):
        results = np.array([self.min_wmd_distance(input) for input in self.source_names])
        self.targets = results[:, 0]
        self.top_scores = results[:, 1]
        self.match_idxs = results[:, 2]


    def _make_matchdf(self):
        ''' Build dataframe for result return '''
        if not self.return_match_idx:
            match_list = []
            for source, targets, top_scores in zip(self.source_names, self.targets, self.top_scores):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score in zip(targets, top_scores):
                        row.append(target)
                        row.append(top_score) 
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)
        else:
            match_list = []
            for source, targets, top_scores, match_idxs in zip(self.source_names, self.targets, self.top_scores, self.match_idxs):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score, match_idx in zip(targets, top_scores, match_idxs):
                        row.append(target)
                        row.append(top_score) 
                        row.append(match_idx)
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score', 'match_idx']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')
                colnames.append(f'match_idx_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)  
        
        return match_df