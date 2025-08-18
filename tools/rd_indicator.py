import pandas as pd


def rd_indicator(file_path:str, filename:str):
    """
    讀取 Excel 檔案並處理RD指標。
    :param file_path: Excel 檔案路徑
    :return: new_file_path。
    """
    
    df_filtered = pd.read_excel(file_path)[:-2]

    if "Stage0" in df_filtered["Stage"].values:
        return "Stage0未刪除，請檢查"
    elif df_filtered["Stage"].isna().any():
        return "Stage欄位有空值，請檢查"
    else:
        # 將 Stage 分為「stage1~4」與「stage5+」
        def classify_stage(stage):
            if isinstance(stage, str):
                if stage.startswith(("Stage1", "Stage2", "Stage3", "Stage4")):
                    return "Stage1~4"
                else:
                    return "Stage5"
            return "其他"

        # 將收案月數分為「大於12個月」與「小於12個月」
        def classify_month(month_text):
            return "大於12個月" if "大於" in str(month_text) else "小於12個月"

        # 加入分組欄位
        df_filtered["StageGroup"] = df_filtered["Stage"].apply(classify_stage)
        df_filtered["MonthsGroup"] = df_filtered["收案月數"].apply(classify_month)
        # print(df_filtered)

        # 分成四組
        group1 = df_filtered[(df_filtered["StageGroup"] == "Stage1~4") & (df_filtered["MonthsGroup"] == "大於12個月")]
        group2 = df_filtered[(df_filtered["StageGroup"] == "Stage1~4") & (df_filtered["MonthsGroup"] == "小於12個月")]
        group3 = df_filtered[(df_filtered["StageGroup"] == "Stage5") & (df_filtered["MonthsGroup"] == "大於12個月")]
        group4 = df_filtered[(df_filtered["StageGroup"] == "Stage5") & (df_filtered["MonthsGroup"] == "小於12個月")]

        # 計算每一組中「分子計次為 Y」的比例
        def calc_Y_ratio(df):
            if len(df) == 0:
                return "無資料"
            count_Y = (df["分子計次"] == "Y").sum()
            total = len(df)
            percent = round(count_Y / total * 100, 2)
            return f"{count_Y}/{total} = {percent}%"

        # 分別計算四組的比例
        result = {
        "分組": [
                "Stage1~4 & 大於12個月",
                "Stage1~4 & 小於12個月",
                "Stage5 & 大於12個月",
                "Stage5 & 小於12個月"
            ],
            "分子計次比例": [
                calc_Y_ratio(group1).split('=')[0].strip(),
                calc_Y_ratio(group2).split('=')[0].strip(),
                calc_Y_ratio(group3).split('=')[0].strip(),
                calc_Y_ratio(group4).split('=')[0].strip()
            ],
            "百分比": [
                calc_Y_ratio(group1).split('=')[1].strip(),
                calc_Y_ratio(group2).split('=')[1].strip(),
                calc_Y_ratio(group3).split('=')[1].strip(),
                calc_Y_ratio(group4).split('=')[1].strip()
            ]
        }
        df_result = pd.DataFrame(result)
        # print(df_result)

        output_path = './static/rd_indicator/'+filename.split('.')[0]+'_已完成.xlsx'
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name="原始資料")
            group1.to_excel(writer, index=False, sheet_name="Stage1~4 & 大於12個月")
            group2.to_excel(writer, index=False, sheet_name="Stage1~4 & 小於12個月")
            group3.to_excel(writer, index=False, sheet_name="Stage5 & 大於12個月")
            group4.to_excel(writer, index=False, sheet_name="Stage5 & 小於12個月")
            df_result.to_excel(writer, index=False, sheet_name="分子計次統計")
            
        print(f"{output_path}已存檔")
        return output_path

if __name__ == "__main__":
    file_path = "./11311RD指標數據.xlsx" 
    res = rd_indicator(file_path)
    print("程式執行完畢", res)
