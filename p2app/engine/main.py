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
from p2app.events.regions import (StartRegionSearchEvent, RegionSearchResultEvent,
                                  LoadRegionEvent, RegionLoadedEvent,
                                  SaveRegionEvent, SaveNewRegionEvent,
                                  RegionSavedEvent, SaveRegionFailedEvent)

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

        # User quits the application
        if isinstance(event, QuitInitiatedEvent):
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
            yield EndApplicationEvent()

        # User opens a database file
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
                        # TODO: Debugging
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
                        # TODO: Debugging
                        cursor.execute('SELECT * FROM continent WHERE continent_id=?', (continent_id,))
                        result = cursor.fetchone()
                        if result:
                            continent = Continent(result[0], result[1], result[2])
                            yield ContinentLoadedEvent(continent)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                # Add a new continent
                if isinstance(event, SaveNewContinentEvent):
                    try:
                        continent = event.continent()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('INSERT INTO continent (continent_code, name) VALUES (?, ?)',
                                       (continent.continent_code, continent.name))
                        self.connection.commit()
                        yield ContinentSavedEvent(continent)
                    except sqlite3.Error as e:
                        yield SaveContinentFailedEvent(str(e))

                # Update continent
                if isinstance(event, SaveContinentEvent):
                    try:
                        continent = event.continent()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('UPDATE continent SET continent_code=?, name=? WHERE continent_id=?',
                                       (continent.continent_code, continent.name, continent.continent_id))
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
                        # TODO: Debugging
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
                        # TODO: Debugging
                        cursor.execute('SELECT * FROM country WHERE country_id=?', (country_id,))
                        result = cursor.fetchone()
                        if result:
                            country = Country(result[0], result[1], result[2])
                            yield CountryLoadedEvent(country)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                # Add a new country
                if isinstance(event, SaveNewCountryEvent):
                    try:
                        country = event.country()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('INSERT INTO country (country_code, name) VALUES (?, ?)',
                                       (country.country_code, country.name))
                        self.connection.commit()
                        yield CountrySavedEvent(country)
                    except sqlite3.Error as e:
                        yield SaveCountryFailedEvent(str(e))

                # Update country
                if isinstance(event, SaveCountryEvent):
                    try:
                        country = event.country()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('UPDATE country SET country_code=?, name=? WHERE country_id=?',
                                       (country.country_code, country.name, country.country_id))
                        self.connection.commit()
                        yield CountrySavedEvent(country)
                    except sqlite3.Error as e:
                        yield SaveCountryFailedEvent(str(e))

                # regions.py
                # Search for a region
                if isinstance(event, StartRegionSearchEvent):
                    try:
                        region_code = event.region_code()
                        name = event.name()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('SELECT * FROM region WHERE region_code=? AND name=?', (region_code, name))
                        result = cursor.fetchone()
                        if result:
                            region = Region(result[0], result[1], result[2])
                            yield RegionSearchResultEvent(region)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                # Load a region
                if isinstance(event, LoadRegionEvent):
                    try:
                        region_id = event.region_id()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('SELECT * FROM region WHERE region_id=?', (region_id,))
                        result = cursor.fetchone()
                        if result:
                            region = Region(result[0], result[1], result[2])
                            yield RegionLoadedEvent(region)
                    except sqlite3.Error as e:
                        yield ErrorEvent(str(e))

                # Add a new region
                if isinstance(event, SaveNewRegionEvent):
                    try:
                        region = event.region()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('INSERT INTO region (region_code, name) VALUES (?, ?)',
                                       (region.region_code, region.name))
                        self.connection.commit()
                        yield RegionSavedEvent(region)
                    except sqlite3.Error as e:
                        yield SaveRegionFailedEvent(str(e))

                # Update region
                if isinstance(event, SaveRegionEvent):
                    try:
                        region = event.region()
                        cursor = self.connection.cursor()
                        # TODO: Debugging
                        cursor.execute('UPDATE region SET region_code=?, name=? WHERE region_id=?',
                                       (region.region_code, region.name, region.region_id))
                        self.connection.commit()
                        yield RegionSavedEvent(region)
                    except sqlite3.Error as e:
                        yield SaveRegionFailedEvent(str(e))

            except sqlite3.Error as e:
                yield DatabaseOpenFailedEvent(str(e))

        # User closes the database file
        if isinstance(event, CloseDatabaseEvent):
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_path = None
            yield DatabaseClosedEvent()

        else:
            yield from ()
