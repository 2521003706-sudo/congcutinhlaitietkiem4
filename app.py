import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.write("Tính toán chi tiết tiền lãi và tổng tiền nhận được theo Lãi đơn & Lãi kép.")

st.markdown("---")

# --- PHẦN NHẬP DỮ LIỆU ---
st.subheader("📋 Nhập thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ):",
        min_value=0.0,
        value=100000000.0,
        step=1000000.0,
        format="%.0f"
    )
    
    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):",
        min_value=1,
        value=12,
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.0,
        value=6.5,
        step=0.1,
        format="%.2f"
    )
    
    hinh_thuc_tra_lai = st.selectbox(
        "Hình thức nhận lãi:",
        options=["Lãnh lãi cuối kỳ", "Lãnh lãi theo tháng", "Lãnh lãi theo quý"]
    )

loai_lai = st.radio(
    "Phương thức tính lãi:",
    options=["Lãi đơn", "Lãi kép"],
    horizontal=True,
    help="Lãi đơn: Tiền lãi không gộp vào gốc. Lãi kép: Tiền lãi định kỳ được cộng vào gốc để tính lãi cho kỳ tiếp theo."
)

st.markdown("---")

# --- XỬ LÝ TÍNH TOÁN ---
def tinh_toan_lai(so_tien, lai_suat_nam, ky_han_thang, hinh_thuc, loai_lai):
    r_nam = lai_suat_nam / 100
    
    # Xác định số kỳ nhận lãi và lãi suất tương ứng từng kỳ
    if hinh_thuc == "Lãnh lãi theo tháng":
        so_ky_nhan_lai = ky_han_thang
        r_ky = r_nam / 12
        ten_ky = "tháng"
    elif hinh_thuc == "Lãnh lãi theo quý":
        so_ky_nhan_lai = ky_han_thang / 3
        r_ky = r_nam / 4
        ten_ky = "quý"
    else:  # Lãnh lãi cuối kỳ
        so_ky_nhan_lai = 1
        r_ky = r_nam * (ky_han_thang / 12)
        ten_ky = "cuối kỳ"

    # Tính toán theo loại lãi
    if loai_lai == "Lãi đơn":
        # Với lãi đơn, số tiền lãi mỗi kỳ luôn tính trên gốc ban đầu
        tong_tien_lai = so_tien * r_nam * (ky_han_thang / 12)
        if hinh_thuc == "Lãnh lãi cuối kỳ":
            tien_lai_dinh_ky = tong_tien_lai
        else:
            tien_lai_dinh_ky = so_tien * r_ky
        tong_goc_va_lai = so_tien + tong_tien_lai

    else:  # Lãi kép
        if hinh_thuc == "Lãnh lãi cuối kỳ":
            # Cuối kỳ mới lãnh lãi thì Lãi kép = Lãi đơn vì không có các kỳ gộp lãi
            tong_tien_lai = so_tien * r_nam * (ky_han_thang / 12)
            tien_lai_dinh_ky = tong_tien_lai
            tong_goc_va_lai = so_tien + tong_tien_lai
        else:
            # Lãi kép nhập gốc định kỳ
            tong_goc_va_lai = so_tien * ((1 + r_ky) ** so_ky_nhan_lai)
            tong_tien_lai = tong_goc_va_lai - so_tien
            tien_lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai  # Mức lãi trung bình mỗi kỳ

    return tien_lai_dinh_ky, tong_tien_lai, tong_goc_va_lai, ten_ky, so_ky_nhan_lai

# Gọi hàm tính toán
tien_lai_dinh_ky, tong_tien_lai, tong_goc_va_lai, ten_ky, so_ky_nhan_lai = tinh_toan_lai(
    so_tien_gui, lai_suat_nam, ky_han_thang, hinh_thuc_tra_lai, loai_lai
)

# --- PHẦN HIỂN THỊ KẾT QUẢ ---
st.subheader("📊 Kết quả tính toán")

# Kiểm tra điều kiện kỳ hạn theo quý
if hinh_thuc_tra_lai == "Lãnh lãi theo quý" and ky_han_thang % 3 != 0:
    st.warning("⚠️ Lưu ý: Kỳ hạn gửi không chia hết cho 3 tháng (1 quý). Kết quả tính theo số kỳ lẻ tương ứng.")

col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.metric(
        label=f"Tiền lãi định kỳ (mỗi {ten_ky}):",
        value=f"{tien_lai_dinh_ky:,.0f} VNĐ"
    )

with col_res2:
    st.metric(
        label="Tổng tiền lãi nhận được:",
        value=f"{tong_tien_lai:,.0f} VNĐ"
    )

with col_res3:
    st.metric(
        label="Tổng gốc + lãi nhận được:",
        value=f"{tong_goc_va_lai:,.0f} VNĐ"
    )

st.markdown("---")

# Bảng tóm tắt thông tin
st.write("### 📝 Tóm tắt hợp đồng tiết kiệm")
st.write(f"- **Số tiền gốc ban đầu:** `{so_tien_gui:,.0f}` VNĐ")
st.write(f"- **Lãi suất:** `{lai_suat_nam}%/năm`")
st.write(f"- **Kỳ hạn:** `{ky_han_thang}` tháng (`{so_ky_nhan_lai:.1f}` kỳ trả lãi)")
st.write(f"- **Hình thức:** `{hinh_thuc_tra_lai}` ({loai_lai})")
