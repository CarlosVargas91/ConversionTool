# importing required modules 
from PyPDF2 import PdfReader # To extract text from PDF
import re # To run regex
import pandas # To use pandas dataframes
import codecs # To output data as utf-8
import utilities
import headersAndFooters

# Module structure
Module = namedtuple("Module", ["name", "reqname"])

# Module Name
modules = [
    Module('DiagnosticCommunicationManager', 'Dcm'),
    Module('ADCDriver', 'Adc'),
    Module('DIODriver', 'Dio'),
    Module('FlashDriver', 'Fls'),
    Module('IOHWAbstraction', 'IoHwAb'),
    Module('PortDriver', 'Port'),
    Module('PWMDriver', 'Pwm'),
    Module('XCP', 'Xcp'),
]

# Regex patterns
regexStrUtf8 = r"\n[0-9. ]*(\[SWS_[\S\s]*?\])\s*([\S\s]*?)\s*\n{0,1}⌈\s*\n([\S\s]*?)\n⌋\([\s\S]*?\)"
regexStrNonUtf8 = r"\n[0-9. ]*(\[SWS_[\S\s]*?\])\s*([\S\s]*?)\s*\n{0,1}d\s*\n([\S\s]*?)\nc\([\s\S]*?\)"

# Loop through all modules
for curModule in modules:
    moduleName = curModule.name
    # Construct Filename
    fileName = 'AUTOSAR_SWS_' + moduleName

    utilities.printHeader('[' + curModule.reqname + '] Start processing ' + fileName + '.pdf')

    # Read PDF
    reader = PdfReader('../' + fileName + '.pdf') 

    # Initialize output text
    text = ""

    # Number of pages
    num_pages = len(reader.pages)

    # Loop through all the pages
    for page_number in range(num_pages):
        # Retrieve the page
        page = reader.pages[page_number]
        # Append the text
        text += page.extract_text()

    # Print number of pages and number of characters
    utilities.printInfo('[' + curModule.reqname + '] Number of pages: ' + str(num_pages) + ', number of characters: ' + str(len(text)))



    headersAndFooters.remove(text, curModule.reqname, num_pages)





    # print(text)

    # Write text to output txt for debugging
    file = codecs.open("text_" + moduleName + ".txt", "w", "utf-8")
    file.write(text)
    file.close()


    # Regex find all SWS ID's of this module
    req_IDs = re.findall(r"\[\s*?SWS\s*_\s*" + re.escape(curModule.reqname) + "\s*_\s*[0-9]+\s*\]", text)

    # Remove all spaces from SWS ID's
    req_IDs = [sub.replace(' ', '') for sub in req_IDs]

    # Remove duplicates
    req_IDs = list(set(req_IDs)) 

    # Sort the list
    req_IDs.sort()

    # Get number of unique req IDs
    num_reqIDs = len(req_IDs)
    # print(req_IDs)

    # Check results
    regqIDs_print = '[' + curModule.reqname + '] Number of requirement tags found: ' + str(num_reqIDs)
    if num_reqIDs > 0:
        utilities.printSuccess(regqIDs_print)
    else:
        utilities.printError(regqIDs_print)

    # Regex find all SWS Requirement blocks
    r1 = re.findall(regexStrUtf8, text)

    print('test1')

    if len(r1) <= 1:
        r1 = re.findall(regexStrNonUtf8, text)

        

    print('test2')

    # print(r1)

    # r1 = re.findall(r"\n[0-9. ]*(\[[\S\s]*?\])\s*([\S\s]*?)\s*\n⌈\s*\n([\S\s]*?)\n⌋", text) # WORKS FOR DIODriver
    # r1 = re.findall(r"\n(\[SWS_.*\])\s*?([ \n\S]*?)d\n(Description[ \n\S]*?\nc\(.*\))", text) # WORKS FOR ADCDriver

    # Setup Pandas Dataframe
    # df = pandas.DataFrame(r1)
    df = pandas.DataFrame(r1, columns=['AUTOSAR ID', 'Object Text', 'AUTOSAR Details'])

    
    print('test3')

    # Clear all newlines from requirement itself
    for ind in df.index:
        # TODO Remove any whitespace from ID
        df['AUTOSAR ID'][ind] = df['AUTOSAR ID'][ind].replace(" ", "")

        # First replace "-/n" with "",
        # Second replace "/n" with " ",
        # Finally strip leading and trailing whitespace
        df['Object Text'][ind] = df['Object Text'][ind].replace("-\n", "").replace("\n", " ").strip()

    # print(df)

    # Get number of requirements in dataframe
    num_reqs = len(df)

    # Check results
    df_print = '[' + curModule.reqname + '] Number of requirements defined: ' + str(num_reqs) + ' of ' + str(num_reqIDs)
    if num_reqs == num_reqIDs:
        utilities.printSuccess(df_print)
    else:
        utilities.printError(df_print)

    # Cross check initial value
    crossCheckNum = 0

    # Perform cross check by looking for all requirement id's in the dataframe
    for req_id in req_IDs:
        if req_id in df['AUTOSAR ID'].values:
            crossCheckNum += 1

    # Print crosscheck result based on number
    if crossCheckNum == num_reqIDs:
        utilities.printSuccess('[' + curModule.reqname + '] Crosscheck PASSED (' + str(crossCheckNum) + '/' + str(num_reqIDs) + ')')
    else:
        utilities.printError('[' + curModule.reqname + '] Crosscheck FAILED (' + str(crossCheckNum) + '/' + str(num_reqIDs) + ')')

    # print(num_reqs)

    # df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
    df.to_csv(fileName + '.csv', index=False)

    utilities.printHeader('[' + curModule.reqname + '] Done processing ' + fileName + '.pdf')
    print()