#!/bin/bash
#

python3 src/pharmacy_counting.py -i input/itcont.txt -o output/top_cost_drug.txt

python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_1/input/itcont.txt  -o insight_testsuite/tests/test_1/output/top_cost_drug.txt

python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_2/input/itcont.txt  -o insight_testsuite/tests/test_2/output/top_cost_drug.txt

python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_big/input/de_cc_data_tst.txt  -o insight_testsuite/tests/test_big/output/top_cost_drug_tst.txt

python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_big/input/de_cc_data_10k.txt  -o insight_testsuite/tests/test_big/output/top_cost_drug_10k.txt


python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_big/input/de_cc_data_100k.txt  -o insight_testsuite/tests/test_big/output/top_cost_drug_100k.txt


python3 src/pharmacy_counting.py -i insight_testsuite/tests/test_big/input/de_cc_data_500k.txt  -o insight_testsuite/tests/test_big/output/top_cost_drug_500k.txt

