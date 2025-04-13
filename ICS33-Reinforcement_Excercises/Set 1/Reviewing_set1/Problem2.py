class Album:
    _songs = []

    def __init__(self, artist):
        self._artist = artist

    def artist(self):
        return self._artist

    def songs(self):
        return self._songs

    def add_song(self, song):
        self._songs.append(song)

a1 = Album('U2')
a1.add_song('Zoo Station')
a1.add_song('The Fly')
print(a1.songs())
a2 = Album('Bruce Hornsby')
a2.add_song('Circus on the Moon')
print(a2.songs())

# Nothing ever assigned a value into self._songs, which means that Album objects never have their own _songs attribute.
# Consequently, any time we access the value of self._songs,
# we're accessing the same class attribute, no matter what Album it is.