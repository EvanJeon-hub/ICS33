# p2app/engine/main.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

import sqlite3
from p2app.events.database import (OpenDatabaseEvent, CloseDatabaseEvent,
                                   DatabaseOpenedEvent, DatabaseClosedEvent,
                                   DatabaseOpenFailedEvent)
from p2app.events.continents import (StartContinentSearchEvent, ContinentSearchResultEvent,
                                     LoadContinentEvent, ContinentLoadedEvent,
                                     SaveContinentEvent, SaveNewContinentEvent,
                                     ContinentSavedEvent, SaveContinentFailedEvent)
from p2app.events.countries import (StartCountrySearchEvent, CountrySearchResultEvent,
                                        LoadCountryEvent, CountryLoadedEvent,
                                        SaveCountryEvent, SaveNewCountryEvent,
                                        CountrySavedEvent, SaveCountryFailedEvent)


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.db_path = None
        self.connection = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        if isinstance(event, OpenDatabaseEvent):
            path = event.path()
            try:
                connection = sqlite3.connect(path)
                connection.execute('SELECT * FROM sqlite_master')
                self.connection = connection
                self.db_path = path
                yield DatabaseOpenedEvent(path)

                if isinstance(event, StartContinentSearchEvent):
                    continent_code = event.continent_code()
                    name = event.name()
                    cursor = self.connection.cursor()
                    cursor.execute('SELECT * FROM continents WHERE continent_code=? AND name=?', (continent_code, name))
                    result = cursor.fetchone()
                    if result:
                        continent = Continent(result[0], result[1], result[2])
                        yield ContinentSearchResultEvent(continent)

                if isinstance(event, LoadContinentEvent):
                    continent_id = event.continent_id()
                    cursor = self.connection.cursor()
                    cursor.execute('SELECT * FROM continents WHERE continent_id=?', (continent_id,))
                    result = cursor.fetchone()
                    if result:
                        continent = Continent(result[0], result[1], result[2])
                        yield ContinentLoadedEvent(continent)






            except sqlite3.Error as e:
                yield DatabaseOpenFailedEvent(str(e))

        if isinstance(event, CloseDatabaseEvent):
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
            yield DatabaseClosedEvent()

        else:
            yield from ()

