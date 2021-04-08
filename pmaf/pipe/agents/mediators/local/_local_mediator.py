from pmaf.database._metakit import DatabaseBackboneMetabase,DatabaseAccessionMetabase,DatabasePhylogenyMetabase,DatabaseTaxonomyMetabase,DatabaseSequenceMetabase
from ._components import MediatorLocalAccessionMixin,MediatorLocalSequenceMixin,MediatorLocalPhylogenyMixin,MediatorLocalTaxonomyMixin

def LocalMediator(database, **kwargs):
    if not isinstance(database,DatabaseBackboneMetabase):
        raise TypeError('`database` has invalid type.')

    assoc_mixin_classes = []
    if isinstance(database,DatabaseAccessionMetabase) and database.storage_manager.has_accs:
        assoc_mixin_classes.append(MediatorLocalAccessionMixin)
    if isinstance(database,DatabasePhylogenyMetabase) and database.storage_manager.has_tree:
        assoc_mixin_classes.append(MediatorLocalPhylogenyMixin)
    if isinstance(database, DatabaseTaxonomyMetabase) and database.storage_manager.has_tax:
        assoc_mixin_classes.append(MediatorLocalTaxonomyMixin)
    if isinstance(database, DatabaseSequenceMetabase) and database.storage_manager.has_repseq:
        assoc_mixin_classes.append(MediatorLocalSequenceMixin)
    return type("LocalMediator", tuple(assoc_mixin_classes), {})(database,**kwargs)
