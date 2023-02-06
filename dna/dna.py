import csv
import sys


def main():

    # TODO: Check for command-line usage
    n = len(sys.argv)
    if (n != 3):
        print("Correct Usage: python dna.py file.csv sequence.txt")
        exit()

    # TODO: Read database file into a variable

    str = []
    row_count = 0
    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)
        dict_from_csv = dict(list(reader)[0])
        str = list(dict_from_csv.keys())
    str.pop(0)
    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
        row_count = len(data)

    # TODO: Read DNA sequence file into a variable
    f = open(sys.argv[2], "r")
    sequence = f.read()

    # TODO: Find longest match of each STR in DNA sequence
    x = len(str)
    count = []
    for i in range(x):
        y = longest_match(sequence, str[i])
        count.append(y)
    # TODO: Check database for matching profiles
    csv_row = []
    mark = 0
    match = False
    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            csv_row = list(row.values())
            for i in range(len(str)):
                if (int(csv_row[i+1]) == count[i]):
                    mark += 1
                    continue
                else:
                    mark = 0
                    break
            if (mark == len(str)):
                print("Match Found: {}".format(csv_row[0]))
                match = True
        if (match == False):
            print("No Match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

