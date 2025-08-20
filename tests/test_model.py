from chumpstreet.model import MacroData


def test_macro_data_model():
    json = {
        'series': 'GDP',
        'start_date': "2020-01-01",
        'end_date': "2020-01-10",
        'data': [{
            'observation_date': "2020-01-01",
            'value': 1.0
        }]
    }
    model = MacroData.model_validate(json)

    assert model.series == "GDP"
    assert len(model.data) == 1
