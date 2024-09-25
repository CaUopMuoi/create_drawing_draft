import pandas as pd
import ezdxf
from ezdxf import transform
# from ezdxf.addons import odafc

# Hàm tính toán tỉ lệ bản vẽ cần chọn
def calculator_scale_draw(value_width, value_length, size_profile):
    # Danh sách các tỉ lệ bản vẽ
    list_scale = [1, 2, 4, 8, 16, 32, 48]
    # giá trị lớn nhất và nhỏ nhất để xác định length, width

    length = max(value_width, value_length)
    width = min(value_width, value_length)

    if size_profile == "pipe" and value_width > value_length:
        length = value_width + value_width


    # tỉ lệ
    scale_length_width = length/width
    # chiều dài nhỏ nhất cần thiết cho bản vẽ
    min_length_template_drawing = None
    if scale_length_width <= 2:
        min_length_template_drawing = length*2.2
    elif scale_length_width <= 3:
        min_length_template_drawing = length*1.6
    elif scale_length_width <= 4:
        min_length_template_drawing = length*1.3
    else:
        min_length_template_drawing = length*1.15
    # so sánh với các tỉ lệ chuẩn của bản vẽ
    for scale_template in list_scale:
        # A4 (297, 210)mm là tỉ lệ 1
        length_template = scale_template*297
        # nếu chiều dài chuẩn của bản vẽ >= chiều dài nhỏ nhất cần thiết cho bản vẽ thì:
        if length_template >= min_length_template_drawing:
            # trả về kết quả tỉ lệ và thoát vòng lặp nếu đúng
            return scale_template
    # nếu không có khung phù hợp sẽ in ra thông báo lỗi !!!
    return 48

def draw_rectangle(msp, DIM_DISTANCE, SOLID_DISTANCE, center_x, center_y, lower_left, upper_right, is_draw_center):
    global NET_THAY
    global DUONG_TAM
    global NET_DIM

    # Tạo các đỉnh của hình chữ nhật
    lower_left_x, lower_left_y = lower_left
    upper_right_x, upper_right_y = upper_right

    # Vẽ các cạnh của hình chữ nhật
    l_rec_1 = msp.add_line(lower_left, (upper_right_x, lower_left_y), NET_THAY)  # Bottom edge
    l_rec_2 = msp.add_line((upper_right_x, lower_left_y), upper_right, NET_THAY)  # Right edge
    l_rec_3 = msp.add_line(upper_right, (lower_left_x, upper_right_y), NET_THAY)  # Top edge
    l_rec_4 = msp.add_line((lower_left_x, upper_right_y), lower_left, NET_THAY)  # Left edge

    length_x = upper_right_x - lower_left_x
    length_y = upper_right_y - lower_left_y
    tam_lower_x = lower_left_x + length_x/2
    tam_left_y = lower_left_y + length_y/2


    # vẽ đường tâm
    # 0: không vẽ
    # 1: vẽ đường dọc
    # 2: vẽ đường ngang
    # 3: vẽ cả 2 đường
    if is_draw_center == True:

        # kích thước đoạn thừa ra của đường tâm
        TI_LE_TAM_THUA_RA = 0.06
        TAM_THUA_RA = min(length_x*TI_LE_TAM_THUA_RA, length_y*TI_LE_TAM_THUA_RA)

        # vẽ đường ngang
        tam_lower_y = lower_left_y - TAM_THUA_RA
        l_duong_tam_1 = msp.add_line((tam_lower_x, tam_lower_y), (tam_lower_x, tam_lower_y + length_y + 2*TAM_THUA_RA), DUONG_TAM)

        # vẽ đường dọc
        tam_left_x = lower_left_x - TAM_THUA_RA
        l_duong_tam_2 = msp.add_line((tam_left_x, tam_left_y), (tam_left_x + length_x + 2*TAM_THUA_RA, tam_left_y), DUONG_TAM)

    
    # khoảng cách cần translate
    dx_translate=None
    dy_translate=None
    # là hình chiếu cạnh phải
    if is_draw_center == True:
        # move dim
        dx_translate = SOLID_DISTANCE + center_x
        dy_translate = center_y
    # là hình chiếu đứng bên trái
    else:
        dx_translate = center_x
        dy_translate = center_y

    # matrix44
    matrix = transform.Matrix44.translate(dx_translate,dy_translate,0)

    # move rec
    l_rec_1.transform(matrix)
    l_rec_2.transform(matrix)
    l_rec_3.transform(matrix)
    l_rec_4.transform(matrix)
    
    # là hình chiếu cạnh phải
    if is_draw_center == True:
        # move đường tâm
        l_duong_tam_1.transform(matrix)
        l_duong_tam_2.transform(matrix)

    # vẽ DIM
    # toạ độ của dim1
    dim1_p1_x = lower_left_x + dx_translate
    dim1_p1_y = upper_right_y + dy_translate
    dim1_p2_x = upper_right_x + dx_translate
    dim1_p2_y = upper_right_y + dy_translate
    # vẽ dim1
    dim1 = msp.add_aligned_dim(
        p1=(dim1_p1_x, dim1_p1_y),  # 1st measurement point
        p2=(dim1_p2_x, dim1_p2_y),  # 2nd measurement point
        distance= DIM_DISTANCE,
        dimstyle="LT",  # default dimension style
        dxfattribs= NET_DIM
    )
    dim1.render()

    # toạ độ của dim2
    dim2_p1_x = upper_right_x + dx_translate
    dim2_p1_y = upper_right_y + dy_translate
    dim2_p2_x = upper_right_x + dx_translate
    dim2_p2_y = lower_left_y + dy_translate
    # vẽ dim2
    dim2 = msp.add_aligned_dim(
        p1=(dim2_p1_x, dim2_p1_y),  # 1st measurement point
        p2=(dim2_p2_x, dim2_p2_y),  # 2nd measurement point
        distance= DIM_DISTANCE,
        dimstyle="LT",  # default dimension style
        dxfattribs= NET_DIM
    )
    dim2.render()

def draw_circle(msp, DIM_DISTANCE, SOLID_DISTANCE, center_x, center_y, lower_left, upper_right, is_draw_center):
    global NET_THAY
    global DUONG_TAM
    global NET_DIM

    # Vẽ hình tròn với tâm tại (0, 0) và bán kính 50
    center = (0, 0)
    radius = 50
    modelspace.add_circle(center, radius)







def draw_plate(msp, scale, thickness, width, length):
    # khoảng cách của DIM với vật thể
    DIM_DISTANCE = 10 * scale
    # khoảng cách của các hình chiếu
    SOLID_DISTANCE = 30 * scale
    # tâm của 2 hình chiếu (khi chưa di chuyển ra tâm bản vẽ)
    center_x = (thickness + SOLID_DISTANCE + length)/2
    center_y = width/2

    center_x_move = scale*297/2 - center_x
    center_y_move = scale*210/2 - center_y + 30*scale

    # vẽ hình chiếu đứng
    draw_rectangle(msp, DIM_DISTANCE, SOLID_DISTANCE, center_x_move, center_y_move, (0, 0), (length, width), is_draw_center=True)

    # vẽ hình chiếu cạnh bên trái
    draw_rectangle(msp, DIM_DISTANCE, SOLID_DISTANCE, center_x_move, center_y_move, (0, 0), (thickness, width), is_draw_center=False)


def draw_pipe(msp, scale, thickness, phi, length):
    # khoảng cách của DIM với vật thể
    DIM_DISTANCE = 10 * scale
    # khoảng cách của các hình chiếu
    SOLID_DISTANCE = 30 * scale

    # tâm của 2 hình chiếu (khi chưa di chuyển ra tâm bản vẽ)
    center_x = (phi + SOLID_DISTANCE + length)/2
    center_y = phi/2

    center_x_move = scale*297/2 - center_x
    center_y_move = scale*210/2 - center_y + 30*scale


    # vẽ hình chiếu đứng
    # draw_rectangle(msp, DIM_DISTANCE, SOLID_DISTANCE, center_x_move, center_y_move, (0, 0), (length, phi), is_draw_center=True)



# def change_plate(msp, plate, material, qty):
#     mtexts = msp.query('MTEXT[layer=="2"]')

#     for mtext in mtexts:
#         if mtext.dxf.text == r"\A1;\pxqc;{\C2;PL100\PMAT'L : ASTM A36/A36M\PQty: 100}":
#             # print(mtext.dxf.text)
#             mtext_change = rf"{plate}\PMAT'L : {material}\PQTY: {qty}"
#             mtext.dxf.text = r"\A1;\pxqc;{\C2;" + mtext_change + "}"

def check_size_profile(value_size):
    size = str(value_size).lower()
    # list_pipe = ["pipe", "tube"]

    # nếu là ống
    if "pipe" in size or "tube" in size:
        print("là ống")
        return "pipe"
    else:
        print("là thép tấm")
        return "plate"

    

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

# LAYER trong bản vẽ template
NET_THAY = {"layer":"0", "linetype":"Continuous"}
NET_DUT = {"layer":"2", "linetype":"HIDDEN"}
DUONG_TAM = {"layer":"1", "linetype":"CENTER"}
NET_AO_NET_SAN = {"layer":"6", "linetype":"PHANTOM"}
NET_DIM = {"layer":"4", "linetype":"Continuous"}


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
    scale = calculator_scale_draw(value_width, value_length, size_profile)

    # đường dẫn đến bản vẽ mẫu
    path_template_drawing = f"file_mau_dxf/S{scale}.dxf"


    # B3: vẽ vào file dxf
    # mở bản vẽ
    doc = ezdxf.readfile(path_template_drawing)
    msp = doc.modelspace()





    # vẽ tấm vào bản vẽ mẫu
    draw_plate(msp, scale, value_thickness, value_width, value_length)

    # change_plate(msp, value_size, value_material, value_qty)
    
    # lưu ra nơi mới
    path_file_finish = PATH_FOLDER_FINISH + value_name + FILE_TAIL
    doc.saveas(path_file_finish)
    # odafc.export_dwg(doc, path_file_finish, version='R2010')
    print(f"xong {value_name + FILE_TAIL}")
    msp.purge() # giải phóng dữ liệu của msp

