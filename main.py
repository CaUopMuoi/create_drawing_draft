# from utils.test import haha
import pandas as pd
import ezdxf

from utils.check import check_size_profile
from utils.calculator import calculator_scale_draw
from utils.drawing import draw_plate, draw_pipe


# Đường dẫn folder chứa file hoàn thành
PATH_FOLDER_FINISH = "ok/"
# Đuôi file (chọn loại file cần lưu)
FILE_TAIL = ".dxf"
# FILE_TAIL = ".dwg"

# Excel
PATH_FILE_EXCEL = "excel1.xlsx"
sheet_name = "CODE"

# Tên các cột trong Sheet excel
NAME = "NAME"
SIZE = "SIZE"
THICKNESS = "Thickness (mm)"
WIDTH = "Width (mm)"
LENGTH = "Length (mm)"
QTY = "Qty"
MATERIAL = "Material"

df = pd.read_excel(PATH_FILE_EXCEL, sheet_name=sheet_name)


# B1: Lặp qua từng hàng của DataFrame
for index, row in df.iterrows():
    # `index` là chỉ số hàng, `row` là Series chứa dữ liệu của hàng đó

    # các giá trị trong hàng
    value_name = row[NAME]
    value_size = row[SIZE]
    value_thickness = row[THICKNESS]
    value_width = row[WIDTH]
    value_length = row[LENGTH]
    value_qty = row[QTY]
    value_material = row[MATERIAL]

    # xem là loại vật tư nào
    size_profile = check_size_profile(value_size)

    # B2: tính toán để chọn file dxf mẫu phù hợp
    scale = calculator_scale_draw(value_thickness, value_width, value_length, size_profile)

    # đường dẫn đến bản vẽ mẫu
    path_template_drawing = f"file_mau_dxf/S{scale}.dxf"

    # B3: vẽ vào file dxf
    # mở bản vẽ
    doc = ezdxf.readfile(path_template_drawing)
    msp = doc.modelspace()
    block_front = doc.blocks.new(name="block_front")
    block_side = doc.blocks.new(name="block_side")

    if size_profile == "pipe":
        # vẽ ống vào bản vẽ mẫu
        draw_pipe(msp, block_front, block_side, scale, value_thickness, value_width, value_length)

    else:
        # vẽ tấm vào bản vẽ mẫu
        draw_plate(msp, block_front, block_side, scale, value_thickness, value_width, value_length)



    # lưu ra nơi mới
    path_file_finish = PATH_FOLDER_FINISH + value_name + FILE_TAIL
    doc.saveas(path_file_finish)
    # odafc.export_dwg(doc, path_file_finish, version='R2010')
    print(f"xong {value_name + FILE_TAIL}")
    msp.purge() # giải phóng dữ liệu của msp


