# split.py

# Functions for sequence and record splitting.

from streamseqs import stream_records, new_record
from splitmasked import io


def find_boundaries(seq, is_masked):
    """
    Get boundaries for splitting of a sequence.

    Parameters
    ----------
        seq : str
            Sequence with masked and unmasked parts
        is_masked : callable
            Takes one argument (a letter from `seq`) and returns `True` if the
            letter is masked and `False` if it is unmasked.

    Returns
    -------
        tuple (bool, list[int])
            (first_masked, [indices for splitting])

    Examples
    --------
    >>> find_boundaries("aaTT", lambda x: x.islower())
    # (True, [0, 2, 4])
    """
    boundaries = [0]
    first_masked = is_masked(seq[0])
    prev_masked = first_masked
    for i, x in enumerate(seq):
        if prev_masked != is_masked(seq[i]):
            boundaries.append(i)
            # Flip current state
            prev_masked = not prev_masked
    boundaries.append(len(seq))
    return (first_masked, boundaries)


def split_from_boundaries(record, boundaries):
    """
    Split a sequence record into parts based on boundaries.

    Parameters
    ----------
        record
            A sequence record
        boundaries
            Boundaries for splitting as returned by `find_boundaries`.
    """
    seq_id = record["id"].split(" ")
    if len(seq_id) > 1:
        name, comment = seq_id
    else:
        name, comment = seq_id[0], ""
    seq = record["seq"]
    qual = record["qual"]
    split_records = []
    for i, end in enumerate(boundaries):
        if i == 0:
            continue
        start = boundaries[i - 1]
        split_seq = seq[start:end]
        if qual is not None:
            split_qual = qual[start:end]
        else:
            split_qual = None
        split_id = f"{name}_part{i} {comment}"
        split_records.append(new_record(split_id, split_seq, split_qual))
    return split_records


def distribute_split(records, first_masked):
    """
    Distribute split records into buckets of `masked` and `unmasked`.

    Parameters
    ----------
        records : list
            List of split records
        first_masked : bool
            Whether the first record in the list is from a masked segment.

    Returns
    -------
        dict {"masked": list, "unmasked": list}
            The input records classified by whether they were masked or
            unmasked in the original record.
    """
    if first_masked:
        masked = records[0::2]
        unmasked = records[1::2]
    else:
        masked = records[1::2]
        unmasked = records[0::2]

    return {"masked": masked, "unmasked": unmasked}


def split_record(record, is_masked):
    """
    Split a sequence record into parts based on masking status.

    Parameters
    ----------
        record
            A sequence record
        is_masked : callable
            Takes one argument (a letter from `seq`) and returns `True` if the
            letter is masked and `False` if it is unmasked.

    Returns
    -------
        list
            A list of the split records.
    """
    first_masked, boundaries = find_boundaries(record["seq"], is_masked)
    split_records = distribute_split(split_from_boundaries(record, boundaries), first_masked)
    return split_records


def construct_is_masked(maskchar):
    """
    Define a matching function from a masking character.
    """
    if maskchar == "lowercase":
        return lambda x: x.islower()
    elif len(maskchar) > 1:
        raise ValueError("`maskchar` must be a single character of `lowercase`!")
    else:
        return lambda x: x == maskchar


def split_masked(
        infile,
        fh_unmasked,
        fh_masked,
        maskchar,
        minlength_masked,
        minlength_unmasked,
        revert_lowercase):
    """
    Split sequence records based on masking status and write masked and
    undmasked parts to separate output files.
    """
    is_masked = construct_is_masked(maskchar)
    for record in stream_records(infile):
        split_records = split_record(record, is_masked)
        io.write_split_records(
            split_records, fh_masked, fh_unmasked,
            minlength_masked, minlength_unmasked, revert_lowercase)
