import pandas as pd
from bookops_worldcat import WorldcatAccessToken
import glob
import numpy as np
from bookops_worldcat import MetadataSession
from pathlib import Path
import os
import time

token = WorldcatAccessToken(
    key="InsertKey",
    secret="InsertSecret",
    scopes=["WorldCatMetadataAPI"],
    principal_id="InsertPrincipal_ID",
    principal_idns="InsertPrincipal_idns")

# locate downloads folder
path1 = str(Path.home() / "Downloads")
# import text file (datasync report) from downloads folder
allFiles = glob.glob(path1 + "/*.txt")
# create dataframe from text file
for file_ in allFiles:
    fileName = os.path.basename(file_)
    fileName = os.path.splitext(fileName)[0]
    data_df = pd.read_csv(file_, sep="|", names=['DATASYNC', 'MMSID', 'FILEINPUT', 'FILEOUTPUT', 'ACTION'])

# find null returned values (if any) in OCLC report, replace with sent values
    data_df['FILEOUTPUT'] = np.where(data_df['FILEOUTPUT'].isnull(), data_df['FILEINPUT'], data_df['FILEOUTPUT'])
    data_df['FILEOUTPUT'] = data_df['FILEOUTPUT'].astype(np.int64)

    # compare input and output in the OCLC report
    data_df['FILEMATCH'] = (data_df['FILEINPUT'] == data_df['FILEOUTPUT'])

    # establish values for query
    df1 = data_df['FILEOUTPUT']

    # query WorldCat for OCLC# and holdings status
    dff3 = []
    dff4 = []
    with MetadataSession(authorization=token, timeout=20) as session:
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

    # add values to dataframe
    data_df['BATCH'] = df4
    data_df['BATCH'] = pd.to_numeric(data_df['BATCH'])
    data_df['ORIGBATCHMATCH'] = (data_df['FILEINPUT'] == data_df['BATCH'])
    data_df['NEWBATCHMATCH'] = (data_df['FILEOUTPUT'] == data_df['BATCH'])
    data_df['HELD'] = df5
    allTrue = data_df[(data_df['FILEMATCH'] == True) & (data_df['ORIGBATCHMATCH'] == True) &
                      (data_df['NEWBATCHMATCH'] == True) & (data_df['HELD'] == True)].index
    data_df.drop(allTrue, inplace=True)
# output
    if data_df.empty is False:
        data_df.to_csv(path1 + '/oclc_result_{}.csv'.format(fileName), index=False)
    if data_df.empty is True:
        print(fileName + ' is clear')
    time.sleep(130)
c = input("press close to exit")
