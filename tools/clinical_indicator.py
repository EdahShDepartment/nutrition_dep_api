import pandas as pd
import os


#DA跟OPD不需要可以拿掉
bed_groups = [
    "3A", "3B", "3C", "3D", "3E", "3F", "3G", "3R",
    "5H", "DA", "5V", "5A", "5B",
    "6A", "6B", "7A", "7B",
    "8A", "8B", "9A", "9B", "10A", "10B", "11A", "11B",
    "12A", "12B", "13A", "13B",
    # "OPD", "門診"
]

def clinical_indicator(file_path: str, filename: str):
    """
    讀取 Excel 檔案並處理臨床指標。
    :param file_path: Excel 檔案路徑
    :return: new_file_path。
    """

    # 床號分群函式
    def classify_strict_bed(bed_no):
        # 5樓以前床號
        bed_groups = [
            "3A", "3B", "3C", "3D", "3E", "3F", "3G", "3R",
            "5H", "DA", "5V",
        ]
        bed_no = str(bed_no).strip().upper()
        # 解決Excel BUG=> 30='3E01', 300='3E02', ...
        if bed_no=="30":
            return '3E'
        elif bed_no=="300":
            return '3E'
        elif bed_no=="3000":
            return '3E'
        elif bed_no=="30000":
            return '3E'
        elif bed_no=="300000":
            return '3E'
        elif bed_no=="3000000":
            return '3E'
        elif bed_no=="30000000":
            return '3E'
        elif bed_no=="300000000":
            return '3E'
        elif bed_no=="3000000000":
            return '3E'
        
        if bed_no[:2] in bed_groups:
            return bed_no[:2]
        elif bed_no=='OPD':
            return 'OPD'
        else:
            #5樓以後看後面兩位數字判斷AB
            #先判斷最右邊是否有英文，有的話就移掉
            if bed_no[-1].isalpha():
                #把英文移掉
                bed_no = bed_no[:-1]
            bed_number_part = bed_no[-2:] # 取右邊兩位數字（床號）
            try:
                bed_number_part=int(bed_number_part)
            except ValueError:
                return "門診"
            if bed_number_part<50:
                r = 'A'
            else:
                r = 'B'
            # 樓層：移除床號（右兩碼）
            floor_part = bed_no[:-2]
            
            return str(floor_part)+r
                
    df = pd.read_excel(file_path)[1:]

    # 移除重複
    filtered_df = df.drop_duplicates(subset=[
        "save as", 
        "病歷號", 
        "姓名", 
        "表單類型", 
        "營養師", 
        "性別",
        "年齡"
    ]).reset_index(drop=True)

    #依照「營養師」分組，計算「表單類型」為 NG 和 Oral 的次數
    grouped_counts_df = filtered_df[filtered_df["表單類型"].isin(["NG", "Oral"])].groupby("營養師")["表單類型"].value_counts().unstack(fill_value=0)
    #新增'服務量'欄位
    grouped_counts_df["服務量"] = grouped_counts_df.apply(
        lambda col: col['NG']+col['Oral'], axis=1
    )
    grouped_counts_df["NG(%)"] = grouped_counts_df.apply(
        lambda col: str(round(col['NG']/col['服務量']*100, 2))+'%' if col['服務量']!=0 else 0, axis=1
    )
    grouped_counts_df["Oral(%)"] = grouped_counts_df.apply(
        lambda col:  str(round(col['Oral']/col['服務量']*100, 2))+'%' if col['服務量']!=0 else 0, axis=1
    )

    # 加入床號分組欄位
    filtered_df["床號分組"] = filtered_df["床號"].apply(classify_strict_bed)
    bed_counts_df = filtered_df.groupby("營養師")["床號分組"].value_counts().unstack(fill_value=0).reindex(columns=bed_groups, fill_value=0)
    # 總計
    summary_row = bed_counts_df.sum()
    summary_row.name = "全科總量"
    bed_counts_df = pd.concat([bed_counts_df, pd.DataFrame([summary_row])])

    # 調整欄位順序
    grouped_counts_df=grouped_counts_df[['NG', 'NG(%)', 'Oral', 'Oral(%)', '服務量']]

    output_path = './static/clinical_indicator/'+filename.split('.')[0]+'_已完成.xlsx'
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="原始資料")
        grouped_counts_df.to_excel(writer, index=True, sheet_name="各營養師服務量")
        bed_counts_df.to_excel(writer, index=True, sheet_name="各營養師負責之病房")
        
    print(f"{output_path}已存檔")
    return output_path
