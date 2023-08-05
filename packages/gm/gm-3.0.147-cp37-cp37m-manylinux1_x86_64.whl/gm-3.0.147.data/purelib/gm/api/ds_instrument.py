from typing import List, Dict

import pandas as pd

from gm.api._utils import invalid_status, timestamp_to_str
from gm.csdk.c_sdk import (
    py_gmi_get_symbol_infos,
    py_gmi_get_symbols_v2,
    py_gmi_get_history_symbols,
    py_gmi_get_previous_n_trading_dates,
    py_gmi_get_next_n_trading_dates,
    py_gmi_get_trading_session,
    py_gmi_get_contract_expire_rest_days,
)
from gm.pb_to_dict import protobuf_to_dict
from gm.pb.instrument_service_pb2 import (
    GetSymbolInfosReq, GetSymbolInfosResp,
    GetSymbolsReq, GetSymbolsResp,
    GetHistorySymbolsReq, GetHistorySymbolsResp,
    GetTradingDatesPrevNReq, GetTradingDatesPrevNResp,
    GetTradingDatesNextNReq, GetTradingDatesNextNResp,
    GetTradingSessionReq, GetTradingSessionResp,
    GetContractExpireRestDaysReq, GetContractExpireRestDaysResp,
)


def get_symbol_infos(sec_type1, sec_type2=0, exchanges=None, symbols=None, fields="", df=False):
    # type: (int, int, str|List[str], str|List[str], str, bool) -> List[Dict]|pd.DataFrame
    """
    查询标的基本信息
    """
    if exchanges is None:
        exchanges = []
    elif isinstance(exchanges, str):
        exchanges = [exchange.strip() for exchange in exchanges.split(",")]
    if symbols is None:
        symbols = []
    elif isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]

    req = GetSymbolInfosReq(
        sec_type1=sec_type1,
        sec_type2=sec_type2,
        exchanges=exchanges,
        symbols=symbols,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_symbol_infos(req)
    if invalid_status(status):
        data = []
    else:
        rsp = GetSymbolInfosResp()
        rsp.ParseFromString(result)
        result = protobuf_to_dict(rsp)
        data = result.get("symbol_infos", [])   # type: List[Dict]
    if df:
        data = pd.DataFrame(data)
    return data


def get_symbols(sec_type1, sec_type2=0, exchanges=None, symbols=None, skip_suspended=True, skip_st=True, fields="", df=False):
    # type: (int, int, str|List[str], str|List[str], bool, bool, str, bool) -> List[Dict]|pd.DataFrame
    """
    查询最新交易日标的交易信息
    """
    if exchanges is None:
        exchanges = []
    elif isinstance(exchanges, str):
        exchanges = [exchange.strip() for exchange in exchanges.split(",")]
    if symbols is None:
        symbols = []
    elif isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]

    req = GetSymbolsReq(
        sec_type1=sec_type1,
        sec_type2=sec_type2,
        exchanges=exchanges,
        symbols=symbols,
        skip_suspended=skip_suspended,
        skip_st=skip_st,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_symbols_v2(req)
    if invalid_status(status):
        data = []
    else:
        rsp = GetSymbolsResp()
        rsp.ParseFromString(result)
        result = protobuf_to_dict(rsp)
        data = result.get("symbols", [])   # type: List[Dict]
    if df:
        data = pd.DataFrame(data)
    return data


def get_history_symbols(sec_type1, sec_type2=0, exchanges=None, symbols=None, skip_suspended=True, skip_st=True, start_date="", end_date="", fields="", df=False):
    # type: (int, int, str|List[str], str|List[str], bool, bool, str, str, str, bool) -> List[Dict]|pd.DataFrame
    """
    查询历史交易日标的交易信息
    """
    if exchanges is None:
        exchanges = []
    elif isinstance(exchanges, str):
        exchanges = [exchange.strip() for exchange in exchanges.split(",")]
    if symbols is None:
        symbols = []
    elif isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]

    req = GetHistorySymbolsReq(
        sec_type1=sec_type1,
        sec_type2=sec_type2,
        exchanges=exchanges,
        symbols=symbols,
        skip_suspended=skip_suspended,
        skip_st=skip_st,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_history_symbols(req)
    if invalid_status(status):
        data = []
    else:
        rsp = GetHistorySymbolsResp()
        rsp.ParseFromString(result)
        result = protobuf_to_dict(rsp)
        data = result.get("symbols", [])   # type: List[Dict]
    if df:
        data = pd.DataFrame(data)
    return data


def get_previous_n_trading_dates(exchange, date, n=1):
    # type: (str, str, int) -> List
    """
    查询指定日期的前n个交易日
    """
    req = GetTradingDatesPrevNReq(
        exchange=exchange,
        date=date,
        n=n,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_previous_n_trading_dates(req)
    if invalid_status(status):
        return []
    rsp = GetTradingDatesPrevNResp()
    rsp.ParseFromString(result)
    result = []
    for date in rsp.trading_dates:
        result.append(timestamp_to_str(date))
    return result


def get_next_n_trading_dates(exchange, date, n=1):
    # type: (str, str, int) -> List
    """
    查询指定日期的后n个交易日
    """
    req = GetTradingDatesNextNReq(
        exchange=exchange,
        date=date,
        n=n,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_next_n_trading_dates(req)
    if invalid_status(status):
        return []
    rsp = GetTradingDatesNextNResp()
    rsp.ParseFromString(result)
    result = []
    for date in rsp.trading_dates:
        result.append(timestamp_to_str(date))
    return result


def get_trading_session(symbols, df=False):
    # type: (str|List[str], bool) -> List
    """
    查询交易日的可交易时段
    """
    if isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]
    req = GetTradingSessionReq(
        symbols=symbols,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_trading_session(req)
    if invalid_status(status):
        data = []
    else:
        rsp = GetTradingSessionResp()
        rsp.ParseFromString(result)
        result = protobuf_to_dict(rsp)
        data = result.get("trading_sessions", [])   # type: List[Dict]
    if df:
        data = pd.DataFrame(data)
    return data


def get_contract_expire_rest_days(symbols, start_date="", end_date="", trade_flag=False, df=False):
    # type: (str|List[str], str, str, bool, bool) -> List
    """
    查询合约到期剩余天数
    """
    if isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]
    req = GetContractExpireRestDaysReq(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        by_trading_days=trade_flag,
    )
    req = req.SerializeToString()
    status, result = py_gmi_get_contract_expire_rest_days(req)
    if invalid_status(status):
        data = []
        if df:
            data = pd.DataFrame(data)
        return data

    rsp = GetContractExpireRestDaysResp()
    rsp.ParseFromString(result)
    result = protobuf_to_dict(rsp)
    data = result.get("contract_expire_rest_days", [])   # type: List[Dict]
    for value in data:
        if value["days_to_expire"] == "":
            value["days_to_expire"] = None
        else:
            value["days_to_expire"] = int(value["days_to_expire"])

    if df:
        data = pd.DataFrame(data)
    return data
