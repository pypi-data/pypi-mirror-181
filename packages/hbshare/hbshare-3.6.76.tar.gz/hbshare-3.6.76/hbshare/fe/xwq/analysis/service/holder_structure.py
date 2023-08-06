# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                  '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
new_color_list = ['#F04950', '#959595', '#6268A2', '#333335', '#D57C56', '#628497']


def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def to_percent_r2(temp, position):
    return '%0.01f'%(temp) + '%'

def to_percent_r3(temp, position):
    return '%0.001f'%(temp) + '%'

def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'

def to_100percent_r2(temp, position):
    return '%0.01f'%(temp * 100) + '%'

def to_100percent_r3(temp, position):
    return '%0.001f'%(temp * 100) + '%'

def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df


class HolderStructure:
    def __init__(self, date, data_path):
        self.date = date
        self.data_path = data_path

        ##### 日历信息 ######
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date('20150101', self.date)

        ##### 全部基金信息 ######
        self.all_fund = HBDB().read_fund_info()
        self.all_fund.to_hdf('{0}all_fund.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund = pd.read_hdf('{0}all_fund.hdf'.format(self.data_path), key='table')
        self.all_fund = self.all_fund.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'BEGIN_DATE', 'zzrq': 'END_DATE', 'jjfl': 'FUND_TYPE_1ST', 'ejfl': 'FUND_TYPE_2ND', 'kffb': 'OPEN_CLOSE'})
        self.all_fund = self.all_fund.dropna(subset=['BEGIN_DATE'])
        self.all_fund['END_DATE'] = self.all_fund['END_DATE'].fillna(20990101)
        self.all_fund['BEGIN_DATE'] = self.all_fund['BEGIN_DATE'].astype(int).astype(str)
        self.all_fund['END_DATE'] = self.all_fund['END_DATE'].astype(int).astype(str)
        self.all_fund['FUND_TYPE_1ST'] = self.all_fund['FUND_TYPE_1ST'].replace(
            {'f': 'FOF型', '1': '股票型', '2': '债券型', '3': '混合型', '4': '另类投资型', '7': '货币型', '9': 'QDII型'})
        self.all_fund['FUND_TYPE_2ND'] = self.all_fund['FUND_TYPE_2ND'].replace(
            {'f3': '债券型FOF', 'f4': '货币型FOF', 'f1': '股票型FOF', 'f2': '混合型FOF', 'f5': '另类投资FOF',
             '13': '普通股票型', '14': '股票型', '15': '增强指数型', '16': '被动指数型',
             '21': '被动指数型债券', '22': '短期纯债型', '23': '混合债券型一级', '24': '混合债券型二级', '25': '增强指数型债券', '26': '债券型',
             '27': '中长期纯债型', '28': '可转换债券型',
             '34': '平衡混合型', '35': '灵活配置型', '36': '混合型', '37': '偏股混合型', '38': '偏债混合型',
             '41': '股票多空', '42': '商品型', '43': 'REITs',
             '91': '股票型QDII', '93': '混合型QDII', '94': '债券型QDII', '95': '另类型QDII'})
        self.all_fund['FUND_TYPE'] = self.all_fund['FUND_TYPE_1ST']
        self.all_fund.loc[self.all_fund['FUND_TYPE_2ND'] == 'REITs', 'FUND_TYPE'] = 'REITs'

        ##### 全部基金持有人信息 ######
        self.all_fund_holder = HBDB().read_fund_holder_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_holder.to_hdf('{0}all_fund_holder.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_holder = pd.read_hdf('{0}all_fund_holder.hdf'.format(self.data_path), key='table')
        self.all_fund_holder = self.all_fund_holder.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'ggrq': 'PUBLISH_DATE', 'grcyfe': 'PERSON',  'grcybl': 'PERSON_RATIO', 'jgcyfe': 'ORGAN', 'jgcybl': 'ORGAN_RATIO', 'ygcyfe': 'STAFF', 'ygcybl': 'STAFF_RATIO'})
        self.all_fund_holder['REPORT_DATE'] = self.all_fund_holder['REPORT_DATE'].astype(str)
        self.all_fund_holder = self.all_fund_holder[self.all_fund_holder['REPORT_DATE'].str.slice(4, 8).isin(['0630', '1231'])]
        self.all_fund_holder = self.all_fund_holder.sort_values(['FUND_CODE', 'REPORT_DATE', 'PUBLISH_DATE']).drop_duplicates(['FUND_CODE', 'REPORT_DATE'], keep='last')

        ##### 全部基金仓位信息 ######
        self.all_fund_position = HBDB().read_fund_position_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_position.to_hdf('{0}all_fund_position.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_position = pd.read_hdf('{0}all_fund_position.hdf'.format(self.data_path), key='table')
        self.all_fund_position = self.all_fund_position.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'jjzzc': 'TOTAL_ASSETS', 'jjjzc': 'NET_ASSETS', 'gptzsz': 'STOCK', 'gptzzjb': 'STOCK_RATIO', 'zqzsz': 'BOND', 'zqzszzjb': 'BOND_RATIO', 'jjtzszhj': 'FUND', 'jjtzhjzjb': 'FUND_RATIO', 'hbzjsz': 'CASH', 'hbzjzjb': 'CASH_RATIO'})
        self.all_fund_position['REPORT_DATE'] = self.all_fund_position['REPORT_DATE'].astype(str)
        self.all_fund_position = self.all_fund_position[self.all_fund_position['REPORT_DATE'].str.slice(4, 8).isin(['0331', '0630', '0930', '1231'])]
        self.all_fund_position = self.all_fund_position.sort_values(['FUND_CODE', 'REPORT_DATE']).drop_duplicates(['FUND_CODE', 'REPORT_DATE'], keep='last')

        ##### 全部基金年度收益（整年非年化收益） ######
        self.all_fund_return_year = HBDB().read_fund_return_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_return_year.to_hdf('{0}all_fund_return_year.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_return_year = pd.read_hdf('{0}all_fund_return_year.hdf'.format(self.data_path), key='table')
        self.all_fund_return_year = self.all_fund_return_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'hb1n': 'RETURN', 'rq1n': 'BEGIN_DATE', 'rqzh': 'END_DATE'})
        self.all_fund_return_year['YEAR'] = self.all_fund_return_year['YEAR'].astype(str)
        self.all_fund_return_year['BEGIN_DATE'] = self.all_fund_return_year['BEGIN_DATE'].replace(99999, np.nan)
        self.all_fund_return_year['RETURN'] = self.all_fund_return_year['RETURN'].replace(99999.0, np.nan)

        ##### 全部基金年度最大回撤 ######
        self.all_fund_maxdrawdown_year = HBDB().read_fund_maxdrawdown_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_maxdrawdown_year.to_hdf('{0}all_fund_maxdrawdown_year.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_maxdrawdown_year = pd.read_hdf('{0}all_fund_maxdrawdown_year.hdf'.format(self.data_path), key='table')
        self.all_fund_maxdrawdown_year = self.all_fund_maxdrawdown_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zbnp1n': 'MAXDRAWDOWN', 'zdhchfts1n': 'RECOVERY_DAYS', 'zdhccxts1n': 'CONTINUE_DAYS'})
        self.all_fund_maxdrawdown_year['YEAR'] = self.all_fund_maxdrawdown_year['YEAR'].astype(str)
        self.all_fund_maxdrawdown_year['MAXDRAWDOWN'] = self.all_fund_maxdrawdown_year['MAXDRAWDOWN'].replace(99999.0, np.nan)
        self.all_fund_maxdrawdown_year['RECOVERY_DAYS'] = self.all_fund_maxdrawdown_year['RECOVERY_DAYS'].replace(99999.0, np.nan)
        self.all_fund_maxdrawdown_year['CONTINUE_DAYS'] = self.all_fund_maxdrawdown_year['CONTINUE_DAYS'].replace(99999.0, np.nan)

        ##### 全部基金年度波动率 ######
        self.all_fund_volatility_year = HBDB().read_fund_volatility_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_volatility_year.to_hdf('{0}all_fund_volatility_year.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_volatility_year = pd.read_hdf('{0}all_fund_volatility_year.hdf'.format(self.data_path), key='table')
        self.all_fund_volatility_year = self.all_fund_volatility_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zzbnp1n': 'VOLATILITY', 'znhzbnp1n': 'ANNUAL_VOLATILITY'})
        self.all_fund_volatility_year['YEAR'] = self.all_fund_volatility_year['YEAR'].astype(str)
        self.all_fund_volatility_year['VOLATILITY'] = self.all_fund_volatility_year['VOLATILITY'].replace(99999.0, np.nan)
        self.all_fund_volatility_year['ANNUAL_VOLATILITY'] = self.all_fund_volatility_year['ANNUAL_VOLATILITY'].replace(99999.0, np.nan)

        ##### 全部基金年度夏普比率 ######
        self.all_fund_sharpe_year = HBDB().read_fund_sharpe_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_sharpe_year.to_hdf('{0}all_fund_sharpe_year.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_sharpe_year = pd.read_hdf('{0}all_fund_sharpe_year.hdf'.format(self.data_path), key='table')
        self.all_fund_sharpe_year = self.all_fund_sharpe_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zzbnp1n': 'SHARPE', 'znhzbnp1n': 'ANNUAL_SHARPE'})
        self.all_fund_sharpe_year['YEAR'] = self.all_fund_sharpe_year['YEAR'].astype(str)
        self.all_fund_sharpe_year['SHARPE'] = self.all_fund_sharpe_year['SHARPE'].replace(99999.0, np.nan)
        self.all_fund_sharpe_year['ANNUAL_SHARPE'] = self.all_fund_sharpe_year['ANNUAL_SHARPE'].replace(99999.0, np.nan)

        ##### 全部基金年度卡玛比率 ######
        self.all_fund_calmer_year = HBDB().read_fund_calmer_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.all_fund_calmer_year.to_hdf('{0}all_fund_calmer_year.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_calmer_year = pd.read_hdf('{0}all_fund_calmer_year.hdf'.format(self.data_path), key='table')
        self.all_fund_calmer_year = self.all_fund_calmer_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zbnp1n': 'CALMER'})
        self.all_fund_calmer_year['YEAR'] = self.all_fund_calmer_year['YEAR'].astype(str)
        self.all_fund_calmer_year['CALMER'] = self.all_fund_calmer_year['CALMER'].replace(99999.0, np.nan)

        ##### 全部基金年度胜率 ######
        self.read_fund_winratio_year = HBDB().read_fund_winratio_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.read_fund_winratio_year.to_hdf('{0}read_fund_winratio_year.hdf'.format(self.data_path), key='table', mode='w')
        self.read_fund_winratio_year = pd.read_hdf('{0}read_fund_winratio_year.hdf'.format(self.data_path), key='table')
        self.read_fund_winratio_year = self.read_fund_winratio_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zbnp1n': 'WINRATIO'})
        self.read_fund_winratio_year['YEAR'] = self.read_fund_winratio_year['YEAR'].astype(str)
        self.read_fund_winratio_year['WINRATIO'] = self.read_fund_winratio_year['WINRATIO'].replace(99999.0, np.nan)

        ##### 全部基金年度损益比 ######
        self.read_fund_pl_year = HBDB().read_fund_pl_year_given_codes(self.all_fund['FUND_CODE'].unique().tolist())
        self.read_fund_pl_year.to_hdf('{0}read_fund_pl_year.hdf'.format(self.data_path), key='table', mode='w')
        self.read_fund_pl_year = pd.read_hdf('{0}read_fund_pl_year.hdf'.format(self.data_path), key='table')
        self.read_fund_pl_year = self.read_fund_pl_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'zsypj1n': 'POSITION_RETURN', 'fsypj1n': 'NEGATIVE_RETURN', 'pjsyb1n': 'PL'})
        self.read_fund_pl_year['YEAR'] = self.read_fund_pl_year['YEAR'].astype(str)
        self.read_fund_pl_year['POSITION_RETURN'] = self.read_fund_pl_year['POSITION_RETURN'].replace(99999.0, np.nan)
        self.read_fund_pl_year['NEGATIVE_RETURN'] = self.read_fund_pl_year['NEGATIVE_RETURN'].replace(99999.0, np.nan)
        self.read_fund_pl_year['PL'] = self.read_fund_pl_year['PL'].replace(99999.0, np.nan)

        ##### 主动权益型基金信息 ######
        self.fund = self.all_fund[self.all_fund['FUND_TYPE_2ND'].isin(['普通股票型', '灵活配置型', '偏股混合型'])]
        self.fund = self.fund[self.fund['END_DATE'] >= self.date]
        # 成立以来股票占基金净资产的比例均值不低于60%
        fund_gptzzjb = HBDB().read_fund_gptzzjb_given_codes(self.fund['FUND_CODE'].unique().tolist())
        fund_gptzzjb.to_hdf('{0}fund_gptzzjb.hdf'.format(self.data_path), key='table', mode='w')
        fund_gptzzjb = pd.read_hdf('{0}fund_gptzzjb.hdf'.format(self.data_path), key='table')
        fund_gptzzjb = fund_gptzzjb.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'gptzzjb': 'EQUITY_IN_NA'})
        fund_gptzzjb['REPORT_DATE'] = fund_gptzzjb['REPORT_DATE'].astype(str)
        fund_gptzzjb_mean = fund_gptzzjb[['FUND_CODE', 'EQUITY_IN_NA']].groupby('FUND_CODE').mean().reset_index()
        fund_gptzzjb_mean = fund_gptzzjb_mean[fund_gptzzjb_mean['EQUITY_IN_NA'] >= 60]
        self.fund = self.fund[self.fund['FUND_CODE'].isin(fund_gptzzjb_mean['FUND_CODE'].unique().tolist())]
        # 近2年以来股票占基金净资产的比例均不低于50%
        fund_gptzzjb = fund_gptzzjb[(fund_gptzzjb['REPORT_DATE'] >= (datetime.strptime(self.date, '%Y%m%d') - timedelta(730)).strftime('%Y%m%d')) & (fund_gptzzjb['REPORT_DATE'] <= self.date)]
        fund_gptzzjb_min = fund_gptzzjb[['FUND_CODE', 'EQUITY_IN_NA']].groupby('FUND_CODE').min().reset_index()
        fund_gptzzjb_min = fund_gptzzjb_min[fund_gptzzjb_min['EQUITY_IN_NA'] >= 50]
        self.fund = self.fund[self.fund['FUND_CODE'].isin(fund_gptzzjb_min['FUND_CODE'].unique().tolist())]
        return

    def get_all_fund_holder(self):
        # 最新一期
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['REPORT_DATE'] == self.date]
        all_fund_position = self.all_fund_position[self.all_fund_position['REPORT_DATE'] == self.date]
        all_fund = self.all_fund.copy(deep=True)
        # all_fund = self.all_fund.sort_values(['FUND_FULL_NAME', 'FUND_CODE']).drop_duplicates('FUND_FULL_NAME')
        holder = all_fund.merge(all_fund_holder[['FUND_CODE', 'ORGAN_RATIO', 'PERSON_RATIO']], on=['FUND_CODE'], how='left').merge(all_fund_position[['FUND_CODE', 'NET_ASSETS']], on=['FUND_CODE'], how='left')
        holder = holder[['FUND_CODE', 'FUND_TYPE', 'NET_ASSETS', 'ORGAN_RATIO', 'PERSON_RATIO']]
        holder = holder.dropna()
        holder['ORGAN_MV'] = 0.01 * holder['ORGAN_RATIO'] * holder['NET_ASSETS']
        holder['PERSON_MV'] = 0.01 * holder['PERSON_RATIO'] * holder['NET_ASSETS']
        organ_holder = holder[['FUND_TYPE', 'ORGAN_MV']].groupby('FUND_TYPE').sum()
        organ_holder.loc['全部', 'ORGAN_MV'] = organ_holder['ORGAN_MV'].sum()
        person_holder = holder[['FUND_TYPE', 'PERSON_MV']].groupby('FUND_TYPE').sum()
        person_holder.loc['全部', 'PERSON_MV'] = person_holder['PERSON_MV'].sum()
        holder = organ_holder.merge(person_holder, left_index=True, right_index=True, how='outer').fillna(0.0)
        holder['ORGAN_RATIO'] = holder['ORGAN_MV'] / (holder['ORGAN_MV'] + holder['PERSON_MV'])
        holder['PERSON_RATIO'] = holder['PERSON_MV'] / (holder['ORGAN_MV'] + holder['PERSON_MV'])
        holder = holder.loc[['全部', '股票型', '混合型', '债券型', '货币型', '另类投资型', 'QDII型', 'FOF型']]

        holder_disp = holder.copy(deep=True)
        holder_disp = holder_disp.reset_index()
        holder_disp['PERSON_RATIO'] = holder_disp['ORGAN_RATIO'] + holder_disp['PERSON_RATIO']
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(ax=ax, x='FUND_TYPE', y='PERSON_RATIO', data=holder_disp, label='个人持有比例', color=bar_color_list[14])
        sns.barplot(ax=ax, x='FUND_TYPE', y='ORGAN_RATIO', data=holder_disp, label='机构持有比例', color=bar_color_list[0])
        h, l = ax.get_legend_handles_labels()
        plt.legend(handles=h[::-1], labels=l[::-1], loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.xlabel('')
        plt.ylabel('')
        plt.title('2022上半年各类型基金持有人结构', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        sns.despine(left=False, bottom=False, top=True, right=True)
        plt.tight_layout()
        plt.savefig('{0}all_fund_holder.png'.format(self.data_path))
        return

    def get_fund_holder(self):
        all_fund_holder = self.all_fund_holder.copy(deep=True)
        all_fund_position = self.all_fund_position.copy(deep=True)
        fund = self.fund.copy(deep=True)
        # fund = self.fund.sort_values(['FUND_FULL_NAME', 'FUND_CODE']).drop_duplicates('FUND_FULL_NAME')
        holder = all_fund_holder[['FUND_CODE', 'REPORT_DATE', 'ORGAN_RATIO', 'PERSON_RATIO']].merge(all_fund_position[['FUND_CODE', 'REPORT_DATE', 'NET_ASSETS']], on=['FUND_CODE', 'REPORT_DATE'], how='left')
        holder = holder[holder['FUND_CODE'].isin(fund['FUND_CODE'].unique().tolist())]
        holder = holder[['FUND_CODE', 'REPORT_DATE', 'NET_ASSETS', 'ORGAN_RATIO', 'PERSON_RATIO']]
        holder = holder.dropna()
        holder['ORGAN_MV'] = 0.01 * holder['ORGAN_RATIO'] * holder['NET_ASSETS']
        holder['PERSON_MV'] = 0.01 * holder['PERSON_RATIO'] * holder['NET_ASSETS']
        organ_holder = holder[['REPORT_DATE', 'ORGAN_MV']].groupby('REPORT_DATE').sum()
        person_holder = holder[['REPORT_DATE', 'PERSON_MV']].groupby('REPORT_DATE').sum()
        holder = organ_holder.merge(person_holder, left_index=True, right_index=True, how='outer').fillna(0.0)
        holder['ORGAN_RATIO'] = holder['ORGAN_MV'] / (holder['ORGAN_MV'] + holder['PERSON_MV'])
        holder['PERSON_RATIO'] = holder['PERSON_MV'] / (holder['ORGAN_MV'] + holder['PERSON_MV'])
        holder = holder.sort_index()

        holder_disp = holder.copy(deep=True)
        holder_disp = holder_disp.iloc[-12:].reset_index()
        holder_disp['ORGAN_MV'] = holder_disp['ORGAN_MV'] / 100000000.0
        holder_disp['PERSON_MV'] = holder_disp['PERSON_MV'] / 100000000.0
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        bar_width = 0.3
        ax1.bar(np.arange(len(holder_disp)) - 0.5 * bar_width, holder_disp['ORGAN_MV'].values, bar_width, label='机构持有规模（亿元）', color=bar_color_list[0])
        ax1.bar(np.arange(len(holder_disp)) + 0.5 * bar_width, holder_disp['PERSON_MV'].values, bar_width, label='个人持有规模（亿元）', color=bar_color_list[14])
        ax2.plot(np.arange(len(holder_disp)), holder_disp['ORGAN_RATIO'].values, label='机构持有比例（右轴）', color=bar_color_list[7])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=3)
        ax1.set_xticks(np.arange(len(holder_disp)))
        ax1.set_xticklabels(labels=holder_disp['REPORT_DATE'].unique().tolist(), rotation=45)
        ax2.set_ylim([0, 0.3])
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.xlabel('')
        plt.ylabel('')
        plt.title('主动权益型基金各报告期持有人结构', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        sns.despine(left=False, bottom=False, top=True, right=False)
        plt.tight_layout()
        plt.savefig('{0}fund_holder.png'.format(self.data_path))
        return

    def get_fund_inner_holder(self):
        all_fund_holder = self.all_fund_holder.copy(deep=True)
        all_fund_position = self.all_fund_position.copy(deep=True)
        fund = self.fund.copy(deep=True)
        # fund = self.fund.sort_values(['FUND_FULL_NAME', 'FUND_CODE']).drop_duplicates('FUND_FULL_NAME')
        holder = all_fund_holder[['FUND_CODE', 'REPORT_DATE', 'STAFF_RATIO']].merge(all_fund_position[['FUND_CODE', 'REPORT_DATE', 'NET_ASSETS']], on=['FUND_CODE', 'REPORT_DATE'], how='left')
        holder = holder[holder['FUND_CODE'].isin(fund['FUND_CODE'].unique().tolist())]
        holder = holder[['FUND_CODE', 'REPORT_DATE', 'NET_ASSETS', 'STAFF_RATIO']]
        holder = holder.dropna()
        holder['STAFF_MV'] = 0.01 * holder['STAFF_RATIO'] * holder['NET_ASSETS']
        staff_holder = holder[['REPORT_DATE', 'STAFF_MV']].groupby('REPORT_DATE').sum()
        all_holder = holder[['REPORT_DATE', 'NET_ASSETS']].groupby('REPORT_DATE').sum()
        holder = staff_holder.merge(all_holder, left_index=True, right_index=True, how='outer').fillna(0.0)
        holder['STAFF_RATIO'] = holder['STAFF_MV'] / holder['NET_ASSETS']
        holder = holder.sort_index()

        holder_disp = holder.copy(deep=True)
        holder_disp = holder_disp.iloc[-12:].reset_index()
        holder_disp['STAFF_MV'] = holder_disp['STAFF_MV'] / 100000000.0
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.bar(np.arange(len(holder_disp)), holder_disp['STAFF_MV'].values, label='内部人持有规模（亿元）', color=bar_color_list[0])
        ax2.plot(np.arange(len(holder_disp)), holder_disp['STAFF_RATIO'].values, label='内部人持有比例（右轴）', color=bar_color_list[7])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=3)
        ax1.set_xticks(np.arange(len(holder_disp)))
        ax1.set_xticklabels(labels=holder_disp['REPORT_DATE'].unique().tolist(), rotation=45)
        ax2.set_ylim([0, 0.005])
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent_r3))
        plt.xlabel('')
        plt.ylabel('')
        plt.title('主动权益型基金各报告期内部持有人情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        sns.despine(left=False, bottom=False, top=True, right=False)
        plt.tight_layout()
        plt.savefig('{0}fund_inner_holder.png'.format(self.data_path))
        return

    def get_fund_return(self):
        latest_date = '20221109'
        fund_return_period = HBDB().read_fund_return_period_given_codes_and_date(self.all_fund['FUND_CODE'].unique().tolist(), latest_date)
        fund_return_period.to_hdf('{0}fund_return_period_{1}.hdf'.format(self.data_path, latest_date), key='table', mode='w')
        fund_return_period = pd.read_hdf('{0}fund_return_period_{1}.hdf'.format(self.data_path, latest_date), key='table')
        fund_return_period = fund_return_period.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'RETURN_TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'zbnhnp': 'ANNUAL_RETURN'})
        fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].astype(int)
        fund_return_period = fund_return_period[fund_return_period['RETURN_TYPE'] == 2998]
        fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].replace({2998: '2022'})
        fund_return_period['RETURN'] = fund_return_period['RETURN'].replace(99999.0, np.nan)
        fund_return_period = fund_return_period.pivot(index='RETURN_TYPE', columns='FUND_CODE', values='RETURN')

        all_fund_return_year = self.all_fund_return_year.pivot(index='YEAR', columns='FUND_CODE', values='RETURN')
        all_fund_return_year = all_fund_return_year.sort_index()
        all_fund_return_year = pd.concat([all_fund_return_year, fund_return_period])

        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        year_list = list(range(2016, 2023))
        period_list = [0, 20, 40, 60, 80, 100]
        fund_holder_return_year = pd.DataFrame(index=year_list, columns=['{0}%-{1}%'.format(period_list[i - 1], period_list[i]) for i, _ in enumerate(period_list) if i != 0] + ['全部'])
        for year in year_list:
            report_date = str(year - 1) + '1231'
            all_fund_holder_date = all_fund_holder[all_fund_holder['REPORT_DATE'] == report_date]
            all_fund_codes = list(set(all_fund_return_year.columns) & set(all_fund_holder_date['FUND_CODE'].unique().tolist()))
            fund_holder_return_year.loc[year, '全部'] = all_fund_return_year.loc[str(year), all_fund_codes].dropna().mean()
            for i, _ in enumerate(period_list):
                if i == 0:
                    continue
                fund_holder_date = all_fund_holder_date[(all_fund_holder_date['ORGAN_RATIO'] >= period_list[i - 1]) & (all_fund_holder_date['ORGAN_RATIO'] <= period_list[i])]
                columns = '{0}%-{1}%'.format(period_list[i - 1], period_list[i])
                fund_codes = list(set(all_fund_return_year.columns) & set(fund_holder_date['FUND_CODE'].unique().tolist()))
                fund_holder_return_year.loc[year, columns] = all_fund_return_year.loc[str(year), fund_codes].dropna().mean()
        fund_holder_return_year.to_excel('{0}fund_holder_return_year.xlsx'.format(self.data_path))
        return

    def get_fund_maxdrawdown(self):
        latest_date = '20221109'
        fund_maxdrawdown_period = HBDB().read_fund_maxdrawdown_period_given_codes_and_date(self.all_fund['FUND_CODE'].unique().tolist(), latest_date)
        fund_maxdrawdown_period.to_hdf('{0}fund_maxdrawdown_period_{1}.hdf'.format(self.data_path, latest_date), key='table', mode='w')
        fund_maxdrawdown_period = pd.read_hdf('{0}fund_maxdrawdown_period_{1}.hdf'.format(self.data_path, latest_date), key='table')
        fund_maxdrawdown_period = fund_maxdrawdown_period.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'zblb': 'MAXDRAWDOWN_TYPE', 'zbnp': 'MAXDRAWDOWN', 'zdhchfts': 'RECOVERY_DAYS', 'zdhccxts': 'CONTINUE_DAYS'})
        fund_maxdrawdown_period['MAXDRAWDOWN_TYPE'] = fund_maxdrawdown_period['MAXDRAWDOWN_TYPE'].astype(int)
        fund_maxdrawdown_period = fund_maxdrawdown_period[fund_maxdrawdown_period['MAXDRAWDOWN_TYPE'] == 2998]
        fund_maxdrawdown_period['MAXDRAWDOWN_TYPE'] = fund_maxdrawdown_period['MAXDRAWDOWN_TYPE'].replace({2998: '2022'})
        fund_maxdrawdown_period['MAXDRAWDOWN'] = fund_maxdrawdown_period['MAXDRAWDOWN'].replace(99999.0, np.nan)
        fund_maxdrawdown_period = fund_maxdrawdown_period.pivot(index='MAXDRAWDOWN_TYPE', columns='FUND_CODE', values='MAXDRAWDOWN')

        all_fund_maxdrawdown_year = self.all_fund_maxdrawdown_year.pivot(index='YEAR', columns='FUND_CODE', values='MAXDRAWDOWN')
        all_fund_maxdrawdown_year = all_fund_maxdrawdown_year.sort_index()
        all_fund_maxdrawdown_year = pd.concat([all_fund_maxdrawdown_year, fund_maxdrawdown_period])

        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        year_list = list(range(2016, 2023))
        period_list = [0, 20, 40, 60, 80, 100]
        fund_holder_maxdrawdown_year = pd.DataFrame(index=year_list, columns=['{0}%-{1}%'.format(period_list[i - 1], period_list[i]) for i, _ in enumerate(period_list) if i != 0] + ['全部'])
        for year in year_list:
            report_date = str(year - 1) + '1231'
            all_fund_holder_date = all_fund_holder[all_fund_holder['REPORT_DATE'] == report_date]
            all_fund_codes = list(set(all_fund_maxdrawdown_year.columns) & set(all_fund_holder_date['FUND_CODE'].unique().tolist()))
            fund_holder_maxdrawdown_year.loc[year, '全部'] = all_fund_maxdrawdown_year.loc[str(year), all_fund_codes].dropna().mean()
            for i, _ in enumerate(period_list):
                if i == 0:
                    continue
                fund_holder_date = all_fund_holder_date[(all_fund_holder_date['ORGAN_RATIO'] >= period_list[i - 1]) & (all_fund_holder_date['ORGAN_RATIO'] <= period_list[i])]
                columns = '{0}%-{1}%'.format(period_list[i - 1], period_list[i])
                fund_codes = list(set(all_fund_maxdrawdown_year.columns) & set(fund_holder_date['FUND_CODE'].unique().tolist()))
                fund_holder_maxdrawdown_year.loc[year, columns] = all_fund_maxdrawdown_year.loc[str(year), fund_codes].dropna().mean()
        fund_holder_maxdrawdown_year.to_excel('{0}fund_holder_maxdrawdown_year.xlsx'.format(self.data_path))
        return

    def get_fund_change_return(self):
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder_change = all_fund_holder.pct_change()
        all_fund_holder = all_fund_holder.unstack().reset_index().dropna()
        all_fund_holder.columns = ['FUND_CODE', 'REPORT_DATE', 'ORGAN_RATIO']
        all_fund_holder_change = all_fund_holder_change.unstack().reset_index().dropna()
        all_fund_holder_change.columns = ['FUND_CODE', 'REPORT_DATE', 'ORGAN_RATIO_CHANGE']
        all_fund_holder = all_fund_holder.merge(all_fund_holder_change, on=['FUND_CODE', 'REPORT_DATE'], how='inner').dropna()
        date_list = sorted(all_fund_holder_change[all_fund_holder_change['REPORT_DATE'] >= '20151231']['REPORT_DATE'].unique().tolist())

        fund_return_period_list = []
        for date in date_list:
            recent_trade_date = self.trade_df[self.trade_df['TRADE_DATE'] <= date]['TRADE_DATE'].iloc[-1]
            fund_return_period = HBDB().read_fund_return_period_given_codes_and_date(self.all_fund['FUND_CODE'].unique().tolist(), recent_trade_date)
            fund_return_period.to_hdf('{0}fund_return_period_{1}.hdf'.format(self.data_path, recent_trade_date), key='table', mode='w')
            fund_return_period = pd.read_hdf('{0}fund_return_period_{1}.hdf'.format(self.data_path, recent_trade_date), key='table')
            fund_return_period_list.append(fund_return_period)
            print(date)
        fund_return_period = pd.concat(fund_return_period_list)
        fund_return_period.to_hdf('{0}fund_return_period_semiyear.hdf'.format(self.data_path), key='table', mode='w')
        fund_return_period = pd.read_hdf('{0}fund_return_period_semiyear.hdf'.format(self.data_path), key='table')
        fund_return_period = fund_return_period.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'RETURN_TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'zbnhnp': 'ANNUAL_RETURN'})
        fund_return_period['END_DATE'] = fund_return_period['END_DATE'].astype(str)
        fund_return_period['REPORT_DATE'] = fund_return_period['END_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')
        fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].astype(int)
        fund_return_period = fund_return_period[fund_return_period['RETURN_TYPE'] == 2106]
        fund_return_period['RETURN'] = fund_return_period['RETURN'].replace(99999.0, np.nan)
        fund_return_period = fund_return_period.dropna()
        fund_return_period = fund_return_period.pivot(index='REPORT_DATE', columns='FUND_CODE', values='RETURN')

        fund_holder_change_return_semiyear = pd.DataFrame(index=date_list[1:], columns=['TOP{0}'.format(i) for i in range(1, 6)] + ['全部'])
        for idx, date in enumerate(date_list):
            if idx == 0:
                continue
            last_date = date_list[idx - 1]
            all_fund_holder_date = all_fund_holder[all_fund_holder['REPORT_DATE'] == last_date]
            all_fund_codes = list(set(fund_return_period.columns) & set(all_fund_holder_date['FUND_CODE'].unique().tolist()))
            fund_holder_change_return_semiyear.loc[date, '全部'] = fund_return_period.loc[date, all_fund_codes].dropna().mean()
            for i in range(5):
                min_q = all_fund_holder_date['ORGAN_RATIO_CHANGE'].quantile(0.2 * i) if i != 0 else all_fund_holder_date['ORGAN_RATIO_CHANGE'].min()
                max_q = all_fund_holder_date['ORGAN_RATIO_CHANGE'].quantile(0.2 * (i + 1)) if i != 4 else all_fund_holder_date['ORGAN_RATIO_CHANGE'].max()
                fund_holder_date = all_fund_holder_date[(all_fund_holder_date['ORGAN_RATIO_CHANGE'] >= min_q) & (all_fund_holder_date['ORGAN_RATIO_CHANGE'] <= max_q)]
                fund_codes = list(set(fund_return_period.columns) & set(fund_holder_date['FUND_CODE'].unique().tolist()))
                fund_holder_change_return_semiyear.loc[date, 'TOP{0}'.format(i + 1)] = fund_return_period.loc[date, fund_codes].dropna().mean()
        fund_holder_change_return_semiyear.to_excel('{0}fund_holder_change_return_semiyear.xlsx'.format(self.data_path))

        fund_holder_return_semiyear_dict = {}
        period_list = [0, 20, 40, 60, 80, 100]
        for idx, date in enumerate(date_list):
            if idx == 0:
                continue
            fund_holder_return_semiyear = pd.DataFrame(index=['TOP{0}'.format(i) for i in range(1, 6)], columns=['TOP{0}'.format(i) for i in range(1, 6)])
            last_date = date_list[idx - 1]
            all_fund_holder_date = all_fund_holder[all_fund_holder['REPORT_DATE'] == last_date]
            for i in range(5):
                print(period_list[i], period_list[i + 1])
                fund_holder_date = all_fund_holder_date[(all_fund_holder_date['ORGAN_RATIO'] >= period_list[i]) & (all_fund_holder_date['ORGAN_RATIO'] <= period_list[i + 1])]
                for j in range(5):
                    print(0.2 * j, 0.2 * (j + 1))
                    min_q = fund_holder_date['ORGAN_RATIO_CHANGE'].quantile(0.2 * j) if j != 0 else fund_holder_date['ORGAN_RATIO_CHANGE'].min()
                    max_q = fund_holder_date['ORGAN_RATIO_CHANGE'].quantile(0.2 * (j + 1)) if j != 4 else fund_holder_date['ORGAN_RATIO_CHANGE'].max()
                    fund_holder_date_group = fund_holder_date[(fund_holder_date['ORGAN_RATIO_CHANGE'] >= min_q) & (fund_holder_date['ORGAN_RATIO_CHANGE'] <= max_q)]
                    fund_codes = list(set(fund_return_period.columns) & set(fund_holder_date_group['FUND_CODE'].unique().tolist()))
                    fund_holder_return_semiyear.loc['TOP{0}'.format(i + 1), 'TOP{0}'.format(j + 1)] = fund_return_period.loc[date, fund_codes].dropna().mean()
            fund_holder_return_semiyear_dict[date] = fund_holder_return_semiyear
        fund_holder_return_semiyear = fund_holder_return_semiyear_dict[date_list[1]]
        for date in date_list[2:]:
            fund_holder_return_semiyear += fund_holder_return_semiyear_dict[date]
        fund_holder_return_semiyear = fund_holder_return_semiyear / (len(date_list) - 1)
        fund_holder_return_semiyear.to_excel('{0}fund_holder_return_semiyear.xlsx'.format(self.data_path))
        return

    def get_fund_shift_cen(self):
        hbs_rank_history = FEDB().read_hbs_rank_history_given_codes(self.fund['FUND_CODE'].unique().tolist())
        hbs_rank_history.to_hdf('{0}hbs_rank_history.hdf'.format(self.data_path), key='table', mode='w')
        hbs_rank_history = pd.read_hdf('{0}hbs_rank_history.hdf'.format(self.data_path), key='table')
        hbs_rank_history = hbs_rank_history.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'shift_ratio_size': 'SIZE_SHIFT_RANK', 'c_level_size': 'SIZE_CEN_RANK', 'shift_ratio_style': 'STYLE_SHIFT_RANK', 'c_level_style': 'STYLE_CEN_RANK', 'shift_ratio_theme': 'THEME_SHIFT_RANK', 'c_level_theme': 'THEME_CEN_RANK', 'shift_ratio_ind': 'INDUSTRY_SHIFT_RANK', 'c_level_ind': 'INDUSTRY_CEN_RANK', 'c_level_stock': 'STOCK_CEN_RANK'})
        hbs_rank_history['REPORT_DATE'] = hbs_rank_history['REPORT_DATE'].astype(str)
        hbs_rank_history['REPORT_DATE'] = hbs_rank_history['REPORT_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')

        fund_turnover = HBDB().read_fund_turnover_given_codes(self.fund['FUND_CODE'].unique().tolist())
        fund_turnover.to_hdf('{0}fund_turnover.hdf'.format(self.data_path), key='table', mode='w')
        fund_turnover = pd.read_hdf('{0}fund_turnover.hdf'.format(self.data_path), key='table')
        fund_turnover = fund_turnover.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'tjqj': 'TYPE', 'hsl': 'STOCK_SHIFT'})
        fund_turnover['REPORT_DATE'] = fund_turnover['REPORT_DATE'].astype(str)
        fund_turnover = fund_turnover.sort_values('REPORT_DATE')
        fund_turnover = fund_turnover[fund_turnover['TYPE'].isin(['1', '3'])]
        fund_turnover['STOCK_SHIFT'] = fund_turnover['STOCK_SHIFT'] * 2.0
        fund_turnover_count = fund_turnover[['REPORT_DATE', 'FUND_CODE']].groupby('REPORT_DATE').count().reset_index().rename(columns={'FUND_CODE': 'COUNT'})
        fund_turnover['STOCK_SHIFT_RANK'] = fund_turnover[['REPORT_DATE', 'STOCK_SHIFT']].groupby('REPORT_DATE').rank(method='min')
        fund_turnover = fund_turnover.merge(fund_turnover_count, on=['REPORT_DATE'], how='left')
        fund_turnover['STOCK_SHIFT_RANK'] = fund_turnover['STOCK_SHIFT_RANK'] / fund_turnover['COUNT']
        fund_turnover = fund_turnover[['FUND_CODE', 'REPORT_DATE', 'STOCK_SHIFT_RANK']]

        hbs_rank_history = hbs_rank_history.merge(fund_turnover, on=['FUND_CODE', 'REPORT_DATE'], how='left')

        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder = all_fund_holder.iloc[-6:]
        all_fund_holder = pd.DataFrame(all_fund_holder.mean()).reset_index()
        all_fund_holder.columns = ['FUND_CODE', 'ORGAN_RATIO']

        period_list = [0, 20, 40, 60, 80, 100]
        columns = list(hbs_rank_history.columns)[2:]
        fund_holder_hbs = pd.DataFrame(index=['{0}%-{1}%'.format(period_list[i], period_list[i + 1]) for i in range(5)], columns=columns)
        for col in columns:
            hbs_rank_history_col = hbs_rank_history.pivot(index='REPORT_DATE', columns='FUND_CODE', values=col).sort_index()
            hbs_rank_history_col = hbs_rank_history_col.iloc[-12:]
            hbs_rank_history_col = pd.DataFrame(hbs_rank_history_col.mean()).reset_index()
            hbs_rank_history_col.columns = ['FUND_CODE', col]
            for i in range(5):
                fund_holder = all_fund_holder[(all_fund_holder['ORGAN_RATIO'] >= period_list[i]) & (all_fund_holder['ORGAN_RATIO'] <= period_list[i + 1])]
                fund_holder = fund_holder.merge(hbs_rank_history_col, on=['FUND_CODE'], how='left')
                index = '{0}%-{1}%'.format(period_list[i], period_list[i + 1])
                fund_holder_hbs.loc[index, col] = fund_holder[col].dropna().mean()
        fund_holder_hbs.to_excel('{0}fund_holder_hbs.xlsx'.format(self.data_path))

        fund_holder_hbs_disp = fund_holder_hbs.reset_index().rename(columns={'index': 'PERIOD'})
        type = '_SHIFT_RANK' # _SHIFT_RANK _CEN_RANK
        fig, ax = plt.subplots(figsize=(12, 6))
        for i, col in enumerate(['SIZE{0}'.format(type), 'STYLE{0}'.format(type), 'THEME{0}'.format(type), 'INDUSTRY{0}'.format(type), 'STOCK{0}'.format(type)]):
            label = '规模' if col.split(type)[0] == 'SIZE' else '风格' if col.split(type)[0] == 'STYLE' else '主题' if col.split(type)[0] == 'THEME' else '行业' if col.split(type)[0] == 'INDUSTRY' else '个股'
            plt.plot(fund_holder_hbs_disp.index, fund_holder_hbs_disp[col].values, '-o', label=label, color=new_color_list[i])
            plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=5)
            ax.set_xticks(np.arange(len(fund_holder_hbs_disp)))
            ax.set_xticklabels(labels=fund_holder_hbs_disp['PERIOD'].unique().tolist())
            ax.yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('')
            plt.ylabel('')
            plt.title('换手率排名' if type == '_SHIFT_RANK' else '集中度排名', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
            sns.despine(left=False, bottom=False, top=True, right=True)
            plt.tight_layout()
            plt.savefig('{0}fund_holder_{1}.png'.format(self.data_path, 'shift' if type == '_SHIFT_RANK' else 'cen'))
        return

    def get_fund_style(self):
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder = all_fund_holder.iloc[-6:]
        all_fund_holder = pd.DataFrame(all_fund_holder.mean()).reset_index()
        all_fund_holder.columns = ['FUND_CODE', 'ORGAN_RATIO']

        hbs_size_property = FEDB().read_hbs_size_property_given_codes(self.fund['FUND_CODE'].unique().tolist())
        hbs_size_property.to_hdf('{0}hbs_size_property.hdf'.format(self.data_path), key='table', mode='w')
        hbs_size_property = pd.read_hdf('{0}hbs_size_property.hdf'.format(self.data_path), key='table')
        hbs_size_property = hbs_size_property.rename(columns={'jjdm': 'FUND_CODE', 'asofdate': 'REPORT_DATE'})
        hbs_size_property = hbs_size_property[['FUND_CODE', 'REPORT_DATE', '大盘_rank', '中盘_rank', '小盘_rank']]
        hbs_style_property = FEDB().read_hbs_style_property_given_codes(self.fund['FUND_CODE'].unique().tolist())
        hbs_style_property.to_hdf('{0}hbs_style_property.hdf'.format(self.data_path), key='table', mode='w')
        hbs_style_property = pd.read_hdf('{0}hbs_style_property.hdf'.format(self.data_path), key='table')
        hbs_style_property = hbs_style_property.rename(columns={'jjdm': 'FUND_CODE', 'asofdate': 'REPORT_DATE'})
        hbs_style_property = hbs_style_property[['FUND_CODE', 'REPORT_DATE', '成长_rank', '价值_rank']]
        hbs_property = hbs_size_property.merge(hbs_style_property, on=['FUND_CODE', 'REPORT_DATE'], how='left')

        period_list = [0, 20, 40, 60, 80, 100]
        columns = list(hbs_property.columns)[2:]
        fund_holder_style = pd.DataFrame(index=['{0}%-{1}%'.format(period_list[i], period_list[i + 1]) for i in range(5)], columns=columns)
        for col in columns:
            for i in range(5):
                fund_holder = all_fund_holder[(all_fund_holder['ORGAN_RATIO'] >= period_list[i]) & (all_fund_holder['ORGAN_RATIO'] <= period_list[i + 1])]
                fund_holder = fund_holder.merge(hbs_property[['FUND_CODE', col]], on=['FUND_CODE'], how='left')
                index = '{0}%-{1}%'.format(period_list[i], period_list[i + 1])
                fund_holder_style.loc[index, col] = fund_holder[col].dropna().mean()
        fund_holder_style.to_excel('{0}fund_holder_style.xlsx'.format(self.data_path))

        fund_holder_style_disp = fund_holder_style.reset_index().rename(columns={'index': 'PERIOD'})
        type = 'SIZE'  # SIZE STYLE
        columns = ['大盘_rank', '中盘_rank', '小盘_rank'] if type == 'SIZE' else ['成长_rank', '价值_rank']
        fig, ax = plt.subplots(figsize=(12, 6))
        for i, col in enumerate(columns):
            plt.plot(fund_holder_style_disp.index, fund_holder_style_disp[col].values, '-o', label=col.replace('_rank', ''), color=new_color_list[i])
            plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=5)
            ax.set_xticks(np.arange(len(fund_holder_style_disp)))
            ax.set_xticklabels(labels=fund_holder_style_disp['PERIOD'].unique().tolist())
            ax.yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('')
            plt.ylabel('')
            plt.title('大中小盘暴露排名' if type == 'SIZE' else '成长价值暴露排名', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
            sns.despine(left=False, bottom=False, top=True, right=True)
            plt.tight_layout()
            plt.savefig('{0}fund_holder_{1}.png'.format(self.data_path, 'size' if type == 'SIZE' else 'style'))
        return

    def get_fund_finance(self):
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder = all_fund_holder.iloc[-6:]
        all_fund_holder = pd.DataFrame(all_fund_holder.mean()).reset_index()
        all_fund_holder.columns = ['FUND_CODE', 'ORGAN_RATIO']

        fund_finance = HBDB().read_fund_valuation_given_codes(self.fund['FUND_CODE'].unique().tolist())
        fund_finance.to_hdf('{0}fund_finance.hdf'.format(self.data_path), key='table', mode='w')
        fund_finance = pd.read_hdf('{0}fund_finance.hdf'.format(self.data_path), key='table')
        fund_finance = fund_finance.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zclb': 'IS_ZC', 'pe': 'PE', 'pb': 'PB', 'roe': 'ROE', 'dividend': 'DIVIDEND'})
        fund_finance['REPORT_DATE'] = fund_finance['REPORT_DATE'].astype(int)
        fund_finance = fund_finance[fund_finance['IS_ZC'] == 1]
        fund_finance = fund_finance[['FUND_CODE', 'REPORT_DATE', 'PE', 'PB', 'ROE', 'DIVIDEND']]
        fund_finance['PE'] = fund_finance['PE'].replace(99999.0, np.nan)
        fund_finance['PB'] = fund_finance['PB'].replace(99999.0, np.nan)
        fund_finance['ROE'] = fund_finance['ROE'].replace(99999.0, np.nan)
        fund_finance['DIVIDEND'] = fund_finance['DIVIDEND'].replace(99999.0, np.nan)

        period_list = [0, 20, 40, 60, 80, 100]
        columns = list(fund_finance.columns)[2:]
        fund_holder_finance = pd.DataFrame(index=['{0}%-{1}%'.format(period_list[i], period_list[i + 1]) for i in range(5)], columns=columns)
        for col in columns:
            hbs_rank_history_col = fund_finance.pivot(index='REPORT_DATE', columns='FUND_CODE', values=col).sort_index()
            hbs_rank_history_col = hbs_rank_history_col.iloc[-12:]
            hbs_rank_history_col = pd.DataFrame(hbs_rank_history_col.mean()).reset_index()
            hbs_rank_history_col.columns = ['FUND_CODE', col]
            for i in range(5):
                fund_holder = all_fund_holder[(all_fund_holder['ORGAN_RATIO'] >= period_list[i]) & ( all_fund_holder['ORGAN_RATIO'] <= period_list[i + 1])]
                fund_holder = fund_holder.merge(hbs_rank_history_col, on=['FUND_CODE'], how='left')
                index = '{0}%-{1}%'.format(period_list[i], period_list[i + 1])
                fund_holder_finance.loc[index, col] = fund_holder[col].dropna().mean()
        fund_holder_finance.to_excel('{0}fund_holder_finance.xlsx'.format(self.data_path))
        return

    def get_fund_brison(self):
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder = all_fund_holder.iloc[-6:]
        all_fund_holder = pd.DataFrame(all_fund_holder.mean()).reset_index()
        all_fund_holder.columns = ['FUND_CODE', 'ORGAN_RATIO']

        fund_brinson = HBDB().read_fund_brinson_attribution_given_codes(self.fund['FUND_CODE'].unique().tolist())
        fund_brinson.to_hdf('{0}fund_brinson.hdf'.format(self.data_path), key='table', mode='w')
        fund_brinson = pd.read_hdf('{0}fund_brinson.hdf'.format(self.data_path), key='table')
        fund_brinson = fund_brinson.rename(columns={'jjdm': 'FUND_CODE', 'tjrq': 'REPORT_DATE', 'asset_allo': '大类资产配置收益', 'sector_allo': '行业配置收益', 'equity_selection': '行业选股收益', 'trading': '交易收益'})
        fund_brinson['REPORT_DATE'] = fund_brinson['REPORT_DATE'].astype(str)
        fund_brinson['REPORT_DATE'] = fund_brinson['REPORT_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')
        fund_brinson = fund_brinson.sort_values('REPORT_DATE')
        fund_brinson['总超额收益'] = fund_brinson['portfolio_return'] - fund_brinson['benchmark_return']
        fund_brinson = fund_brinson[['FUND_CODE', 'REPORT_DATE', '总超额收益', '大类资产配置收益', '行业配置收益', '行业选股收益', '交易收益']]
        fund_brinson['总超额收益'] = fund_brinson['总超额收益'].replace(99999.0, np.nan)
        fund_brinson['大类资产配置收益'] = fund_brinson['大类资产配置收益'].replace(99999.0, np.nan)
        fund_brinson['行业配置收益'] = fund_brinson['行业配置收益'].replace(99999.0, np.nan)
        fund_brinson['行业选股收益'] = fund_brinson['行业选股收益'].replace(99999.0, np.nan)
        fund_brinson['交易收益'] = fund_brinson['交易收益'].replace(99999.0, np.nan)

        period_list = [0, 20, 40, 60, 80, 100]
        columns = list(fund_brinson.columns)[2:]
        fund_holder_brison = pd.DataFrame(index=['{0}%-{1}%'.format(period_list[i], period_list[i + 1]) for i in range(5)], columns=columns)
        for col in columns:
            hbs_rank_history_col = fund_brinson.pivot(index='REPORT_DATE', columns='FUND_CODE', values=col).sort_index()
            hbs_rank_history_col = hbs_rank_history_col.iloc[-6:]
            hbs_rank_history_col = pd.DataFrame(hbs_rank_history_col.mean()).reset_index()
            hbs_rank_history_col.columns = ['FUND_CODE', col]
            for i in range(5):
                fund_holder = all_fund_holder[(all_fund_holder['ORGAN_RATIO'] >= period_list[i]) & (all_fund_holder['ORGAN_RATIO'] <= period_list[i + 1])]
                fund_holder = fund_holder.merge(hbs_rank_history_col, on=['FUND_CODE'], how='left')
                index = '{0}%-{1}%'.format(period_list[i], period_list[i + 1])
                fund_holder_brison.loc[index, col] = fund_holder[col].dropna().mean()
        fund_holder_brison.to_excel('{0}fund_holder_brison.xlsx'.format(self.data_path))
        return

    def get_fund_company(self):
        all_fund_holder = self.all_fund_holder[self.all_fund_holder['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_holder = all_fund_holder.pivot(index='REPORT_DATE', columns='FUND_CODE', values='ORGAN_RATIO').sort_index()
        all_fund_holder = all_fund_holder.iloc[-6:]
        all_fund_holder = pd.DataFrame(all_fund_holder.mean()).reset_index()
        all_fund_holder.columns = ['FUND_CODE', 'ORGAN_RATIO']

        fund_company_list = []
        for fund_code in self.fund['FUND_CODE'].unique().tolist():
            fund_company = HBDB().read_fund_company_given_code(fund_code)
            fund_company_list.append(fund_company)
        fund_company = pd.concat(fund_company_list)
        fund_company.to_hdf('{0}fund_company.hdf'.format(self.data_path), key='table', mode='w')
        fund_company = pd.read_hdf('{0}fund_company.hdf'.format(self.data_path), key='table')
        fund_company = fund_company.rename(columns={'JJDM': 'FUND_CODE', 'JGDM': 'COMPANY_CODE', 'JGMC': 'COMPANY_NAME'})

        all_fund_holder = all_fund_holder.merge(fund_company, on=['FUND_CODE'], how='left')
        all_fund_holder = all_fund_holder[['COMPANY_NAME', 'ORGAN_RATIO']].groupby('COMPANY_NAME').mean()
        all_fund_holder = all_fund_holder.sort_values('ORGAN_RATIO', ascending=False)
        return

    def get_analysis(self):
        self.get_all_fund_holder()
        self.get_fund_holder()
        self.get_fund_inner_holder()
        self.get_fund_return()
        self.get_fund_maxdrawdown()
        self.get_fund_change_return()
        self.get_fund_shift_cen()
        self.get_fund_style()
        self.get_fund_finance()
        self.get_fund_brison()
        self.get_fund_company()
        return



if __name__ == "__main__":
    date = '20220630'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/fund_holder_structure/'
    HolderStructure(date, data_path).get_analysis()