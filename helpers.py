import logging, os

from bs4 import BeautifulSoup
import bs4  # for assertions


log = logging.getLogger(__name__)


def load_xml( filepath ):
    assert type(filepath) == str
    log.debug( f'filepath, ``{filepath}``' )
    assert os.path.exists( filepath )
    xml = None
    with open( filepath, encoding='utf-8' ) as f:
        xml = f.read()
    assert type(xml) == str
    soup = BeautifulSoup( xml, 'xml' )
    assert type(soup) == bs4.BeautifulSoup
    return soup



    # ## load up english xml-object --------------------------
    # english_xml_path = os.path.abspath( './source_xml_files/engDecameron.xml' )
    # log.debug( f'english_xml_path, ``{english_xml_path}``' )
    # assert os.path.exists( english_xml_path )
    # #
    # english_xml = None
    # with open( english_xml_path, encoding='utf-8' ) as f:
    #     english_xml = f.read()
    #     log.debug( f'type(english_xml), ``{type(english_xml)}``' )
    # assert type(english_xml) == str
    # #
    # english_soup = BeautifulSoup( english_xml, 'xml' )
    # assert type(english_soup) == bs4.BeautifulSoup
