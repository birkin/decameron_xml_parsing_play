'''
Xml parsing play using BeautifulSoup.
- BeautifulSoup documentation: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>

Setup:
- create a directory 'decameron_xml_parsing_stuff'
- cd into that and run $ python3 -m venv ./env_decameron
- run $ git clone https://github.com/birkin/decameron_xml_parsing_play.git
- run $ source ./env_decameron/bin/activate
- run $ pip install pip --upgrade
- run $ pip install -r ./decameron_xml_parsing_play/requirements.pip

Usage:
- cd into directory 'decameron_xml_parsing_play'
- run $ source ../env_decameron/bin/activate
- run $ python3 ./main.py
'''

import logging, os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers


## set up logging -------------------------------
logging.basicConfig(
    level='DEBUG',
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    )
log = logging.getLogger(__name__)
log.info( '\n\nstarting log\n============' )


## load up xml-objects --------------------------
english_xml_path = os.path.abspath( './source_xml_files/engDecameron.xml' )
log.debug( f'english_xml_path, ``{english_xml_path}``' )
italian_xml_path = os.path.abspath( './source_xml_files/itDecameron.xml' )
log.debug( f'italian_xml_path, ``{italian_xml_path}``' )
english_soup = helpers.load_xml( english_xml_path )
assert type(english_soup) == bs4.BeautifulSoup
italian_soup = helpers.load_xml( italian_xml_path )
assert type(italian_soup) == bs4.BeautifulSoup


## find english prologue ------------------------
english_prologue_results = english_soup.select( 'prologue' )  # select returns multiples
assert type(english_prologue_results) == bs4.element.ResultSet
english_prologue_obj = english_prologue_results[0]
assert type(english_prologue_obj) == bs4.element.Tag
# log.debug( f'english_prologue_obj, ``{english_prologue_obj}``' )


## find milestones in prologue ------------------
prologue_milestones = english_prologue_obj.select('milestone')
assert type(prologue_milestones) == bs4.element.ResultSet
for prologue_milestone_object in prologue_milestones:
    assert type(prologue_milestone_object) == bs4.element.Tag
    mstone_id = prologue_milestone_object['id']
    log.debug( f'mstone_id, ``{mstone_id}``' )


## find all <div2> elements & store dct info ----
div2_results = english_soup.select( 'div2' )
div2_data_info = []
for div2_obj in div2_results:
    assert type(div2_obj) == bs4.element.Tag
    type_attribute = div2_obj['type']
    who = div2_obj['who']
    id_attribute = div2_obj['id']
    heads = div2_obj.select( 'head' )
    log.debug( f'heads, ``{heads}``' )
    head_text = heads[0].text
    div2_truncated_text = div2_obj.text[0:100]
    dct = {
        'id': id_attribute,
        'type': type_attribute,
        'who': who,
        'head_text': head_text,
        'div2_truncated_text': div2_truncated_text + '...'
    }
    div2_data_info.append( dct )
    # log.debug( f'div2_obj, ``{div2_obj}``' )
    log.debug( f'div2-info, ``{pprint.pformat(dct)}``' )
    # break


## build html -----------------------------------

html_soup = BeautifulSoup( '<html><body></body></html>', 'html.parser' )
for entry in div2_data_info:
    assert type(entry) == dict
    log.debug( f'entry, ``{entry}``' )
    item_soup = BeautifulSoup( f'<div id={entry["id"]}></div>', 'html.parser' )
    p_head_tag = item_soup.new_tag( 'p' )
    p_head_tag.string = f'Head: ``{entry["head_text"]}``'
    item_soup.div.append(p_head_tag)
    p_who_tag = item_soup.new_tag( 'p' )
    p_who_tag.string = f'Who ``{entry["who"]}``'
    item_soup.div.append(p_who_tag)
    hr_tag = item_soup.new_tag( 'hr' )
    item_soup.div.append( hr_tag )
    # log.debug( f'item_soup, ``{item_soup}``' )
    # break
    html_soup.body.append( item_soup )

html_output = html_soup.prettify(formatter='html')

html_ouput_path = os.path.abspath( './output_html/output.html' )
with open( html_ouput_path, 'w' ) as f:
    f.write( html_output)

## end ------------------------------------------
