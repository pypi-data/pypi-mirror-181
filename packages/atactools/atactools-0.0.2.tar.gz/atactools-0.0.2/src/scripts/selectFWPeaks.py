# File Name: selectFWPeaks.py
# Created By: ZW
# Created On: 2022-11-02
# Purpose: postprocessing script for ATAC-Seq data that selects the most 
#    representative set of non-overlapping, fixed-width peaks by peak score

# Module imports
# ----------------------------------------------------------------------------
from argparse import ArgumentParser
from atactools import peaks
from atactools.peaks import STRATEGIES
from pathlib import Path

# Main Execution Block
# ----------------------------------------------------------------------------
def main():
    # setup commandline parser 
    # ------------------------------------------------------------------------
    descr  = """
     Postprocessing script for ATAC-Seq data that selects the most 
     representative set of non-overlapping, fixed-width peaks by peak score
    """
    parser = ArgumentParser(description=descr)
    parser.add_argument("-n", "--norm-strategy", metavar="NORM_METHOD",
            type=str, choices=STRATEGIES,
            help="normalization strategy for peak scores")
    parser.add_argument("-w ","--write-out-all", metavar="NORM_ALL_BED",
            type=str, default=None,
            help="specify optional filename to report all records + normalized scores")
    parser.add_argument("output_bed", metavar="OUTPUT", type=str,
            help="output file destination (BED6) for selected peaks")
    parser.add_argument("input_peaks", metavar="IN_PEAKS", type=str, nargs='+', 
            help="input peaks files to select (.bed or .narrowPeak)")  
    args = parser.parse_args()
    
    # read in each input file, normalize according to the specified method and sort
    # ------------------------------------------------------------------------
    normalized_peaks = [] # list for final normalized peak set from all files
    for infile in args.input_peaks:
        # resolve the input file type and the class of the subsequent peak object
        infile_path = Path(infile).resolve()
        if infile_path.suffix == ".narrowPeak":
            peaks_type = peaks.NarrowPeak
            field_name = "log_qval"
        elif infile_path.suffix == ".bed":
            peaks_type = peaks.Bed6
            field_name = "score"
        else:
            errmsg = f"Error. Cannot resolve file type for {infile_path.name} from extension"
            raise ValueError(errmsg)

        # open file buffer, and read in peaks
        raw_peaks = [] # list for unnormalized peaks as they're read
        with open(infile_path, 'r') as input_obj:
            print(f"Reading and normalizing peaks from {infile_path.name}..")
            for fields in input_obj:
                raw_peaks.append(peaks_type(*fields.strip().split()))
            
            # sort and normalize 
            normd = peaks.normalize_peaks(raw_peaks, field_name, args.norm_strategy)
            normalized_peaks.extend(normd)

    # sort concatenated peak set
    print("Sorting Concatenated Peak set..")
    normalized_peaks.sort()

    # write out the normalized scores for all peaks if indicated by the user
    if args.write_out_all:
        print(f"Writing out all records with normalized scores...")
        with open(args.write_out_all, 'w') as fobj:
            for peak in normalized_peaks:
                fobj.write(
                    f"{peak.chrom}\t{peak.chromStart}\t{peak.chromEnd}"
                    f"\t{peak.name}\t{peak.norm_score}\t{peak.strand}\n"
                )

    # Select peaks, rolling from right to left by normalized score
    # ------------------------------------------------------------------------
    norm_peaks_n = len(normalized_peaks)
    focus_peak = normalized_peaks.pop(0)
    overlap_frame = [focus_peak]
    final_peaks = []
    
    # roll through and select peaks
    while len(normalized_peaks) > 0:
        if focus_peak.intersect(normalized_peaks[0]):
            overlap_frame.append(normalized_peaks.pop(0))
        else:
            scores = [p.norm_score for p in overlap_frame]
            max_idx = scores.index(max(scores))
            final_peaks.append(overlap_frame[max_idx])
            focus_peak = normalized_peaks.pop(0)
            overlap_frame = [focus_peak]

    # select final peaks 
    scores = [p.norm_score for p in overlap_frame]
    max_idx = scores.index(max(scores))
    final_peaks.append(overlap_frame[max_idx])

    # report the number of selected peaks
    final_peaks_n = len(final_peaks)
    print(f"Raw peaks: {norm_peaks_n}, Selected peaks: {final_peaks_n}")
    
    # write final bed outputs
    with open(args.output_bed, 'w') as fobj:
        for peak in final_peaks:
            fobj.write(
                f"{peak.chrom}\t{peak.chromStart}\t{peak.chromEnd}"
                f"\t{peak.name}\t{peak.norm_score}\t{peak.strand}\n"
            )

