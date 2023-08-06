# Python AML.Engine

This provides access to the .Net implementation of the [AML.Engine](https://github.com/AutomationML/AMLEngine2.1) - an API for simple access to AutoamtionML files.

Access to the functionalities of the .Net dlls is provided via the [pythonnet](https://pythonnet.github.io/) package.

Besides the access to the native API of the AML.Engine, the package also contains some additional helper functions implemented in Python that are available via the *amlhelper* module.

## Usage

```python
# ensure the package is loaded correctly and the required DLLs are registered with pythonnet
import amlengine

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

```

### .Net version

By default, the DLLs compiled for .Net Framework 4.8 are used. However, using another version provided by the AML.Engine is also possible. Therefore, set the environment variable *AML_ENGINE_DOTNET_VERSION* to one of the following values before importing the *amlengine*:
 - net5.0
 - net6.0
 - net48 (default)
 - netcoreapp3.1