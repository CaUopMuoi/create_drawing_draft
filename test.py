import ezdxf
from ezdxf import transform

# Tạo file DXF mới
doc = ezdxf.new(dxfversion='R2010')
msp = doc.modelspace()

block1 = doc.blocks.new(name="1")

# Vẽ hình tròn với tâm tại (0, 0) và bán kính 50
center = (0, 0)
radius = 50
circle = block1.add_circle(center, radius)

dim = block1.add_diameter_dim(
    center=(0, 0),
    radius=50,
    angle=45,
    dimstyle="EZ_RADIUS",
    override={"dimtoh": 1}
)
dim.render()

dim1 = block1.add_aligned_dim(
    p1=(0, 0),  # 1st measurement point
    p2=(50, 0),  # 2nd measurement point
    distance= 20,
    dimstyle="LT",  # default dimension style
    # dxfattribs= NET_DIM
)
dim1.render()

msp.add_blockref("1", insert=(100,100))

# Lưu file DXF
doc.saveas("circle_with_dimension.dxf")
