# ensure the package is loaded correctly and the required DLLs are registered with pythonnet
print('before import')
import amlengine
print('after import')

# depending on what functionalities you want to use
from Aml.Engine import *
from Aml.Engine.CAEX import *
from Aml.Engine.CAEX.Extensions import *
from Aml.Engine.AmlObjects import *
from Aml.Engine.AmlObjects.Extensions import *
from Aml.Engine.Services import *
from Aml.Engine.Adapter import *

# access to the native .Net API
aml_file = CAEXDocument.New_CAEXDocument(CAEXDocument.CAEXSchema.CAEX2_15)

print('amlengine successfully imported')