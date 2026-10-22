from pathlib import Path

from escape.testkit import Fail, check_call, data_file, need_function, scratch_path, write_file

LEDGER_ENTRIES = [
    ("1891-01-03", "candles", 12),
    ("1891-01-05", "coal", 40),
    ("1891-01-09", "bread", 7),
    ("1891-02-11", "candles", 8),
    ("1891-02-14", "coal", 35),
    ("1891-02-20", "ink", 3),
    ("1891-03-02", "candles", 15),
    ("1891-03-08", "bread", 9),
]


def test_count_lines(s):
    """count_lines counts every line of the ledger"""
    check_call(s, "count_lines", data_file("ledger.txt"), 12)


def test_count_lines_other_files(s):
    """count_lines works on other files too"""
    check_call(s, "count_lines", write_file("two.txt", "first\nsecond"), 2)
    check_call(s, "count_lines", write_file("empty.txt", ""), 0)


def test_read_entries(s):
    """read_entries reads every entry as (date, item, amount)"""
    check_call(s, "read_entries", data_file("ledger.txt"), LEDGER_ENTRIES)


def test_read_entries_other_file(s):
    """read_entries skips comments and blanks in another file"""
    path = write_file("small.txt", "# just a comment\n\n1900-01-01 , soap , 4\n")
    check_call(s, "read_entries", path, [("1900-01-01", "soap", 4)])


def test_total_spent(s):
    """total_spent adds up one item"""
    ledger = data_file("ledger.txt")
    check_call(s, "total_spent", (ledger, "coal"), 75)
    check_call(s, "total_spent", (ledger, "candles"), 35)
    check_call(s, "total_spent", (ledger, "ink"), 3)


def test_total_spent_missing(s):
    """total_spent is 0 for something never bought"""
    check_call(s, "total_spent", (data_file("ledger.txt"), "gold"), 0)


def test_write_report(s):
    """write_report writes the totals in alphabetical order"""
    func = need_function(s, "write_report")
    report = scratch_path("report.txt")
    func(data_file("ledger.txt"), report)
    if not Path(report).exists():
        raise Fail("write_report didn't create the report file. Open it with `open(report_filename, \"w\")`.")
    lines = Path(report).read_text(encoding="utf-8").splitlines()
    wanted = ["bread: 16", "candles: 35", "coal: 75", "ink: 3"]
    if [line.strip() for line in lines if line.strip()] != wanted:
        raise Fail("The report should contain these lines:\n{}\nbut it contains:\n{}".format(
            "\n".join(wanted), "\n".join(lines) or "(nothing)"))
