import re # To run regex
import utilities

def remove(text, moduleName, num_pages):
    # Remove Headers
    resultRemoveHeaders = re.subn("(?:Requirements on |Specification of)[\s\S]+?AUTOSAR CP R[\d-]+ *", "", text)

    # Use result
    text = resultRemoveHeaders[0]

    # Check results
    resultRemoveHeaders_print = '[' + moduleName + '] Headers removed: ' + str(resultRemoveHeaders[1]) + ' of ' + str(num_pages)
    if resultRemoveHeaders[1] == num_pages:
        utilities.printSuccess(resultRemoveHeaders_print)
    elif (num_pages - resultRemoveHeaders[1]) == 1:
        utilities.printWarning(resultRemoveHeaders_print)
    else:
        utilities.printError(resultRemoveHeaders_print)



    # Remove Footers
    # resultRemoveFooters = re.subn("5\n[\S\n\t ]*?4\n", "", text)
    resultRemoveFooters = re.subn("(?:\n\s*?5\s*?){0,1}\n\s*?\d+\s+of\s+\d+\s+Document ID[\s\S]*?\n", "", text)

    # Use result
    text = resultRemoveFooters[0]

    # Check results
    resultRemoveFooters_print = '[' + moduleName + '] Footers removed: ' + str(resultRemoveFooters[1]) + ' of ' + str(num_pages)
    if resultRemoveFooters[1] == num_pages:
        utilities.printSuccess(resultRemoveFooters_print)
    elif (num_pages - resultRemoveFooters[1]) == 1:
        utilities.printWarning(resultRemoveFooters_print)
    else:
        utilities.printError(resultRemoveFooters_print)

    return text