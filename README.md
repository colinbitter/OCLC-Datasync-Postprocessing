# OCLC-Datasync-Postprocessing

OCLC-Datasync-Postprocessing.py targets text files in the downloads folder in windows. All text files in the folder will be processed. The program is intended for use with the bibliographic processing report (BibProcessingReport.txt).<br/><br/>OCLC-Datasync-Postprocessing.py retrieves the most recent OCLC# from WorldCat using bookops-worldcat, checks if the record is held by your institution, and then makes comparisons between the OCLC#s in each column. If all records are held by your institution and all OCLC#s match within each record, then no action is taken. If a record is unheld, or if any OCLC#s do not match, then the results are output to csv.
Contact OCLC to set up the WorldCat Metadata API for use with bookops-worldcat.
