"""DummyIrodsConnector base

"""


class DummyDataObject():
    def __init__(self, path):
        self._path = path


class DummyCollection():
    class Metadata():
        def get_all(self, key):
            return []
    
    def __init__(self, path):
        self._path = path
        self.metadata = DummyCollection.Metadata()

class DummyIrodsConnector():
    """Create a connection to an iRODS system.

    """
    _ienv = {}
    _password = ''
    _permissions = None
    _resources = None
    _session = None

    def __init__(self, irods_env_file='', password='', irods_auth_file=''):
        """iRODS authentication with Python client.

        Parameters
        ----------
        irods_env_file : str
            JSON document with iRODS connection parameters.
        password : str
            Plain text password.

        """
        self.__name__ = 'DummyIrodsConnector'
        self.irods_env_file = irods_env_file
        if password:
            self.password = password
        self._irods_auth_file = irods_auth_file

    @property
    def davrods(self):
        """DavRODS server URL.

        Returns
        -------
        str
            URL of the configured DavRODS server.

        """
        # FIXME move iBridges parameters to iBridges configuration
        return self.ienv.get('davrods_server', None)

    @property
    def default_resc(self):
        """Default resource name from iRODS environment.

        Returns
        -------
        str
            Resource name.

        """
        return self.ienv.get('irods_default_resource', None)

    @property
    def ienv(self):
        """iRODS environment dictionary.

        Returns
        -------
        dict
            iRODS environment dictionary obtained from its JSON file.

        """
        return self._ienv

    @property
    def password(self):
        """iRODS password.

        Returns
        -------
        str
            iRODS password pre-set or decoded from iRODS authentication
            file.  Can be a PAM negotiated password.

        """
        return self._password

    @password.setter
    def password(self, password):
        """iRODS password setter method.

        Pararmeters
        -----------
        password : str
            Unencrypted iRODS password.

        """
        if password:
            self._password = password

    @password.deleter
    def password(self):
        """iRODS password deleter method.

        """
        self._password = ''

    @property
    def permissions(self):
        """iRODS permissions mapping.

        Returns
        -------
        dict
            Correct permissions mapping for the current server version.

        """
        return self._permissions

    @property
    def resources(self):
        """iRODS resources metadata.

        Returns
        -------
        dict
            Name, parent, status, context, and free_space of all
            resources.

        NOTE: free_space of a resource is the free_space annotated, if
              so annotated, otherwise it is the sum of the free_space of
              all its children.

        """
        return self._resources

    @property
    def session(self):
        """iRODS session.

        Returns
        -------
        iRODSSession
            iRODS connection based on given environment and password.

        """
        return self._session

    def get_user_info(self):
        """Query for user type and groups.

        Returns
        -------
        str
            iRODS user type name.
        list
            iRODS group names.

        """
        user_type = [
        ]
        user_groups = [
        ]
        return user_type, user_groups

    def dataobject_exists(self, path):
        """Check if an iRODS data object exists.

        Parameters
        ----------
        path : str
            Name of an iRODS data object.

        Returns
        -------
        bool
            Existence of the data object with `path`.

        """
        return True

    def collection_exists(self, path):
        """Check if an iRODS collection exists.

        Parameters
        ----------
        path : str
            Name of an iRODS collection.

        Returns
        -------
        bool
            Existance of the collection with `path`.

        """
        return True

    def get_dataobject(self, path):
        """Instantiate an iRODS data object.

        Parameters
        ----------
        path : str
            Name of an iRODS data object.

        Returns
        -------
        iRODSDataObject
            Instance of the data object with `path`.

        """
        return DummyDataObject(path)

    def get_collection(self, path):
        """Instantiate an iRODS collection.

        Parameters
        ----------
        path : str
            Name of an iRODS collection.

        Returns
        -------
        iRODSCollection
            Instance of the collection with `path`.

        """
        return DummyCollection(path)

    @staticmethod
    def is_dataobject(obj):
        """Check if `obj` is an iRODS data object.

        Parameters
        ----------
        obj : iRODS object instance
            iRODS instance to check.

        Returns
        -------
        bool
            If `obj` is an iRODS data object.

        """
        return isinstance(obj, DummyDataObject)

    @staticmethod
    def is_collection(obj):
        """Check if `obj` is an iRODS collection.

        Parameters
        ----------
        obj : iRODS object instance
            iRODS instance to check.

        Returns
        -------
        bool
            If `obj` is an iRODS collection.

        """
        return isinstance(obj, DummyCollection)

    @staticmethod
    def is_dataobject_or_collection(obj):
        """Check if `obj` is an iRODS data object or collection.

        Parameters
        ----------
        obj : iRODS object instance
            iRODS instance to check.

        Returns
        -------
        bool
            If `obj` is an iRODS data object or collection.

        """
        return isinstance(obj, (
            DummyDataObject,
            DummyCollection))

    def addMetadata(self, items, key, value, units=None):
        """
        Adds metadata to all items
        items: list of iRODS data objects or iRODS collections
        key: string
        value: string
        units: (optional) string 

        Throws:
            CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
        """
        pass

    def addMultipleMetadata(self, items, avus):
        return True
        

    def updateMetadata(self, items, key, value, units=None):
        """
        Updates a metadata entry to all items
        items: list of iRODS data objects or iRODS collections
        key: string
        value: string
        units: (optional) string

        Throws: CAT_NO_ACCESS_PERMISSION
        """
        pass

    def deleteMetadata(self, items, key, value, units):
        """
        Deletes a metadata entry of all items
        items: list of iRODS data objects or iRODS collections
        key: string
        value: string
        units: (optional) string

        Throws:
            CAT_SUCCESS_BUT_WITH_NO_INFO: metadata did not exist
        """
        pass
