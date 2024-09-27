from redux import global_layers


def draw_circle(msp, DIM_DISTANCE, t, d):
    center = (0, 0)
    r = d/2

    msp.add_circle(center, r, global_layers.layer_3)
    msp.add_circle(center, r-t, global_layers.layer_3)

    # vẽ tâm
    msp.add_line((-r-DIM_DISTANCE/5, 0), (r+DIM_DISTANCE/5,0), global_layers.layer_1)
    msp.add_line((0, -r-DIM_DISTANCE/5), (0, r+DIM_DISTANCE/5), global_layers.layer_1)

    dim = msp.add_diameter_dim(
        center=center,
        radius=r,
        angle=225,
        dimstyle="LT",
        # override={"dimtoh": 1}
        dxfattribs=global_layers.layer_4
    )
    dim.render()

def draw_body_pipe(msp, DIM_DISTANCE, l , w, t):

    p1 = (-l/2, -w/2)
    p2 = (-l/2, w/2)
    p3 = (l/2, w/2)
    p4 = (l/2, -w/2)



    msp.add_line(p1, p2, global_layers.layer_3)
    msp.add_line(p2, p3, global_layers.layer_3)
    msp.add_line(p3, p4, global_layers.layer_3)
    msp.add_line(p4, p1, global_layers.layer_3)

    l_rec_56 = msp.add_line(p2, p3, global_layers.layer_2)
    l_rec_56.translate(0, -t,0)

    l_rec_78 = msp.add_line(p4, p1, global_layers.layer_2)
    l_rec_78.translate(0,t,0)

    # vẽ tâm
    msp.add_line((p1[0] - DIM_DISTANCE/5, 0), (p3[0] + DIM_DISTANCE/5, 0), global_layers.layer_1)

    # vẽ dim1
    dim1 = msp.add_aligned_dim(
        p1=p2,  # 1st measurement point
        p2=p3,  # 2nd measurement point
        distance= DIM_DISTANCE,
        dimstyle="LT",  # default dimension style
        dxfattribs= global_layers.layer_4
    )
    dim1.render()


def draw_rectangle(msp, DIM_DISTANCE, l , w):

    p1 = (-l/2, -w/2)
    p2 = (-l/2, w/2)
    p3 = (l/2, w/2)
    p4 = (l/2, -w/2)

    msp.add_line(p1, p2, global_layers.layer_3)
    msp.add_line(p2, p3, global_layers.layer_3)
    msp.add_line(p3, p4, global_layers.layer_3)
    msp.add_line(p4, p1, global_layers.layer_3)

    # vẽ dim1
    dim1 = msp.add_aligned_dim(
        p1=p2,  # 1st measurement point
        p2=p3,  # 2nd measurement point
        distance= DIM_DISTANCE,
        dimstyle="LT",  # default dimension style
        dxfattribs= global_layers.layer_4
    )
    dim1.render()

    # vẽ dim2
    dim2 = msp.add_aligned_dim(
        p1=p3,  # 1st measurement point
        p2=p4,  # 2nd measurement point
        distance= DIM_DISTANCE,
        dimstyle="LT",  # default dimension style
        dxfattribs= global_layers.layer_4
    )
    dim2.render()



def draw_plate(msp, block_front, block_side, scale, thickness, width, length):
    # khoảng cách của DIM với vật thể
    DIM_DISTANCE = 10 * scale
    # khoảng cách của các hình chiếu
    SOLID_DISTANCE = 30 * scale

    # chiều dài tổng của chi tiết
    length_x = thickness + DIM_DISTANCE + SOLID_DISTANCE + length + DIM_DISTANCE

    # di chuyển ra giữa của trục 0
    l_t = -length_x/2 + thickness/2
    l_p = length_x/2 - DIM_DISTANCE - length/2

    # di chuyển đến tâm bản vẽ
    l_bv_t_x = scale*297/2 + l_t
    l_bv_p_x = scale*297/2 + l_p

    l_bv_t_y = scale*210/2 - DIM_DISTANCE/2 + 30*scale
    l_bv_p_y = l_bv_t_y



    # nhớ sửa lại width length của tôn tấm trong file excel (length > width) ????????????????????????
    draw_rectangle(block_side, DIM_DISTANCE, thickness , width)
    draw_rectangle(block_front, DIM_DISTANCE, length , width)

    msp.add_blockref(block_side.dxf.name, insert=(l_bv_t_x, l_bv_t_y))
    msp.add_blockref(block_front.dxf.name, insert=(l_bv_p_x, l_bv_p_y))


def draw_pipe(msp, block_front, block_side, scale, thickness, diameter, length):
    # khoảng cách của DIM với vật thể
    DIM_DISTANCE = 10 * scale
    # khoảng cách của các hình chiếu
    SOLID_DISTANCE = 30 * scale

    # chiều dài tổng của chi tiết
    length_x = diameter + DIM_DISTANCE + SOLID_DISTANCE + length

    # di chuyển ra giữa của trục 0
    l_t = -length_x/2 + diameter/2
    l_p = length_x/2 - length/2

    # di chuyển đến tâm bản vẽ
    l_bv_t_x = scale*297/2 + l_t
    l_bv_p_x = scale*297/2 + l_p

    l_bv_t_y = scale*210/2 - DIM_DISTANCE/2 + 30*scale
    l_bv_p_y = l_bv_t_y



    draw_circle(block_side, DIM_DISTANCE, thickness, diameter)
    draw_body_pipe(block_front, DIM_DISTANCE, length , diameter, thickness)

    msp.add_blockref(block_front.dxf.name, insert=(l_bv_p_x, l_bv_p_y))
    msp.add_blockref(block_side.dxf.name, insert=(l_bv_t_x, l_bv_t_y))