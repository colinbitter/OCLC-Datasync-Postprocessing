import pandas as pd
from bookops_worldcat import WorldcatAccessToken
import glob
import numpy as np

token = WorldcatAccessToken(
    key="InsertKey",
    secret="InsertSecret",
    scopes=["WorldCatMetadataAPI"],
    principal_id="InsertPrincipal_ID",
    principal_idns="InsertPrincipal_idns")

from bookops_worldcat import MetadataSession
session = MetadataSession(authorization=token) #can change timeout here if needed

#locate downloads folder
from pathlib import Path
downloads_path = str(Path.home() / "Downloads")
path1 = downloads_path
#import text file (datasync report) from downloads folder
allFiles = glob.glob(path1 + "/*.txt")
#create dataframe from text file
data_df = pd.DataFrame()
list_ = []
for file_ in allFiles:
    data_df = pd.read_csv(file_, sep="|", names=['DATASYNC', 'MMSID', 'FILEINPUT', 'FILEOUTPUT', 'ACTION'])

#find null returned values (if any) in OCLC report, replace with sent values
data_df['FILEOUTPUT']= np.where(data_df['FILEOUTPUT'].isnull(), data_df['FILEINPUT'], data_df['FILEOUTPUT'])
data_df['FILEOUTPUT']= data_df['FILEOUTPUT'].astype(np.int64)

#compare input and output in the OCLC report
data_df['FILEMATCH'] = (data_df['FILEINPUT'] == data_df['FILEOUTPUT'])

#establish values for query
df1 = data_df['FILEOUTPUT']

#query WorldCat for OCLC# and holdings status
dff3 = []
dff4 = []
with MetadataSession(authorization=token) as session:
    for x in df1:
        result = session.holding_get_status(oclcNumber=x)
        result2 = result.json()['content']
        df = pd.json_normalize(result2)
        dff1 = df['currentOclcNumber']
        dff2 = df['holdingCurrentlySet']
        for i in dff1:
            dff3.append(i)
        df4 = pd.DataFrame(dff3)
        for i in dff2:
            dff4.append(i)
        df5 = pd.DataFrame(dff4)

#add values to dataframe
data_df['BATCH'] = df4
data_df['BATCH'] = pd.to_numeric(data_df['BATCH'])
data_df['ORIGBATCHMATCH'] = (data_df['FILEINPUT'] == data_df['BATCH'])
data_df['NEWBATCHMATCH'] = (data_df['FILEOUTPUT'] == data_df['BATCH'])
data_df['HELD'] = df5

#output to csv
data_df.to_csv(path1 + "/oclc_result.csv", index=False)
