import pymongo

"""Models data from a MongoDB

This class is a self-training assignment in Python and for use in a course
dealing with MongoDB. This class will allow for the creation of easy to use
objects to interact with data stored in a MongoDB server.

"""

class BasicModel(object):
    """Models data from a MongoDB

    This class is a self-training assignment in Python and for use in a course
    dealing with MongoDB. This class will allow for the creation of easy to use
    objects to interact with data stored in a MongoDB server.

    """

    def __init__(self, data={}, collection="trashbin", db="test", 
                 host="localhost", safe_conn=False):
        """Initalize the Model

        Initialize data on the object, also builds the DB connection information
        for the model. The model __init__ accepts a named collection and db 
        parameters to specify where the data is stored in the database.
        
        """
        self._conn = pymongo.Connection("mongodb://%s" % host, safe=safe_conn)
        self._db = self._conn[db]
        self._collection = self._db[collection]
        self._data = data
        self.new = True
        self.loaded = False
        self.modified = False

    def load(self, query, override=False):
        """Load Model data from the Database based on the given query.

        Load data into this Model from a pre-existing record in the Database. This
        method returns a boolean value representing it's succes, also found on 
        model.loaded.

        If this Model has already been loaded (model.loaded == True), then the 
        optional named parameter "override" is required to reload this Model with 
        new data otherwise an AlreadyLoadedError will be raised.
        
        """ 
        if self.loaded and not override:
            raise AlreadyLoadedError("This model has already been loaded "
                                     "from the database")
        document = self._collection.find_one(query)
        if document is not None:
            self._data = document
            self.loaded = True
            self.new = False
        return self.loaded

    def save(self):
        """Insert or Update the model based on if it's a new Model

        This method will insert or update, dependiong on whether this is a new
        model or a pre-existing model. This method will also only save if data
        has been changed.
        
        """
        if not self.modified: return
        if self.new:
            self._collection.insert(self._data)
            self.new = False
        else:
            self._collection.update({ "_id": self.get("_id") }, self._data)
        self.modified = False

    def set(self, new_props, value=None):
        """Set properties, via a dict or prop, value, arguments

        This is the perferred method for altering Data on the Model as it plugs
        into some higher level features like "model.modifed"
        
        """
        if type(new_props) is str: 
            self._data[new_props] = value
            self.modified = True
        elif type(new_props) is dict:
            for key in new_props:
                self._data[key] = new_props[key]
                self.modified = True
        else:
            raise InvalidArgumentError("set expects new_props to be a string "
                                       "or dict")

    def _get_prop(self, prop):
        """Iternal get function for fetching properties"""
        if prop in self._data:
            return self._data[prop]
        elif hasattr(self, "_defaults") and prop in self._defaults:
            self.set(prop, self._defaults[prop])
            return self._data[prop]
        else:
            return None

    def get(self, *args):
        """Get properties from this Model

        This should be the preferred method for accessing properties to make
        it more clear the approach. This method can take a single property to
        fetch or multiple properties to fetch (which returns a list)
        
        """
        if len(args) == 1:
            prop = args[0]
            return self._get_prop(prop)      
        elif len(args) > 1:
            ret_list = []
            for prop in args:
              ret_list.append(self._get_prop(prop))
            return ret_list
        else:
            raise InvalidArgumentError("get required at least one argument"
                                           "to fetch a property") 

    def remove(self, *args):
        """Delete properties from the Model

        This will permanently remove properties and their values from the
        Model as well as mark it as modified.
        
        """
        for prop in args:
            if prop in self._data:
                del self._data[prop]
                self.modified = True

class InvalidArgumentError(Exception):
    """Invalid Arguments Passed to a function"""

class AlreadyLoadedError(Exception):
    """Model has already been loaded and override=True was not given"""
