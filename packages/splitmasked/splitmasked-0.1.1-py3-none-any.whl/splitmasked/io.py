# io.py

# Utilities for input/output operations.

from streamseqs import format_record, new_record

def filter_and_format(record, min_length, revert_lowercase):
    if min_length > 0 and len(record["seq"]) < min_length:
        return ""
    if revert_lowercase:
        record["seq"] = record["seq"].upper()
    return format_record(record)


def write_split_records(
        split_record,
        fh_unmasked,
        fh_masked,
        minlength_masked,
        minlength_unmasked,
        revert_lowercase):
    if fh_masked:
        for record in split_record["masked"]:
            fh_masked.write(filter_and_format(record, minlength_masked, revert_lowercase))
    if fh_unmasked:
        for record in split_record["unmasked"]:
            fh_unmasked.write(filter_and_format(record, minlength_unmasked, False))
