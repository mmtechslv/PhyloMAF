from pmaf.database._metakit import (
    DatabaseBackboneMetabase,
    DatabaseAccessionMetabase,
    DatabasePhylogenyMetabase,
    DatabaseTaxonomyMetabase,
    DatabaseSequenceMetabase,
)
from ._components import (
    MediatorLocalAccessionMixin,
    MediatorLocalSequenceMixin,
    MediatorLocalPhylogenyMixin,
    MediatorLocalTaxonomyMixin,
)
from typing import Any, TypeVar

AnyLocalMediator = TypeVar("AnyLocalMediator", bound=DatabaseBackboneMetabase)


def LocalMediator(
    database: DatabaseBackboneMetabase, **kwargs: Any
) -> AnyLocalMediator:
    """Factory function to create local :term:`mediator` for given database
    client.

    Parameters
    ----------
    database
        Database client for which local mediator will be produced
    kwargs
        Compatibility

    Returns
    -------
    New class that inherits any combination of mixin classes :class:`~pmaf.pipe.agents.mediators._local._components.MediatorLocalAccessionMixin`, :class:`~pmaf.pipe.agents.mediators._local._components.MediatorLocalPhylogenyMixin`, :class:`~pmaf.pipe.agents.mediators._local._components.MediatorLocalSequenceMixin`, :class:`~pmaf.pipe.agents.mediators._local._components.MediatorLocalTaxonomyMixin`
        New local mediator class with appropriate mixin classes that can mediate given `database` client
    """
    if not isinstance(database, DatabaseBackboneMetabase):
        raise TypeError("`database` has invalid type.")

    assoc_mixin_classes = []
    if (
        isinstance(database, DatabaseAccessionMetabase)
        and database.storage_manager.has_accs
    ):
        assoc_mixin_classes.append(MediatorLocalAccessionMixin)
    if (
        isinstance(database, DatabasePhylogenyMetabase)
        and database.storage_manager.has_tree
    ):
        assoc_mixin_classes.append(MediatorLocalPhylogenyMixin)
    if (
        isinstance(database, DatabaseTaxonomyMetabase)
        and database.storage_manager.has_tax
    ):
        assoc_mixin_classes.append(MediatorLocalTaxonomyMixin)
    if (
        isinstance(database, DatabaseSequenceMetabase)
        and database.storage_manager.has_repseq
    ):
        assoc_mixin_classes.append(MediatorLocalSequenceMixin)
    return type("LocalMediator", tuple(assoc_mixin_classes), {})(database, **kwargs)
