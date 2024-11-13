import streamlit as st
import bcrypt
from web3 import Web3

# Kết nối với một blockchain node
blockchain_node = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Thay YOUR_INFURA_PROJECT_ID bằng ID của bạn
web3 = Web3(Web3.HTTPProvider(blockchain_node))

# Hàm mã hóa mật khẩu
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Kiểm tra mật khẩu
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Tạo tài khoản blockchain
def create_blockchain_account():
    account = web3.eth.account.create()
    return account.address, account.key.hex()  # Sử dụng account.key.hex() để trả về private key dạng chuỗi

# Hàm đăng ký người dùng
def register_user(username, password):
    hashed_password = hash_password(password)
    user_address, user_private_key = create_blockchain_account()
    st.session_state["users"][username] = {
        "password": hashed_password,
        "address": user_address,
        "private_key": user_private_key,
        "devices": []
    }
    st.success("Đăng ký thành công! Địa chỉ ví: " + user_address)

# Hàm đăng nhập người dùng
def login_user(username, password):
    user = st.session_state["users"].get(username)
    if user and check_password(user["password"], password):
        st.session_state["logged_in"] = True
        st.session_state["current_user"] = username
        st.success("Đăng nhập thành công!")
    else:
        st.error("Thông tin đăng nhập không đúng.")

# Quản lý tài khoản
def account_management():
    st.subheader("Quản lý Tài khoản")
    if st.button("Cập nhật Thông tin Cá nhân"):
        st.info("Chức năng đang được phát triển.")

# Cài đặt bảo mật và quyền riêng tư
def security_settings():
    st.subheader("Cài đặt Bảo mật")
    if st.checkbox("Bật Xác thực Hai Yếu Tố (2FA)"):
        st.write("2FA đã được bật.")
    
    st.subheader("Quyền Riêng Tư")
    privacy = st.selectbox("Kiểm soát quyền riêng tư:", ["Công khai", "Chỉ bạn bè", "Riêng tư"])
    st.write(f"Chế độ quyền riêng tư hiện tại: {privacy}")

# Quản lý thiết bị
def device_management():
    st.subheader("Quản lý Thiết bị")
    devices = st.session_state["users"][st.session_state["current_user"]]["devices"]
    st.write("Danh sách thiết bị đã đăng nhập:")
    for device in devices:
        st.write(f"- {device}")

# Giao diện chính
def main():
    st.title("WebChat-Blockchain")

    # Kiểm tra trạng thái người dùng
    if "users" not in st.session_state:
        st.session_state["users"] = {}
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Đăng ký hoặc Đăng nhập
    if not st.session_state["logged_in"]:
        choice = st.sidebar.selectbox("Chọn chức năng", ["Đăng Nhập", "Đăng Ký"])
        username = st.sidebar.text_input("Tên người dùng")
        password = st.sidebar.text_input("Mật khẩu", type="password")

        if choice == "Đăng Ký":
            if st.sidebar.button("Đăng Ký"):
                if username in st.session_state["users"]:
                    st.sidebar.error("Tên người dùng đã tồn tại.")
                else:
                    register_user(username, password)

        elif choice == "Đăng Nhập":
            if st.sidebar.button("Đăng Nhập"):
                login_user(username, password)

    else:
        # Khi người dùng đã đăng nhập
        st.sidebar.write(f"Xin chào, {st.session_state['current_user']}!")
        page = st.sidebar.radio("Trang", ["Quản lý Tài khoản", "Cài đặt Bảo mật", "Quản lý Thiết bị"])

        if page == "Quản lý Tài khoản":
            account_management()
        elif page == "Cài đặt Bảo mật":
            security_settings()
        elif page == "Quản lý Thiết bị":
            device_management()

        # Đăng xuất
        if st.sidebar.button("Đăng Xuất"):
            st.session_state["logged_in"] = False
            st.sidebar.write("Bạn đã đăng xuất.")

if __name__ == "__main__":
    main()
