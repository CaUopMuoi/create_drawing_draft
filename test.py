import ezdxf

# Tạo file DXF mới
doc = ezdxf.new(dxfversion='R2010')
modelspace = doc.modelspace()

# Vẽ hình tròn với tâm tại (0, 0) và bán kính 50
center = (0, 0)
radius = 50
modelspace.add_circle(center, radius)

# # Thêm dim đo kích thước cho hình tròn (Radius dim)
# dim = modelspace.add_radial_dim(
#     center=center,  # Tâm của hình tròn
#     radius=radius,  # Bán kính của hình tròn
#     angle=0,  # Góc của đường đo
#     override={"dimtad": 1}  # Tùy chọn thiết lập hiển thị
# )

# # Định dạng dim style (nếu cần)
# dim.render()

# Lưu file DXF
doc.saveas("circle_with_dimension.dxf")
