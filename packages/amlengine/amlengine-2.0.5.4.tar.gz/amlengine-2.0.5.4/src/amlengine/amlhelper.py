from datetime import datetime
from io import BufferedIOBase
from logging import getLogger
import warnings
import clr

from Aml.Engine import *
from Aml.Engine.CAEX import *
from Aml.Engine.CAEX.Extensions import *
from Aml.Engine.AmlObjects import *
from Aml.Engine.AmlObjects.Extensions import *
from Aml.Engine.Services import *
from Aml.Engine.Adapter import *

try:
    # required for operation with Mono on Beantalk
    clr.AddReference("System.Memory")
except Exception:
    pass

clr.AddReference("System.Xml")
clr.AddReference("System.IO")
from System.Xml import *
from System.IO import *

logging = getLogger(__name__)


def create_aml_document(file_name, writer_name, writer_id, version='1.0', release='1.0.0'):
    """
    This function creates and returns a new instance of Aml.Engine.CAEX.CAEXDocument. The CAEX version of the file
    will be set to 2.15.

    :param str file_name: The file name to set
    :param str writer_name: The writer name to set in the meta information of the document
    :param str writer_id: The writer ID to set in the meta information of the document
    :param str version: The version to set in the meta information of the document
    :param str release: The release to set in the meta information of the document
    :return: An instance of Aml.Engine.CAEX.CAEXDocument
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        aml_file = CAEXDocument.New_CAEXDocument(CAEXDocument.CAEXSchema.CAEX2_15)

    set_meta_information(aml_file, file_name, writer_name, writer_id, version, release)

    aml_file.CAEXFile.FileName = file_name
    return aml_file


def save_to_bytes(caex_document, pretty_print=False):
    """
        Save the given instance of Aml.Engine.CAEX.CAEXDocument to a 'bytes' object.

        :param caex_document: An instance of Aml.Engine.CAEX.CAEXDocument
        :param pretty_print:
        :return: An instance of bytes
        """
    return bytes(caex_document.SaveToStream(pretty_print).ToArray())


def load_aml_document(path_or_bytes):
    """
    Loads and returns an AML document

    :param str path_or_bytes: The path to a stored AML document, a file-like object or a byte array
    :return: An instance of Aml.Engine.CAEX.CAEXDocument
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            if isinstance(path_or_bytes, str):
                return CAEXDocument.LoadFromFile(path_or_bytes)
            elif isinstance(path_or_bytes, BufferedIOBase):
                content = path_or_bytes.read()
                return CAEXDocument.LoadFromBinary(content)
            else:
                return CAEXDocument.LoadFromBinary(path_or_bytes)
        except Exception as e:
            raise FileNotFoundError(e)


def set_meta_information(caex_document, writer_project, writer_name, writer_id, version='1.0', release='1.0.0'):
    """
    This function sets the meta information required from AutomationML standard. If meta information about the same
    writer_id already exists, this meta information is replaced.

    :param CAEXDocument caex_document: The instance of Aml.Engine.CAEX.CAEXDocument for which the meta information shall
    be set
    :param str writer_project: The writer project title/ID to set
    :param str writer_name: The writer name to set
    :param str writer_id: The writer ID to set
    :param str version: The version to set
    :param str release: The release to set
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        AmlObjectsExtensions.SetMetaInformation(caex_document.CAEXFile, writer_name, writer_id, "Festo AG & Co. KG",
                                                "www.festo.com", version, release, datetime.now().isoformat(),
                                                writer_project, writer_project)


def import_aml_contents(from_object, to_object, import_instance_hierarchies=True, import_suc_libs=True,
                        import_rc_libs=True, import_if_libs=True, overwrite=False):
    """
    Merges the AML contents (IHs, SUCLibs, RCLibs, and/or IFLibs) of a given AML document into another AML document.
    Unless 'overwrite' is set to 'True', existing instance hierarchies or libraries in the 'target_file' are not
    overwritten.

    Note: Both 'from_object' and 'to_object' need to be either paths to an AML document or instances
    of # 'Aml.Engine.CAEX.CAEXDocument' (the type representing an AML document). 'from_object' can also be a list of
    paths or # instances. In that case, the contents of all objects will be merged.

    :param from_object: Either an instance of Aml.Engine.CAEX.CAEXDocument, a string representing a path to an AML file
    or a list of instances of Aml.Engine.CAEX.CAEXDocument or paths to AML files
    :param to_object: Either an instance of Aml.Engine.CAEX.CAEXDocument or a string representing a path to an AML file
    :param bool import_instance_hierarchies: Whether InstanceHierarchies shall be imported
    :param bool import_suc_libs: Whether SystemUnitClassLibraries shall be imported
    :param bool import_rc_libs: Whether RoleClassLibraries shall be imported
    :param bool import_if_libs: Whether InterfaceLibraries shall be imported
    :param bool overwrite: Whether existing IHs, SUCLibs, RCLibs, and/or IFLibs with the same name shall be overwritten
    """
    if isinstance(from_object, list):
        for single_from_object in from_object:
            import_aml_contents(single_from_object, to_object, import_instance_hierarchies, import_suc_libs,
                                import_rc_libs, import_if_libs, overwrite)

    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            if isinstance(from_object, str):
                file_to_merge_object = load_aml_document(from_object).CAEXFile
            else:
                file_to_merge_object = from_object.CAEXFile

            if isinstance(to_object, str):
                target_file_object = load_aml_document(to_object).CAEXFile
            else:
                target_file_object = to_object.CAEXFile

            if import_instance_hierarchies:
                existing_ih_names = \
                    [existing_ih.Name for existing_ih in AMLEngineAdapter.InstanceHierarchies(target_file_object)]
                for ih in AMLEngineAdapter.InstanceHierarchies(file_to_merge_object):
                    if ih.Name in existing_ih_names:
                        if overwrite:
                            logging.info('AML Helper: Overwriting existing Instance Hierarchy %s during merging!',
                                         ih.Name)
                            target_file_object.InstanceHierarchy.Insert(ih)
                        else:
                            logging.info('AML Helper: Skipping import of Instance Hierarchy %s. Already exists!',
                                         ih.Name)
                    else:
                        logging.info('AML Helper: Instance Hierarchy %s imported during merging.', ih.Name)
                        target_file_object.InstanceHierarchy.Insert(ih)

            if import_suc_libs:
                existing_suc_lib_names = \
                    [existing_lib.Name for existing_lib in AMLEngineAdapter.SystemUnitClassLibraries(target_file_object)]
                for suc_lib in AMLEngineAdapter.SystemUnitClassLibraries(file_to_merge_object):
                    if suc_lib.Name in existing_suc_lib_names:
                        if overwrite:
                            logging.info('AML Helper: Overwriting existing SUC Library %s during merging!',
                                         suc_lib.Name)
                            target_file_object.SystemUnitClassLib.Insert(suc_lib)
                        else:
                            logging.info('AML Helper: Skipping import of SUC Library %s. Already exists!', suc_lib.Name)
                    else:
                        logging.info('AML Helper: SUC Library %s imported during merging.', suc_lib.Name)
                        target_file_object.SystemUnitClassLib.Insert(suc_lib)

            if import_rc_libs:
                existing_rc_lib_names = \
                    [existing_lib.Name for existing_lib in AMLEngineAdapter.RoleClassLibraries(target_file_object)]
                for rc_lib in AMLEngineAdapter.RoleClassLibraries(file_to_merge_object):
                    if rc_lib.Name in existing_rc_lib_names:
                        if overwrite:
                            logging.info('AML Helper: Overwriting existing RC Library %s during merging!', rc_lib.Name)
                            target_file_object.RoleClassLib.Insert(rc_lib)
                        else:
                            logging.info('AML Helper: Skipping import of RC Library %s. Already exists!', rc_lib.Name)
                    else:
                        logging.info('AML Helper: RC Library %s imported during merging.', rc_lib.Name)
                        target_file_object.RoleClassLib.Insert(rc_lib)

            if import_if_libs:
                existing_if_lib_names = \
                    [existing_lib.Name for existing_lib in AMLEngineAdapter.InterfaceClassLibraries(target_file_object)]
                for if_lib in AMLEngineAdapter.InterfaceClassLibraries(file_to_merge_object):
                    if if_lib.Name in existing_if_lib_names:
                        if overwrite:
                            logging.info('AML Helper: Overwriting existing IF Library %s during merging!', if_lib.Name)
                            target_file_object.InterfaceClassLib.Insert(if_lib)
                        else:
                            logging.info('AML Helper: Skipping import of IF Library %s. Already exists!', if_lib.Name)
                    else:
                        logging.info('AML Helper: IF Library %s imported during merging.', if_lib.Name)
                        target_file_object.InterfaceClassLib.Insert(if_lib)


def instantiate_element_by_path(caex_document, path_to_element_to_instantiate, name=None, _id=None, parent=None):
    """
    Creates an instance of the element specified via 'path_to_element_to_instantiate'.

    For example, when 'path_to_element_to_instantiate' points to a SystemUnitClass, an 'InternalElement' will be
    created based on this SUC.

    :param Aml.Engine.CAEX.CAEXDocument caex_document: The CAEXDocument used as starting point to find the element
    represented by 'path_to_element_to_instantiate'
    :param str path_to_element_to_instantiate: The path to the element to instantiate
    (e.g. 'MTPDataObjectSUCLib/DataAssembly')
    :param str name: An optional name to used for the newly created element
    :param str _id: An optional ID to used for the newly created element
    :param Aml.Engine.CAEX.CAEXObject parent: An optional parent element for the new element. If parent is not 'None',
    the newly created element will be inserted in its associated sequence (e.g. in the InternalElement sequence for
    an InternalElement).
    :return: The instantiated element or 'None' if the element could not be created (e.g. because the given path was not
    valid in the context of the given document
    """
    if caex_document is None:
        raise ValueError("AML Helper: Parameter 'caex_document' must not be none!")
    if path_to_element_to_instantiate is None:
        raise ValueError("AML Helper: Parameter 'path_to_element_to_instantiate' must not be none!")

    element_to_instantiate = find_by_path(caex_document, path_to_element_to_instantiate)
    if element_to_instantiate is None:
        logging.error('AML Helper: Unable to instantiate element. Path "%s" not found!', path_to_element_to_instantiate)
        return None
    instance = element_to_instantiate.CreateClassInstance()
    if name is not None:
        instance.Name = name
    if _id is not None:
        instance.ID = str(_id)

    if parent is not None:
        parent.Insert(instance)

    return instance


def instantiate_element_by_type(caex_document, element_type, name=None, _id=None, parent=None):
    """
    Creates an instance of the given element type.

    For example, when 'element_type' is 'Aml.Engine.CAEX.InternalElementType', an 'InternalElement' will be created.

    :param Aml.Engine.CAEX.CAEXDocument caex_document: The CAEXDocument used as starting point to find the element
    represented by 'path_to_element_to_instantiate'
    :param element_type: The type of the element to create
    :param str name: An optional name to used for the newly created element
    :param str _id: An optional ID to used for the newly created element
    :param Aml.Engine.CAEX.CAEXObject parent: An optional parent element for the new element. If parent is not 'None',
    the newly created element will be inserted in its associated sequence (e.g. in the InternalElement sequence for
    an InternalElement).
    :return: The instantiated element or 'None' if the element could not be created (e.g. because the given path was not
    valid in the context of the given document
    """
    if caex_document is None:
        raise ValueError("AML Helper: Parameter 'caex_document' must not be none!")
    if element_type is None:
        raise ValueError("AML Helper: Parameter 'path_to_element_to_instantiate' must not be none!")

    instance = CAEXElementFactory.Create[element_type](caex_document)
    if name is not None:
        instance.Name = name
    if _id is not None:
        instance.ID = str(_id)

    if parent is not None:
        parent.Insert(instance)

    return instance


def find_by_path(caex_document, path):
    """
    Finds and returns an element represented by a given AML path.

    :param Aml.Engine.CAEX.CAEXDocument caex_document: The document in which to search for the element
    :param path: The path representing the element to find
    :return: The found element or 'None'
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return CAEXFileTypeExtensions.FindFastByPath(caex_document.CAEXFile, path, False)


def find_by_id(caex_document, _id):
    """
    Finds and returns an element represented by a given ID.

    :param Aml.Engine.CAEX.CAEXDocument caex_document: The document in which to search for the element
    :param _id: The ID representing the element to find
    :return: The found element or 'None'
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return CAEXFileTypeExtensions.FindFastByID(caex_document.CAEXFile, _id)


def get_attribute_value(caex_object, attribute_name):
    """
    Returns the value of an attribute of a CAEX object

    :param Aml.Engine.CAEX.CAEXObject caex_object:
    :param str attribute_name:
    :return: The attribute value or 'None' if the attribute does not exists or if no value is specified
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return AMLEngineAdapter.GetAttributeValue(caex_object, attribute_name)


def get_attribute(caex_object, attribute_name):
    """
        Returns an attribute of a CAEX object

        :param Aml.Engine.CAEX.CAEXObject caex_object:
        :param str attribute_name:
        :return: The attribute (an instance of Aml.Engine.CAEX.AttributeType)
        """
    for attribute in caex_object.Attribute:
        if attribute.Name == attribute_name:
            return attribute
    logging.debug('AML Helper: Attribute %s not part of CAEX object %s', attribute_name, caex_object)
    return None


def set_attribute(caex_object, attribute_name, attribute_value, attribute_data_type=None,
                  create_if_not_exists=True):
    """
    Sets an attribute in a given CAEXObject

    :param Aml.Engine.CAEX.CAEXObject caex_object:
    :param str attribute_name: The name of the attribute to set
    :param Any attribute_value: The value to set
    :param attribute_data_type: Optionally the data type to set
    :param create_if_not_exists: Whether the attribute shall be created if it does not already exist in the given object
    """
    attribute = get_attribute(caex_object, attribute_name)

    if attribute is None:
        if create_if_not_exists:
            logging.debug('AML Helper: Attribute %s created in CAEX object %s', attribute_name, caex_object)
            attribute = caex_object.Attribute.Append(attribute_name)
        else:
            return

    if attribute_value is not None:
        if isinstance(attribute_value, str):
            attribute.Value = attribute_value
        else:
            attribute.Value = XmlConvert.ToString(attribute_value)

    if attribute_data_type is not None:
        attribute.AttributeDataType = attribute_data_type


def get_instance_hierarchies(caex_document):
    """
    Returns the list of InstanceHierachies defined in the given CAEXDocument

    :param caex_document: An instance of Aml.Engine.CAEX.CAEXDocument or Aml.Engine.CAEX.CAEXFile
    :return:
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if isinstance(caex_document, CAEXDocument):
            return AMLEngineAdapter.InstanceHierarchies(caex_document.CAEXFile)
        elif isinstance(caex_document, CAEXFile):
            return AMLEngineAdapter.InstanceHierarchies(CAEXFile)
        else:
            raise ValueError('Illegal type for parameter "caex_document": %s!', str(type(caex_document)))


def get_descendants(caex_document, element_type):
    """
    Returns the descendants of the given type defined in the given CAEXDocument

    :param caex_document: An instance of Aml.Engine.CAEX.CAEXDocument or Aml.Engine.CAEX.CAEXFile
    :param element_type: The type of descendants to filter
    :return:
    """
    if caex_document is None:
        return []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return CAEXBasicObjectExtensions.Descendants[element_type](caex_document)


def get_parent_object(caex_object):
    """
    Returns the parent object for a given CAEXObject

    :param Aml.Engine.CAEX.CAEXObject caex_object:
    :return:
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return CAEXBasicObjectExtensions.GetParent[CAEXObject](caex_object)


def filter_by_suc(internal_elements, suc, child_sucs=False):
    """
    Returns those of the given internal elements that specify the given suc

    :param internal_elements: The list of elements to filter
    :param suc: The SytemUnitClass (either as object or as string) to filter for
    :param child_sucs: If set to 'True', the filter will also return instances of any child SUCs.
    :return:
    """
    if isinstance(suc, SystemUnitClassType):
        suc = suc.CAEXPath()
    elif not isinstance(suc, str):
        suc = str(suc)

    filtered = []
    for ie in internal_elements:
        ie_suc = get_suc(ie)

        if ie_suc == suc or (child_sucs and ie_suc.startswith(suc)):
            filtered.append(ie)

    return filtered


def get_suc(internal_element):
    try:
        return internal_element.SystemUnitClass.CAEXPath()
    except:
        return internal_element.RefBaseSystemUnitPath


def strip_libraries(from_object):
    """
    Removes all SUCLibs, RCLibs, and ICLibs from  a given AML document.

    Note: 'from_object' needs to be either a path to an AML document or an instance of
    'Aml.Engine.CAEX.CAEXDocument' (the type representing an AML document).

    :param from_object: Either an instance of Aml.Engine.CAEX.CAEXDocument or a string representing a path to an AML
    file
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if isinstance(from_object, str):
            caex_file = load_aml_document(from_object).CAEXFile
        else:
            caex_file = from_object.CAEXFile

        AMLEngineAdapter.SystemUnitClassLibraries(caex_file).Remove()
        AMLEngineAdapter.RoleClassLibraries(caex_file).Remove()
        AMLEngineAdapter.InterfaceClassLibraries(caex_file).Remove()

