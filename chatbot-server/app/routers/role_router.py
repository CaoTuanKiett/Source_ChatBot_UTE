from app import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import SessionLocal
from app.models import role_model

router = APIRouter()


# Dependency để lấy session DB cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API lấy danh sách roles với users
@router.get(
    "/roles/users/{schoolId}", response_model=List[schemas.RoleWithUsersResponse]
)
def get_roles_with_users_api(db: Session = Depends(get_db), schoolId: int = 0):
    # Gọi hàm trong model để lấy dữ liệu
    try:
        roles_with_users = role_model.get_roles_with_users(db=db, schoolId=schoolId)
        return roles_with_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API cập nhật role với users
@router.put("/roles/users", response_model=schemas.RoleResponse)
def update_role_with_users_api(
    role: schemas.Role, user_ids: List[int], db: Session = Depends(get_db)
):
    # Gọi hàm trong model để cập nhật dữ liệu
    try:
        roleNew = role_model.update_role_and_users_api(
            db=db, role=role, user_ids=user_ids
        )
        return {"idRole": roleNew.id_vai_tro, "message": "Role updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##Chưa check
# API tạo mới role với users
@router.post("/roles/users", response_model=schemas.RoleResponse)
def create_role_with_users_api(
    role: schemas.Role, user_ids: List[int], db: Session = Depends(get_db)
):
    # Gọi hàm trong model để tạo dữ liệu
    try:
        roleNew = role_model.create_role_with_users(db=db, role=role, user_ids=user_ids)
        return schemas.RoleResponse(
            idRole=roleNew.idRole, message="Role created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API xóa role
@router.delete("/role/{role_id}", response_model=schemas.RoleResponse)
def delete_role_api(role_id: int, db: Session = Depends(get_db)):
    # Gọi hàm trong model để xóa dữ liệu
    try:
        role = role_model.delete_role(db=db, role_id=role_id)
        return {"idRole": role.id_vai_tro, "message": "Role deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API lấy role theo id
@router.get("/role/{role_id}", response_model=schemas.Role)
def get_role_by_id_api(role_id: int, db: Session = Depends(get_db)):
    # Gọi hàm trong model để lấy dữ liệu
    try:
        role = role_model.get_role_by_id(db=db, role_id=role_id)
        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API cập nhật role
@router.put("/role/{role_id}", response_model=schemas.RoleResponse)
def update_role_api(role_id: int, role: schemas.Role, db: Session = Depends(get_db)):
    # Gọi hàm trong model để cập nhật dữ liệu
    try:
        role = role_model.update_role(db=db, role_id=role_id, role=role)
        return {"idRole": role.id_vai_tro, "message": "Role updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API tạo mới role
@router.post("/role", response_model=schemas.RoleResponse)
def create_role_api(role: schemas.Role, db: Session = Depends(get_db)):
    # Gọi hàm trong model để tạo dữ liệu
    try:
        role = role_model.create_role(db=db, role=role)
        return {"idRole": role.id_vai_tro, "message": "Role created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API lấy danh sách roles
@router.get("/roles", response_model=List[schemas.Role2])
def get_roles_api(db: Session = Depends(get_db)):
    # Gọi hàm trong model để lấy dữ liệu
    try:
        roles = role_model.get_roles(db=db)
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
