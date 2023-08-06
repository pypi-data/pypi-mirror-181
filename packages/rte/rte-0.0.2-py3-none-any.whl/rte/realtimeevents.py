from venv import create
from xml.etree.ElementTree import SubElement
from reahl.web.libraries import Library
from reahl.web.fw import UserInterface, Url
from reahl.web.layout import PageLayout, Footer
from reahl.web.bootstrap.page import HTML5Page
from reahl.web.bootstrap.ui import P, HTMLElement, Img, Div, H, A, Ul, Li, Widget, Meta
from reahl.web.bootstrap.navs import Nav, TabLayout, PillLayout, DropdownMenu, NavLayout
from reahl.web.bootstrap.carousel import Carousel
from reahl.web.holder.holder import PlaceholderImage, PredefinedTheme, CustomTheme
from reahl.component.modelinterface import EmailField, Field
from reahl.web.bootstrap.grid import ColumnLayout, ColumnOptions, ResponsiveSize, Container
from reahl.domain.systemaccountmodel import LoginSession
# from reahl.domainui.bootstrap.accounts import AccountUI
from reahl.web.bootstrap.navbar import Navbar, ResponsiveLayout
from accounts import AccountUI


class BaseLayout(HTML5Page):
    def __init__(self, view, bookmarks):
        super().__init__(view)
        self.bookmarks = bookmarks
        self.head.add_child(Meta(view, 'viewport', 'width=device-width, initial-scale=1'))

        self.use_layout(PageLayout(document_layout=Container(fluid=True)))
        self.layout.header.add_child(self.create_navbar(view))

        self.layout.footer.add_child(FooterWidget(view))

    def create_contents(self, view):
        contents_layout = Div(view).use_layout(Container())
        contents_colums = ColumnLayout(ColumnOptions('main', size=ResponsiveSize(md=12))).with_slots()
        contents_layout.add_child(Div(view).use_layout(contents_colums))
        return contents_layout

    def create_navbar(self, view):
        navbar_container = Div(view).use_layout(Container())
        navbar = Navbar(view, css_id='home-navbar')
        navbar.use_layout(ResponsiveLayout('md', collapse_brand_with_content=False, colour_theme='light', bg_scheme=None))
        navbar.layout.set_brand_text('Real Time Events')
        menu = Nav(view).use_layout(TabLayout(content_justification='fill')).with_bookmarks(self.bookmarks['home'])

        menu.add_dropdown("Executives", self.create_sub_menu_on_nav(self.bookmarks['other_pages']['exec']))
        menu.add_dropdown("Commissions", self.create_sub_menu_on_nav(self.bookmarks['other_pages']['comm']))
        menu.add_dropdown("Committees", self.create_sub_menu_on_nav(self.bookmarks['other_pages']['commit']))

        structure_sub_menu = DropdownMenu(view)
        for bookmark in self.bookmarks['structure']: 
            structure_sub_menu.add_bookmark(bookmark)
        menu.add_dropdown('Structures', structure_sub_menu)

        menu.add_bookmark(self.bookmarks['account'][0]).append_class('login-button')
        navbar.layout.add(menu)
        navbar_container.add_child(navbar)

        return navbar_container

    def create_sub_menu_on_nav(self, pages):
        menu = DropdownMenu(self.view)
        # menu.add_header(H(self.view, '3', 'Executives'))
        for bookmark in pages:
            menu.add_bookmark(bookmark)
        return menu


class DefaultContnentsLayout(BaseLayout):
    def __init__(self, view, bookmarks):
        super().__init__(view, bookmarks=bookmarks)
        # The homepage needs a different layout. This is to add the caroucel :(
        if view.relative_path == '/':
           self.layout.contents.add_child(HomePage(view))
        else:
            contents_layout = Div(view).use_layout(Container())
            contents_colums = ColumnLayout(ColumnOptions('main', size=ResponsiveSize(md=12))).with_slots()
            contents_layout.add_child(Div(view).use_layout(contents_colums))
            self.layout.contents.add_child(contents_layout) 



class HomePage(Widget):
    def __init__(self, view):
        super(HomePage, self).__init__(view)
        self.add_child(self.create_carousel(view))
        container = self.add_child(self.create_layout(view))

        container.add_child(HomePageSection(view, 'Notices'))
        for i in range (1, 5):
            container.add_child(NoticeEntry(view))
        container.add_child(HomePageSection(view, 'Recent Articles'))
        for i in range (1, 5):
            container.add_child(NoticeEntry(view))
        container.add_child(HomePageSection(view, 'Upcoming Tournaments'))


    def create_carousel(self, view):
            carousel = Carousel(view, 'my_carousel_id', show_indicators=False)
            carousel.add_control(previous=True)
            # carousel.add_control()
            carousel.add_slide(PlaceholderImage(view, 800, 700, text='Placeholder image', theme=PredefinedTheme('lava')))
            carousel.add_slide(PlaceholderImage(view, 800, 700, text='Another placeholder', theme=CustomTheme(bg='00216f', fg='ffffff')))
            carousel.add_slide(PlaceholderImage(view, 800, 700, text='Use an Img here', theme=PredefinedTheme('industrial')))
            return carousel
    
    def create_layout(self, view):
        contents_layout = Div(view).use_layout(Container())
        # contents_colums = ColumnLayout(ColumnOptions('main', size=ResponsiveSize(md=3))).with_slots()
        # contents_layout.add_child(Div(view).use_layout(contents_colums))
        return contents_layout


class HomePageSection(Widget):
    def __init__(self, view, text):
        super(HomePageSection, self).__init__(view)
        self.div = self.add_child(Div(view))
        self.div.add_child(H(view, '3', text=text))
        self.div.append_class('homepage-section')

    
class NoticeEntryWidget(Widget):
    def __init__(self, view):
        super(NoticeEntryWidget, self).__init__(view)
        self.div = self.add_child(Div(view))
        self.div.append_class('notice-entry')
        # self.div.append_class('card')
        # self.div.append_class('card-exhibit-meduim')

class NoticeEntry(NoticeEntryWidget):
    def __init__(self, view):
        super().__init__(view)
        # self.div = self.add_child(Div(view))
        self.div.add_child(P(view, text='this is a test'))


class LegalNotice(P):
    def __init__(self, view, text, name):
        super().__init__(view, text=text, css_id=name)
        self.set_as_security_sensitive()



class StructureWidget(HTMLElement):
    def __init__(self, view):
        super().__init__(view, tag_name='structure_page', children_allowed=True)
        self.add_child(P(view, text='this is a place holder for ... '))
        self.add_child(P(view, text='this is a place holder for some more ... '))


class StructureProvincesWidget(StructureWidget):
    def __init__(self, view):
        super().__init__(view)
        self.div.add_child(P(view, text='this is the provinces page '))


class StructureRegionWidget(StructureWidget):
    def __init__(self, view):
        super().__init__(view)
        self.add_child(P(view, text='THIS IS SOME OTHER WIDGET :0 '))


class PlaceHolderWidget(Div):
    def __init__(self, view):
        super().__init__(view)
        self.add_child(P(view, text='[ this is simply a place holder ]'))


class FooterWidget(Widget):
    def __init__(self, view, css_id=None):
        super().__init__(view, css_id)
        self.main_footer_div = self.add_child(Div(view))
        self.main_footer_div.use_layout(Container())
        foot_layout = ColumnLayout(ColumnOptions('footer_left', ResponsiveSize(md=6)), ColumnOptions('footer_right', ResponsiveSize(md=6)))
        self.main_footer_div.add_child(Div(view).use_layout(foot_layout))
        foot_layout.columns['footer_left'].add_child(FooterWidgetAboutUs(view))
        foot_layout.columns['footer_right'].add_child(FooterWidgetContactUs(view))


class FooterWidgetAboutUs(Widget):
    def __init__(self, view, css_id=None):
        super().__init__(view, css_id)
        about_us_footer = "Chess South African is about the administration, \
        development and coordination of all chess activities within South Africa \
        in all areas such as coaching organising and playing whether at International, \
        Provincial, Regions, Clubs and Schools. \n \
        The Federation is actively involved from grassroots development to \
        Elite Chess in all 9 Provinces with the assistance of it's 9 Provincial members. \n \
        Chess South African is a affiliated to the Africa Chess Confederation (ACC) \
        and the International Chess Federation (FIDE), the Olympic Committee (SASCOC) \
        and recognised by Sport and Recreation South Africa (SRSA)."

        self.add_child(H(view, text='About Us', priority='4'))
        self.add_child(P(view, text=about_us_footer))

class FooterWidgetContactUs(Widget):
    def __init__(self, view, css_id=None):
        super().__init__(view, css_id)
        contact_us_footer = "Email, facebook, blah blah"

        self.add_child(H(view, text='Contact Us', priority='4'))
        self.add_child(P(view, text=contact_us_footer))
        self.add_child(A(view, Url('https://chessa.co.za/ratingsdatabase/ratingsdatabase.aspx'), 'Rating Database'))


class CompiledBootstrap(Library):
    def __init__(self):
        super().__init__('custom')
        self.egg_name = 'rte'
        self.shipped_in_directory = 'dist'
        self.files = [
                      'theme.css',
                      'main.js',
                      ]


class RealTimeEventsUI(UserInterface):
    def assemble(self):
        login_session = LoginSession.for_current_session()
        if login_session.account:
            logged_in_as = login_session.account.email
        else:
            logged_in_as = 'Guest'

        home = self.assemble_home()
        structure = self.assemble_structure()
        execu = self.assemble_executives()
        commit = self.assemble_committee()
        comm = self.assememble_commissions()

        terms_of_service = self.define_view('/terms_of_service', title='Terms of service')
        terms_of_service.set_slot('main', LegalNotice.factory('The terms of servies defined as ...', 'terms'))

        privacy_policy = self.define_view('/privacy_policy', title='Privacy policy')
        privacy_policy.set_slot('main', LegalNotice.factory('You have the right to remain silent ...', 'privacypolicy'))

        disclaimer = self.define_view('/disclaimer', title='Disclaimer')
        disclaimer.set_slot('main', LegalNotice.factory('Disclaim ourselves from negligence ...', 'disclaimer'))

        class LegalBookmarks:
            terms_bookmark = terms_of_service.as_bookmark(self)
            privacy_bookmark = privacy_policy.as_bookmark(self)
            disclaimer_bookmark = disclaimer.as_bookmark(self)

        accounts = self.define_user_interface('/accounts', AccountUI,
                                      {'login_main': 'main'},
                                      name='accounts', bookmarks=LegalBookmarks)
        

        account_bookmarks = [accounts.get_bookmark(relative_path=relative_path) 
                             for relative_path in ['/login', '/register', '/registerHelp', '/verify']]

        bookmarks = {'home': home, 
                     'structure': structure, 
                     'account': account_bookmarks,
                     'other_pages': {
                        'exec': execu,
                        'commit': commit,
                        'comm': comm
                        }
                    }

        self.define_page(DefaultContnentsLayout, bookmarks)


    def assemble_home(self):
        home = self.define_view('/', title='Home')
        # home.set_slot('main', HomePage.factory())
        documents = self.define_view('/documents', title='Documents')
        documents.set_slot('main', P.factory(text='Welcome to documents'))

        return [v.as_bookmark(self) for v in [home, documents]]

    def assemble_structure(self):
        structure_provinces = self.define_view('/structure/provinces', title='Provinces')
        structure_provinces.set_slot('main', StructureRegionWidget.factory())
        structure_regions = self.define_view('/structure/regions', title='Regions')
        structure_regions.set_slot('main', Img.factory(src="https://image.spreadshirtmedia.net/image-server/v1/mp/products/T1459A839PA4459PT28D180843796W6682H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/looney-tunes-bugs-bunny-kopf-vintage-sticker.jpg", alt="Some alternative text"))
        structure_clubs = self.define_view('/structure/clubs', title='Clubs')
        structure_clubs.set_slot('main', StructureWidget.factory())
        return [v.as_bookmark(self) for v in [structure_provinces, structure_clubs, structure_regions]]

    def assemble_executives(self):
        executives_provincial = self.define_view('/executives/provincial', title='Provincial')
        executives_regional = self.define_view('/executives/regional', title='Regional')
        return [v.as_bookmark(self) for v in [executives_provincial, executives_regional]]

    def assemble_committee(self):
        commit_appeals = self.define_view('/committee/appeals', title='Appeals')
        commit_consti = self.define_view('/committee/constitution', title='Constitutional')
        commit_dev = self.define_view('/committee/development', title='Development')
        commit_ethics = self.define_view('/committee/ethics', title='Ethics')
        commit_events = self.define_view('/committee/events', title='Events')
        commit_fin = self.define_view('/committee/fin', title='Finance')
        commit_grief = self.define_view('/committee/grievance', title='Grievance')
        commit_nat_sel = self.define_view('/committee/nat-selections', title='National Selections')
        commit_public_rel = self.define_view('/committee/public-relations', title='Public Relations')
        commit_quali = self.define_view('/committee/qulifications', title='Qualifications')
        commit_ratings = self.define_view('/committee/ratings-relations', title='Ratings & Registrations')
        commit_trans = self.define_view('/committee/transformations', title='Transformation')
        return [v.as_bookmark(self) for v in [commit_appeals, commit_consti, commit_dev, commit_ethics,
                                       commit_events, commit_fin, commit_grief, commit_nat_sel, 
                                       commit_public_rel, commit_quali, commit_ratings, commit_trans]]


    def assememble_commissions(self):
        comm_adult = self.define_view('/comm/adult', title='Adult Chess')
        comm_artibers_org = self.define_view('/comm/arbiters', title='Arbiters & Organisers')
        comm_phy_chall = self.define_view('/comm/physically-challenged', title='Physically Challenged')
        comm_players = self.define_view('/comm/players', title='Players')
        comm_trainers_managers = self.define_view('/comm/trainers-managers', title='Trainers & Mangers')
        comm_youth = self.define_view('/comm/youth', title='Youth Chess')
        comm_women = self.define_view('/comm/women', title='Women Chess')        
        return [v.as_bookmark(self) for v in [comm_adult, comm_artibers_org, comm_phy_chall,
                                              comm_players, comm_trainers_managers,
                                              comm_youth, comm_women]]


