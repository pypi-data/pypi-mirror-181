'''Demo REST API to do enquiries of the details of a country.

The strange name comes from the name of an entity and  helmsman whois also
a navigator hence looking for details of a country.  The strange name  also
contribute to finding a unique name on yPI and at the same time not squatting
useful names on the public domain.
'''
import json
from webob.exc import HTTPForbidden

from reahl.web.fw import UserInterface, CheckedRemoteMethod, JsonResult
from reahl.component.modelinterface import Field, EmailField
from reahl.component.exceptions import AccessRestricted
from reahl.web.bootstrap.page import HTML5Page
from reahl.web.bootstrap.ui import P, Ul, Li
from reahl.domain.systemaccountmodel import (
    AccountManagementInterface,
    LoginSession,
    EmailAndPasswordSystemAccount,
)
from reahl.sqlalchemysupport import Session, Base
from sqlalchemy import Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class CountryCurrency(Base):
    """
    Define the many-to-many relationship between Country and Currency.

    :param country_id: country.id from country table
    :param currency_id: curency.id from currency table
    """

    __tablename__ = 'country_currency'

    country_id = Column(Integer, ForeignKey('country.id'), primary_key=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), primary_key=True)


class Country(Base):
    """
    Country table definition.

    :param cca2: Country code alpha of length 2 (unique)
    :param cca3: Country code alpha of length 3 (unique)
    :param name_common: Country common name
    :param active: Soft delete of the country. True wil remove the country
     form displasy, but not physically delete the record.
    """

    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    cca2 = Column(String(2), unique=True)
    cca3 = Column(String(3), unique=True)
    name_common = Column(String(100))
    active = Column(Boolean)

    # many to many Country<->Currency
    currencies = relationship(
        'Currency', secondary="country_currency", viewonly=True
    )  # , overlaps="currencies")

    def __init__(self, cca2, cca3, name_common, active):
        self.cca2 = cca2
        self.cca3 = cca3
        self.name_common = name_common
        self.active = active

    def __str__(self):
        return f"<Country(id = {self.id}, cca3 = {self.cca3}, \
            cca2 = {self.cca2}, name_common = {self.name_common}, \
            name_common = {self.name_common} \
            active = {self.active}"

    def __repr__(self):
        return f"Country({self.cca2}, {self.cca3}, {self.name_common}, {self.active})"


class Currency(Base):
    """
    Currency table definition.

    :param curr_iso: Three digit iso currency code.
    :param name: Currency description
    :param symbol: Currency symbol
    """

    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    curr_iso = Column(String(3), unique=True)
    name = Column(String(50))
    symbol = Column(String(25))
    # many to many Country<->Currency
    countries = relationship(
        'Country', secondary='country_currency', viewonly=True
    )  # , overlaps="currencies")

    def __init__(self, curr_iso, name, symbol):
        self.curr_iso = curr_iso
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"<Currency(curr_iso = {self.curr_iso}, name = {self.name}"

    def __repr__(self):
        return f"Country({self.curr_iso}, {self.name}, {self.symbol})"


class JsonField(Field):
    """
    Process the inputs and outputs to the API from JSON to Python dict and vica-versa.
    """

    def parse_input(self, unparsed_input):
        """
        Parse input from the caller

        :param unparsed_input: JSON string received from sender
        :return: str with the contents.
        """
        return json.loads(unparsed_input if unparsed_input != '' else 'null')

    def unparse_input(self, parsed_value):
        """
        Un-parse input from the caller.

        :param parsed_input: JSON string received from sender
        :return: str with the contents.
        """
        return json.dumps(parsed_value)


class CheckedRemoteMethod2(CheckedRemoteMethod):
    def handle_get_or_post(self, request, input_values):
        try:
            return super().handle_get_or_post(request, input_values)
        except AccessRestricted as e:
            raise HTTPForbidden(str(e))


class APIPage(HTML5Page):
    """ """

    def __init__(self, view):
        super().__init__(view)
        methods = [
            # CheckedRemoteMethod2(
            #         view, 'create_country', self.create_country,
            #         JsonResult(JsonField()), disable_csrf_check=True,
            #         cca3 = Field(),
            #         cca2 = Field(),
            #         name_common = Field(),
            #         curr_iso = Field()
            # ),
            CheckedRemoteMethod2(
                view,
                'add_country',
                self.add_country,
                JsonResult(JsonField()),
                disable_csrf_check=True,
                cca2=Field(),
                cca3=Field(),
                name_common=Field(),
            ),
            CheckedRemoteMethod2(
                view,
                'delete_country',
                self.delete_country,
                JsonResult(JsonField()),
                disable_csrf_check=True,
                cca=Field(),
            ),
            CheckedRemoteMethod2(
                view,
                'find_country',
                self.find_country,
                JsonResult(JsonField()),
                immutable=True,
                disable_csrf_check=True,
                cca=Field(),
            ),
            CheckedRemoteMethod2(
                view,
                'list_countries',
                self.list_countries,
                JsonResult(JsonField()),
                immutable=True,
                disable_csrf_check=True,
                curr_iso=Field(),
            ),
            CheckedRemoteMethod(
                view,
                'log_in',
                self.log_in,
                JsonResult(JsonField()),
                disable_csrf_check=True,
                user_name=EmailField(),
                password=Field(),
            ),
        ]

        self.add_child(P(view, text='This is the ProdigyHelmsman API. Methods:'))
        self.add_child(Ul(view))
        for method in methods:
            view.add_resource(method)
            self.add_child(Li(view)).add_child(
                P(
                    view,
                    text='%s [%s]: %s'
                    % (method.name, method.http_methods, method.get_url()),
                )
            )

    def add_country(self, cca2=None, cca3=None, name_common=None):
        """
        Add country to database.  If the country already exists by previous
        soft delete, it will set the "active" flag and update teh rest of
        the attributes.

        :param cca2: 2 digit alpha for the respective country being added.
        :param cca3: 3 digit alpha for the respective country being added.
        :param name_common: Common name of country.

        :return: {}
        """
        # print(cca2, cca3, name_common)
        # import pdb; pdb.set_trace()
        if cca2 and cca3 and name_common:
            country = Session.query(Country).filter_by(cca2=cca2).first()
            if country:
                country.active = True
            else:
                Session.add(
                    Country(cca2=cca2, cca3=cca3, name_common=name_common, active=True)
                )
        return {}

    def can_access_api(self):
        """
        Determine if the caller can access (authenticated) API.

        :return: True or False
        """
        login_session = LoginSession.for_current_session()
        return login_session.is_logged_in()

    def delete_country(self, cca=None):
        """
        Soft delete from the country record from database.  The "active"
        flag of the table will be set false.

        :param cca: 2 or 3 digit alpha for the respective country being deleted.

        :return: {}
        """
        if cca:
            country = None
            if len(cca) == 2:
                country = Session.query(Country).filter_by(cca2=cca).first()
            elif len(cca) == 3:
                country = Session.query(Country).filter_by(cca3=cca).first()
            if country:
                country.active = False
        return {}

    def find_country(self, cca=None):
        """
        Find a country in the country table with either the 2 or 3 digit alpha code.

        :param cca: 2 or 3 digit alpha for the respective country being enquired on.
        :return: cca3, cca2, name_common
        """
        # import pdb;pdb.set_trace()
        if len(cca) == 2:
            country = (
                Session.query(Country)
                .filter(Country.cca2 == cca, Country.active == True)  # noqa
                .first()
            )
        else:
            country = (
                Session.query(Country)
                .filter(Country.cca3 == cca, Country.active == True)  # noqa
                .first()
            )
        if country:
            return [
                {
                    'cca3': country.cca3,
                    'cca2': country.cca2,
                    'name_common': country.name_common,
                }
            ]
        return []

    def list_countries(self, curr_iso=None):
        """
        Find the details of all the countries.  If the curr_iso parameter
        is set, it will find the countries with that specific currency.

        :param curr_iso: Currency tto filter on.

        :return: cca, cca2, name_common, curr_iso
        """
        countries_data = []
        if curr_iso:
            rows = (
                Session.query(Country, Currency)
                .filter(
                    CountryCurrency.country_id == Country.id,
                    CountryCurrency.currency_id == Currency.id,
                    Currency.curr_iso == curr_iso,
                    Country.active == True,  # noqa
                )
                .order_by(Country.name_common)
                .all()
            )
        else:
            rows = (
                Session.query(Country, Currency)
                .filter(
                    CountryCurrency.country_id == Country.id,
                    CountryCurrency.currency_id == Currency.id,
                    Country.active == True,  # noqa
                )
                .order_by(Country.name_common)
                .all()
            )
        for det in rows:
            countries_data.append(
                {
                    'cca3': det.Country.cca3,
                    'cca2': det.Country.cca2,
                    'name_common': det.Country.name_common,
                    'curr_iso': det.Currency.curr_iso,
                }
            )
        return countries_data

    def log_in(self, user_name=None, password=None):
        """
        AUthenticate the session.

        :param user_name:  Existing user_name.
        :param password: Pasword of the user.

        :return: True or False
        """
        AccountManagementInterface.for_current_session()
        # print(f'logging in with {user_name}[{password}]')
        EmailAndPasswordSystemAccount.log_in(user_name, password, False)
        return self.can_access_api()


class APIUI(UserInterface):
    def assemble(self):
        self.define_view('/api', title='API', page=APIPage.factory())
