from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import table_models as models
from app import schemas
from datetime import datetime
from typing import List


# Hàm model lấy dữ liệu roles với users
def get_roles_with_users(
    db: Session, schoolId: int
) -> List[schemas.RoleWithUsersResponse]:
    # Truy vấn tất cả vai trò
    roles = db.query(models.VaiTro).all()
    result = []
    for role in roles:
        role_data = schemas.RoleWithUsersResponse(
            role=schemas.Role2(
                idRole=role.id_vai_tro,
                roleName=role.ten_vai_tro,
                description=role.mo_ta,
                createdBy=role.nguoi_tao,
                updatedBy=role.nguoi_cap_nhat,
                createdTime=role.thoi_gian_tao,
                updatedTime=role.thoi_gian_cap_nhat,
            ),
            users=[],
        )

        # Truy vấn người dùng theo vai trò
        users = (
            db.query(models.NguoiDung)
            .filter(models.NguoiDung.vai_tro_id == role.id_vai_tro)
            .filter(models.NguoiDung.truong_id == schoolId)
            .all()
        )
        for user in users:
            user_data = schemas.User2(
                idUser=user.id_nguoi_dung,
                username=user.ho_ten,
                avatarUrl=user.anh_dai_dien,
                email=user.email,
                birthday=user.ngay_sinh,
                position=user.chuc_vu,
                status=user.trang_thai,
                address=user.dia_chi,
                phone=user.so_dien_thoai,
                createdTime=user.thoi_gian_tao,
                updatedTime=user.thoi_gian_cap_nhat,
                createdBy=user.nguoi_tao,
                roleID=user.vai_tro_id,
                schoolID=user.truong_id,
            )
            role_data.users.append(user_data)

        result.append(role_data)

    return result


# hàm Update role với users
def update_role_with_users(db: Session, role_id: int, user_ids: List[int]):
    print("update_role_with_users", role_id)
    # Truy vấn role từ DB
    role = db.query(models.VaiTro).filter(models.VaiTro.id_vai_tro == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Truy vấn tất cả các user hiện tại đang có role_id này
    current_users = (
        db.query(models.NguoiDung).filter(models.NguoiDung.vai_tro_id == role_id).all()
    )

    # Truy vấn danh sách user mới từ DB
    new_users = (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung.in_(user_ids))
        .all()
    )

    # Tạo danh sách các user cần gỡ role
    users_to_remove_role = [
        user for user in current_users if user.id_nguoi_dung not in user_ids
    ]

    # Gỡ role của những user không còn thuộc danh sách mới
    for user in users_to_remove_role:
        print("update_role_with_users333", user)
        user.vai_tro_id = None  # Hoặc giá trị mặc định nếu cần
        print("update_role_with_users444", user)

    # Cập nhật role cho những user mới
    for user in new_users:
        user.vai_tro_id = role_id

    # Lưu thay đổi vào database
    db.commit()
    return role


# hàm thêm role với users
def create_role_with_users(
    db: Session, role: schemas.Role, user_ids: List[int]
) -> List[schemas.RoleWithUsersResponse]:
    # Tạo mới role
    role_new = create_role(db=db, role=role)
    # Truy vấn danh sách user từ DB
    users = (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung.in_(user_ids))
        .all()
    )

    # Cập nhật role cho từng user
    for user in users:
        user.vai_tro_id = role_new.id_vai_tro

    db.commit()
    return role


# hàm xóa role
def delete_role(db: Session, role_id: int):
    # Truy vấn role từ DB
    role = db.query(models.VaiTro).filter(models.VaiTro.id_vai_tro == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Truy vấn danh sách user có role bị xóa
    users = (
        db.query(models.NguoiDung).filter(models.NguoiDung.vai_tro_id == role_id).all()
    )

    # Cập nhật role của các user thành None
    for user in users:
        user.vai_tro_id = None

    # Xóa role
    db.delete(role)
    db.commit()

    return role


# hàm lấy role theo id
def get_role_by_id(db: Session, role_id: int):
    # Truy vấn role từ DB
    role = db.query(models.VaiTro).filter(models.VaiTro.id_vai_tro == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# hàm cập nhật role
def update_role(db: Session, role_id: int, role: schemas.Role):
    print("update_role@@@", role_id)
    # Truy vấn role từ DB
    role_db = (
        db.query(models.VaiTro).filter(models.VaiTro.id_vai_tro == role_id).first()
    )
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")

    # Kiểm tra roleName đã tồn tại chưa
    if role_db.ten_vai_tro != role.roleName:
        role_roleName = (
            db.query(models.VaiTro)
            .filter(models.VaiTro.ten_vai_tro == role.roleName)
            .first()
        )
        if role_roleName:
            raise HTTPException(status_code=400, detail="Role already exists")

    # Cập nhật dữ liệu mới
    if role.roleName is not None:
        role_db.ten_vai_tro = role.roleName
    if role.description is not None:
        role_db.mo_ta = role.description
    if role.updatedBy is not None:
        role_db.nguoi_cap_nhat = role.updatedBy

    role_db.thoi_gian_cap_nhat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    return role_db


# hàm tạo mới role
def create_role(db: Session, role: schemas.Role):
    # Kiểm tra roleName đã tồn tại chưa
    role_db = (
        db.query(models.VaiTro)
        .filter(models.VaiTro.ten_vai_tro == role.roleName)
        .first()
    )
    if role_db:
        raise HTTPException(status_code=400, detail="Role already exists")

    # Tạo mới role
    new_role = models.VaiTro(
        ten_vai_tro=role.roleName,
        mo_ta=role.description,
        thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        nguoi_tao=role.createdBy,
    )
    db.add(new_role)
    db.commit()
    return new_role


# lấy danh sách role
def get_roles(db: Session):
    roles = db.query(models.VaiTro).all()
    return roles


# Cập nhật role và users
def update_role_and_users_api(db: Session, role: schemas.Role, user_ids: List[int]):
    # Gọi hàm trong model để cập nhật dữ liệu
    try:
        roleNew = update_role(db=db, role_id=role.idRole, role=role)
        update_role_with_users(db=db, role_id=role.idRole, user_ids=user_ids)

        return roleNew
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Search role by every field and schoolId
def search_role(db: Session, dataSearch: schemas.SearchData):
    # Truy vấn tất cả roles
    roles = (
        db.query(models.VaiTro)
        .filter(
            models.VaiTro.ten_vai_tro.like(f"%{dataSearch.searchValue}%")
            | models.VaiTro.mo_ta.like(f"%{dataSearch.searchValue}%")
        )
        .all()
    )
    result = []
    for role in roles:
        role_data = schemas.RoleWithUsersResponse(
            role=schemas.Role2(
                idRole=role.id_vai_tro,
                roleName=role.ten_vai_tro,
                description=role.mo_ta,
                createdBy=role.nguoi_tao,
                updatedBy=role.nguoi_cap_nhat,
                createdTime=role.thoi_gian_tao,
                updatedTime=role.thoi_gian_cap_nhat,
            ),
            users=[],
        )

        # Truy vấn người dùng theo vai trò
        users = (
            db.query(models.NguoiDung)
            .filter(models.NguoiDung.vai_tro_id == role.id_vai_tro)
            .filter(models.NguoiDung.truong_id == dataSearch.schoolId)
            .all()
        )
        for user in users:
            user_data = schemas.User2(
                idUser=user.id_nguoi_dung,
                username=user.ho_ten,
                avatarUrl=user.anh_dai_dien,
                email=user.email,
                birthday=user.ngay_sinh,
                position=user.chuc_vu,
                status=user.trang_thai,
                address=user.dia_chi,
                phone=user.so_dien_thoai,
                createdTime=user.thoi_gian_tao,
                updatedTime=user.thoi_gian_cap_nhat,
                createdBy=user.nguoi_tao,
                roleID=user.vai_tro_id,
                schoolID=user.truong_id,
            )
            role_data.users.append(user_data)

        result.append(role_data)

    return result
