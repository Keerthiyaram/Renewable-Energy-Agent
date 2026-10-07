from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.asset import RenewableAsset
from app.schemas.assets import RenewableAssetCreate, RenewableAssetUpdate, RenewableAsset as RenewableAssetSchema

router = APIRouter()


@router.post("/", response_model=RenewableAssetSchema, status_code=status.HTTP_201_CREATED)
async def create_asset(asset: RenewableAssetCreate, db: Session = Depends(get_db)):
    """Create a new renewable asset."""
    # Check if asset_id already exists
    existing = db.query(RenewableAsset).filter(RenewableAsset.asset_id == asset.asset_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Asset with asset_id '{asset.asset_id}' already exists"
        )
    
    db_asset = RenewableAsset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get("/", response_model=List[RenewableAssetSchema])
async def get_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all renewable assets."""
    assets = db.query(RenewableAsset).offset(skip).limit(limit).all()
    return assets


@router.get("/{asset_id}", response_model=RenewableAssetSchema)
async def get_asset(asset_id: str, db: Session = Depends(get_db)):
    """Get a specific renewable asset by asset_id."""
    asset = db.query(RenewableAsset).filter(RenewableAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with asset_id '{asset_id}' not found"
        )
    return asset


@router.put("/{asset_id}", response_model=RenewableAssetSchema)
async def update_asset(asset_id: str, asset_update: RenewableAssetUpdate, db: Session = Depends(get_db)):
    """Update a renewable asset."""
    asset = db.query(RenewableAsset).filter(RenewableAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with asset_id '{asset_id}' not found"
        )
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)
    
    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    """Delete a renewable asset."""
    asset = db.query(RenewableAsset).filter(RenewableAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with asset_id '{asset_id}' not found"
        )
    
    db.delete(asset)
    db.commit()
    return None
