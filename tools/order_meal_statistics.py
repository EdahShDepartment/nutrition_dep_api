import pandas as pd
import calendar
from datetime import datetime


MEAL_DICT={'HME41001': '早普',
         'HME41016': '早午晚普',
         'HME41018': '早普',
         'HME41055': '早午晚普',
         'HME41057': '早午晚普',
         'HME41073': '早午晚普',
         'HME41004': '早治1',
         'HME41017': '早午晚治1',
         'HME41021': '早治1',
         'HME41056': '早午晚治1',
         'HME41058': '早午晚治1',
         'HME41074': '早午晚治1',
         'HME41027': '早治2',
         'HME41031': '早治2',
         'HME41075': '早午晚治2',
         'HME41076': '早午晚治2',
         'HME41077': '早午晚治2',
         'HME41078': '早午晚治2',
         'HME41007': '早產',
         'HME41081': '早午晚產',
         'HME41083': '早午晚產',
         'HME41070': '早月',
         'HME41082': '早午晚月',
         'HME41010': '早貴',
         'HME41024': '早貴',
         'HME41079': '早午晚貴',
         'HME41084': '早午晚貴',
         'HME41002': '午普',
         'HME41019': '午普',
         'HME41005': '午治1',
         'HME41022': '午治1',
         'HME41028': '午治2',
         'HME41032': '午治2',
         'HME41008': '午產',
         'HME41071': '午月',
         'HME41011': '午貴',
         'HME41025': '午貴',
         'HME41003': '晚普',
         'HME41020': '晚普',
         'HME41006': '晚治1',
         'HME41023': '晚治1',
         'HME41029': '晚治2',
         'HME41033': '晚治2',
         'HME41009': '晚產',
         'HME41072': '晚月',
         'HME41080': '晚月子點心',
         'HME41012': '晚貴',
         'HME41026': '晚貴'}

COLUMNS_ORDER = [
    '早普', '早治1', '早治2', '早產', '早月', '早貴',
    '午普', '午治1', '午治2', '午產', '午月', '午貴',
    '晚普', '晚治1', '晚治2', '晚產', '晚月', '晚月子點心', '晚貴',
    '午餐 禁食']

PRICE_DICT = {
    '早普': 65,
    '早治1': 65,
    '早治2': 75,
    '早產': 105,
    '早月': 400,
    '早貴': 105,

    '午普': 105,
    '午治1': 115,
    '午治2': 125,
    '午產': 155,
    '午月': 400,
    '午貴': 155,

    '晚普': 105,
    '晚治1': 115,
    '晚治2': 135,
    '晚產': 195,
    '晚月': 400,
    '晚貴': 195,

    '晚月子點心': 200}


def order_meal_statistics(file_path:str, filename:str, month:int):
    """
    讀取 Excel 檔案並處理訂餐統計。
    :param file_path: Excel 檔案路徑
    :return: new_file_path。
    """
    
    df = pd.read_excel(file_path)

    now = datetime.now()
    year = now.year
    _, days_in_month = calendar.monthrange(year, month)

    df["餐別分類"] = df["price_code"].map(MEAL_DICT).fillna("午餐 禁食")

    # 根據餐別分類與日期進行分組統計
    daily_meal_counts = df.groupby(["start_date", "餐別分類"])["compute_0003"].sum().unstack(fill_value=0)
    #將各欄位+上早午晚
    daily_meal_counts['早普'] = daily_meal_counts.get('早普', 0) + daily_meal_counts.get('早午晚普', 0)
    daily_meal_counts['午普'] = daily_meal_counts.get('午普', 0) + daily_meal_counts.get('早午晚普', 0)
    daily_meal_counts['晚普'] = daily_meal_counts.get('晚普', 0) + daily_meal_counts.get('早午晚普', 0)

    daily_meal_counts['早治1'] = daily_meal_counts.get('早治1', 0) + daily_meal_counts.get('早午晚治1', 0)
    daily_meal_counts['午治1'] = daily_meal_counts.get('午治1', 0) + daily_meal_counts.get('早午晚治1', 0)
    daily_meal_counts['晚治1'] = daily_meal_counts.get('晚治1', 0) + daily_meal_counts.get('早午晚治1', 0)

    daily_meal_counts['早治2'] = daily_meal_counts.get('早治2', 0) + daily_meal_counts.get('早午晚治2', 0)
    daily_meal_counts['午治2'] = daily_meal_counts.get('午治2', 0) + daily_meal_counts.get('早午晚治2', 0)
    daily_meal_counts['晚治2'] = daily_meal_counts.get('晚治2', 0) + daily_meal_counts.get('早午晚治2', 0)

    daily_meal_counts['早月'] = daily_meal_counts.get('早月', 0) + daily_meal_counts.get('早午晚月', 0)
    daily_meal_counts['午月'] = daily_meal_counts.get('午月', 0) + daily_meal_counts.get('早午晚月', 0)
    daily_meal_counts['晚月'] = daily_meal_counts.get('晚月', 0) + daily_meal_counts.get('早午晚月', 0)

    daily_meal_counts['早產'] = daily_meal_counts.get('早產', 0) + daily_meal_counts.get('早午晚產', 0)
    daily_meal_counts['午產'] = daily_meal_counts.get('午產', 0) + daily_meal_counts.get('早午晚產', 0)
    daily_meal_counts['晚產'] = daily_meal_counts.get('晚產', 0) + daily_meal_counts.get('早午晚產', 0)

    daily_meal_counts['早貴'] = daily_meal_counts.get('早貴', 0) + daily_meal_counts.get('早午晚貴', 0)
    daily_meal_counts['午貴'] = daily_meal_counts.get('午貴', 0) + daily_meal_counts.get('早午晚貴', 0)
    daily_meal_counts['晚貴'] = daily_meal_counts.get('晚貴', 0) + daily_meal_counts.get('早午晚貴', 0)


    ordered_meal_counts = daily_meal_counts.reindex(columns=COLUMNS_ORDER, fill_value=0)
    df_total = ordered_meal_counts.copy()
    df_total.loc['Amount'] = df_total.sum()

    # 取出「數量」這一列
    total_row = df_total.loc["Amount"]
    # 數量 × 單價計算價錢
    price_row = total_row.multiply(pd.Series(PRICE_DICT), fill_value=0)
    df_total.loc["Price"] = price_row

    df_total.loc["分隔線"] = '-'

    df_total.loc["總數量", "早普"] = df_total.loc['Amount'].sum()
    df_total.loc["應付金額", "早普"] = df_total.loc['Price'].sum()

    df_total.loc[" ", "早普"] = 'Total'
    df_total.loc[" ", "早治1"] = '日平均'
    df_total.loc[" ", "早治2"] = '餐平均'

    df_total.loc["普餐", "早普"] = df_total.loc["Amount", "早普"]+df_total.loc["Amount", "午普"]+df_total.loc["Amount", "晚普"]
    df_total.loc["普餐", "早治1"] = round(df_total.loc["普餐", "早普"]/days_in_month, 1)
    df_total.loc["普餐", "早治2"] = round(df_total.loc["普餐", "早治1"]/3, 1)
    df_total.loc["治1餐", "早普"] = df_total.loc["Amount", "早治1"]+df_total.loc["Amount", "午治1"]+df_total.loc["Amount", "晚治1"]
    df_total.loc["治1餐", "早治1"] = round(df_total.loc["治1餐", "早普"]/days_in_month, 1)
    df_total.loc["治1餐", "早治2"] = round(df_total.loc["治1餐", "早治1"]/3, 1)
    df_total.loc["治2餐", "早普"] = df_total.loc["Amount", "早治2"]+df_total.loc["Amount", "午治2"]+df_total.loc["Amount", "晚治2"]
    df_total.loc["治2餐", "早治1"] = round(df_total.loc["治2餐", "早普"]/days_in_month, 1)
    df_total.loc["治2餐", "早治2"] = round(df_total.loc["治2餐", "早治1"]/3, 1)
    df_total.loc["產後餐", "早普"] = df_total.loc["Amount", "早產"]+df_total.loc["Amount", "午產"]+df_total.loc["Amount", "晚產"]
    df_total.loc["產後餐", "早治1"] = round(df_total.loc["產後餐", "早普"]/days_in_month, 1)
    df_total.loc["產後餐", "早治2"] = round(df_total.loc["產後餐", "早治1"]/3, 1)
    df_total.loc["月子餐", "早普"] = df_total.loc["Amount", "早月"]+df_total.loc["Amount", "午月"]+df_total.loc["Amount", "晚月"]
    df_total.loc["月子餐", "早治1"] = round(df_total.loc["月子餐", "早普"]/days_in_month, 1)
    df_total.loc["月子餐", "早治2"] = round(df_total.loc["月子餐", "早治1"]/3, 1)
    df_total.loc["貴賓餐", "早普"] = df_total.loc["Amount", "早貴"]+df_total.loc["Amount", "午貴"]+df_total.loc["Amount", "晚貴"]
    df_total.loc["貴賓餐", "早治1"] = round(df_total.loc["貴賓餐", "早普"]/days_in_month, 1)
    df_total.loc["貴賓餐", "早治2"] = round(df_total.loc["貴賓餐", "早治1"]/3, 1)
    
    output_path = './static/order_meal_statistics/'+filename.split('.')[0]+'_已完成.xlsx'
    df_total.to_excel(output_path, index=True)
    
    print(df_total)
    print(f"{output_path}已存檔")
    return output_path

if __name__ == "__main__":
    file_path = "./202506.xlsx" 
    res = order_meal_statistics(file_path)
    print("程式執行完畢", res)