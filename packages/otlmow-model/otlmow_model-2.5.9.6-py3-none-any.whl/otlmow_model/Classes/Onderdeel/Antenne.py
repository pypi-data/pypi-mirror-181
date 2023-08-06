# coding=utf-8
from otlmow_model.BaseClasses.OTLAttribuut import OTLAttribuut
from otlmow_model.Classes.Abstracten.Communicatieapparatuur import Communicatieapparatuur
from otlmow_model.Datatypes.KlAntenneFrequentierange import KlAntenneFrequentierange
from otlmow_model.Datatypes.KlAntenneMerk import KlAntenneMerk
from otlmow_model.Datatypes.KlAntenneModelnaam import KlAntenneModelnaam


# Generated with OTLClassCreator. To modify: extend, do not edit
class Antenne(Communicatieapparatuur):
    """Toestel verbonden met een zender of ontvanger ten behoeve van het opvangen of verspreiden van signalen."""

    typeURI = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Antenne'
    """De URI van het object volgens https://www.w3.org/2001/XMLSchema#anyURI."""

    def __init__(self):
        super().__init__()

        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#BekledingComponent')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#ConstructieElement')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Draagconstructie')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Flitspaal')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Wegkantkast')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Antenne')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#PTRegelaar')
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Verkeersregelaar')

        self._frequentierange = OTLAttribuut(field=KlAntenneFrequentierange,
                                             naam='frequentierange',
                                             label='frequentierange',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Antenne.frequentierange',
                                             definition='Geeft de frequentierange aan waarbinnen de antenne gebruikt kan worden.',
                                             owner=self)

        self._merk = OTLAttribuut(field=KlAntenneMerk,
                                  naam='merk',
                                  label='merk',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Antenne.merk',
                                  definition='Het merk van de antenne.',
                                  owner=self)

        self._modelnaam = OTLAttribuut(field=KlAntenneModelnaam,
                                       naam='modelnaam',
                                       label='modelnaam',
                                       objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Antenne.modelnaam',
                                       definition='De modelnaam/product range van een antenne.',
                                       owner=self)

    @property
    def frequentierange(self) -> str:
        """Geeft de frequentierange aan waarbinnen de antenne gebruikt kan worden."""
        return self._frequentierange.get_waarde()

    @frequentierange.setter
    def frequentierange(self, value):
        self._frequentierange.set_waarde(value, owner=self)

    @property
    def merk(self) -> str:
        """Het merk van de antenne."""
        return self._merk.get_waarde()

    @merk.setter
    def merk(self, value):
        self._merk.set_waarde(value, owner=self)

    @property
    def modelnaam(self) -> str:
        """De modelnaam/product range van een antenne."""
        return self._modelnaam.get_waarde()

    @modelnaam.setter
    def modelnaam(self, value):
        self._modelnaam.set_waarde(value, owner=self)
