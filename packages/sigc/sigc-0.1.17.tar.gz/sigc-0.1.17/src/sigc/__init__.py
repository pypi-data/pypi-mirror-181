from pkg_resources import get_distribution, DistributionNotFound

#try:
#    __version__ = get_distribution("sigc").version
#except DistributionNotFound:
#    pass

from sigc.core import (
    genesets2GeneSig,
	metabolism_sigs,
    sigc_score
)

__all__ = [
    "genesets2GeneSig",
	"metabolism_sigs",
    "sigc_score"
]

