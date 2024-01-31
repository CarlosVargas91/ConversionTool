# importing required modules 
from PyPDF2 import PdfReader # To extract text from PDF
import re # To run regex
import pandas # To use pandas dataframes
import codecs # To output data as utf-8
import utilities
import headersAndFooters

regex_id_pre = r"\[\s*?SWS\s*_\s*"
regex_id_preCp = r"\[\s*?ECUC_\s*_\s*"
regex_id_post = r"\s*_\s*[0-9]+\s*\]"
regex_startReq = r"^\s+[d⌈]"
regex_startReq23 = r"^\s*"
regex_endReq = r"\s*?[c⌋]\s?\([\s\S]*?\)"

regex_footer = r"(?:\n\s*?5\s*?)?\n\s*?\d+\s+of\s+\d+\s+Document ID"
regex_header = r"(?:Requirements on |Specification of)[\s\S]+?AUTOSAR CP R[\d-]+ *(?:\n\s*4)"

progressBarSize = 50

def convertModule(moduleName, moduleAbbreviation, fileName):
    # Read PDF
    reader = PdfReader('../' + fileName + '.pdf') 

    # Number of pages
    num_pages = len(reader.pages)

    # Print number of pages and number of characters
    # utilities.printInfo('[' + moduleAbbreviation + '] Number of pages: ' + str(num_pages))

    # Initialize empty reqID set
    req_IDs = set()

    # Initialize empty dataset
    ds = list()

    debugList = list()

    # Initialize carry
    carryId = ''
    carryText = ''

    # Initialize removal metrics
    numHeaders = 0
    numHeadersRemoved = 0
    numFooters = 0
    numFootersRemoved = 0
    
    debugPrint = 0

    progressBarValue = 0

    # Loop through all the pages
    for page_number in range(num_pages):
        if not debugPrint:
            if page_number == num_pages-1:
                utilities.printInfo('\r   [' + moduleAbbreviation + '] Processing page ' + str(page_number+1) + ' of ' + str(num_pages), True)
                print('')
            else:
                utilities.printInfo('\r   [' + moduleAbbreviation + '] Processing page ' + str(page_number+1) + ' of ' + str(num_pages), True)

        # Retrieve the page text
        page_text = reader.pages[page_number].extract_text()

        # Retrieve the page size
        page_size = len(page_text)

        # Initialize cursor at 0
        cursor = 0

        while(cursor < page_size):
            
            if debugPrint:
                debugList.append(page_text)
                
            # Check if carry active
            if carryId == '':
                # Look for Req ID in remainder
                x = re.search(regex_id_pre + re.escape(moduleAbbreviation) + regex_id_post, page_text[cursor:])

                if not x:
                    x = re.search(regex_id_preCp + re.escape(moduleAbbreviation) + regex_id_post, page_text[cursor:]) # Workaround for different files

                # Check if found
                if x:
                    # Get req ID and remove spaces
                    req_ID = x.group().replace(' ', '')

                    # Append ID to list
                    req_IDs.add(req_ID)

                    if debugPrint:
                        print('page' + str(page_number+1) + ': id found: ' + req_ID)

                    # Increase cursor by end offset of found group span
                    cursor += x.span()[1]

                    # ID found, look for starting character
                    y = re.search(regex_startReq, page_text[cursor:])

                    # could not find, probably is Autosar 23 document
                    if not y: 
                        y = re.search(regex_startReq23, page_text[cursor:])

                    # Check if found
                    if y:
                        if debugPrint:
                            print('page' + str(page_number+1) + 'start found! ' + str(y.span()))

                        # Reduce remainder by end offset of found group span
                        cursor += y.span()[1]

                        # TODO search for end
                        z = re.search(regex_endReq, page_text[cursor:])

                        # # Check if found
                        if z:
                            if debugPrint:
                                print('page' + str(page_number+1) + 'end found! ' + str(z.span()))
                                print()
                                print(page_text[cursor:cursor+z.span()[0]])
                                print()

                            # Append to dataset
                            ds.append(
                                {
                                    'AUTOSAR ID': req_ID,
                                    'Object Text': req_ID + page_text[cursor:cursor+z.span()[0]]
                                }
                            )

                            # Reduce remainder by end offset of found group span
                            cursor += z.span()[1]
                        else:
                            if debugPrint:
                                print('page' + str(page_number+1) + 'end not found!!!')
                                print(page_text[cursor:])

                            carryId = req_ID
                            carryText = page_text[cursor:]

                            # Remove footer
                            numFooters += 1
                            rmF = re.search(regex_footer, carryText)

                            # Check result of footer removal
                            if rmF:
                                carryText = carryText[:rmF.span()[0]]
                                numFootersRemoved += 1

                            # Stop loop
                            break
                else:
                    # No requirement found anymore, stop loop
                    if debugPrint:
                        print('Could not find an ID ')
                    break
            else:
                # Carry Active, search for end
                z = re.search(regex_endReq, page_text)

                # # Check if found
                if z:
                    # Setup temp variable for post text
                    tempPost = page_text[:cursor+z.span()[0]]

                    if debugPrint:
                        print('page' + str(page_number+1) + 'end found! ' + str(z.span()))
                        print('RAW:')
                        print(carryText)
                        print()
                        print(tempPost)
                        print()

                    # Remove Headers
                    numHeaders += 1
                    rmH = re.search(regex_header, tempPost)

                    # Check result of header removal
                    if rmH:
                        tempPost = tempPost[rmH.span()[1]:]
                        numHeadersRemoved += 1

                    if debugPrint:
                        print('FIXED:')
                        print(carryText + tempPost)
                        print()

                    # Append to dataset
                    ds.append(
                        {
                            'AUTOSAR ID': carryId,
                            'Object Text': req_ID + carryText + tempPost
                        }
                    )

                    # Reduce remainder by end offset of found group span
                    cursor += z.span()[1]

                    # Reset carry
                    carryId = ''
                    carryText = ''
                else:
                    if debugPrint:
                        print('page' + str(page_number+1) + 'end not found!!!')

                    tempText = page_text

                    # Remove Headers
                    numHeaders += 1
                    rmH = re.search(regex_header, tempText)

                    # Check result of header removal
                    if rmH:
                        tempText = tempText[rmH.span()[1]:]
                        numHeadersRemoved += 1

                    # Remove footer
                    numFooters += 1
                    rmF = re.search(regex_footer, tempText)

                    # Check result of footer removal
                    if rmF:
                        tempText = tempText[:rmF.span()[0]]
                        numFootersRemoved += 1

                    # Append to carryText
                    carryText = carryText + tempText

                    # Continue search on next page
                    utilities.printError('END not found on new page, continue search on next page...')
                    break

    with open('debugPrint.txt', 'w', encoding="utf-8-sig") as f:
        for item in debugList:
            f.write(item)

    # Convert dataset to dataframe
    df = pandas.DataFrame(ds)

    # Get sizes
    num_reqIDs = len(req_IDs)
    num_reqs = len(df)

    # Print number of requirements found
    utilities.printInfo('[' + moduleAbbreviation + '] Number of requirement defined/referenced: ' + str(num_reqs) + '/' + str(num_reqIDs))

    # Cross check initial value
    crossCheckNum = 0

    # utilities.printInfo('[' + moduleAbbreviation + '] Starting Crosscheck...')

    # Perform cross check by looking for all requirement id's in the dataframe
    for req_id in req_IDs:
        if req_id in df['AUTOSAR ID'].values:
            crossCheckNum += 1
        else:
            utilities.printError('[' + moduleAbbreviation + '] No requirement definition found for ' + req_id)

    # Print crosscheck result based on number
    if crossCheckNum == num_reqIDs:
        utilities.printSuccess('[' + moduleAbbreviation + '] Crosscheck PASSED (' + str(crossCheckNum) + '/' + str(num_reqIDs) + ')')
    else:
        utilities.printError('[' + moduleAbbreviation + '] Crosscheck FAILED (' + str(crossCheckNum) + '/' + str(num_reqIDs) + ')')

    df.to_csv(fileName + '.csv', encoding="utf-8-sig", index=False)

    utilities.printInfo('[' + moduleAbbreviation + '] Exported to ' + fileName + '.csv')

    # print(df)