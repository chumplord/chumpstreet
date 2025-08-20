import pytest


@pytest.mark.asyncio
async def test_get_market_data_for_single_ticker(client):
    arguments = {
        'tickers': ['SPY'],
        'start_date': '2020-01-01',
        'end_date': '2020-01-05'
    }

    response = await client.call_tool('get_market_data', arguments)

    market_data = response.data

    assert market_data.start_date == '2020-01-01'
    assert market_data.end_date == '2020-01-05'
    assert len(market_data.data) == 2
    assert len(market_data.errors) == 0


@pytest.mark.asyncio
async def test_get_market_data_for_multi_ticker(client):
    arguments = {
        'tickers': ['SPY', 'TLT', 'DXY', 'GLD', 'CL=F'],
        'start_date': '2020-01-01',
        'end_date': '2020-01-05'
    }

    response = await client.call_tool('get_market_data', arguments)

    market_data = response.data

    assert market_data.start_date == '2020-01-01'
    assert market_data.end_date == '2020-01-05'
    assert len(market_data.data) == 10
    assert len(market_data.errors) == 0


@pytest.mark.asyncio
async def test_get_market_data_with_no_ticker(client):
    arguments = {
        'tickers': [],
        'start_date': '2020-01-01',
        'end_date': '2020-01-05'
    }

    response = await client.call_tool('get_market_data', arguments)

    market_data = response.data

    assert market_data.start_date == '2020-01-01'
    assert market_data.end_date == '2020-01-05'
    assert len(market_data.data) == 0
    assert len(market_data.errors) == 1
    assert market_data.errors[0].message == "Tickers must be a non-empty list of strings"


@pytest.mark.asyncio
async def test_get_market_data_with_bad_ticker(client):
    arguments = {
        'tickers': ['ABC'],
        'start_date': '2020-01-01',
        'end_date': '2020-01-05'
    }

    response = await client.call_tool('get_market_data', arguments)

    market_data = response.data

    assert market_data.start_date == '2020-01-01'
    assert market_data.end_date == '2020-01-05'
    assert len(market_data.data) == 0
    assert len(market_data.errors) == 1
    assert market_data.errors[0].message == "No data returned for tickers: ['ABC']"


@pytest.mark.asyncio
async def test_get_macro_data_for_single_series(client):
    response = await client.call_tool('get_macro_data', {
        'series_list': ['GDP'],
        'start_date' : '2020-01-01',
        'end_date': '2020-01-05'
    })

    macro_data = response.data

    assert macro_data.start_date == '2020-01-01'
    assert macro_data.end_date == '2020-01-05'
    assert macro_data.series == ['GDP']
    assert len(macro_data.data) == 1
    assert len(macro_data.errors) == 0


@pytest.mark.asyncio
async def test_get_macro_data_for_multiple_series(client):
    response = await client.call_tool('get_macro_data', {
        'series_list': ['GDP', 'CPIAUCSL', 'UNRATE', 'FEDFUNDS'],
        'start_date' : '2020-01-01',
        'end_date': '2020-01-05'
    })

    macro_data = response.data

    assert macro_data.start_date == '2020-01-01'
    assert macro_data.end_date == '2020-01-05'
    assert macro_data.series == ['GDP', 'CPIAUCSL', 'UNRATE', 'FEDFUNDS']
    assert len(macro_data.data) == 4
    assert len(macro_data.errors) == 0


@pytest.mark.asyncio
async def test_get_macro_data_with_bad_series(client):
    response = await client.call_tool('get_macro_data', {
        'series_list': ['XXX'],
        'start_date' : '2020-01-01',
        'end_date': '2020-01-05'
    })

    macro_data = response.data

    assert macro_data.start_date == '2020-01-01'
    assert macro_data.end_date == '2020-01-05'
    assert macro_data.series == ['XXX']
    assert len(macro_data.data) == 0
    assert len(macro_data.errors) == 1
    assert 'The series does not exist' in macro_data.errors[0].message