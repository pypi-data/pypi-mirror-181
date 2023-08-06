""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------
"""
class BaseError(Exception):
    """Base class for all exceptions we'll raise."""
    pass

class NoInternetError(BaseError):
    """No internet."""
    pass

class HttpResponseError(BaseError):
    """There was a problem with an HTTP response."""
    pass

class InvalidParameterError(BaseError):
    """Invalid parameter."""
    pass

class AmbiguousLatestError(InvalidParameterError):
    """They pass "latest" for a version parameter, but index latest does not match latest version locally installed."""
    pass

class FileError(BaseError):
    """Base class for data-related errors."""
    pass

class DatasetNotInstalledError(FileError):
    """They requested a dataset they haven't installed."""
    pass

class DataVersionNotInstalledError(FileError):
    """They requested a version they haven't installed of a dataset."""
    pass

class PackageCannotHandleDataVersionError(BaseError):
    """They tried to load a new version of the data, but they have an old version of the package that doesn't have the code for the new data, so they need to update the package."""
    pass

class MissingFileError(FileError):
    """A data file was missing."""
    pass

class DownloadFailedError(FileError):
    """A file download failed."""
    pass

class DataError(BaseError):
    """Something was wrong with the data."""
    pass

class ReindexMapError(DataError):
    """Problem reindexing a dataframe."""
    pass

class DropFromSingleIndexError(DataError):
    """They tried to drop a level from a single-level index."""
    pass

class NoDefinitionsError(DataError):
    """They tried to access definitions for a dataset that doesn't provide any."""
    pass

class DataFrameNotIncludedError(DataError):
    """They requested a dataframe that's not included in the dataset."""
    pass

# Warnings
class BaseWarning(UserWarning):
    """Base class for all warnings we'll generate."""
    pass

class FailedReindexWarning(BaseWarning):
    """Error reindexing a dataframe."""
    pass

class InsertedNanWarning(BaseWarning):
    """NaNs were inserted during a dataframe join."""
    pass

class DuplicateColumnHeaderWarning(BaseWarning):
    """Due to a requested column multiindex flattening, the column index now has duplicate labels."""
    pass

class FlattenSingleIndexWarning(BaseWarning):
    """They tried to flatten a single-level index. We didn't do anything."""
    pass

class FilledMutationDataWarning(BaseWarning):
    """Mutation data was automatically filled during a dataframe join."""
    pass

class ParameterWarning(BaseWarning):
    """We should warn them about a parameter for some reason."""
    pass

class OldDataVersionWarning(BaseWarning):
    """They're using an old data version."""
    pass

class OldPackageVersionWarning(BaseWarning):
    """They're using an old version of the package."""
    pass

class PublicationEmbargoWarning(BaseWarning):
    """There is a publication embargo on the dataset."""
    pass

class DownloadingNewLatestWarning(BaseWarning):
    """Downloading a new latest data version. If they want to use an old version, they'll have to manually specify it."""
    pass

class FileNotUpdatedWarning(BaseWarning):
    """A file they wanted to update wasn't updated."""
    pass

class DatasetAlreadyInstalledWarning(BaseWarning):
    """The dataset was already installed, and they didn't want to redownload it."""
    pass

class StatsWarning(BaseWarning):
    """Statistics-related warnings."""
    pass

class StDevWarning(StatsWarning):
    """Warning about standard deviation."""
    pass

class PvalWarning(StatsWarning):
    """Some warning related to p values."""
    pass

# Developer-directed exceptions
class BaseDevError(Exception):
    """For exceptions that are probably the developer's fault."""
    pass
