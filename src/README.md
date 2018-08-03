This is the directory where your source code would reside.

Drug is the primary index, patient name is the secondary index,
the goal is to calculate/sort cost

I choose a nested dict as the data structure to store information,
as shown in the below example

drug_map = {
    'CHLORPROMAZINE': {
        'MARIA:RODRIGUEZ': 2000.0, 
        'JAMES:JOHNSON': 1000.0
    }, 
    'AMBIEN': {
        'JAMES:SMITH': 100.0, 
        'MARIA:GARCIA': 200.0
    }, 
    'BENZTROPINE MESYLATE': {
        'DAVID:SMITH': 1500.0
    }
}

I have tested code for up to 500k line of data and found its performance scales linearly.
see my analysis in "docs" sub-folder using a jupyter notebook.


