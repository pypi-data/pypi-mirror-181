# splitmasked
![pytest-badge](https://github.com/osthomas/splitmasked/actions/workflows/pytest.yaml/badge.svg)

`splitmasked` splits sequence records in FAST(A/Q) files based on their masking
status. What constitutes masking can be defined with the `--maskchar` option
(eg. `N` or `lowercase`). Both masked and unmasked parts can be retained and
written to separate output files.

## Installation

```bash
pip install splitmasked
```

## Usage

```bash
splitmasked \
    --maskchar lowercase \
    --minlength_masked 100 \
    --minlength_unmasked 20 \
    --outfile_masked /dev/null \
    --outfile_unmasked unmasked.fastq \
    input.fastq
```

## Examples

### Input

```
@Seq1 comment1
aaaaaTTTTTTAAgatgatgatgAATGAA
+
AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@Seq2 comment2
ATGATAGAgagagtTTTATA
+
HHHHHHHHHHHHHHHHHHHH
```

### Output

With `--maskchar lowercase`:

**unmasked.fastq**

```
@Seq1_part2 comment1
TTTTTTAA
+
AAAAAAAA
@Seq1_part4 comment1
AATGAA
+
AAAAAA
@Seq2_part1 comment2
ATGATAGA
+
HHHHHHHH
@Seq2_part3 comment2
TTTATA
+
HHHHHH
```

**masked.fastq**

```
@Seq1_part1 comment1
aaaaa
+
AAAAA
@Seq1_part3 comment1
gatgatgatg
+
AAAAAAAAAA
@Seq2_part2 comment2
gagagt
+
HHHHHH
```
