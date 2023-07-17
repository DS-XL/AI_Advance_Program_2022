# Before this code, please transform the PDF to EXCEL using Adobe
# This code is used to transform EXCEL data to CSV file
import pandas as pd
from collections import defaultdict
import re
import os
pd.set_option('display.max_columns', 500)


# Read the file
def read_file(f):
    with open(f) as fh:
        lines = fh.readlines()
    return lines


def save_func(lines):
    data = defaultdict(list)
    saver = None
    group_id = None
    group_name = None
    for line in lines:
        line = line.rstrip()
        if line == ',,,,,,,,,,,,':
            saver = pd.concat([saver, pd.DataFrame(data)], ignore_index=True)
            # saver = pd.DataFrame(data)
            # if saver.shape[0] > 0:
            #     if os.path.exists(save_place):
            #         saver.to_csv(save_place, mode='a', header=False, index=False)
            #     else:
            #         saver.to_csv(save_place, mode='a', header=True, index=False)
            data = defaultdict(list)
            continue
        if line[:5] == "Group" and ",,,,,,,,,,,," in line:
            new_line = line.replace(",,,,,,,,,,,,", "")
            new_line = re.sub('\s{2,}', ' ', new_line)
            items = new_line.split(' ')
            if len(items) < 3:
                group_id = None
                group_name = None
            else:
                group_id = items[1]
                group_name = " ".join(items[2:])
                # print(line, items, group_id, group_name)
            continue
        if line[:7] == 'Article':
            continue
        if line[:4] == 'Sold':
            continue
        if line[:5] == 'Price':
            continue
        if 'Total' in line:
            continue
        info = line.split(',')
        data['group_id'].append(group_id)
        data['group_name'].append(group_name)
        if info[0][0].isnumeric():
            try:
                info[0] = str(int(float(info[0])))
            except:
                pass
        data['article'].append(info[0])
        data['name'].append(info[1])
        data['gross_amount'].append(info[3])
        data['net_amount'].append(info[4])
        data['pieces_sold'].append(info[5])
        data['quantity_sold'].append(info[6])
        data['avg_price'].append(info[7])
        data['discount_amount'].append(info[8])
        data['avg_discount'].append(info[9])
        data['reference_amount'].append(info[10])
        data['ref_pct'].append(info[11])
        data['tot_pct'].append(info[12])
    return saver


if __name__ == "__main__":
    save_data = None
    for m in range(1, 13):
        year = '2022'
        month = str(m)
        file_name = f"Plano_{month.zfill(2)}_{year}"
        if not os.path.exists(os.path.join("./assets/data", f"{file_name}.csv")):
            raise Exception(f"File {file_name} does not exist!")
        file_path = os.path.join("./assets/data", f"{file_name}.csv")
        save_path = os.path.join("./assets/data", f"{file_name}_clean.csv")
        all_lines = read_file(file_path)
        res = save_func(all_lines)
        res['year'] = int(year)
        res['month'] = int(month)
        print(res.shape)
        save_data = pd.concat([save_data, res], ignore_index=True)
    print("Done!")
    save_data.to_csv('/Users/yuhaibo/workspace/DS_advanced_G3_internal/assets/data/Plano_2022_clean.csv', mode='a', header=True, index=False)
