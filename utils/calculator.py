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
