# p2app/engine/main.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

import sqlite3

from p2app.events.app import QuitInitiatedEvent, EndApplicationEvent, ErrorEvent
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
                connection.execute('PRAGMA foreign_keys = ON;')
                self.connection = connection
                self.db_path = path
                yield DatabaseOpenedEvent(path)

                # Continents.py
                # Search for a continent
                if isinstance(event, StartContinentSearchEvent):
                    try:
                        continent_code = event.continent_code()
                        name = event.name()
                        cursor = self.connection.cursor()
                        cursor.execute('SELECT * FROM continent WHERE continent_code=? AND name=?', (continent_code, name))
                        result = cursor.fetchone()
                        if result:
                            continent = Continent(result[0], result[1], result[2])
                            yield ContinentSearchResultEvent(continent)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                if isinstance(event, LoadContinentEvent):
                    try:
                        continent_id = event.continent_id()
                        cursor = self.connection.cursor()
                        cursor.execute('SELECT * FROM continent WHERE continent_id=?', (continent_id,))
                        result = cursor.fetchone()
                        if result:
                            continent = Continent(result[0], result[1], result[2])
                            yield ContinentLoadedEvent(continent)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                # Update continent
                if isinstance(event, SaveContinentEvent):
                    try:
                        continent = event.continent()
                        cursor = self.connection.cursor()
                        cursor.execute('UPDATE continent SET continent_code=?, name=? WHERE continent_id=?',
                                       (continent.continent_code, continent.name, continent.continent_id))
                        self.connection.commit()
                        yield ContinentSavedEvent(continent)
                    except sqlite3.Error as e:
                        yield SaveContinentFailedEvent(str(e))

                # Add a new continent
                if isinstance(event, SaveNewContinentEvent):
                    try:
                        continent = event.continent()
                        cursor = self.connection.cursor()
                        cursor.execute('INSERT INTO continent (continent_code, name) VALUES (?, ?)',
                                       (continent.continent_code, continent.name))
                        self.connection.commit()
                        yield ContinentSavedEvent(continent)
                    except sqlite3.Error as e:
                        yield SaveContinentFailedEvent(str(e))

                # Countries.py
                # Search for a country
                if isinstance(event, StartCountrySearchEvent):
                    try:
                        country_code = event.country_code()
                        name = event.name()
                        cursor = self.connection.cursor()
                        cursor.execute('SELECT * FROM country WHERE country_code=? AND name=?', (country_code, name))
                        result = cursor.fetchone()
                        if result:
                            country = Country(result[0], result[1], result[2])
                            yield CountrySearchResultEvent(country)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                if isinstance(event, LoadCountryEvent):
                    try:
                        country_id = event.country_id()
                        cursor = self.connection.cursor()
                        cursor.execute('SELECT * FROM country WHERE country_id=?', (country_id,))
                        result = cursor.fetchone()
                        if result:
                            country = Country(result[0], result[1], result[2])
                            yield CountryLoadedEvent(country)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))



            except sqlite3.Error as e:
                yield DatabaseOpenFailedEvent(str(e))

        if isinstance(event, CloseDatabaseEvent):
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
            yield DatabaseClosedEvent()

        if isinstance(event, QuitInitiatedEvent):
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
            yield EndApplicationEvent()

        else:
            yield from ()
