from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from db import DBCollection, get_collection
from models import CreateClusterSchema, Cluster

cluster_router = APIRouter(
    prefix="/{organization_id}/clusters", tags=["payment clusters"]
)
organization_collection = get_collection(DBCollection.ORGANIZATION)
cluster_collection = get_collection(DBCollection.CLUSTER)


@cluster_router.post("")
async def create_cluster(organization_id: str, cluster_data: CreateClusterSchema):
    organization_in_db = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    if not organization_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"organization with id {organization_id} not found",
        )
    new_cluster = Cluster(**cluster_data.model_dump(), organization_id=organization_id)
    result = await cluster_collection.insert_one(new_cluster.model_dump())
    cluster_in_db = await cluster_collection.find_one({"_id": result.inserted_id})
    return Cluster.model_load(cluster_in_db).model_dump()


@cluster_router.get("")
async def get_clusters():
    ...


@cluster_router.get("/{cluster_id}")
async def get_cluster():
    ...


@cluster_router.patch("/{cluster_id}")
async def update_cluster():
    ...


@cluster_router.post("/{cluster_id}/deploy")
async def deploy_cluster():
    ...


@cluster_router.post("/{cluster_id}/teardown")
async def teardown_cluster():
    ...
