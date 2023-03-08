"""
This class is used to set the program version. It's useful because, once modified the program version in this file, all the other parts of the program will receive the modification.
"""
class Version:
    def __init__(self):
        self.version = '0.9.0'

    """
    @return the program version
    """
    def getVersion(self):
        return self.version

    """
    @return the program major version
    """
    def getMajorVersion(self):
        return self.version.split('.')[0]

    """
    @return the program minor version
    """
    def getMinorVersion(self):
        return self.version.split('.')[1]

    """
    @return the program patch version
    """
    def getPatchVersion(self):
        return self.version.split('.')[2]

    """
    @param version: a version to compare
    @return True if the program version is older than the given version. False otherwise.
    """
    def olderThan(self, version):
        version = version.split('.')
        given_major = int(version[0])
        given_minor = int(version[1])
        given_patch = int(version[2])

        using_major = int(self.getMajorVersion())
        using_minor = int(self.getMinorVersion())
        using_patch = int(self.getPatchVersion())

        if given_major > using_major:
            return True
        elif given_major == using_major and given_minor > using_minor:
            return True
        elif given_major == using_major and given_minor == using_minor and given_patch > using_patch:
            return True

        return False
