import os
from os.path import dirname, realpath, join, exists
import sys
import clr
import abc

SYSTEM_IO_PACKAGING_VERSION = '6.0.0'
AML_ENGINE_VERSION = '2.0.5'
AML_ENGINE_RESOURCES_VERSION = '1.0.0'
AML_ENGINE_SERVICES_VERSION = '2.0.3'
if 'AML_ENGINE_DOTNET_VERSION' in os.environ:
    DOTNET_VERSION = os.environ['AML_ENGINE_DOTNET_VERSION']
else:
    DOTNET_VERSION = 'net48'

if 'SYSTEM_IO_PACKAGING_DOTNET_VERSION' in os.environ:
    PACKAGING_DOTNET_VERSION = os.environ['SYSTEM_IO_PACKAGING_DOTNET_VERSION']
else:
    PACKAGING_DOTNET_VERSION = 'net461'

system_io_packaging_path = join(dirname(realpath(__file__)), 'nuget', 'system.io.packaging.' + SYSTEM_IO_PACKAGING_VERSION, 'lib', PACKAGING_DOTNET_VERSION)
amlengine_path = join(dirname(realpath(__file__)), 'nuget', 'aml.engine.' + AML_ENGINE_VERSION, 'lib', DOTNET_VERSION)
amlengine_resources_path = join(dirname(realpath(__file__)), 'nuget', 'aml.engine.resources.' + AML_ENGINE_RESOURCES_VERSION, 'lib', DOTNET_VERSION)
amlengine_services_path = join(dirname(realpath(__file__)), 'nuget', 'aml.engine.services.' + AML_ENGINE_SERVICES_VERSION, 'lib', DOTNET_VERSION)

sys.path.insert(0, system_io_packaging_path)
sys.path.insert(0, amlengine_services_path)
sys.path.insert(0, amlengine_resources_path)
sys.path.insert(0, amlengine_path)

print(DOTNET_VERSION)
print(PACKAGING_DOTNET_VERSION)
print(sys.path)

# load the AMLEngine dlls
clr.AddReference("System.IO.Packaging")
clr.AddReference("Aml.Engine")
clr.AddReference("Aml.Engine.Services")
