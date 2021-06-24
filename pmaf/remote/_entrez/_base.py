from Bio import Entrez,SeqIO
from functools import wraps as metawrapper
import time
import urllib3
from .. import _shared as remote_shared
from ._base_blocks import IdiomaticBase
from ._metakit import EntrezBackboneMetabase

def control_request_runtime(method_pass):
    """

    Parameters
    ----------
    method_pass :
        

    Returns
    -------

    """
    @metawrapper(method_pass)
    def wrapper(instance_self,*args,**kwargs):
        """

        Parameters
        ----------
        instance_self :
            
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        attempt_counter = instance_self._get_attempts()
        retry = True
        method_pass_ret = False
        while retry:
            last_runtime = instance_self._get_last_runtime()
            if (last_runtime < 1) and (instance_self._max_requests == instance_self._get_request_count()):
                time.sleep(1 - last_runtime)
                last_runtime = 0
                instance_self._reset_request_counter()
            if (last_runtime >= 1) or (instance_self._max_requests == instance_self._get_request_count()):
                time.sleep(1)
                last_runtime = 0
                instance_self._reset_request_counter()
            starttime = time.time()
            try:
                method_pass_ret = method_pass(instance_self,*args,**kwargs)
                attempt_counter = attempt_counter - 1
                retry = False
            except urllib3.exceptions.HTTPError as http_error:
                if attempt_counter == 0:
                    raise http_error
                else:
                    retry = True
            endtime = time.time()
            instance_self._next_request()
            runtime = endtime-starttime
            instance_self._set_last_runtime(last_runtime+runtime)
            request_log = {'request':method_pass.__name__,'attempts':instance_self._get_attempts()-attempt_counter,'runtime':instance_self._get_last_runtime()}
            instance_self._add_request_log(request_log)
        return method_pass_ret
    return wrapper


class EntrezBase(EntrezBackboneMetabase,IdiomaticBase):
    """"""
    def __init__(self,email,api_key = None,tool='PhyloMAF'):
        super().__init__()
        self._BioEntrez = None
        self._init_state = False
        self._retmax = 5
        self.__last_runtime = 0
        self._max_requests = 3
        self.__request_counter = 0
        self._api_key = None
        self.__request_logs = []
        self._attempts = 3

        if remote_shared.validate_email(email):
            self._email = email
        else:
            ValueError('Invalid Email Address')
        if api_key is not None:
            self._api_key = api_key

        self._tool_name = tool

        self._init_entrez()

    def __repr__(self):
        class_name = self.__class__.__name__
        state = 'Ready' if self.check_init() else 'Broken'
        email = self._email
        api_state = 'On' if self._api_key is not None else 'Off'
        repr_str = "<{}:[{}], API:[{}], Email: [{}]>".format(class_name, state, api_state, email)
        return repr_str

    def _init_entrez(self):
        """"""
        self._BioEntrez = Entrez
        self._BioEntrez.email = self._email
        self._BioEntrez.tool = self._tool_name
        self._BioEntrez.api_key = self._api_key if self._api_key is not None else None
        self._max_requests  = 10 if self._api_key is not None else self._max_requests
        self._init_state = True
        return

    def check_init(self):
        """Check instance ready status."""
        ret = False
        if self._init_state:
            ret = True
        return ret

    def _get_attempts(self):
        """"""
        return self._attempts

    def _set_last_runtime(self,runtime):
        """

        Parameters
        ----------
        runtime :
            

        Returns
        -------

        """
        self.__last_runtime = runtime
        return

    def _get_last_runtime(self):
        """"""
        return self.__last_runtime

    def _reset_request_counter(self,):
        """"""
        self.__request_counter = 0
        return

    def _get_request_count(self):
        """"""
        return self.__request_counter

    def _next_request(self):
        """"""
        self.__request_counter = self.__request_counter + 1
        return

    def _add_request_log(self,method_name):
        """

        Parameters
        ----------
        method_name :
            

        Returns
        -------

        """
        self.__request_logs.append({'Request':method_name,'Cumulative Runtime': self.__last_runtime,'Request Count':self.__request_counter})
        return

    def get_request_logs(self):
        """Get low level request codes for debugging."""
        return self.__request_logs

    @control_request_runtime
    def _request_sequence_feature_table_by_acc_id(self,accession_id,handle=False):
        """

        Parameters
        ----------
        accession_id :
            
        handle :
            (Default value = False)

        Returns
        -------

        """
        efetch_handle = self._BioEntrez.efetch(db='nuccore', id=accession_id, rettype='ft', retmode='text')
        if handle:
            return efetch_handle
        else:
            return  efetch_handle.read()

    @control_request_runtime
    def _request_chromosomes_by_genome_id(self,genome_id):
        """

        Parameters
        ----------
        genome_id :
            

        Returns
        -------

        """
        with self._BioEntrez.elink(dbfrom='genome', db='nuccore', id=genome_id, idtype='acc',term='gene+in+chromosome[prop]') as elink_handle:
            elink_record = self._BioEntrez.read(elink_handle)
        return elink_record

    @control_request_runtime
    def _request_genomes_by_taxid(self,taxid):
        """

        Parameters
        ----------
        taxid :
            

        Returns
        -------

        """
        with self._BioEntrez.elink(dbfrom='taxonomy', db='genome', id=taxid) as elink_handle:
            elink_record = self._BioEntrez.read(elink_handle)
        return elink_record

    @control_request_runtime
    def _request_taxid_by_query(self,query):
        """

        Parameters
        ----------
        query :
            

        Returns
        -------

        """
        with self._BioEntrez.esearch(db='taxonomy', retmax=self._retmax, term=query) as esearch_handle:
            esearch_record = self._BioEntrez.read(esearch_handle)
        return esearch_record

    @control_request_runtime
    def _request_sequence_fasta(self,acc_id, start, end, strand):
        """

        Parameters
        ----------
        acc_id :
            
        start :
            
        end :
            
        strand :
            

        Returns
        -------

        """
        with self._BioEntrez.efetch(db='nuccore', id=acc_id, rettype='fasta', retmode='text', strand=str(strand),seq_start=str(start), seq_stop=str(end)) as efetch_handle:
            efetch_record = efetch_handle.read()
        return efetch_record

    @property
    def state(self):
        """State of the instance."""
        return self.check_init()



