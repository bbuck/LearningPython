import pymongo

class Model(object):

  """Initalize the Model

  Initialize data on the object, also builds the DB connection information
  for the model. The model __init__ accepts a named collection and db parameters
  to specify where the data is stored in the database.
  """
  def __init__(self, data = {}, collection = "trashbin", db = "test", host = "localhost", safe_conn = False):
    self.__conn__ = pymongo.Connection("mongodb://%s" % host, safe = safe_conn)
    self.__db__ = self.__conn__[db]
    self.__collection__ = self.__db__[collection]
    self.new = True
    self.__data__ = data
    self.loaded = False
    self.modified = False

  """Load Model data from the Database based on Query

  Load data into this Model from a pre-existing record in the Database. This method
  returns a boolean value representing it's succes, also found on model.loaded.

  If this Model has already been loaded (model.loaded == True), then the optional
  named parameter "override" is required to reload this Model with new data otherwise
  an AlreadyLoadedException will be raised.
  """
  def load(self, query, override = False):
    if self.loaded and not override:
      raise AlreadyLoadedException
    if not self.__collection__:
      return False
    document = self.__collection__.find_one(query)
    if document:
      self.__data__ = document
      self.loaded = True
      self.new = False
    return self.loaded

  """Inserts or Updates a record based on whether or not it's a new Model

  This method will insert or update, dependiong on whether this is a new
  model or a pre-existing model. This method will also only save if data
  has been changed.
  """
  def save(self):
    if not self.modified or not self.__collection__:
      return
    if self.new:
      self.__collection__.insert(self.__data__)
      self.new = False
    else:
      self.__collection__.update({ "_id": self.get("_id") }, self.__data__)
    self.modified = False

  """Set properties, via a dict or prop, value, arguments

  This is the perferred method for altering Data on the Model as it plugs
  into some higher level features like "model.modifed"
  """
  def set(self, newProps, value = None):
    if value: # Assume newProps is string
      self.__data__[newProps] = value
      self.modified = True
    else: # It better be a dict
      for key in newProps:
        self.__data__[key] = newProps[key]
        self.modified = True

  """Iternal get function for fetching properties

  Internal use only
  """
  def _get_prop(self, prop):
    if prop in self.__data__:
      return self.__data__[prop]
    elif hasattr(self, "__defaults__") and prop in self.__defaults__:
      self.set(prop, self.defaults[prop])
      return self.__data__[prop]
    else:
      return None

  """Get properties from this Model

  This should be the preferred method for accessing properties to make
  it more clear the approach. This method can take a single property to
  fetch or multiple properties to fetch (which returns a list)
  """
  def get(self, *args):
    if len(args) == 1:
      prop = args[0]
      return self._get_prop(prop)      
    elif len(args) > 1:
      ret_list = []
      for prop in args:
        ret_list.append(self._get_prop(prop))
      return ret_list
    else:
      raise InvalidArgumentException

  """Delete properties from the Model

  This will permanently remove properties and their values from the
  Model as well as mark it as modified.
  """
  def remove(self, *args):
    for prop in args:
      if prop in self.__data__:
        del self.__data__[prop]
        self.modified = True

class InvalidArgumentException(Exception):
  pass

class AlreadyLoadedException(Exception):
  pass