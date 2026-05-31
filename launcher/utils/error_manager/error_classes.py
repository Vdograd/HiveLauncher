class DataBaseError(Exception): # Code 1001
    def __init__(self, error: Exception | None = None): ...

class MinecraftError(Exception): ... # Code 2001

class UserNotFoundError(DataBaseError): ... # Code 1002
class NotCorrectPasswordError(DataBaseError): ... # Code 1003
class UserAlreadyExistsError(DataBaseError): ... #Code: 1004
class UserAlreadyAddedError(DataBaseError): ... #Code: 1005

class ModLoaderError(MinecraftError): ... # Code 2010
class ForgeLoaderError(ModLoaderError): ... # Code 2011
class FabricLoaderError(ModLoaderError): ... # Code 2012

class ForgeInstallError(ForgeLoaderError): ... # Code 2013
class ForgeStartError(ForgeLoaderError): ... # Code 2014

class FabricInstallError(FabricLoaderError): ... # Code 2015
class FabricStartError(FabricLoaderError): ... # Code 2016

class MinecraftInstallError(MinecraftError): ... # Code: 2002
class MinecraftStartError(MinecraftError): ... # Code: 2003
