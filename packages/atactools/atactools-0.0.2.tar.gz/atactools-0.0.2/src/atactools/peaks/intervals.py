# File Name: intervals.py
# Created By: ZW
# Created On: 2022-11-03
# Purpose: defines classes for BED style intervals commonly
#  used in peakcalling and post-processing tasks.


# module imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from operator import lt, gt, eq
from re import split as re_split
from typing import Union


# function definitions
# ----------------------------------------------------------------------------
# function prep_chrom_compare() splits contig names that are a combo of
# strings and digits to use as sorting keys in sort functions and similar 
# processes. for example: 'chr1' -> ('chr', 1). this function can be 
# used in the sorted() function with the key=prep_chrom_comp argument
def prep_chrom_comp(chrom: str):
    def recode(substr: str):
        return int(substr) if substr.isdigit() else substr.lower()
    return [recode(sub) for sub in re_split('([0-9]+)',chrom)]


# class definitions
# ----------------------------------------------------------------------------
# class Interval() - base class for all BED-type genome interval objects. 
# * indexing of genomic intervals follow BED conventions. This means that
#   chromosome scaffolds begin at base 0. the the end of the interval is 
#   equal to 1 + the feature end. this represents half-open intervals of the type
#   [chromStart, chromEnd), and but importantly, they represent 
#   chrom:(chromStart+1)-chromEnd intervals in position notation, for example:
#   chr1:1-1000 is equivalent to the Interval "chr1 0 1000" or chr1: [0,1000)
#
#  * the class contains only four attributes:
#     1. chromosome (chrom) -required- 
#     2. chromosome start position (chromEnd) -required-
#     3. chromosome end position (chromEnd) -required- 
#     4. feature name (name) -required-
@dataclass
class Interval():
    chrom: str
    chromStart: int
    chromEnd: int
    name: str

    # add a default field not specified in the user-specified
    # arguments for the normalized_score field
    def __post_init__(self):
        self.norm_score = -1

    # define a custom printout representation for the Interval
    def __repr__(self):
        spec = f" {self.chrom} {self.chromStart} {self.chromEnd} {self.name} "
        return repr(f"Interval({spec})")
    
    # define a custom function for the equal to (==) comparator
    # based on identical interval information on matchin coordinates
    def __eq__(self, other):
        comp = ((self.chrom == other.chrom) and
                (self.chromStart == other.chromStart) and
                (self.chromEnd == other.chromEnd))
        return comp
    
    # define a custom function for the less than (<) comparator
    # based on interval algebra on matching chromosomes
    def __lt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return True
        elif gt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return False
        else: # if the chromosomes names are equal by natural sort
            comp = ((self.chromEnd < other.chromStart) or
                    ((self.chromStart == other.chromStart) and
                    (self.chromEnd < other.chromEnd)))
            return comp
    
    # define a custom function for the greater than (>) comparator
    # based on interval algebra on matching chromosomes
    def __gt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return False
        elif gt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return True
        else: # if the chromosomes names are equal by natural sort
            comp = (self.chromStart > other.chromStart)
            return comp
    
    # define a custom function for the less than or equal to (<=) comparator
    # based on niterval algebra on matching chromosomes
    def __le__(self,other):
        return (self.__lt__(other) or self.__eq__(other))
    
    # define a custom function for the greater than or equal to (>=) comparator
    # based on interval algebra on matching chromosomes
    def __ge__(self,other):
        return (self.__gt__(other) or self.__eq__(other))
    
    # define a custom function to determine whether the interval intersects
    # another interval. intervals on separate chromosomes do not intersect
    def intersect(self,other):
        if self.chrom != other.chrom: return True
        else:
            return not (  # define intersection conditions
                (other.chromEnd < self.chromStart) or 
                (other.chromStart > self.chromEnd)) 


# class Bed6() - child class of Interval() which adds score and strand.
# * complies with the BED6 standard found on the UCSC file format standards
#   webpage: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
# 
# * the class adds two attributes to the Interval base class:
#    1. interval score (score); typically 1-1000 -required, missing denoted by '.'-
#    2. feature strandness (strand) -required, missingness denoted by '.'-
@dataclass
class Bed6(Interval):
    score: Union[int,str]
    strand: str

    # define a custom printout representation for the Bed6
    def __repr__(self):
        spec_int = f" {self.chrom} {self.chromStart} {self.chromEnd} {self.name}"
        spec_bed = spec_int + f" {self.score} {self.strand} "
        return repr(f"Bed6({spec_bed})")
    

# class NarrowPeak() - child class of Bed6() which adds four attributes; 
# signal Value p-value, q-value, and summit offset.
# * complies with the narrowPeak standard found on the UCSC file format standards
#   webpage: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
# 
# * the class adds four attributes to the Bed6 base class:
#    1. signal value, or overall enrichment (sigval) -required-
#    2. -log10 of p-value of the peak enrichment (log_pval) -required-
#    3. -log10 of FDR adjusted q-value (log_qval) -required-
#    4. basepair offset from chromStart for peak summit (summit) -required-
@dataclass
class NarrowPeak(Bed6):
    sigval: float
    log_pval: float
    log_qval: float
    summit: int
    
    # define a custom printout representation for the Bed6
    def __repr__(self):
        spec_int = f" {self.chrom} {self.chromStart} {self.chromEnd} {self.name}"
        spec_bed = spec_int + f" {self.score} {self.strand}"
        spec_nrrw = spec_bed + f" {self.log_pval} {self.log_qval} {self.summit} "
        return repr(f"NarrowPeak({spec_nrrw})")

