from typing import TypeVar
from pmaf.biome._metakit import BiomeBackboneMetabase
from pmaf.biome.assembly._metakit import BiomeAssemblyBackboneMetabase
from pmaf.biome.survey._metakit import BiomeSurveyBackboneMetabase
from pmaf.biome.essentials._metakit import EssentialBackboneMetabase

AnyBiome = TypeVar('AnyBiome', bound = BiomeBackboneMetabase)
AnyBiomeAssembly = TypeVar('AnyBiomeAssembly', bound = BiomeAssemblyBackboneMetabase)
AnyBiomeSurvey = TypeVar('AnyBiomeSurvey', bound = BiomeSurveyBackboneMetabase)
AnyBiomeEssential = TypeVar('AnyBiomeEssential', bound = EssentialBackboneMetabase)