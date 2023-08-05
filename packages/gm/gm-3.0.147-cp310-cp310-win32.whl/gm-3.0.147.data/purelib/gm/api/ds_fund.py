from typing import List, Dict, Any

import pandas as pd

from gm.api._utils import invalid_status, pb_to_dict
from gm.csdk.c_sdk import (
    py_gmi_stk_get_industry_category,
    py_gmi_stk_get_industry_constituents,
    py_gmi_stk_get_symbol_industry,
    py_gmi_stk_get_index_constituents,
    py_gmi_stk_get_index_history_constituents,
    py_gmi_stk_get_dividend,
    py_gmi_stk_get_adj_factor,
    py_gmi_fut_get_continuous_contracts,
    py_gmi_fut_get_contract_info,
    py_gmi_fnd_get_adj_factor,
    py_gmi_fnd_get_dividend,
    py_gmi_fnd_get_split,

    py_gmi_stk_get_sector_category,
    py_gmi_stk_get_sector_constituents,
    py_gmi_stk_get_symbol_sector,
    py_stk_get_ration,
    py_gmi_stk_get_shareholder_num,
    py_gmi_stk_get_top_shareholder,
    py_gmi_stk_get_share_change,
    py_gmi_stk_get_fundamentals_balance,
    py_gmi_stk_get_fundamentals_cashflow,
    py_gmi_stk_get_fundamentals_income,
    py_gmi_fut_get_transaction_ranking,
    py_gmi_fut_get_warehouse_receipt,
    py_gmi_fnd_get_etf_constituents,
    py_gmi_fnd_get_portfolio,
    py_gmi_fnd_get_net_value,
    py_gmi_bnd_get_conversion_price,
    py_gmi_bnd_get_call_info,
    py_gmi_bnd_get_put_info,
    py_gmi_bnd_get_amount_change,
)
from gm.pb.fund_stk_service_pb2 import (
    GetIndustryCategoryReq, GetIndustryCategoryRsp,
    GetIndustryConstituentsReq, GetIndustryConstituentsRsp,
    GetSymbolIndustryReq, GetSymbolIndustryRsp,
    GetIndexConstituentsReq, GetIndexConstituentsRsp,
    GetIndexHistoryConstituentsReq, GetIndexHistoryConstituentsRsp,
    GetDividendReq, GetDividendRsp,
    GetAdjFactorReq, GetAdjFactorRsp,
    GetSectorCategoryReq, GetSectorCategoryRsp,
    GetSectorConstituentsReq, GetSectorConstituentsRsp,
    GetSymbolSectorReq, GetSymbolSectorRsp,
    GetRationReq, GetRationRsp,
    GetShareholderNumReq, GetShareholderNumRsp,
    GetTopShareholderReq, GetTopShareholderRsp,
    GetShareChangeReq, GetShareChangeRsp,
    GetFundamentalsBalanceReq, GetFundamentalsBalanceRsp,
    GetFundamentalsCashflowReq, GetFundamentalsCashflowRsp,
    GetFundamentalsIncomeReq, GetFundamentalsIncomeRsp,
)
from gm.pb.fund_fut_service_pb2 import (
    GetContinuousContractsReq, GetContinuousContractsRsp,
    FutGetContractInfoReq, FutGetContractInfoRsp,
    FutGetTransactionRankingReq, FutGetTransactionRankingRsp,
    GetWarehouseReceiptReq, GetWarehouseReceiptRsp,
)
from gm.pb.fund_fnd_service_pb2 import (
    FndGetAdjFactorReq, FndGetAdjFactorRsp,
    FndGetDividendReq, FndGetDividendRsp,
    GetSplitReq, GetSplitRsp,
    GetEtfConstituentsReq, GetEtfConstituentsRsp,
    GetPortfolioReq, GetPortfolioRsp,
    GetNetValueReq, GetNetValueRsp,
)
from gm.pb.fund_bnd_service_pb2 import (
    GetConversionPriceReq, GetConversionPriceRsp,
    GetCallInfoReq, GetCallInfoRsp,
    GetPutInfoReq, GetPutInfoRsp,
    GetAmountChangeReq, GetAmountChangeRsp,
)


def _invalid_source_level(source, level):
    # type: (str, int) -> bool
    source = source.lower()
    if not (source == "zjh2012" or source == "sw2021"):
        return True
    if level > 3 or level < 1:
        return True
    if source == "zjh2012" and level == 3:
        return True
    return False


def stk_get_industry_category(source="zjh2012", level=1):
    # type: (str, int) -> pd.DataFrame
    """
    查询行业分类

    * source: 行业来源, 默认值 'zjh2012'
    * level: 行业分级, 默认值 1, (1:一级行业, 2:二级行业, 3:三级行业)
    """
    if _invalid_source_level(source, level):
        return pd.DataFrame()

    req = GetIndustryCategoryReq(
        source=source,
        level=level,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_industry_category(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetIndustryCategoryRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str]]
    return pd.DataFrame(data)


def stk_get_industry_constituents(industry_code, date=""):
    # type: (str, str) -> pd.DataFrame
    """
    查询行业成分股
    """
    req = GetIndustryConstituentsReq(
        industry_code=industry_code,
        date=date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_industry_constituents(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetIndustryConstituentsRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict]
    return pd.DataFrame(data)


def stk_get_symbol_industry(symbols, source="zjh2012", level=1, date=""):
    # type: (str|List[str], str, int, str) -> pd.DataFrame
    """
    查询股票的所属行业

    证监会行业分类2012没有三级行业, 若输入source='zjh2012', level=3则参数无效, 返回空
    """
    if _invalid_source_level(source, level):
        return pd.DataFrame()

    if isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]
    req = GetSymbolIndustryReq(
        symbols=symbols,
        source=source,
        level=level,
        date=date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_symbol_industry(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetSymbolIndustryRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str]]
    return pd.DataFrame(data)


def stk_get_sector_category(sector_type):
    # type: (str) -> pd.DataFrame
    """
    查询板块分类
    """
    req = GetSectorCategoryReq(
        sector_type=sector_type,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_sector_category(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetSectorCategoryRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])  # type: List[Dict[str, str]]
    return pd.DataFrame(data)


def stk_get_sector_constituents(sector_code):
    # type: (str) -> pd.DataFrame
    """
    查询板块成分股
    """
    req = GetSectorConstituentsReq(
        sector_code=sector_code,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_sector_constituents(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetSectorConstituentsRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])  # type: List[Dict[str, str]]
    return pd.DataFrame(data)


def stk_get_symbol_sector(symbols, sector_type):
    # type: (str|List[str], str) -> pd.DataFrame
    """
    查询股票的所属板块
    """
    if isinstance(symbols, str):
        symbols = [symbol.strip() for symbol in symbols.split(",")]
    req = GetSymbolSectorReq(
        symbols=symbols,
        sector_type=sector_type,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_symbol_sector(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetSymbolSectorRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])  # type: List[Dict[str, str]]
    return pd.DataFrame(data)


def stk_get_index_constituents(index):
    # type: (str) -> pd.DataFrame
    """
    查询指数最新成分股(每天下午5点到凌晨12点才有数据)
    """
    req = GetIndexConstituentsReq(
        index=index,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_index_constituents(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetIndexConstituentsRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_index_history_constituents(index, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询指数历史成分股
    """
    req = GetIndexHistoryConstituentsReq(
        index=index,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_stk_get_index_history_constituents(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetIndexHistoryConstituentsRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])  # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_dividend(symbol, start_date, end_date):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询股票分红送股信息
    """
    req = GetDividendReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )

    req = req.SerializeToString()
    status, result = py_gmi_stk_get_dividend(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetDividendRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_ration(symbol, start_date, end_date):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询股票配股信息
    """
    req = GetRationReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )

    req = req.SerializeToString()
    status, result = py_stk_get_ration(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetRationRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_adj_factor(symbol, start_date="", end_date="", base_date=""):
    # type: (str, str, str, str) -> pd.DataFrame
    """
    查询股票的复权因子
    """
    req = GetAdjFactorReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        base_date=base_date,
    )

    req = req.SerializeToString()
    status, result = py_gmi_stk_get_adj_factor(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetAdjFactorRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str|float]]
    return pd.DataFrame(data)


def stk_get_shareholder_num(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询股东户数
    """
    req = GetShareholderNumReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )

    req = req.SerializeToString()
    status, result = py_gmi_stk_get_shareholder_num(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetShareholderNumRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_top_shareholder(symbol, start_date="", end_date="", tradable_holder=False):
    # type: (str, str, str, bool) -> pd.DataFrame
    """
    查询十大股东
    """
    req = GetTopShareholderReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        tradable_holder=tradable_holder,
    )

    req = req.SerializeToString()
    status, result = py_gmi_stk_get_top_shareholder(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetTopShareholderRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def stk_get_share_change(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询股本变动
    """
    req = GetShareChangeReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )

    req = req.SerializeToString()
    status, result = py_gmi_stk_get_share_change(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetShareChangeRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def fut_get_continuous_contracts(csymbol, start_date="", end_date=""):
    # type: (str, str, str) -> List[Dict[str, Any]]
    """
    查询连续合约对应的真实合约
    """
    req = GetContinuousContractsReq(
        csymbol=csymbol,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fut_get_continuous_contracts(req)
    if invalid_status(status):
        return []
    res = GetContinuousContractsRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str]]
    return data


def fut_get_contract_info(product_codes, df=False):
    # type: (str|List[str], bool) -> List[Dict[str, str|int]] | pd.DataFrame
    """
    查询期货标准品种信息
    """
    if isinstance(product_codes, str):
        product_codes = [code.strip() for code in product_codes.split(",")]
    req = FutGetContractInfoReq(
        product_codes=product_codes,
    )

    req = req.SerializeToString()
    status, result = py_gmi_fut_get_contract_info(req)
    if invalid_status(status):
        data = []
        if df:
            data = pd.DataFrame(data)
        return data
    res = FutGetContractInfoRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str|int]]
    if df:
        data = pd.DataFrame(data)
    return data


def fut_get_transaction_ranking(symbol, trade_date="", indicator="volume"):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询期货每日成交持仓排名
    """
    req = FutGetTransactionRankingReq(
        symbol=symbol,
        trade_date=trade_date,
        indicator=indicator,
    )

    req = req.SerializeToString()
    status, result = py_gmi_fut_get_transaction_ranking(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = FutGetTransactionRankingRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    data = pd.DataFrame(data)   # type: pd.DataFrame
    if data.empty:
        return data
    # ranking_change_is_null 字段用于判断 ranking_change 是否为空, 最终输出需要删除这个字段
    data.loc[data["ranking_change_is_null"] == True, "ranking_change"] = None
    return data.drop(axis=1, columns="ranking_change_is_null")


def fut_get_warehouse_receipt(product_code, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询期货仓单数据
    """
    req = GetWarehouseReceiptReq(
        product_code=product_code,
        start_date=start_date,
        end_date=end_date,
    )

    req = req.SerializeToString()
    status, result = py_gmi_fut_get_warehouse_receipt(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetWarehouseReceiptRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def fnd_get_etf_constituents(etf):
    # type: (str) -> pd.DataFrame
    """
    查询ETF最新成分股
    """
    req = GetEtfConstituentsReq(
        etf=etf,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_etf_constituents(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetEtfConstituentsRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def fnd_get_portfolio(fund, report_type, portfolio_type, start_date="", end_date=""):
    # type: (str, int, str, str, str) -> pd.DataFrame
    """
    查询基金的资产组合
    """
    req = GetPortfolioReq(
        fund=fund,
        start_date=start_date,
        end_date=end_date,
        report_type=report_type,
        portfolio_type=portfolio_type,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_portfolio(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetPortfolioRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    if portfolio_type == "stk":
        data = result.get("portfolio_stock", [])
    elif portfolio_type == "bnd":
        data = result.get("portfolio_bond", [])
    elif portfolio_type == "fnd":
        data = result.get("portfolio_fund", [])
    else:
        data = []
    return pd.DataFrame(data)


def fnd_get_net_value(fund, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询基金的净值数据
    """
    req = GetNetValueReq(
        fund=fund,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_net_value(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetNetValueRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def fnd_get_adj_factor(fund, start_date="", end_date="", base_date=""):
    # type: (str, str, str, str) -> pd.DataFrame
    """
    查询基金复权因子
    """
    req = FndGetAdjFactorReq(
        fund=fund,
        start_date=start_date,
        end_date=end_date,
        base_date=base_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_adj_factor(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = FndGetAdjFactorRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, str|float]]
    return pd.DataFrame(data)


def fnd_get_dividend(fund, start_date, end_date):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询基金分红信息
    """
    req = FndGetDividendReq(
        fund=fund,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_dividend(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = FndGetDividendRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def fnd_get_split(fund, start_date, end_date):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询基金分红信息
    """
    req = GetSplitReq(
        fund=fund,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_fnd_get_split(req)
    if invalid_status(status):
        return pd.DataFrame()
    res = GetSplitRsp()
    res.ParseFromString(result)
    result = pb_to_dict(res)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def bnd_get_conversion_price(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询可转债转股价变动信息
    """
    req = GetConversionPriceReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_bnd_get_conversion_price(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetConversionPriceRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def bnd_get_call_info(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询可转债赎回信息
    """
    req = GetCallInfoReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_bnd_get_call_info(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetCallInfoRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def bnd_get_put_info(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询可转债回售信息
    """
    req = GetPutInfoReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_bnd_get_put_info(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetPutInfoRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)


def bnd_get_amount_change(symbol, start_date="", end_date=""):
    # type: (str, str, str) -> pd.DataFrame
    """
    查询可转债剩余规模变动信息
    """
    req = GetAmountChangeReq(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    req = req.SerializeToString()
    status, result = py_gmi_bnd_get_amount_change(req)
    if invalid_status(status):
        return pd.DataFrame()
    rsp = GetAmountChangeRsp()
    rsp.ParseFromString(result)
    result = pb_to_dict(rsp)
    data = result.get("data", [])   # type: List[Dict[str, Any]]
    return pd.DataFrame(data)
