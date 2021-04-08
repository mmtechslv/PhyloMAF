from pmaf.database._metakit import  DatabaseAccessionMetabase
from collections import defaultdict
import numpy as np

class DatabaseAccessionMixin(DatabaseAccessionMetabase):
    def get_accession_by_tid(self, ids=None, subs=False, iterator=True):
        if self.storage_manager.state == 1:
            repseq_map_gen = self.find_rid_by_tid(ids, subs=subs, iterator=True)

            def acc_generator():
                for taxon_id, repseq_ids in repseq_map_gen:
                    yield taxon_id, self._retrieve_accs_by_id(repseq_ids)

            acc_gen = acc_generator()
            if iterator:
                return acc_gen
            else:
                tmp_seq_dict = defaultdict(None)
                for taxon_id, acc_dict in acc_gen:
                    tmp_seq_dict[taxon_id] = acc_dict
                return dict(tmp_seq_dict)
        else:
            raise RuntimeError('Storage is closed.')

    def get_accession_by_rid(self, ids=None, iterator=False):
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = np.asarray(self.xrid)
            else:
                target_ids = np.asarray(ids)

            def acc_generator():
                for rid in target_ids:
                    yield rid, self._retrieve_accs_by_id([rid])[rid]

            if iterator:
                return acc_generator()
            else:
                return self._retrieve_accs_by_id(target_ids)
        else:
            raise RuntimeError('Storage is closed.')

    def _retrieve_accs_by_id(self, repseq_ids):
        if len(repseq_ids) > 0:
            tmp_acc_df = self.storage_manager.get_element_data_by_ids('sequence-accession', repseq_ids)
            tmp_repseq_transformed = tmp_acc_df.apply(lambda acc: acc.to_dict(), axis=1).to_dict()
            return tmp_repseq_transformed
        else:
            return None