import pytest
from graphspace_python.graphs.classes.gslegend import GSLegend


def test_gslegend():
	test_set_legend_json()
	test_add_legend_entries()
	test_add_invalid_legend_entries()
	test_add_invalid_style_legend_entries()
	test_get_legend_json()
	test_remove_legend_entries()
	test_remove_invalid_legend_entries()
	test_delete_legend_json()
	pass


def test_set_legend_json():
	Ld = GSLegend()

	legend_json = {
	   "legend":{
	        "nodes":{
	            "Source Receptor": {
	                "shape":"triangle",
	                "background-color":"#ff1400"
	            }
	        },
	        "edges":{
	            "Phosphorylation":{
	                "line-color":"#0fcf25",
	                "line-style":"solid",
	                "arrow-shape":"triangle"
	            }
	        }
	    }
	}

	Ld.set_legend_json(legend_json)
	assert legend_json == Ld.legend_json


def test_add_legend_entries():
	expected_legend_json = {'legend':{'nodes': {'Receptor': {'background-color': 'black', 'shape':'star'}}}}
	Ld = GSLegend()
	Ld.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
	assert Ld.legend_json == expected_legend_json


def test_add_invalid_legend_entries():
	Ld = GSLegend()
	style = {'background-color': 'yellow'}
	with pytest.raises(Exception):
		Ld.add_legend_entries('nodes', 'TF', style)


def test_add_invalid_style_legend_entries():
	Ld = GSLegend()
	style = {'background-color': 'yellow', 'shape':'decagon'}
	with pytest.raises(Exception):
		Ld.add_legend_entries('nodes', 'TF', style)


def test_get_legend_json():
	Ld = GSLegend()
	Ld.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
	assert Ld.legend_json == Ld.get_legend_json()


def test_remove_legend_entries():
	Ld = GSLegend()
	Ld.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
	Ld.remove_legend_entries('nodes', 'Receptor')
	assert len(Ld.get_legend_json()['legend']['nodes']) == 0


def test_remove_invalid_legend_entries():
	Ld = GSLegend()
	Ld.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
	with pytest.raises(Exception):
		Ld.remove_legend_entries('nodes', 'TF')


def test_delete_legend_json():
	Ld = GSLegend()
	Ld.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
	Ld.add_legend_entries(element_type='edges', label='Physical', style={'line-color': 'black', 'line-style': 'solid', 'arrow-shape':'none'})
	Ld.delete_legend_json()
	assert len(Ld.get_legend_json()['legend']) == 0
