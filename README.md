# OCLC-Datasync-Postprocessing

OCLC-Datasync-Postprocessing.py targets text files in the downloads folder in windows. The first text file in the folder will be processed. The program is intended for use with the bibliographic processing report (BibProcessingReport.txt).<br/><br/>OCLC-Datasync-Postprocessing.py retrieves the most recent OCLC# from WorldCat using bookops-worldcat, checks if the record is held by your institution, and then makes comparisons between the OCLC#s in each column.
Contact OCLC to set up the WorldCat Metadata API for use with bookops-worldcat.
