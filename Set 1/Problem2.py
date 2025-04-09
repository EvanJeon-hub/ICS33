class Album:
    def __init__(self, artist):
        self._artist = artist
        self._songs = []

    def artist(self):
        return self._artist

    def songs(self):
        return self._songs

    def add_song(self, song):
        self._songs.append(song)

# The problem with this code is that _songs is defined as a class variable.
# Therefore, _songs will include all instances for a1 and a2.
# As a solution, _song should be stated as self._songs = [] in __init__ function
# in order to prevent storing songs with the wrong artist.
